##########################################################################
#                                                                        #
# Soubor: argument_handler.py                                            #
# Vytvoren: 2022-04-03                                                   #
# Posledni zmena: 2022-04-03                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Skript pro zpracovani uzivatelskych argumentu                   #
#                                                                        #
##########################################################################

import re

from custom_exception import InvalidXMLFormat, FrameNotExist, VariableNotExist


def save_var_to_frame(runtime_environment, var_frame, var_name, var_act_value):
    if var_frame == "GF":
        global_frame = runtime_environment["global_frame"]
        if var_name in global_frame.keys():
            global_frame[var_name] = var_act_value
        else:
            global_frame.update({var_name: var_act_value})

    elif var_frame == "LF":
        local_frames_stack = runtime_environment["local_frames_stack"]

        if len(local_frames_stack) == 0:
            raise FrameNotExist

        local_frame = local_frames_stack[-1]  # posledni lokalni ramec

        if var_name in local_frame.keys():
            local_frame[var_name] = var_act_value
        else:
            local_frame.update({var_name: var_act_value})

    elif var_frame == "TF":
        tmp_frame = runtime_environment["tmp_frame"]

        if tmp_frame is None:
            raise FrameNotExist
        else:
            if var_name in tmp_frame.keys():
                tmp_frame[var_name] = var_act_value
            else:
                tmp_frame.update({var_name: var_act_value})

    else:
        raise InvalidXMLFormat


def check_is_existing_variable(runtime_environment, var_frame, var_name):
    if var_frame == "GF":
        global_frame = runtime_environment["global_frame"]

        if var_name not in global_frame.keys():
            raise VariableNotExist

    elif var_frame == "LF":
        local_frames_stack = runtime_environment["local_frames_stack"]

        if len(local_frames_stack) == 0:
            raise FrameNotExist

        local_frame = local_frames_stack[-1]

        if var_name not in local_frame.keys():
            raise VariableNotExist

    elif var_frame == "TF":
        tmp_frame = runtime_environment["tmp_frame"]

        if tmp_frame is None:
            raise FrameNotExist

        if var_name not in tmp_frame.keys():
            raise VariableNotExist


# https://stackoverflow.com/questions/21300996/process-decimal-escape-in-string
def replace(match):
    return chr(int(match.group(1)))


def process_decimal_escape(string_value):
    regex = re.compile(r"\\(\d{1,3})")
    new_value = regex.sub(replace, string_value)

    return new_value


def bool_str_2_bool(bool_val):
    if bool_val == "true":
        return True
    elif bool_val == "false":
        return False
    else:
        raise InvalidXMLFormat


def int_str_2_int(int_val):
    try:
        val = int(int_val)
    except ValueError:
        raise

    return val


def get_var_val(runtime_environment, var_frame, var_name):
    if var_frame == "GF":
        global_frame = runtime_environment["global_frame"]

        if var_name not in global_frame.keys():
            raise VariableNotExist

        var_value = global_frame[var_name]

    elif var_frame == "LF":
        local_frames_stack = runtime_environment["local_frames_stack"]

        if len(local_frames_stack) == 0:
            raise FrameNotExist

        local_frame = local_frames_stack[-1]

        if var_name not in local_frame.keys():
            raise VariableNotExist

        var_value = local_frame[var_name]

    elif var_frame == "TF":
        tmp_frame = runtime_environment["tmp_frame"]

        if tmp_frame is None:
            raise FrameNotExist

        if var_name not in tmp_frame.keys():
            raise VariableNotExist

        var_value = tmp_frame[var_name]

    else:
        raise InvalidXMLFormat

    return var_value


def get_not_var_val(arg):
    arg_type = arg.get_type()

    if arg_type == "string":
        val = arg.get_val()

    elif arg_type == "type":
        val = arg.get_val()

    elif arg_type == "bool":
        try:
            val = bool_str_2_bool(arg.get_val())
        except InvalidXMLFormat:
            raise

    elif arg_type == "nil":
        val = arg.get_val()

    elif arg_type == "int":
        try:
            val = int_str_2_int(arg.get_val())
        except ValueError:
            raise InvalidXMLFormat

    elif arg_type == "label":
        val = arg.get_val()

    else:
        raise InvalidXMLFormat

    return val


def get_arg_val(runtime_environment, arg):
    if arg.get_type() == "var":
        var_frame = arg.get_var_frame()
        var_name = arg.get_var_name()

        return get_var_val(runtime_environment, var_frame, var_name)

    return get_not_var_val(arg)
