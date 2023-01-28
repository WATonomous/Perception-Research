FROM nvidia/cuda:10.0-devel-ubuntu18.04 

RUN apt-get update && apt-get install wget -yq
RUN apt-get install build-essential g++ gcc -y

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get install libgl1-mesa-glx libglib2.0-0 -y
RUN apt-get install openmpi-bin openmpi-common libopenmpi-dev libgtk2.0-dev git -y

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda
# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH
RUN conda install python=3.7
RUN conda install pytorch==1.2 torchvision cudatoolkit=10.0 -c pytorch
RUN pip install cython
RUN pip install -U 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'

WORKDIR /home/docker

COPY src/centerfusion/CenterFusion/ centerfusion

RUN pip install -r centerfusion/requirements.txt

