##########################################################################
#                                                                        #
# Soubor: interpret.py                                                   #
# Vytvoren: 2022-04-03                                                   #
# Posledni zmena: 2022-04-03                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Hlavni skript interpreteru pro jazyk IPPcode22                  #
#                                                                        #
##########################################################################

from instruction_set import inst_set
from operand import Operand

def valid_name(name):


def valid_var(var):
    if var.get_type() != "var":
        return False
    elif var.get_var_frame() not in ["GF", "TF", "LF"]:
        return False

    return valid_name(var.get_var_name())


def valid_symb(symb):

def valid_label(label):

def valid_type(type):


def valid_args(opcode, *argv):
    expected_args = inst_set[opcode]

    for (exp_arg_type, arg) in zip(expected_args, argv):
        if exp_arg_type == "var":
            if not valid_var(arg):
                return False
        elif exp_arg_type == "symb":
            if not valid_symb(arg):
                return False
        elif exp_arg_type == "label":
            if not valid_label(arg):
                return False
        elif exp_arg_type == "type":
            if not valid_type(arg):
                return False

    return True
