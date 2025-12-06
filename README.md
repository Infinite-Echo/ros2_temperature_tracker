# ros2_temperature_tracker
ROS 2 Package to monitor and publish **CPU** and **GPU** temperatures

## **Build**
1. **Download** the repository:

```bash
git clone https://github.com/Infinite-Echo/ros2_temperature_tracker.git --depth 1 --single-branch
```

2. **Navigate** into the project root:

```bash
cd ros2_temperature_tracker
```

3. **Build** docker image of `ros2_temperature_tracker`:

```bash
bash scripts/1_build_docker_image.bash
```

## **Run**

**Run** docker container of `ros2_temperature_tracker`:

>Note: The command below only runs ros2_temperature_tracker to show only CPU.

```bash
bash scripts/2_run_docker_container_cpu.bash
```

>Note: The command below only runs ros2_temperature_tracker to show CPU and GPU.

```bash
bash scripts/3_run_docker_container_gpu.bash
```


## **Verify** 

By running the aforementioned command, you should see a similar terminal output when you run the command below:

```bash
docker exec -it ros2_temperature_tracker_c bash -c "source /temperature_tracker_ws/install/setup.bash && ros2 topic echo /cpu_temperature"
```

```bash
header:
  stamp:
    sec: 0
    nanosec: 0
  frame_id: CPU
temperature: 47.0
variance: 0.0
---
header:
  stamp:
    sec: 0
    nanosec: 0
  frame_id: CPU
temperature: 48.0
variance: 0.0
---
```

## **Parameters**
### publish_gpu_temperature
Enables GPU temperature publishing. 

>Note: Only enable if using an Nvidia GPU. Other GPUs are not supported.
>> If you have an nvidia GPU and it is not being detected by the node, try using 'nvidia-smi' in a terminal. 


### publish_cpu_temperature
Enables CPU temperature publishing.

>Note: This works by reading directly from thermal files in the system. It has been tested on Ubuntu `20.04` and `24.04`.


### cpu_type_id
The string value found in `/sys/class/thermal/thermal_zone*/type`:

>Note: Usually "x86_pkg_temp" represents the CPU. This may be different depending on CPU architecture.

Use the command below for auto-configuration of a localized CPU core sensor.

```bash
bash scripts/5_configure_params.bash
```

### gpu_output_topic

The string value representing the desired output topic name for the GPU temperature to be published on


### cpu_output_topic

The string value representing the desired output topic name for the CPU temperature to be published on


### publish_rate

Time in seconds for the temperatures to be published

>Note: This must be a double value. Using a value without a decimal in the params file will result in an error (i.e., '1' should be '1.0').
