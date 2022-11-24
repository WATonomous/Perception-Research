# Perception Research
This repository is used as a playground to run perception experiments. Each of these are containerized through Docker. Current projects include 
- Using transfer learning with the YOLOv5 model (by freezing backbone layers) to perform traffic sign detection
- Synthetic Data Generation for Traffic Signs using CARLA
- Multimodal Object Deteciton with BEVFusion

**Pre-requisite**: Before you run any of the commands below, make sure you are familiar with [Docker](https://www.docker.com/). If not, we highly recommend going through this [2-hour video](https://www.youtube.com/watch?v=fqMOX6JJhGo) which teaches you the basics of Docker.

## Getting Started
To get started, run the `docker compose up` command, followed by the name of the service you are interested in (if you don't specify, you will end up launching every single service...). You can find all the services we have under [docker-compose.yml](./docker-compose.yml).
```bash
docker compose up <imageName> # ex: docker compose up yolov5
```

Then, to enter the terminal of the Docker container, open a new terminal and run
```bash
docker exec -it <ContainerID> /bin/bash
```

If you want to develop from the inside container itself, we recommend using VSCode built-in Docker container.

## Current Investigation Areas
### Traffic Sign Classification with YOLOv5
YOLOv5 for transfer learning with traffic signs. We are getting the traffic sign detection from:
- https://www.kaggle.com/code/hemraj12/traffic-signs-detection-on-carla-simulator/data?select=ts

Some Training Pages:
- https://kikaben.com/yolov5-transfer-learning-dogs-cats/
- https://github.com/ultralytics/yolov5/issues/1314
- https://pyimagesearch.com/2022/06/20/training-the-yolov5-object-detector-on-a-custom-dataset/

## File Structure
- `src` for storing the code to investigate models