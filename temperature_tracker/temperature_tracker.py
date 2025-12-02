import GPUtil
from os.path import exists

import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor, ParameterType
from sensor_msgs.msg import Temperature


class TemperatureTracker(Node):
    def __init__(self):
        super().__init__("temperature_tracker")
        self.init_parameters()
        self.init_vars()
        self.init_publishers()
        self.timer = self.create_timer(self.publish_rate, self.publish_temperatures)
        self.get_logger().info("[ temperature_tracker ] - [RUNNING]")

    def init_parameters(self):
        self.declare_params()
        self.publish_gpu_temperature = self.get_parameter("publish_gpu_temperature").get_parameter_value().bool_value
        self.publish_cpu_temperature = self.get_parameter("publish_cpu_temperature").get_parameter_value().bool_value
        self.cpu_id = self.get_parameter("cpu_type_id").get_parameter_value().string_value
        self.publish_rate = self.get_parameter("publish_rate").get_parameter_value().double_value

    def declare_params(self):
        self.declare_parameter("publish_gpu_temperature", value=False, 
                               descriptor=ParameterDescriptor(type=ParameterType.PARAMETER_BOOL, 
                                                              description="Enable GPU temperature publishing"))
        self.declare_parameter("publish_cpu_temperature", value=True, 
                               descriptor=ParameterDescriptor(type=ParameterType.PARAMETER_BOOL, 
                                                              description="Enable CPU temperature publishing"))
        self.declare_parameter("cpu_type_id", value="x86_pkg_temp", 
                               descriptor=ParameterDescriptor(type=ParameterType.PARAMETER_STRING, 
                                                              description="CPU ID (dependent on architecture)"))
        self.declare_parameter("publish_rate", value=1.0, 
                               descriptor=ParameterDescriptor(type=ParameterType.PARAMETER_DOUBLE, 
                                                              description="Publish rate of temperatures in seconds"))
        self.declare_parameter("gpu_output_topic", value="gpu_temperature", 
                               descriptor=ParameterDescriptor(type=ParameterType.PARAMETER_STRING, 
                                                              description="ROS2 topic to publish GPU temperature"))
        self.declare_parameter("cpu_output_topic", value="cpu_temperature", 
                               descriptor=ParameterDescriptor(type=ParameterType.PARAMETER_STRING, 
                                                              description="ROS2 topic to publish CPU temperature"))

    def init_publishers(self):
        if self.publish_cpu_temperature:
            self.cpu_output_topic = self.get_parameter("cpu_output_topic").get_parameter_value().string_value
            self.cpu_publisher = self.create_publisher(Temperature, self.cpu_output_topic, 10)
            self.get_logger().info(f"Publishing CPU temperature on topic: [ {self.cpu_output_topic} ]...")
        if self.publish_gpu_temperature and (len(self.GPUs) > 0):
            self.gpu_publishers = []
            for i in range(len(self.GPUs)):
              gpu_output_topic = f'{self.get_parameter("gpu_output_topic").get_parameter_value().string_value}{i}'
              self.gpu_publishers.append(self.create_publisher(Temperature, gpu_output_topic, 10))
              self.get_logger().info(f"Publishing GPU temperature on topic: [ {gpu_output_topic} ]...")
        if not self.publish_gpu_temperature and not self.publish_cpu_temperature:
            self.get_logger().warning("Not publishing CPU or GPU temperature. Is this intentional?")

    def init_vars(self):
        if self.publish_cpu_temperature:
            self.cpu_temp_msg = Temperature()
            self.cpu_temp_msg.header.frame_id = "CPU"
            self.cpu_zone = self.find_cpu_zone()

        if self.publish_gpu_temperature:
            try:
                self.GPUs = GPUtil.getGPUs()
                self.gpu_temp_msg = Temperature()
            except:
                self.get_logger().error("Publish GPU set to True but no GPU was found. Try 'nvidia-smi' to see if GPU is being detected.")

    def find_cpu_zone(self):
        i = 0
        while(exists(f'/sys/class/thermal/thermal_zone{str(i)}/type')):
            file = open(f'/sys/class/thermal/thermal_zone{str(i)}/type', "r")
            data = file.read().strip()
            if data == self.cpu_id:
                return i
            else:
                i += 1
        self.get_logger().warning("No CPU Zone Found. Unable to read temperature.")
        return -1

    def get_cpu_temperature(self):
        if self.cpu_zone != -1:
            temperature_file_path = f'/sys/class/thermal/thermal_zone{str(self.cpu_zone)}/temp'
            temperature_file = open(temperature_file_path, "r")
            temperature = int(temperature_file.read().strip())
            temperature_file.close()
            return float(temperature/1000.0)

    def get_gpu_temperature(self, gpu):
        return gpu.temperature

    def publish_temperatures(self):
        if self.publish_cpu_temperature:
            self.cpu_temp_msg.temperature = self.get_cpu_temperature()
            self.cpu_temp_msg.header.stamp = self.get_clock().now().to_msg()
            self.cpu_publisher.publish(self.cpu_temp_msg)
        if self.publish_gpu_temperature:
            for i in range(len(self.GPUs)):
              gpu = self.GPUs[i]
              self.gpu_temp_msg.temperature = self.get_gpu_temperature(gpu)
              self.gpu_temp_msg.header.stamp = self.get_clock().now().to_msg()
              self.gpu_temp_msg.header.frame_id = gpu.name
              self.gpu_publishers[i].publish(self.gpu_temp_msg)

def main(args=None):
    rclpy.init(args=args)
    tracker = TemperatureTracker()
    while rclpy.ok():
        rclpy.spin(tracker)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
