#!/usr/bin/env bash

script_dir="$(dirname "$(realpath "$0")")"

set -e

CONTAINER_NAME="ros2_temperature_tracker_c"

echo "=== Checking for existing container: $CONTAINER_NAME ==="

# Stop container if running
if [ "$(docker ps -q -f name=^${CONTAINER_NAME}$)" ]; then
    echo "Stopping running container..."
    docker stop "$CONTAINER_NAME"
fi

# Remove container if it exists (running or exited)
if [ "$(docker ps -aq -f name=^${CONTAINER_NAME}$)" ]; then
    echo "Removing existing container..."
    docker rm "$CONTAINER_NAME"
fi

echo "=== Starting docker compose ==="
docker compose -f ${script_dir}/docker_cpu.compose.yaml up -d

echo "=== Done! ==="
docker ps -f name=$CONTAINER_NAME

unset script_dir
