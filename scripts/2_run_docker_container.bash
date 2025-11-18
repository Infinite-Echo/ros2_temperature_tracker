#!/usr/bin/env bash

PARAM_FILE="/temperature_tracker_ws/temperature_tracker_parameters.yaml"

docker run -it --rm \
  --privileged \
  --name ros2_temperature_tracker_c \
  -v /sys/class/thermal:/sys/class/thermal:ro \
  -v /sys/devices/virtual/thermal:/sys/devices/virtual/thermal:ro \
  -v /sys/class/hwmon:/sys/class/hwmon:ro \
  -v ./params/temperature_tracker_parameters.yaml:$PARAM_FILE \
  -e RMW_IMPLEMENTATION=rmw_cyclonedds_cpp \
  ros2_temperature_tracker:jazzy bash \
  -c "source /temperature_tracker_ws/install/setup.bash && \
  ros2 run temperature_tracker temperature_tracker \
  --ros-args --params-file $PARAM_FILE \
  "