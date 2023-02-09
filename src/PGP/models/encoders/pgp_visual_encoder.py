from models.encoders.pgp_encoder import PGPEncoder
import typing as T
import torch
import torchvision
from torch.nn.utils.rnn import pack_padded_sequence
import torch.nn as nn

class PGPVisualEncoder(PGPEncoder):
    def __init__(self, args: T.Dict):
        super().__init__(args)
        self.resnet = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)

        self.resnet_channels = args['resnet_channels']
        self.roi_output_size = args['roi_output_size']
        self.post_roi_mlp: T.List[int] = args['post_roi_mlp']
        assert(len(self.post_roi_mlp) > 0)
        self.target_agent_vis_enc_size = args['target_agent_vis_enc_size']
        self.geo_vis_fuse_mlp = args['geo_vis_fuse_mlp']

        # MLP to embed roi feat
        roi_feat_size = self.resnet_channels * (self.roi_output_size**2)
        self.target_agent_visual_emb = self._construct_mlp([roi_feat_size] + self.post_roi_mlp)

        # GRU to encode roi sequences
        self.target_agent_visual_enc = nn.GRU(self.post_roi_mlp[-1], self.target_agent_vis_enc_size, batch_first=True)

        # MLP to fuse visual and geometric feats after they're individually encoded
        fuse_input_size = self.target_agent_vis_enc_size + args['target_agent_enc_size']
        fuse_output_size = args['target_agent_enc_size']
        self.target_agent_geo_vis_fuse = self._construct_mlp([fuse_input_size] + self.geo_vis_fuse_mlp + [fuse_output_size])

    def _construct_mlp(self, layers: T.List[int]) -> nn.Sequential:
        mlp = []
        for i in range(1, len(layers)):
            mlp.append(nn.Linear(layers[i-1], layers[i]))
        return nn.Sequential(*mlp)
    
    def _foward_target_encoding(self, inputs):
        geo_enc = super()._foward_target_encoding(inputs)
        vis_enc = self._vis_encoding(inputs)
        target_enc = self.target_agent_geo_vis_fuse(torch.cat((geo_enc, vis_enc),dim=1))
        return target_enc

    def _vis_encoding(self, inputs):
        # [N, L, 256 * (roi_output_size**2)]
        target_agent_visual_features = self._extract_img_featues(
            imgs=inputs['target_agent_images'],
            rois=inputs['target_agent_visuals'],
            roi_output_size=self.roi_output_size
        )
        target_agent_visual_features_emb = self.target_agent_visual_emb(target_agent_visual_features)
        """
        The sequence_lengths tensor represents the actual lengths of the sequences in the batch, 
        and its elements should correspond to the number of time steps in each sequence. 
        The max_length dimension of the sequences tensor represents the padded length 
        of the longest sequence in the batch, to which all other sequences are padded to.

        For example, if you have a batch of sequences of varying lengths [3, 2, 4], the 
        sequence_lengths tensor would be torch.tensor([3, 2, 4]), and the max_length would be 4 
        (since that's the length of the longest sequence). The sequences tensor would have 
        shape (3, 4, input_size), where the first 3 time steps of the first sequence, 
        the first 2 time steps of the second sequence, and all 4 time steps of the third 
        sequence are valid, and the remaining time steps are padded with zeros.

        When you use nn.utils.rnn.pack_padded_sequence, 
        the sequence_lengths tensor is used to determine which time 
        steps are valid and which are padding, and the nn.GRU module will 
        only process the valid time steps and ignore the padding.
        """
        seq_lens = inputs['target_agent_image_sequence_len']
        seq = pack_padded_sequence(target_agent_visual_features_emb, seq_lens.cpu(), 
                                   batch_first=True, enforce_sorted=False)
        _, target_agent_vis_enc = self.target_agent_visual_enc(seq)
        return target_agent_vis_enc.squeeze(0)

    def _extract_img_featues(self, imgs, rois, roi_output_size):
        N, L, C, H, W = imgs.shape
        imgs_flat = imgs.view(N*L, C, H, W)
        imgs_flat = self.resnet.conv1(imgs_flat)
        imgs_flat = self.resnet.bn1(imgs_flat)
        imgs_flat = self.resnet.relu(imgs_flat)
        imgs_flat = self.resnet.maxpool(imgs_flat)

        imgs_flat = self.resnet.layer1(imgs_flat)
        imgs_flat = self.resnet.layer2(imgs_flat)
        imgs_flat = self.resnet.layer3(imgs_flat)
        imgs_flat = self.resnet.layer4(imgs_flat)
        orig_W = 1600
        scale = imgs_flat.shape[-1] / orig_W
        rois = rois.view(N*L, -1).unsqueeze(1).unbind()
        rois = torchvision.ops.roi_align(imgs_flat, rois, roi_output_size, scale)
        return rois.view(N*L, -1).view(N,L,-1)

        

