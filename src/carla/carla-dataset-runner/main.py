"""
Dataset Creation Plan: Consult https://stevengong.co/notes/Synthetic-Data-Generation

This file runs for a single world.

The way this works is that a bunch of vehicles are spawned. And then we just choose one of the vehicles
as our ego vehicle.

"""
import argparse
import os
import sys
from CarlaWorld import CarlaWorld
from HDF5Saver import HDF5Saver
from utils.create_video_on_hdf5.create_content_on_hdf5 import read_hdf5_test, treat_single_image, create_video_sample
import datetime


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Settings for the data capture", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-wi', '--width', default=1600, type=int, help="camera rgb and depth sensor width in pixels")
    parser.add_argument('-he', '--height', default=1200, type=int, help="camera rgb and depth sensor width in pixels")
    parser.add_argument('-fov', '--fov', default=90, type=int, help="camera rgb and depth sensor fov")
    parser.add_argument('-ve', '--vehicles', default=100, type=int, help="number of vehicles to spawn in the simulation")
    parser.add_argument('-wa', '--walkers', default=100, type=int, help="number of walkers to spawn in the simulation")
    parser.add_argument('-etr', '--egos_to_run', default=10, type=int, help="number of egos to run (good to get multiple perspectives...?)")
    parser.add_argument('-fpe', '--frames_per_ego', default=30, type=int, help="number of frames to record for each ego")
    parser.add_argument('-fps', '--frames_per_second', default=10, type=int, help="frames per second to render CARLA in")
    parser.add_argument('-v', '--video', default=True, action="store_true", help="record a mp4 video on top of the recorded hdf5 file")
    parser.add_argument('-d', '--depth', action='store_true', help="show the depth video side by side with the rgb")
    parser.add_argument('-w', '--world', default='Town04', type=str, help="name of the world to run the data generation in")
    #TODO: Set the world
    

    args = parser.parse_args()
    assert(args.width > 0 and args.height > 0)
    if args.vehicles == 0 and args.walkers == 0:
        print('Are you sure you don\'t want to spawn vehicles and pedestrians in the map?')

    # Sensor setup (rgb and depth share these values). We should have custom setup
    sensor_width = args.width
    sensor_height = args.height
    fov = args.fov
    egos_to_run = args.egos_to_run
    frames_per_ego = args.frames_per_ego
    fps = args.frames_per_second
    
    # Beginning data capture procedure
    if not os.path.exists("data"):
        os.makedirs("data")
    output_filename = os.path.join("data", datetime.datetime.utcnow().isoformat(" ") + ".hdf5")
    HDF5_file = HDF5Saver(sensor_width, sensor_height, output_filename)
    print("HDF5 File opened")

    CarlaWorld = CarlaWorld(HDF5_file=HDF5_file, world=args.world)

    timestamps = []

    print('Starting to record data...')
    CarlaWorld.spawn_npcs(number_of_vehicles=args.vehicles, number_of_walkers=args.walkers)
    # Generate a dataset in each weather condition
    for weather_option in CarlaWorld.weather_options:
        CarlaWorld.set_weather(weather_option)
        ego_vehicle_iteration = 0
        while ego_vehicle_iteration < egos_to_run:
            CarlaWorld.begin_data_acquisition(sensor_width, sensor_height, fov,
                                             frames_to_record_one_ego=frames_per_ego, timestamps=timestamps,
                                             egos_to_run=egos_to_run, fps=fps)
            print('Setting another vehicle as EGO.')
            ego_vehicle_iteration += 1
        print(f'Setting weather to {weather_option}')

    CarlaWorld.remove_npcs()
    print('Finished simulation.')
    print('Saving timestamps...')
    CarlaWorld.HDF5_file.record_all_timestamps(timestamps)
    HDF5_file.close_HDF5()

    # For later visualization
    if args.video:
        create_video_sample(output_filename, show_depth=args.depth)
