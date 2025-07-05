# Launches Gazebo with specified dynamic event

# Each dynamic event is associated with an vehicle spawn origin and a map

import os

from ament_index_python import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, TimerAction
from launch.actions import IncludeLaunchDescription
from launch.actions import SetLaunchConfiguration
from launch.actions import GroupAction
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import TextSubstitution, IfElseSubstitution, EqualsSubstitution
from launch.substitutions import FindExecutable
from launch.conditions import IfCondition
from launch_ros.actions import Node

def generate_launch_description():

    # vehicle model file (hard-coded, but can be extended to get path from user)
    model_file = os.path.join(get_package_share_directory('simulation'),
                               'models/vehicle/ads_dv.sdf')
    
    # copy file contents
    with open(model_file, 'r') as infp:
        robot_desc = infp.read()

    # args that can be set from the command line or a default will be used
    event_launch_arg = DeclareLaunchArgument(
        "event", default_value=TextSubstitution(text="acceleration")
    )
    model_file_launch_arg = DeclareLaunchArgument(
        "model_file", default_value=TextSubstitution(text=model_file)
    )
    name_launch_arg = DeclareLaunchArgument(
        "name", default_value=TextSubstitution(text="ads_dv")
    )
    autostart_launch_arg = DeclareLaunchArgument(
        "autostart", default_value=TextSubstitution(text="true")
    )
    verbosity_launch_arg = DeclareLaunchArgument(
        "verbosity", default_value=TextSubstitution(text="1")
    )
    
    set_autostart = SetLaunchConfiguration(
        name='autostart_flag',
        value=IfElseSubstitution(
            LaunchConfiguration("autostart"),
            if_value="-r",
            else_value=""),
    )

    set_acceleration = GroupAction([
        SetLaunchConfiguration(
             name='x',
             value='-51.0'
        ),
        SetLaunchConfiguration(
            name='y',
            value='0.0'
        ),
        SetLaunchConfiguration(
             name='z',
             value='0.0'
        ),
        SetLaunchConfiguration(
            name='R',
            value='0.0'
        ),
        SetLaunchConfiguration(
             name='P',
             value='0.0'
        ),
        SetLaunchConfiguration(
            name='Y',
            value='0.0'
        ),
        SetLaunchConfiguration(
            name='world',
            value='map'
        ),
        SetLaunchConfiguration(
            name='map_file',
            value='acceleration.sdf'
        )
        ], 
        scoped=False,
        condition=IfCondition(
            EqualsSubstitution(LaunchConfiguration('event'), "acceleration")
            )
    )

    set_skidpad = GroupAction([
        SetLaunchConfiguration(
             name='x',
             value='0.0'
        ),
        SetLaunchConfiguration(
            name='y',
            value='-12.0'
        ),
        SetLaunchConfiguration(
             name='z',
             value='0.0'
        ),
        SetLaunchConfiguration(
            name='R',
            value='0.0'
        ),
        SetLaunchConfiguration(
             name='P',
             value='0.0'
        ),
        SetLaunchConfiguration(
            name='Y',
            value='1.57079632679'
        ),
        SetLaunchConfiguration(
            name='world',
            value='map'
        ),
        SetLaunchConfiguration(
            name='map_file',
            value='skidpad.sdf'
        )
        ], 
        scoped=False,
        condition=IfCondition(
            EqualsSubstitution(LaunchConfiguration('event'), "skidpad")
            )
    )

    set_autocross = GroupAction([
        SetLaunchConfiguration(
             name='x',
             value='0.0'
        ),
        SetLaunchConfiguration(
            name='y',
            value='0.0'
        ),
        SetLaunchConfiguration(
             name='z',
             value='0.0'
        ),
        SetLaunchConfiguration(
            name='R',
            value='0.0'
        ),
        SetLaunchConfiguration(
             name='P',
             value='0.0'
        ),
        SetLaunchConfiguration(
            name='Y',
            value='0.0'
        ),
        SetLaunchConfiguration(
            name='world',
            value='map'
        ),
        SetLaunchConfiguration(
            name='map_file',
            value='autocross.sdf'
        )
        ], 
        scoped=False,
        condition=IfCondition(
            EqualsSubstitution(LaunchConfiguration('event'), "autocross")
            )
    )

    set_trackdrive = GroupAction([
        SetLaunchConfiguration(
             name='x',
             value='0.0'
        ),
        SetLaunchConfiguration(
            name='y',
            value='0.0'
        ),
        SetLaunchConfiguration(
             name='z',
             value='0.0'
        ),
        SetLaunchConfiguration(
            name='R',
            value='0.0'
        ),
        SetLaunchConfiguration(
             name='P',
             value='0.0'
        ),
        SetLaunchConfiguration(
            name='Y',
            value='0.0'
        ),
        SetLaunchConfiguration(
            name='world',
            value='map'
        ),
        SetLaunchConfiguration(
            name='map_file',
            value='trackdrive.sdf'
        )
        ], 
        scoped=False,
        condition=IfCondition(
            EqualsSubstitution(LaunchConfiguration('event'), "trackdrive")
            )
    )

    set_gz_args = SetLaunchConfiguration(
        name='gz_args',
        value=[LaunchConfiguration('map_file'), ' ',
               LaunchConfiguration('autostart_flag'), ' ',
               '-v ', LaunchConfiguration('verbosity')]
    )

    ros_gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('ros_gz_sim'), 'launch'),
                '/gz_sim.launch.py']),
        launch_arguments={'gz_args': LaunchConfiguration('gz_args')}.items(),
        )
    
    spawn_vehicle = Node(
        package="ros_gz_sim",
        executable="create",
        name="create_node",
        output="both",
        parameters=[
            {'world': LaunchConfiguration('world')},
            {'file': "ads_dv.sdf"},
            {'name': LaunchConfiguration('name')},
            {'x': LaunchConfiguration('x')},
            {'y': LaunchConfiguration('y')},
            {'z': LaunchConfiguration('z')},
            {'R': LaunchConfiguration('R')},
            {'P': LaunchConfiguration('P')},
            {'Y': LaunchConfiguration('Y')}
        ]
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[
            {'use_sim_time': True},
            {'robot_description': robot_desc},
        ]
    )

    spawn_pose_publisher = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="spawn_pose_publisher",
        arguments=[
            "--x", LaunchConfiguration('x'),
            "--y", LaunchConfiguration('y'),
            "--z", LaunchConfiguration('z'),
            "--roll", LaunchConfiguration('R'),
            "--pitch", LaunchConfiguration('P'),
            "--yaw", LaunchConfiguration('Y'),
            "--frame-id", LaunchConfiguration('world'),
            "--child-frame-id", "ads_dv"
        ]
    )

    ros_gz_bridge = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('simulation'), 'launch'),
                '/ros_gz_bridge.launch.py']),
        )


    return LaunchDescription([
        event_launch_arg,
        model_file_launch_arg,
        name_launch_arg,
        autostart_launch_arg,
        verbosity_launch_arg,

        set_autostart,
        set_acceleration,
        set_skidpad,
        set_autocross,
        set_trackdrive,
        set_gz_args,
        
        ros_gz_sim,
        spawn_vehicle,
        robot_state_publisher,
        spawn_pose_publisher,
        ros_gz_bridge
    ])
