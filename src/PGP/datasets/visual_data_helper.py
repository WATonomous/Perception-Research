import numpy as np
import torch
from PIL import Image
from pyquaternion.quaternion import Quaternion
from typing import List, Tuple, Union, Dict
from shapely.geometry import MultiPoint, box

from nuscenes.nuscenes import NuScenes
from nuscenes.utils.geometry_utils import view_points

from torchvision import transforms

class VisualDataHelper(object):
    def __init__(self, nusc: NuScenes, t_h: int, transform: transforms.Compose = None):
        self.nusc = nusc
        self.t_h = t_h
        if transform is None:
            self.transform = None
        else:
            self.transform = self._compose_transform(transform)

    def _compose_transform(self, transform: Dict) -> transforms.Compose:
        comp = []
        if 'resize' in transform:
            comp.append(transforms.Resize(transform['resize']))
        if 'to_tensor' in transform and transform['to_tensor']:
            comp.append(transforms.ToTensor())
        if 'normalize' in transform:
            norm = transform['normalize']
            comp.append(transforms.Normalize(mean=norm['mean'], std=norm['std']))
        return transforms.Compose(comp)

    def _ann_token_from_sample_instance(self, s_tok: str, i_tok: str) -> str:
        """
        Returns the annotation token of instance i_tok at sample s_tok
            the sample must contain the instance
        """
        ann = None
        for sample_ann_token in self.nusc.get('sample', s_tok)['anns']:
            sample_ann = self.nusc.get('sample_annotation', sample_ann_token)
            if sample_ann['instance_token'] == i_tok:
                assert ann is None, f"Found two annotations matching instance {i_tok} \
                    in sample {s_tok}"
                ann = sample_ann
        assert ann is not None, f"Did not find instance {i_tok} in sample {s_tok}"
        return ann['token']
    
    def _post_process_coords(self, corner_coords: List,
                            imsize: Tuple[int, int] = (1600, 900)) -> Union[Tuple[float, float, float, float], None]:
        """
        Get the intersection of the convex hull of the reprojected bbox corners and the image canvas, return None if no
        intersection.
        :param corner_coords: Corner coordinates of reprojected bounding box.
        :param imsize: Size of the image canvas.
        :return: Intersection of the convex hull of the 2D box corners and the image canvas.
        """
        polygon_from_2d_box = MultiPoint(corner_coords).convex_hull
        img_canvas = box(0, 0, imsize[0], imsize[1])
        if polygon_from_2d_box.intersects(img_canvas):
            img_intersection = polygon_from_2d_box.intersection(img_canvas)
            intersection_coords = np.array([coord for coord in img_intersection.exterior.coords])

            min_x = min(intersection_coords[:, 0])
            min_y = min(intersection_coords[:, 1])
            max_x = max(intersection_coords[:, 0])
            max_y = max(intersection_coords[:, 1])

            return min_x, min_y, max_x, max_y
        else:
            return None

    def _camera_box(self, sd_tok: str, ann_tok: str):
        """
        Attempts to 3D->2D project ann_tok to sd_tok

        sd_tok: A sample_data token from a camera
        ann_tok: A sample_annotation token

        Returns: {
            'cam_channel': the name of the camera channel (str),
            'cam_file': the camera channel jpg file (str),
            'roi_min_x': min_x (int),
            'roi_min_y': min_y (int),
            'roi_max_x': max_x (int),
            'roi_max_y': max_y (int), 
        }, or None if the camera cannot see the annotation
        """
        # Project global box to cam
        global_box = self.nusc.get_box(ann_tok)
        sd_rec = self.nusc.get('sample_data', sd_tok)
        assert(sd_rec['sensor_modality'] == 'camera')
        cs_rec = self.nusc.get('calibrated_sensor', sd_rec['calibrated_sensor_token'])
        ego_pose_rec = self.nusc.get('ego_pose', sd_rec['ego_pose_token'])
        camera_intrinsic = np.array(cs_rec['camera_intrinsic'])
        # Move to the ego-pose frame.
        global_box.translate(-np.array(ego_pose_rec['translation']))
        global_box.rotate(Quaternion(ego_pose_rec['rotation']).inverse)
        # Move to the calibrated sensor frame.
        global_box.translate(-np.array(cs_rec['translation']))
        global_box.rotate(Quaternion(cs_rec['rotation']).inverse)
        # Filter out the corners that are not in front of the calibrated sensor.
        corners_3d = global_box.corners()
        in_front = np.argwhere(corners_3d[2, :] > 0).flatten()
        corners_3d = corners_3d[:, in_front]

        # Project 3d box to 2d.
        corner_coords = view_points(corners_3d, camera_intrinsic, True).T[:, :2].tolist()

        # Keep only corners that fall within the image.
        final_coords = self._post_process_coords(corner_coords)

        # Skip if the convex hull of the re-projected corners does not intersect the image canvas.
        if final_coords is None:
            return None
        else:
            min_x, min_y, max_x, max_y = final_coords
            return {
                'cam_channel': sd_rec['channel'],
                'cam_file': sd_rec['filename'],
                'roi_min_x': min_x,
                'roi_min_y': min_y,
                'roi_max_x': max_x,
                'roi_max_y': max_y,
            }
        
    def _best_channel(self, ann_rec, channel_pref=None):
        """
        Returns the best camera to view ann_tok from
            If no camera can view ann_tok (yes, this can happen, idk why), returns None

        ann_tok: Annotation token to get the best view of
        channel_pref: If you can view ann_tok from this channel, do so
        """
        # ann_rec = self.nusc.get('sample_annotation', ann_tok)
        sample_rec = self.nusc.get('sample', ann_rec['sample_token'])
        channels = [key for key in sample_rec['data'].keys() if 'CAM' in key]
        views = []
        for channel in channels:
            view = self._camera_box(sample_rec['data'][channel], ann_rec['token'])
            if view:
                views.append(view)
        if len(views) == 0:
            return None
        if channel_pref is not None:
            pref_view = [v for v in views if v['cam_channel'] == channel_pref]
            if len(pref_view) > 0:
                assert len(pref_view) == 1
                return pref_view[0]
        def area(view):
            return (view['roi_max_x'] - view['roi_min_x']) * (view['roi_max_y'] - view['roi_min_y'])
        return sorted(views, key=area, reverse=True)[0]
    
    def get_target_agent_visuals(self, s_t: str, i_t: str, seconds: int) -> List[Dict]:
        """
        Gets the visual information for agent instance `i_t` at sample time `s_t`, for the past `seconds`
        """
        curr_ann_tok = self._ann_token_from_sample_instance(s_t, i_t)
        ann_rec = self.nusc.get('sample_annotation', curr_ann_tok)
        ann_rec_hist = [ann_rec]
        # nuscenes dataset is annotated at 2Hz
        for _ in range(2 * seconds):
            # if we've ran out of history for this instance
            if not ann_rec['prev']:
                break
            ann_rec = self.nusc.get('sample_annotation', ann_rec['prev'])
            ann_rec_hist.append(ann_rec)
        curr_channel = None
        views = []
        for ar in ann_rec_hist:
            view = self._best_channel(ar, curr_channel)
            views.append(view)
            if view:
                curr_channel = view['cam_channel']
        return views
    
    def load_visuals(self, data: Dict):
        """
        Using the information in data['inputs']['target_agent_visuals'], which is a variable size List (1 to 5 elements) of
            Dict{
                'cam_file': str,
                'roi_min_x': float,
                'roi_min_y': float,
                'roi_max_y': float,
                'roi_max_y': float
            }
        
        This function relaces the data['inputs']['target_agent_visuals'] key with a tensor of padded ROIs of shape (L=5, F=4)
            where the last dim (F) is the vector [roi_min_x, roi_min_y, roi_max_x, roi_max_y]. The L dimension is
            padded with all-zero ROIs if we have no visual information for that element in the sequence

        This function also adds the key data['inputs']['target_agent_images'], which is a tensor of shape (L=5, C=3, W, H)
            which is the transformed image data transformed by self.transform
            Again, the L dim is padded with zero-valued images if we have no image for that element in the sequence

        This function also adds the key data['inputs']['target_agent_image_masks'], which is the same shape as
            data['inputs']['target_agent_images'] (L=5, C=3, W, H). The mask is 1 in sequence elements (accross the L dim)
            that are valid images, and 0 else where
        
        """
        if self.transform is None:
            return data
        visuals = data['inputs']['target_agent_visuals']
        imgs = [Image.open(f"{self.nusc.dataroot}/{v['cam_file']}") for v in visuals]
        rois = [torch.tensor([v['roi_min_x'], v['roi_min_y'], v['roi_max_x'], v['roi_max_y']]) for v in visuals]
        imgs = [img.convert("RGB") for img in imgs]
        imgs = [self.transform(img) for img in imgs]
        img_shape = imgs[0].shape
        masks = [torch.zeros(img_shape) for _ in imgs]
        while (len(imgs) < self.t_h*2+1):
            imgs.append(torch.zeros(img_shape))
            masks.append(torch.ones(img_shape))
            rois.append(torch.zeros(4, dtype=rois[0].dtype))
        visuals = data['inputs']['target_agent_visuals'] = torch.stack(rois)
        data['inputs']['target_agent_images'] = torch.stack(imgs)
        data['inputs']['target_agent_image_masks'] = torch.stack(masks)
        return data


