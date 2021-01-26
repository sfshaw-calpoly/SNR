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

lin_control_mappings = {
    "number": [None],
    "name": ["controller_name"],
    "axis_0": ["stick_left_x", int,  100, 0, 0],
    "axis_1": ["stick_left_y", int, -100, 0, 0],
    "axis_2": ["trigger_left", int, 50, 50, 0],
    "axis_3": ["stick_right_x", int, 100, 0, 0],
    "axis_4": ["stick_right_y", int, -100, 0, 0],
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
win_control_mappings = {
    "number": [None],
    "name": ["controller_name"],
    "axis_0": ["stick_left_x", int,  100, 0, 0],
    "axis_1": ["stick_left_y", int, -100, 0, 0],
    "axis_2": ["trigger_left", int, 100, 0, 0],
    "axis_3": ["stick_right_y", int, 100, 0, 0],
    "axis_4": ["stick_right_x", int, -100, 0, 0],
    "axis_5": ["trigger_right", int, 100, 0, 0],
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