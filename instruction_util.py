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

from custom_exception import FrameNotExist, VariableNotExist

def save_var_to_frame(runtime_enviroment, var_frame, var_name, var_act_value):
    if var_frame == "GF":
        global_frame = runtime_enviroment["global_frame"]
        if var_name in global_frame.keys():
            global_frame[var_name] = var_act_value
        else:
            global_frame.update({var_name : var_act_value})

    elif var_frame == "LF":
        local_frames_stack = runtime_enviroment["local_frames_stack"]

        if len(local_frames_stack) == 0:
            # TODO error
            raise FrameNotExist

        local_frame = local_frames_stack[-1] # posledni lokalni ramec

        if var_name in local_frame.keys():
            local_frame[var_name] = var_act_value
        else:
            local_frame.update({var_name: var_act_value})

    # elif var_frame == "TF":
        # TODO
    # else:
        # TODO error

# 0 - OK
# 1 - Variable not exist
# 2 - Frame not exist
def is_existing_var(runtime_enviroment, var_frame, var_name):
    if var_frame == "GF":
        global_frame = runtime_enviroment["global_frame"]

        if var_name not in global_frame.keys():
            return False, 1

    elif var_frame == "LF":
        local_frames_stack = runtime_enviroment["local_frames_stack"]

        if len(local_frames_stack) == 0:
            return False, 2

        local_frame = local_frames_stack[-1]

        if not var_name in local_frame.keys():
            return False, 1

    elif var_frame == "TF":
        # TODO
        return

    return True, 0


# def get_var_val():


# def get_not_var_val():


def get_arg_val(arg):
    return 12
