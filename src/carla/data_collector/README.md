# Carla Data Collector

This data collection tool performs the following two tasks:
- `carla_data_saver.py` works with CARLA and ScenarioRunner (optional) to save CARLA sensor data and simulation metadata. This can be used to generate an object detection synthetic dataset or object tracking synthetic dataset. Example configuration files are in folder configs.
- `carla_annotator.py` generates annotations for CARLA camera images saved by carla_data_saver.py. Two annotation formats are supported: [kwcoco](https://kwcoco.readthedocs.io/en/release/) and [MOTS](https://motchallenge.net/instructions)

The original code for this tool was found [here](https://github.com/carla-simulator/carla/pull/4992)

### Crashes

```bash
perception-research-carla_server-1  | sh: 1: xdg-user-dir: not found
perception-research-carla_server-1  | Signal 11 caught.
perception-research-carla_server-1  | Malloc Size=65538 LargeMemoryPoolOffset=65554 
perception-research-carla_server-1  | 4.26.2-0+++UE4+Release-4.26 522 0
perception-research-carla_server-1  | Disabling core dumps.
perception-research-carla_server-1  | CommonUnixCrashHandler: Signal=11
perception-research-carla_server-1  | Engine crash handling finished; re-raising signal 11 for the default handler. Good bye.
perception-research-carla_server-1  | Segmentation fault (core dumped)
perception-research-carla_server-1 exited with code 139
```

To prevent crashes:
- Set a higher timeout interval (i.e. 10.0s). The default 2.0s (for sync.) crashes a lot.
- Reduce the number of sensors you are mounting (i.e only camera)





### Steps to use the data collection tool:

1. Run the carla docker containers
2. Generate traffic: in general, there are three ways to create vehicles/pedestrians
    (a). Use a traffic generation script that has one vehicle with role_name assigned, e.g., ```manual_control.py``` or ```generate_traffic.py``` (with argument --hero). This is because if this tool attaches sensors to a particular vehicle and it uses role_name to find it as in bullet 4(b) below. But if the tool spawns static sensors at a specified location following 4(a), role_name is not required.
    (b). Use ScenarioRunner to generate the traffic (remember to use argument --sync to enable sync mode.
    (c). Create vehicles in the data collector’s configuration file. An example is in ```data_collector/configs/config.yaml```
3. Run ```data_collector/carla_data_saver.py``` with the desired configuration file to collect images and metadata. Command line argument '--config-name' allows users to choose the configuration file. By default, output files will be saved in ```outputs/simulation-date/simulation-time``` folder. The tool will create one folder for each spawned sensor and metadata files will be saved in ```metadata``` folder. This data collection tool supports two cases:
    (a). It can spawn sensors at a specified transform statically (e.g., put the set of sensors at an intersection and monitor the traffic). An example configuration is here ```data_collector/configs/config_static_sensors.yaml```. In this example, ```transform``` is the world coordinate in the town map.
    (b). Attach sensors to a vehicle with ```role_name```. ```data_collector/configs/config_scenario_runner.yaml``` is an example to work with ScenarioRunner. And ```data_collector/configs/config_sensors_hero.yaml``` is an example to work with scripts (e.g., ```manual_control.py```, ```geneate_traffic.py```) that generate traffic. Note that in this case, ```transform``` is the local coordinate relative to the ```attach_to``` vehicle.
4. Run ```data_collector/carla_annotator.py``` to generate annotations in ```kwcoco``` or ```MOTS``` format for saved images

## Docker

We recommend to run the data collection tool with docker and below are some instructions to run a data collection with the CARLA client docker image.

1. Follow instructions here https://carla.readthedocs.io/en/0.9.13/build_docker/ to pull CARLA image, which is for the CARLA server.
2. Run make docker_image to generate the CARLA client docker image.
3. To run a simulation (without generating annotation) with configuration file ```configs/config_tracking.yaml``` and save the data in the directory ```/datasets/data_collector```, use command ```make /datasets/data_collector/config_tracking /run1/collection_done```. Here ```run1``` is a folder that the generated data will be saved and it can be replaced with any preferred folder name to differentiate different runs of simulation. Remember to set environment variable DATASET properly if you want to save data to a different directory.
4. To run a CARLA simulation and generate kwcoco annotations, use the command ```TRACKING_FORMAT=kwcoco make /datasets/data_collector/config_tracking/run1/kwcoco_annotations.json```. To generate MOTS annotations, use ```make /datasets/data_collector/config_tracking/run1/instances.zip```.