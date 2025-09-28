from moveit_configs_utils import MoveItConfigsBuilder
from launch import LaunchDescription
from launch_ros.actions import Node # We need to import Node now

# Use the correct function names from your launches.py file
from moveit_configs_utils.launches import (
    generate_static_virtual_joint_tfs_launch,
    generate_rsp_launch,
    generate_move_group_launch,
    # We no longer need generate_spawn_controllers_launch
    generate_moveit_rviz_launch,
)

def generate_launch_description():
    # Build the config dictionary
    moveit_config = (
        MoveItConfigsBuilder("staubli_tx200", package_name="staubli_tx200_moveit_config")
        .to_moveit_configs()
    )

    # --- Create the list of launch entities ---

    # 1. Start the Robot State Publisher
    robot_state_publisher_launch = generate_rsp_launch(moveit_config)

    # 2. Start RViz
    rviz_launch = generate_moveit_rviz_launch(moveit_config)

    # 3. Start the static virtual joint transforms
    static_tf_launch = generate_static_virtual_joint_tfs_launch(moveit_config)

    # 4. Start the MoveGroup node
    move_group_launch = generate_move_group_launch(moveit_config)
    
    # --- MODIFIED: Manually create the spawner nodes ---
    # This is the logic copied from the helper function, but modified.
    
    # Define the list of controllers you want to spawn.
    # We are explicitly OMITTING "joint_state_broadcaster".
    controllers_to_spawn = ["staubli_manipulator_controller"]
    
    # Create a list to hold the spawner nodes
    spawner_nodes = []
    for controller in controllers_to_spawn:
        spawner_nodes.append(
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=[controller],
                output="screen",
            )
        )
    
    # --- Build the final LaunchDescription ---
    # We create a list of all the launch actions we want to run
    launch_actions = [
        robot_state_publisher_launch,
        rviz_launch,
        static_tf_launch,
        move_group_launch,
    ]
    # Add all the spawner nodes to the list
    launch_actions.extend(spawner_nodes)

    return LaunchDescription(launch_actions)