import sys
import os
import carla
import random


# Carla initialization
client = carla.Client('carla_server', 2000)
client.set_timeout(10.0)
world = client.get_world()
print('Successfully connected to CARLA')

# Weather stuff
#weather = carla.WeatherParameters(cloudyness=30.0, precipitation=30.0, precipitation_deposits=0.0, wind_intensity=30.0, sun_azimuth_angle=0.0, sun_altitude_angle=-60.0)
# weather = carla.WeatherParameters(cloudyness=-1, precipitation=-1, precipitation_deposits=-1, wind_intensity=-1, sun_azimuth_angle=-1, sun_altitude_angle=-1)
#world.set_weather(weather)
#print('Changed weather.')

# Spawn selected vehicle
blueprint = world.get_blueprint_library().filter('vehicle.*')
# blueprint_1 = world.get_blueprint_library().filter('vehicle.audi.a2')[0]
blueprint_1 = blueprint[12]  # 25 = max
print('spawning ', blueprint_1)

#print('destroying', world.get_actors()[len(world.get_actors())-1])
world.get_actors()[len(world.get_actors())-1].destroy()

spawn_points = world.get_map().get_spawn_points()[15]
print(spawn_points)
#spawn_point = carla.Transform(carla.Location(x=-6.4, y=-40.0, z=2.0), carla.Rotation(pitch=0.000000, yaw=92.004189, roll=0.000000))
#spawn_point = carla.Transform(carla.Location(x=144.059280, y=129.749863, z=1.320625), carla.Rotation(pitch=0.000000, yaw=179.999756, roll=0.000000))

actor = world.spawn_actor(blueprint_1, spawn_points)
print('Spawned vehicle!')
