# Multi-Task Multi-Sensor Fusion with BEVFusion
This is a fork of the original BEVFusion available [here](https://github.com/mit-han-lab/bevfusion).

![demo](assets/demo.gif)

## Data Download and Preprocessing
The dataset used in this project is [NuScenes](https://www.nuscenes.org/).Below are the steps we took to **download and preprocess the dataset** for this project:
1. [Downloaded](https://www.nuscenes.org/download) and extracted nuscenes detection and map extension datasets to `/mnt/wato-drive/perception/nuscenes_BEVFUSION`
2. Ran the [mmdet preprocessing](https://github.com/open-mmlab/mmdetection3d/blob/master/docs/en/datasets/nuscenes_det.md) on the downloaded dataset.


The **pretrained [weights](https://github.com/mit-han-lab/bevfusion#evaluation)** have been downloaded to  `/mnt/wato-drive/perception/bevfusion_pretrain`, and mmoun

In practice, we also copied over these folders into our `/mnt/scratch` directory because it provides a faster read and write, i.e.
- `/mnt/wato-drive/perception/nuscenes_BEVFUSION` $\rightarrow$ `trpro-ubuntu1:/mnt/scratch/nuscenes_BEVFUSION/nuscenes_BEVFUSION`
- `/mnt/wato-drive/perception/bevfusion_pretrain` $\rightarrow$ `/mnt/scratch/bevfusion_pretrain`.


We mount our folders onto the container the following way (you can find this under the [docker-compose.yml](../../docker-compose.yml) file):
- `./src/bevfusion/.vscode:/root/bevfusion/.vscode`
- `./src/bevfusion/.gitignore:/root/bevfusion/.gitignore`
- `/mnt/scratch/nuscenes_BEVFUSION/nuscenes_BEVFUSION:/root/bevfusion/data/nuscenes`
- `/mnt/scratch/nuscenes_BEVFUSION/nuscenes_BEVFUSION:/drive_dataset`
- `/mnt/scratch/bevfusion_pretrain:/pretrain`

## Running Eval
Once the data preprocessing has been done, we can launch a new BEVFusion container by running
```bash
docker-compose up bevfusion
```

The docker container will come with the `bevfusion` repository mounted at `~/bevfusion`. For more info on how this container is built, see the [Dockerfile](../../docker/bevfusion/Dockerfile).

Now, either connect to the Docker container through VSCode (you can find info [here](https://code.visualstudio.com/docs/devcontainers/containers)), or run the following command to enter the terminal of the docker container:
```bash
docker exec -it perception-research-bevfusion-1 /bin/bash
```

Inside the container, run the following command to start eval (this takes ~800 seconds)
```bash
torchpack dist-run -np 5 python tools/test.py configs/nuscenes/det/transfusion/secfpn/camera+lidar/swint_v0p075/convfuser.yaml /pretrain/bevfusion-det.pth --eval bbox #  -np 5 means to use 5 GPUS
```

## Visualize Predictions
This takes around ~25 minutes to run.
```bash
mkdir visualization
torchpack dist-run -np 5 python tools/visualize.py configs/nuscenes/det/transfusion/secfpn/camera+lidar/swint_v0p075/convfuser.yaml --checkpoint /pretrain/bevfusion-det.pth --out-dir ./visualization --mode pred --box-score 0.1
```
Then, try tuning the box-score hyper parameter in the visualization script. Typically a higher threshold will filter out a lot of low confidence boxes and make the visualization look better. You can also potentially adjust the nms_threshold in configuration files to a very low value such that there will be fewer duplicate boxes in your visualization.




The generated folder was moved into `/mnt/scratch/bevfusion_viz`.


If you want to run your own visualizations, do it in the following format:
```bash
torchpack dist-run -np 1 python tools/visualize.py [config file] --checkpoint [checkpoint file] --out-dir [output dir] --mode [pred/gt] --bbox-score 0.1
```
This will generate a bunch of images.
