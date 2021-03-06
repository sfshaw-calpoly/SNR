"""Configurable settings that apply to the operation of the robot
"""


import logging
from typing import Dict, List, Union

from .mode import Mode


class Settings:
    # Debugging printing and logging
    # TODO: Track debugging for server and client separately
    DEBUGGING_DELAY_S = 0
    DEBUG_PRINTING = True
    DEBUG_LOGGING = False  # Not yet implemented
    DEBUG_CHANNELS = {
        "camera_event": True,
        "camera_verbose": False,

        "controller": False,
        "controller_error": True,
        "controller_event": False,
        "controller_verbose": False,
        "controls_reader": False,
        "controls_reader_verbose": False,
        "control_mappings": False,
        "control_mappings_verbose": False,

        "datastore": True,
        "datastore_dump": True,
        "datastore_error": True,
        "datastore_event": False,
        "datastore_verbose": False,

        "discovery_server_verbose": True,

        "execute_task": True,
        "execute_task_verbose": True,

        "encode": False,
        "encode_verbose": False,
        "decode": False,
        "decode_verbose": False,

        "framework": True,
        "framework_warning": False,
        "framework_verbose": True,

        "gui_verbose": False,
        "gui_telem": False,
        "gui_control": False,

        "int_temp_mon": True,

        "motor_control": False,
        "motor_control_verbose": False,

        "node": True,
        "node_verbose": False,

        "proc_endpoint_error": True,
        "proc_endpoint_event": False,

        "profiling_avg": True,
        "profiling_task": True,
        "profiling_endpoint": True,
        "profiling_dump": True,

        "robot": True,
        "robot_verbose": False,

        "robot_control": True,
        "robot_control_warning": True,
        "robot_control_event": False,
        "robot_control_verbose": False,

        "schedule": True,
        "schedule_warn": True,
        "schedule_event": False,
        "schedule_verbose": False,
        "schedule_new_tasks": False,

        "serial": True,
        "serial_finder": True,
        "serial_error": True,
        "serial_warning": True,
        "serial_verbose": False,
        "serial_sim": False,

        "serial_packet": False,

        "simulation": False,
        "simulation_verbose": False,

        "sleep": True,

        "sockets": True,
        "sockets_client": False,
        "sockets_server": False,
        "sockets_error": False,
        "sockets_critical": False,
        "sockets_warning": True,
        "sockets_event": False,
        "sockets_status": False,
        "sockets_verbose": False,

        "sockets_send": False,
        "sockets_send_verbose": False,

        "sockets_receive": False,
        "sockets_receive_verbose": False,

        "telemetry_verbose": True,

        "test": True,

        "thrust_vec": True,
        "thrust_vec_verbose": False,

        "throttle": True,
        "throttle_values": True,
        "throttle_verbose": False,
        "axis_update_verbose": False,
    }

    NODE_SLEEP_TIME = 0.015  # eg 0.015 -> max 30 tasks per second
    THREAD_END_WAIT_S = 2
    DISABLE_SLEEP = False
    ENABLE_PROFILING = True
    PROFILING_AVG_WINDOW_LEN = 30

    # Command Line User Interface
    USE_TOPSIDE_CLUI = False
    TOPSIDE_CLUI_NAME = "topside_clui"
    UI_DATA_KEY = "UI_data"
    TOPSIDE_UI_TICK_RATE = 24  # Hz (Times per second)
    USE_GUI = True
    USE_GUI_ELEMENTS = {
        "controller": True,
        "telem": True
    }

    # XBox Controller
    USE_CONTROLLER: bool = True
    REQUIRE_CONTROLLER = False
    SIMULATE_INPUT: bool = False
    CONTROLLER_NAME = "topside_xbox_controller"
    CONTROLLER_INIT_TICK_RATE = 1
    CONTROLLER_TICK_RATE = 30  # Hz (Times per second)
    CONTROLLER_ZERO_TRIGGERS = True
    '''Mapping of pygame joystick output to values we can make sense of
    Examples:
    "pygame_name": ["name_we_use"],
    "pygame_name": ["name_we_use", cast_type],
    "pygame_name": ["name_we_use", cast_type, scale_factor],
    "pygame_name": ["name_we_use", cast_type, scale_factor, shift_ammount],
    "pygame_name": ["name_we_use", cast_type, scale_factor, shift_ammount,
                    dead_zone],
    to drop a value use "pygame_name": [None],
    '''
    control_mappings: Dict[str, List[Union[None, str, type, int]]] = {
        "number": [None],
        "name": ["controller_name"],
        "axis_0": ["stick_left_x", int, 100, 0, 10],
        "axis_1": ["stick_left_y", int, -100, 0, 10],
        "axis_2": ["trigger_left", int, 50, 50, 0],
        "axis_3": ["stick_right_x", int, 100, 0, 10],
        "axis_4": ["stick_right_y", int, -100, 0, 10],
        "axis_5": ["trigger_right", int, 50, 50, 0],
        "button_0": ["button_a", bool],
        "button_1": ["button_b", bool],
        "button_2": ["button_x", bool],
        "button_3": ["button_y", bool],
        "button_4": ["button_left_bumper", bool],
        "button_5": ["button_right_bumper", bool],
        "button_6": ["button_back", bool],
        "button_7": ["button_start", bool],
        "button_8": ["button_xbox", bool],
        "button_9": ["button_left_stick", bool],
        "button_10": ["button_right_stick", bool],
        "dpad": ["dpad", tuple],
        "num_buttons": [None],
        "num_dpad": [None],
        "num_axes": [None],
    }

    # Log Levels
    log_level: Dict[Mode, int] = {
        Mode.TEST: logging.WARNING,
        Mode.DEBUG: logging.DEBUG,
        Mode.DEPLOYED: logging.INFO,
    }

    # Robot Control
    THROTTLE_DATA_NAME = "robot_throttle_data"

    # Motor control
    MOTOR_CONTROL_TICK_RATE = 15
    DEFAULT_MOTOR_VALUE = 0
    NUM_MOTORS = 6
    MOTOR_MAX_DELTA = 5

    DISCOVERY_SERVER_PORT = 39129

    # Sockets Connection
    SOCKETS_SERVER_TIMEOUT = 640
    SOCKETS_CLIENT_TIMEOUT = 4
    SOCKETS_OPEN_ATTEMPTS = 10
    SOCKETS_MAX_CONNECTIONS = 2  # Maximun concurrent connections
    # Should only ever be 1, after 2 thigns have gone very wrong
    # Maximum number of times to try creating or opening a socket
    SOCKETS_CONNECT_ATTEMPTS = 120
    SOCKETS_RETRY_WAIT_S = 1  # seconds to wait before retrying
    MAX_SOCKET_SIZE = 8192  # Maximum size for single receiving call
    '''Note: SOCKETS_CONNECT_ATTEMPTS * SOCKETS_RETRY_WAIT = sockets timeout
        connection
        This timeout should be very long to allow the server to open its socket
        before the client gives up on connecting to it.
    '''

    # Controls Sockets Connection
    # USE_CONTROLS_SOCKETS = True
    # REQUIRE_CONTROLS_SOCKETS = True
    # controls_server_ip = TOPSIDE_IP
    # controls_server_port = 9120
    # CONTROLS_SOCKETS_CONFIG = SocketsConfig(controls_server_ip,
    #                                         controls_server_port,
    #                                         # REQUIRE_CONTROLS_SOCKETS
    #                                         )

    # Telemetry Sockets Connection
    # USE_TELEMETRY_SOCKETS = True
    # REQUIRE_TELEMETRY_SOCKETS = True
    # telemetry_server_ip = ROBOT_IP
    # telemetry_server_port = 9121
    # TELEMETRY_SOCKETS_CONFIG = SocketsConfig(telemetry_server_ip,
    #                                          telemetry_server_port,
    #                                          REQUIRE_TELEMETRY_SOCKETS)

    # Serial Connection
    SIMULATE_SERIAL = True
    SERIAL_BAUD = 115200  # Serial Baudrate
    SERIAL_MAX_ATTEMPTS = 4  # Maximum number of times to connect
    SERIAL_RETRY_WAIT_S = 0.5  # Time to wait before retrying serial connection
    SERIAL_TIMEOUT = 4
    SERIAL_SETUP_WAIT_PRE_S = 1
    SERIAL_SETUP_WAIT_POST = 1

    # Zynq Zybo FPGA DMA
    SIMULATE_DMA = False

    # Temperature Monitor
    USE_ROBOT_PI_TEMP_MON = False
    SIMULATE_ROBOT_INT_TEMP = True  # TODO: Implement temperature simulation

    ROBOT_INT_TEMP_NAME = "robot_int_temp_mon"
    INT_TEMP_MON_TICK_RATE = 0.25  # Hz (Readings per second)
    INT_TEMP_MON_AVG_PERIOD = 4  # Number of readings to average over

    # Robot selection
    ROBOT_NAME = "Seaymour"
