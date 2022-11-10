# Perception Research
This repository is used as a playground to train custom Perception models that are containerized through Docker. Current projects include using transfer learning with the YOLOv5 model (by freezing backbone layers) to train the traffic sign detection. 

To get started, run the following for the model you are interested in
```bash
./build.sh <imageName> # ex: build.sh yolov5
./spinup.sh <imageName> # ex: spinup.sh yolov5.
```

Then, to enter the terminal of the Docker container, run
```bash
docker exec -it <ContainerID> /bin/bash
```

## Current Investigation Areas
### Traffic Sign Classification with YOLOv5
YOLOv5 for transfer learning with traffic signs. We are getting the traffic sign detection from:
- https://www.kaggle.com/code/hemraj12/traffic-signs-detection-on-carla-simulator/data?select=ts

Some Training Pages:
- https://kikaben.com/yolov5-transfer-learning-dogs-cats/
- https://github.com/ultralytics/yolov5/issues/1314
- https://pyimagesearch.com/2022/06/20/training-the-yolov5-object-detector-on-a-custom-dataset/

## File Structure
- `datasets` for storing relatively small datasets. Mounted at `/datasets`
- `projects` for storing the code to investigate models. Mounted at `/projects`
- `nodes` for storing ROS2 code. Mounted at `/perception_ws/src`



## ROS2
We don't really need to use ROS2 in this repository, however if you really want to use it you can under `nodes`. Some guides on creating ROS2 nodes below.

### Creating New Packages
One way to go about creating ROS2 packages is actually running the commands from a Docker container, i.e. `ros2 pkg create --build-type ament_python <package_name>` for Python packages. However, we run into permission errors since the folder is created with root user. You'll need to change the permissions so that everyone can read, write and delete (i.e. giving the `users` group to all files and subdirectories).

Another way is to copy paste the template package called `template_pkg` inside `nodes/template_pkg`. You'll need to change a few files after you rename everything.

### Starting Up ROS2 Nodes
Run the following command:
```
ros2 run <package_name> <executable_name>
```

If you have a launch file, run
```
ros2 launch <package_name> <launch_name>
```
