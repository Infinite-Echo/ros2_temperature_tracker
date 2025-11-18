from setuptools import setup

package_name = 'temperature_tracker'

setup(
    name=package_name,
    version='0.2.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='colin',
    maintainer_email='colin.fuelberth@icloud.com',
    description='A ROS 2 Package to monitor and publish CPU and GPU temperatures',
    license='MIT License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'temperature_tracker = temperature_tracker.temperature_tracker:main'
        ],
    },
)
