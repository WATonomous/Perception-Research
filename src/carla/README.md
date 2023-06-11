# Synthetic Data Generation in CARLA

### Getting Started
For the data generation work, we use 2 [containers](../../profiles/carla.docker-compose.yml), `carla_server` (base CARLA image to run the CARLA engine) and `carla_dev` (CARLA development image to interface with the CARLA engine).


Start up the CARLA server by running
```bash
docker compose -p <user_id> up carla_server
```

Then, start up the CARLA dev environment by running
```bash
docker compose -p <user_id> up carla_dev
```


### First Project: Generating Traffic Sign Bounding Boxes
More documentation inside [carla-dataset-runner](carla-dataset-runner/README.md)









## Version Discrepencies
- We run Carla offscreen which leads to some issues. see [here](https://carla.readthedocs.io/en/latest/adv_rendering_options/)
#### Carla 0.9.10.1
- To run the server we use this command:
```bash
SDL_VIDEODRIVER=offscreen SDL_HINT_CUDA_DEVICE=0 ./CarlaUE4.sh \
    -quality-level=${CARLA_QUALITY:-Low} -world-port=2000 -nosound -carla-server
```
- see [here](https://github.com/carla-simulator/carla/issues/225)
- ```SDL_VIDEODRIVER=offscreen SDL_HINT_CUDA_DEVICE=0``` is a workaround to run Carla offscreen

#### Carla 0.9.11
- The same command for version 0.9.10.1 does not really work for this version
- The docker container just closes immediately

#### Carla 0.9.12
- Starting in this version we can now use the ```-RenderOffScreen``` option. see [here](https://carla.readthedocs.io/en/latest/adv_rendering_options/)

#### Carla 0.9.13
- same as 0.9.12
- ```client.get_available_maps()``` works
- This error comes up occasionally when loading a world:
```
profiles-carla_server-1  | Signal 11 caught.
profiles-carla_server-1  | Signal 11 caught.
profiles-carla_server-1  | Signal 11 caught.
profiles-carla_server-1  | Malloc Size=65538 LargeMemoryPoolOffset=65554 
profiles-carla_server-1  | 4.26.2-0+++UE4+Release-4.26 522 0
profiles-carla_server-1  | Disabling core dumps.
profiles-carla_server-1  | CommonUnixCrashHandler: Signal=11
profiles-carla_server-1  | Engine crash handling finished; re-raising signal 11 for the default handler. Good bye.
profiles-carla_server-1  | Segmentation fault (core dumped)
profiles-carla_server-1 exited with code 139
```
- Worlds that I have seen loaded successfully
    - Town01(_Opt)
    - Town02(_Opt)
    - Town04(_Opt)
    - Town05(_Opt)

- Worlds that I have never loaded successfully
    - Town03(_Opt)
