FROM ros:jazzy

# Install build tools + pip
RUN apt-get update && apt-get install -y \
    git \
    python3-pip \
    python3-colcon-common-extensions \
    ros-jazzy-rmw-cyclonedds-cpp \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps used by temperature tracker
RUN pip3 install --no-cache-dir GPUtil --break-system-packages

# Create workspace
WORKDIR /temperature_tracker_ws/src

# Fetch repo
RUN mkdir ros2_temperature_tracker 
COPY ./ ./ros2_temperature_tracker

# Install rosdep dependencies
WORKDIR /temperature_tracker_ws
RUN apt-get update && rosdep update && rosdep install --from-paths src -i -y

# Build
RUN . /opt/ros/jazzy/setup.sh && colcon build --symlink-install

# Source workspace on container entry
RUN echo "source /temperature_tracker_ws/install/setup.bash" >> /root/.bashrc

CMD ["/bin/bash"]
