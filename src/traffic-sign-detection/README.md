# Traffic Sign Detection
This is a small project to train a 2D Object Detection to detect different kinds of traffic signs.

Next steps: Getting CARLA to synthetically generate traffic sign data, and making predictions on that new dataset.

## Steps
1. We started with our experiment obtaining a public traffic sign dataset from Kaggle, available [here](https://www.kaggle.com/code/hemraj12/traffic-signs-detection-on-carla-simulator/data?select=ts). We downloaded it locally into `/mnt/wato-drive/perception/kaggle_traffic_sign` folder.
2. We wrote our own script to format that dataset into YOLOv5 friendly file structure, which are found in `script.py`, and `data.yml` is the specification.
3. We used the official YOLOv5 Docker Image (`ultralytics/yolov5:latest`) to do training. This was added to our `docker-compose.yml` as a service called `yolov5`.

Starting training is as simple as running the following commands:
```bash
docker compose up yolov5
```

In a new terminal, run
```bash
docker exec -it perception-research-yolov5-1 /bin/bash # name of container might be slightly different

# Start training
python3 train.py --data /datasets/kaggle_traffic_sign/data.yaml --weights yolov5x.pt --epochs 100 --batch 4 --freeze 10
```

As the training is happening, you can visualize the loss through Tensorboard. We specified`"6006:6006"` connect the ports from inside the Docker container to outside container.

The last step you need to do is port forward from the remote server onto your local computer:
```bash
ssh -NfL 6006:localhost:6006 <username>@<hostname> # ex: s36gong@trpro-ubuntu1.watocluster.local
```

Then, go to http://localhost:6006/ and you should be able to see tensorboard running.
