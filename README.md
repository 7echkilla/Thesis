## Repository structure

Thesis\
└── 3DThesis

### Install docker
- sudo apt install docker.io

### Enable docker service on session
- sudo systemctl start docker

### Build docker image: 
- cd ~/Project/Thesis
- sudo docker build -t 3dthesis_image .
  - -t 3dthesis_image specifies the tag for your image (i.e., 3dthesis_image is the name of the image).
  - . tells Docker to use the current directory (where the Dockerfile is) as the build context.

### Run the container:
- docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --device /dev/dri:/dev/dri --group-add video --privileged -e XDG_RUNTIME_DIR=/tmp/runtime-root 3dthesis_image
  - -it: Runs the container in interactive mode and allocates a terminal.
  - --rm: Removes the container once it's stopped.
- Run a simulation: ./Thesis/3DThesis/build/application/3dThesis ParamInput.txt
- Run simulation in parallel: mpirun -np [num_processors] ./Thesis/3DThesis/build/application/3dThesis ParamInput.txt
  - /bin/bash: Opens terminal inside the active container.
  - mpirun --version: Shows the version of OpenMPI

### Stop & Remove the container:
- sudo docker ps -a   # List all containers (including stopped ones)
- sudo docker stop <container_id>
- sudo docker rm <container_id> 

### Remove the image:
- docker rmi 3dthesis_image

### Stop docker service on session end:
- sudo systemctl stop docker

### Restart docker after config changes:
- sudo systemctl restart docker

### Docker service status:
- sudo systemctl status docker

### Check for images:
- sudo docker images

### Run simulation while in container:
- /Thesis/3DThesis/examples/snapshot# /Thesis/3DThesis/build/./bin/3DThesis ./ParamInput.txt 