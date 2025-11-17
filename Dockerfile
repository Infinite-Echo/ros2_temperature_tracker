FROM ros:jazzy

# Install build tools
RUN apt-get update && apt-get install -y \
    git \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

# Create workspace
WORKDIR /ros2_ws/src

# Fetch repo
# RUN git clone https://github.com/cardboardcode/ros2_temperature_tracker.git
RUN mkdir ros2_temperature_tracker 
COPY ./ ./ros2_temperature_tracker

# Install rosdep dependencies
WORKDIR /ros2_ws
RUN apt-get update && rosdep update && rosdep install --from-paths src -i -y

# Build
RUN . /opt/ros/jazzy/setup.sh && colcon build --symlink-install

# Source workspace on container entry
RUN echo "source /ros2_ws/install/setup.bash" >> /root/.bashrc

CMD ["/bin/bash"]
