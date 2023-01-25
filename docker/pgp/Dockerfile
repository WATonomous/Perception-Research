# FROM nvidia/cuda:10.1-devel-ubuntu18.04
FROM nvidia/cuda:11.0.3-devel-ubuntu20.04

# RUN apt-get update && apt-get install wget -yq
# RUN apt-get install build-essential g++ gcc -y
ENV DEBIAN_FRONTEND noninteractive
# RUN apt-get install libgl1-mesa-glx libglib2.0-0 -y
# RUN apt-get install openmpi-bin openmpi-common libopenmpi-dev libgtk2.0-dev git -y

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# python
RUN apt-get update -y
ENV http_proxy $HTTPS_PROXY
ENV https_proxy $HTTPS_PROXY

RUN apt-get install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get install -y \
    python3.7 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# pgp dependencies
RUN pip install \
    protobuf==3.20.* \
    nuscenes-devkit \
    ray \
    psutil \
    positional-encodings==5.0.0 \
    imageio \
    tensorboard 
    
RUN pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
# RUN pip install torch==1.10.0+cu111 torchvision==0.11.0+cu111 pytorchvideo -f https://download.pytorch.org/whl/cu111/torch_stable.html

# WORKDIR /root
# RUN apt-get install libgl1-mesa-glx libglib2.0-0 tmux -y
# RUN pip install setuptools==59.5.0
# RUN echo "source activate pgp" > ~/.bashrc
# ENV PATH /opt/conda/envs/env/bin:$PATH
# COPY src/bevfusion /root/bevfusion
# WORKDIR /root/bevfusion
# RUN python setup.py develop

# ================= User Setup ===================
RUN apt-get update && apt-get install -y curl sudo && \
    rm -rf /var/lib/apt/lists/*

# Add a docker user so that created files in the docker container are owned by a non-root user
RUN addgroup --gid 1000 docker && \
    adduser --uid 1000 --ingroup docker --home /home/docker --shell /bin/bash --disabled-password --gecos "" docker && \
    echo "docker ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/nopasswd

# Remap the docker user and group to be the same uid and group as the host user.
# Any created files by the docker container will be owned by the host user.
RUN USER=docker && \
    GROUP=docker && \                                                                     
    curl -SsL https://github.com/boxboat/fixuid/releases/download/v0.4/fixuid-0.4-linux-amd64.tar.gz | tar -C /usr/local/bin -xzf - && \                                                                                                            
    chown root:root /usr/local/bin/fixuid && \                                                                              
    chmod 4755 /usr/local/bin/fixuid && \
    mkdir -p /etc/fixuid && \                                                                                               
    printf "user: $USER\ngroup: $GROUP\npaths:\n  - /home/docker/" > /etc/fixuid/config.yml

USER docker:docker
WORKDIR /home/docker/

ENTRYPOINT ["/usr/local/bin/fixuid"]
CMD ["sleep", "inf"]