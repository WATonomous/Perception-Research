# Carla (0.9.13) dataset Collector
Script used for collecting data on CARLA version 0.9.13.  Built on top of [AlanNaoto/carla-dataset-runner](https://github.com/AlanNaoto/carla-dataset-runner)

Types of data captured include RGB, depth and bounding box of vehicles and pedestrians collection. Other types of data (semantic segmentation, lidar, ...) are not yet implemented, but could be by following the same data structure. Here is a sample of the collected data on Town02:

## Getting started
Install 
```bash
pip3 install numpy
pip3 install h5py
```


### Running the dataset collector
Running the dataset collector is as easy as 
```
python3 main.py
```

You can also specify certain things, such as the number of vehicles to spawn
```
python3 main.py -ve 50
```

Further commands can be seen by running the --help flag.

After running this command, the script will begin collecting the data from the sensors by iterating over the predefined weather and ego vehicle variations. Finally, it will create a HDF5 file containing all the data and also a MP4 video showing the RGB recorded footage. 

\*At the moment, to avoid high correlation between consecutive frames, it is saving only once every 5th frame.

## HDF5 data output format
The HDF5 file is structured in the following groups, where each frame entry is assigned a common UTC timestamp. A common parser for this file is provided in [create_content_on_hdf5.py](utils/create_video_on_hdf5/create_content_on_hdf5.py).

* bounding_box
    * vehicles
    * walkers
* depth
* rgb
* ego_speed
* timestamps


Data            | Description | Type 
-------------   | ----------- | ----------
bounding boxes  | array [xmin, ymin, xmax, ymax] | int 
depth           | array [sensor_width * sensor_image] | float
rgb             | array [sensor_width * sensor_image * 3 channels] | int
ego_speed       | array [vx, vy, vz in m/s] | float
timestamps      | UTC milisseconds since the UNIX epoch format | int
