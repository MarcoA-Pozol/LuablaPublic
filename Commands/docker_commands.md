# Docker Common Commands

## Docker Basics
```sh
# Check Docker version
docker --version

# Display system-wide information
docker info
```

## Working with Containers
```sh
# List all running containers
docker ps

# List all containers (including stopped ones)
docker ps -a

# Start a container
docker start container_id

# Stop a running container
docker stop container_id

# Remove a container
docker rm container_id
```

## Working with Images
```sh
# List all images
docker images

# Pull an image from Docker Hub
docker pull image_name

# Remove an image
docker rmi image_name
```

## Running Containers
```sh
# Run a container from an image
docker run -d --name container_name image_name

# Run a container with an interactive shell
docker run -it image_name /bin/bash
```

## Managing Volumes
```sh
# List volumes
docker volume ls

# Create a volume
docker volume create volume_name

# Remove a volume
docker volume rm volume_name
```

## Networks
```sh
# List networks
docker network ls

# Create a network
docker network create network_name

# Connect a container to a network
docker network connect network_name container_id
```

## Docker Compose
```sh
# Start services defined in docker-compose.yml
docker-compose up -d

# Stop services
docker-compose down
```

## Clean Up
```sh
# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove all unused data
docker system prune -a
```