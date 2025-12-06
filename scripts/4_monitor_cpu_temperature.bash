#!/usr/bin/env bash

docker exec -it ros2_temperature_tracker_c bash -c "source /ros_entrypoint.sh && ros2 topic echo /cpu_temperature"
