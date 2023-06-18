# Start from a base image with CUDA and TensorRT support
FROM nvcr.io/nvidia/tensorrt:23.01-py3 as base

# Install dependencies
RUN apt-get update && apt-get install -y \
    unzip \
    libprotobuf-dev \
    python3-pip \
    git \
    libgl1-mesa-glx
	
# Install Python dependencies
RUN pip3 install onnx

# Set up workspace
WORKDIR /app

# Clone the git repository
RUN git clone --recursive https://github.com/NVIDIA-AI-IOT/Lidar_AI_Solution.git

# Set working directory to CUDA-BEVFusion
WORKDIR /app/Lidar_AI_Solution/CUDA-BEVFusion

# Add the model and nuScenes data files (you should place these in the Docker context)
RUN pip3 install gdown
# model.zip
RUN gdown --id 1bPt3D07yyVuSuzRAHySZVR2N15RqGHHN
#nuScenes-example-data.zip
RUN gdown --id 1RO493RSWyXbyS12yWk5ZzrixAeZQSnL8

# Unzip the models and data
RUN unzip model.zip && unzip nuScenes-example-data.zip

# Set the environment variables (assuming the libraries are installed in the standard paths)
RUN sed -i 's@/path/to/TensorRT/lib@/lib/x86_64-linux-gnu@g' tool/environment.sh && \
    sed -i 's@/path/to/TensorRT/include@/usr/include/x86_64-linux-gnu@g' tool/environment.sh && \
    sed -i 's@/path/to/TensorRT/bin@/workspace/tensorrt/bin/@g' tool/environment.sh && \
    sed -i 's@/path/to/cuda/lib64@/usr/local/cuda/lib64@g' tool/environment.sh && \
    sed -i 's@/path/to/cuda/include@/usr/local/cuda/include@g' tool/environment.sh && \
    sed -i 's@/path/to/cuda/bin@/usr/local/cuda/bin@g' tool/environment.sh && \
    sed -i 's@/path/to/cuda@/usr/local/cuda@g' tool/environment.sh && \
    sed -i 's@/path/to/cudnn/lib@/usr/lib/x86_64-linux-gnu@g' tool/environment.sh && \
    sed -i 's@USE_Python=OFF@USE_Python=ON@g' tool/environment.sh
