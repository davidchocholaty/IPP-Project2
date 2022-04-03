##########################################################################
#                                                                        #
# Soubor: interpret.py                                                   #
# Vytvoren: 2022-03-30                                                   #
# Posledni zmena: 2022-03-30                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Hlavni skript interpreteru pro jazyk IPPcode22                  #
#                                                                        #
##########################################################################

from instruction_set import inst_set
from operand import Operand, create_operand
from custom_exception import InvalidOperandValue, InvalidXMLFormat, FrameNotExist, VariableNotExist, \
    InvalidOperandType, ZeroDivision, UnexpectedInstructionError
from instruction_util import save_var_to_frame, get_arg_val, check_is_existing_variable


class Instruction:
    def __init__(self, root, opcode):
        self.root = root
        self.opcode = opcode
        self.arg1 = None
        self.arg2 = None
        self.arg3 = None

    def no_arg(self):
        root_args = self.root[self.opcode]

        if len(root_args) >= 0:
            raise InvalidXMLFormat

    def one_arg(self, inst_order):
        root_args = self.root[inst_order]

        if len(root_args) == 1:
            fst_arg = root_args.find("arg1")

            try:
                self.arg1 = create_operand(fst_arg)
            except InvalidXMLFormat:
                raise
            except InvalidOperandValue:
                raise

        else:
            raise InvalidXMLFormat

    def two_args(self, inst_order):
        root_args = self.root[inst_order]

        if len(root_args) == 2:
            fst_arg = root_args.find("arg1")
            sec_arg = root_args.find("arg2")

            try:
                self.arg1 = create_operand(fst_arg)
                self.arg2 = create_operand(sec_arg)
            except InvalidXMLFormat:
                raise
            except InvalidOperandValue:
                raise

        else:
            raise InvalidXMLFormat

    def three_args(self, inst_order):
        root_args = self.root[inst_order]

        if len(root_args) == 3:
            fst_arg = root_args.find("arg1")
            sec_arg = root_args.find("arg2")
            thd_arg = root_args.find("arg3")

            try:
                self.arg1 = create_operand(fst_arg)
                self.arg2 = create_operand(sec_arg)
                self.arg3 = create_operand(thd_arg)
            except InvalidXMLFormat:
                raise
            except InvalidOperandValue:
                raise

        else:
            raise InvalidXMLFormat

    def parse_instruction(self, inst_order):
        if self.opcode in inst_set:
            inst_args = inst_set[self.opcode]
            args_cnt = len(inst_args)
        else:
            raise InvalidXMLFormat

        try:
            if args_cnt == 0:
                self.no_arg()
            elif args_cnt == 1:
                self.one_arg(inst_order)
            elif args_cnt == 2:
                self.two_args(inst_order)
            elif args_cnt == 3:
                self.three_args(inst_order)
            else:
                raise InvalidXMLFormat

        except InvalidOperandValue:
            raise
        except InvalidXMLFormat:
            raise

    def arithmetic(self, runtime_enviroment):
        var1_frame = self.arg1.get_var_frame()
        var1_name = self.arg1.get_var_name()

        try:
            check_is_existing_variable(runtime_enviroment, var1_frame, var1_name)
            arg2_value = get_arg_val(runtime_enviroment, self.arg2)
            arg3_value = get_arg_val(runtime_enviroment, self.arg3)
        except InvalidXMLFormat:
            raise
        except VariableNotExist:
            raise
        except FrameNotExist:
            raise

        if not isinstance(arg2_value, int) or not isinstance(arg3_value, int):
            raise InvalidOperandType

        if self.opcode == "ADD":
            res = arg2_value + arg3_value
        elif self.opcode == "SUB":
            res = arg2_value - arg3_value
        elif self.opcode == "MUL":
            res = arg2_value * arg3_value
        elif self.opcode == "IDIV":
            if arg3_value == 0:
                raise ZeroDivision

            res = int(arg2_value / arg3_value)
        else:
            raise UnexpectedInstructionError

        save_var_to_frame(runtime_enviroment, var1_frame, var1_name, res)

    def execute(self, runtime_enviroment):
        try:
            if self.opcode == "MOVE":
                if self.arg2.get_type() == "label":
                    raise InvalidXMLFormat

                var1_frame = self.arg1.get_var_frame()
                var1_name = self.arg1.get_var_name()

                arg2_value = get_arg_val(runtime_enviroment, self.arg2)

                save_var_to_frame(runtime_enviroment, var1_frame, var1_name, arg2_value)

            #elif self.opcode == "CREATEFRAME":
            #elif self.opcode == "PUSHFRAME":
            #elif self.opcode == "POPFRAME":
            elif self.opcode == "DEFVAR":
                var_frame = self.arg1.get_var_frame()
                var_name = self.arg1.get_var_name()
                save_var_to_frame(runtime_enviroment, var_frame, var_name, None)

            #elif self.opcode == "CALL":
            #elif self.opcode == "RETURN":
            #elif self.opcode == "PUSHS":
            #elif self.opcode == "POPS":
            elif self.opcode == "ADD":
                self.arithmetic(runtime_enviroment)

            elif self.opcode == "SUB":
                self.arithmetic(runtime_enviroment)

            elif self.opcode == "MUL":
                self.arithmetic(runtime_enviroment)

            elif self.opcode == "IDIV":
                self.arithmetic(runtime_enviroment)

            # elif self.opcode == "LT":
            # elif self.opcode == "GT":
            # elif self.opcode == "EQ":
            # elif self.opcode == "AND":
            # elif self.opcode == "OR":
            # elif self.opcode == "NOT":
            # elif self.opcode == "INT2CHAR":
            # elif self.opcode == "STRI2INT":
            # elif self.opcode == "READ":
            elif self.opcode == "WRITE":
                val = get_arg_val(runtime_enviroment, self.arg1)

                #if self.arg1.get_type() == "bool":

                val = str(val)
                print(val, end='', flush=True)

            # elif self.opcode == "CONCAT":
            # elif self.opcode == "STRLEN":
            # elif self.opcode == "GETCHAR":
            # elif self.opcode == "SETCHAR":
            # elif self.opcode == "TYPE":
            # elif self.opcode == "LABEL":
            # elif self.opcode == "JUMP":
            # elif self.opcode == "JUMPIFEQ":
            # elif self.opcode == "JUMPIFNEQ":
            # elif self.opcode == "EXIT":
            # elif self.opcode == "DPRINT":
            # elif self.opcode == "BREAK":
        except InvalidXMLFormat:
            raise
        except VariableNotExist:
            raise
        except FrameNotExist:
            raise
        except InvalidOperandType:
            raise
        except ZeroDivision:
            raise
        except UnexpectedInstructionError:
            raise

        return
