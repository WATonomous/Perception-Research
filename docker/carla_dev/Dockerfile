FROM carlasim/carla:0.9.13

FROM ubuntu:20.04

COPY --from=0 /home/carla/PythonAPI /home/carla-python

# bypass any required inputs
ENV DEBIAN_FRONTEND=noninteractive

# Set up dependencies for python3.7 and carla
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential \ 
    wget curl software-properties-common \
    # carla python api dependencies
    libpng-dev libjpeg-dev libtiff-dev libgeos-dev \
    # opencv dependencies
    ffmpeg libsm6 libxext6 \
    # data_collector dependencies
    git xdg-user-dirs xdg-utils fontconfig zip

# install python3.7
RUN add-apt-repository ppa:deadsnakes/ppa -y; \
    apt-get update -y; \
    apt-get install --no-install-recommends -y \
        python3.7 python3.7-dev python3.7-tk python3.7-distutils; \
    curl https://bootstrap.pypa.io/get-pip.py | python3.7
RUN rm -rf /tmp/*
RUN ln -sf /usr/bin/python3.7 /usr/bin/python
RUN ln -sf /usr/bin/python3.7 /usr/bin/python3
RUN python3 -m pip install pip -U

WORKDIR /home
COPY ../src/carla carla

# carla python api dependencies
RUN python3 -m pip --no-cache-dir install --upgrade -r \
    carla-python/carla/requirements.txt

# install the python libraries we want
RUN python3 -m pip --no-cache-dir install --upgrade \
    notebook matplotlib pycocotools scipy opencv-python scikit-image Cython

# add carla python api to python path
ENV PYTHONPATH "${PYTHONPATH}:/home/carla-python/carla/dist/carla-0.9.13-py3.7-linux-x86_64.egg"

# data collector dependencies
RUN python3 -m pip --no-cache-dir install --upgrade -r \
    carla/data_collector/requirements.txt

WORKDIR /home/carla
