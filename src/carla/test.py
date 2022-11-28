""" Testing if our connection is working. """

import carla

client = carla.Client('carla_server', 2000)
client.set_timeout(60.0)

print("Available Maps:", client.get_available_maps())

town = 'Town04'
try:
    world = client.load_world(town)
    print("Map", town, "loaded successfully")
except:
    print("Failed to load Map", town)
