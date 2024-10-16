from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, FindExecutable, PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    launch_arg_imu_filter = DeclareLaunchArgument(
        'imu_filter',
        default_value='/home/tomas-jelinek/clearpath/platform/config/imu_filter.yaml',
        description='')

    imu_filter = LaunchConfiguration('imu_filter')

    # Include Packages
    pkg_clearpath_platform = FindPackageShare('clearpath_platform')

    # Declare launch files
    launch_file_platform = PathJoinSubstitution([
        pkg_clearpath_platform, 'launch', 'platform.launch.py'])

    # Include launch files
    launch_platform = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_file_platform]),
        launch_arguments=
            [
                (
                    'setup_path'
                    ,
                    '/home/tomas-jelinek/clearpath/'
                )
                ,
                (
                    'use_sim_time'
                    ,
                    'true'
                )
                ,
                (
                    'namespace'
                    ,
                    'a200_0000'
                )
                ,
            ]
    )

    # Nodes
    node_cmd_vel_bridge = Node(
        name='cmd_vel_bridge',
        executable='parameter_bridge',
        package='ros_gz_bridge',
        namespace='a200_0000',
        output='screen',
        arguments=
            [
                'a200_0000/cmd_vel@geometry_msgs/msg/Twist[ignition.msgs.Twist'
                ,
                '/model/a200_0000/robot/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist'
                ,
            ]
        ,
        remappings=
            [
                (
                    'a200_0000/cmd_vel'
                    ,
                    'cmd_vel'
                )
                ,
                (
                    '/model/a200_0000/robot/cmd_vel'
                    ,
                    'platform/cmd_vel_unstamped'
                )
                ,
            ]
        ,
        parameters=
            [
                {
                    'use_sim_time': True
                    ,
                }
                ,
            ]
        ,
    )

    node_odom_base_tf_bridge = Node(
        name='odom_base_tf_bridge',
        executable='parameter_bridge',
        package='ros_gz_bridge',
        namespace='a200_0000',
        output='screen',
        arguments=
            [
                '/model/a200_0000/robot/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V'
                ,
            ]
        ,
        remappings=
            [
                (
                    '/model/a200_0000/robot/tf'
                    ,
                    'tf'
                )
                ,
            ]
        ,
        parameters=
            [
                {
                    'use_sim_time': True
                    ,
                }
                ,
            ]
        ,
    )

    node_imu_0_gz_bridge = Node(
        name='imu_0_gz_bridge',
        executable='parameter_bridge',
        package='ros_gz_bridge',
        namespace='a200_0000',
        output='screen',
        parameters=
            [
                {
                    'use_sim_time': True
                    ,
                    'config_file': '/home/tomas-jelinek/clearpath/sensors/config/imu_0.yaml'
                    ,
                }
                ,
            ]
        ,
    )

    node_imu_filter_node = Node(
        name='imu_filter_node',
        executable='imu_filter_madgwick_node',
        package='imu_filter_madgwick',
        namespace='a200_0000',
        output='screen',
        remappings=
            [
                (
                    'imu/data_raw'
                    ,
                    'sensors/imu_0/data_raw'
                )
                ,
                (
                    'imu/mag'
                    ,
                    'sensors/imu_0/magnetic_field'
                )
                ,
                (
                    'imu/data'
                    ,
                    'sensors/imu_0/data'
                )
                ,
                (
                    '/tf'
                    ,
                    'tf'
                )
                ,
            ]
        ,
        parameters=
            [
                imu_filter
                ,
            ]
        ,
    )

    node_gps_0_gz_bridge = Node(
        name='gps_0_gz_bridge',
        executable='parameter_bridge',
        package='ros_gz_bridge',
        namespace='a200_0000',
        output='screen',
        parameters=
            [
                {
                    'use_sim_time': True
                    ,
                    'config_file': '/home/tomas-jelinek/clearpath/sensors/config/gps_0.yaml'
                    ,
                }
                ,
            ]
        ,
    )

    # Create LaunchDescription
    ld = LaunchDescription()
    ld.add_action(launch_arg_imu_filter)
    ld.add_action(launch_platform)
    ld.add_action(node_cmd_vel_bridge)
    ld.add_action(node_odom_base_tf_bridge)
    ld.add_action(node_imu_0_gz_bridge)
    ld.add_action(node_imu_filter_node)
    ld.add_action(node_gps_0_gz_bridge)
    return ld
