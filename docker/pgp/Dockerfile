# FROM nvidia/cuda:10.1-devel-ubuntu18.04
FROM nvidia/cuda:11.3.1-devel-ubuntu20.04

RUN apt-get update && apt-get install wget -yq
# RUN apt-get install build-essential g++ gcc -y
ENV DEBIAN_FRONTEND noninteractive
# RUN apt-get install libgl1-mesa-glx libglib2.0-0 -y
# RUN apt-get install openmpi-bin openmpi-common libopenmpi-dev libgtk2.0-dev git -y

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda
# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH
RUN conda create --name pgp
SHELL ["conda", "run", "-n", "pgp", "/bin/bash", "-c"]
# RUN conda install python=3.8
# Versions specificed in PGP
# RUN conda install pytorch==1.7.1 torchvision==0.8.2 torchaudio==0.7.2 cudatoolkit=10.1 -c pytorch
# Versions from bevfusion
RUN conda install pytorch==1.10.1 torchvision==0.11.2 torchaudio==0.10.1 cudatoolkit=11.3 -c pytorch
# RUN pip install Pillow==8.4.0
# RUN pip install tqdm
# RUN pip install torchpack
# RUN pip install mmcv==1.4.0 mmcv-full==1.4.0 mmdet==2.20.0
# RUN pip install mpi4py==3.0.3
# RUN pip install numba==0.48.0
RUN pip install nuscenes-devkit
RUN pip install ray
RUN pip install psutil
RUN pip install positional-encodings==5.0.0
RUN pip install imageio
RUN pip install tensorboard
WORKDIR /root
RUN apt-get install libgl1-mesa-glx libglib2.0-0 tmux -y
RUN echo "source activate pgp" > ~/.bashrc
ENV PATH /opt/conda/envs/env/bin:$PATH
# COPY src/bevfusion /root/bevfusion
# WORKDIR /root/bevfusion
# RUN python setup.py develop