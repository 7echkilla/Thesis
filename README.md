### install docker
- sudo apt install docker.io

### enable docker service on session
- sudo systemctl start docker

### Build docker image: 
- cd ~/Project/Thesis
- docker build -t 3dthesis_image .
  - -t 3dthesis_image specifies the tag for your image (i.e., 3dthesis_image is the name of the image).
  - . tells Docker to use the current directory (where the Dockerfile is) as the build context.

### Run the container:
- docker run -it --rm 3dthesis_image /bin/bash
  - -it: Runs the container in interactive mode and allocates a terminal.
  - --rm: Removes the container once it's stopped.
- Run a simulation: ./Thesis/3DThesis/build/application/3dThesis ParamInput.txt
- Run simulation in parallel: mpirun -np [num_processors] ./Thesis/3DThesis/build/application/3dThesis ParamInput.txt
  - /bin/bash: Opens terminal inside the active container.
  - mpirun --version: Shows the version of OpenMPI

### Stop & Remove the container:
- docker ps -a   # List all containers (including stopped ones)
- docker stop <container_id>
- docker rm <container_id> 

### Remove the image:
- docker rmi 3dthesis_image

### Stop docker service on session end:
- sudo systemctl stop docker

### Restart docker after config changes:
- sudo systemctl restart docker

### Docker service status:
- sudo systemctl status docker