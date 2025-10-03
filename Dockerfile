# use Ubuntu as the base image
FROM ubuntu:22.04

# avoid prompts on build
ENV DEBIAN_FRONTEND=noninteractive

# configure timezone and locales
RUN apt update && apt install -y \
    tzdata \
    locales \
    && ln -fs /usr/share/zoneinfo/UTC /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && locale-gen en_US.UTF-8

# install dependencies
RUN apt update && apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
    python3-dev \
    gfortran \
    libfftw3-dev \
    liblapack-dev \
    libopenblas-dev \
    cmake \
    git \
    wget \
    paraview \
    # optional parallel libraries
    mpi-default-bin \
    mpi-default-dev \
    libopenmpi-dev \
    && rm -rf /var/lib/apt/lists/*

# install mpi4py for parallel processing (optional)
RUN pip3 install mpi4py

# set relative project directory
WORKDIR /Thesis

# clone 3DThesis repo into 3DThesis
RUN git clone https://github.com/ORNL-MDF/3DThesis.git 3DThesis

# set working directory for building 3DThesis
WORKDIR /Thesis/3DThesis

# build 3DThesis
# RUN mkdir build && cd build && \
#     cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=install .. && \
#     cmake --build build --target install -j$(nproc)

RUN mkdir -p /Thesis/3DThesis/build && \
    cd /Thesis/3DThesis/build && \
    cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=install .. && \
    cmake --build . --target install -j$(nproc)

# et the entrypoint to open a bash terminal
ENTRYPOINT ["/bin/bash"]