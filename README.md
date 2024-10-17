# Configuration of Jackal robot

Robot.yaml file is the most important, it has all the configuration of the used robot and also link to the custom workspace for the simulation which has been downloaded from the Clearpath docsheets.


# Jackal Robot Configuration
**Overview** This package contains the configuration files for simulating a Jackal robot. The most important file is robot.yaml, which contains the sensor, controller, and URDF configurations.

**Explanation of the configuration**
https://docs.clearpathrobotics.com/docs/ros/config/yaml/sensors/overview

#
**Key File:**

**robot.yaml**: This file defines the configuration for the robot's sensors (like LiDAR) and controllers (for velocity, IMU, etc.).
Custom workspace link: The robot configuration uses a custom simulation workspace, which is downloaded from the ClearPath documentation. Ensure you’ve sourced the proper workspace before launching the simulation.


Modifying the robot.yaml This file can be customized for additional sensors, actuators, or robot-specific parameters. For example, adding or modifying LiDAR sensor configurations or adjusting controller parameters for improved performance.

