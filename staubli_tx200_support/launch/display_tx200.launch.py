import os
import launch
import launch_ros
import xacro # Import the xacro library

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    print("generate_launch_description STARTING")

    # Declare the launch argument
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time', 
        default_value='false',
        description='Use simulation clock if true'
    )

    # Get the path to the URDF file
    xacro_file = os.path.join(
        get_package_share_directory('staubli_tx200_support'),
        'urdf',
        'tx200.xacro'
    )

    # Process the xacro file to get the robot_description
    robot_description_content = xacro.process_file(xacro_file).toxml()

    # Define the robot_state_publisher node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'robot_description': robot_description_content  # Pass the processed content directly
        }]
    )

    # IMPORTANT: The GUI is a separate node in ROS2
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )
    # pkg_client = get_package_share_directory('industrial_robot_client')
    # rviz_config_file = os.path.join(pkg_client, 'config', 'robot_state_visualize.rviz')
    rviz_config_file = r'/home/ros2/.rviz2/config.rviz'
    
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )

    return LaunchDescription([
        use_sim_time_arg,
        # The LogInfo actions are fine for debugging but can be removed
        launch.actions.LogInfo(msg=['use_sim_time: ', LaunchConfiguration('use_sim_time')]),
        robot_state_publisher_node, joint_state_publisher_gui_node, rviz_node
    ])