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

import sys

from instruction_set import inst_set
from operand import Operand, create_operand
from custom_exception import InvalidOperandValue, InvalidXMLFormat, FrameNotExist, VariableNotExist, \
    InvalidOperandType, ZeroDivision, UnexpectedInstructionError, ValueNotInRange, InvalidUnicodeValue, \
    InvalidStringIndex
from instruction_util import save_var_to_frame, get_arg_val, check_is_existing_variable, int_str_2_int


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

    def get_arg_val_two_operands(self, runtime_environment):
        try:
            arg2_value = get_arg_val(runtime_environment, self.arg2)
        except InvalidXMLFormat:
            raise
        except VariableNotExist:
            raise
        except FrameNotExist:
            raise

        return arg2_value

    def get_args_vals_three_operands(self, runtime_environment):
        try:
            arg2_value = get_arg_val(runtime_environment, self.arg2)
            arg3_value = get_arg_val(runtime_environment, self.arg3)
        except InvalidXMLFormat:
            raise
        except VariableNotExist:
            raise
        except FrameNotExist:
            raise

        return arg2_value, arg3_value

    def arithmetic(self, runtime_environment):
        var1_frame = self.arg1.get_var_frame()
        var1_name = self.arg1.get_var_name()

        try:
            check_is_existing_variable(runtime_environment, var1_frame, var1_name)
            arg2_value, arg3_value = self.get_args_vals_three_operands(runtime_environment)
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

        save_var_to_frame(runtime_environment, var1_frame, var1_name, res)

    def relational(self, runtime_environment):
        var1_frame = self.arg1.get_var_frame()
        var1_name = self.arg1.get_var_name()

        try:
            check_is_existing_variable(runtime_environment, var1_frame, var1_name)
            arg2_value, arg3_value = self.get_args_vals_three_operands(runtime_environment)
        except InvalidXMLFormat:
            raise
        except VariableNotExist:
            raise
        except FrameNotExist:
            raise

        if self.opcode == "LT":
            if type(arg2_value) != type(arg3_value):
                raise InvalidOperandType

            if isinstance(arg2_value, int) or \
                    isinstance(arg2_value, str) or \
                    isinstance(arg2_value, bool):
                res = arg2_value < arg3_value
            else:
                raise InvalidOperandType

        elif self.opcode == "GT":
            if type(arg2_value) != type(arg3_value):
                raise InvalidOperandType

            if isinstance(arg2_value, int) or \
                    isinstance(arg2_value, str) or \
                    isinstance(arg2_value, bool):
                res = arg2_value > arg3_value
            else:
                raise InvalidOperandType

        elif self.opcode == "EQ":
            if arg2_value == "nil":
                arg2_value = None
            if arg3_value == "nil":
                arg3_value = None

            if arg2_value is not None and \
                    arg3_value is not None and \
                    type(arg2_value) != type(arg3_value):
                raise InvalidOperandType

            if isinstance(arg2_value, int) or \
                    isinstance(arg2_value, str) or \
                    isinstance(arg2_value, bool) or \
                    arg2_value is None:  # or \
                # arg3_value is None:
                res = arg2_value == arg3_value
            else:
                raise InvalidOperandType

        else:
            raise UnexpectedInstructionError

        save_var_to_frame(runtime_environment, var1_frame, var1_name, res)

    def boolean(self, runtime_environment):
        var1_frame = self.arg1.get_var_frame()
        var1_name = self.arg1.get_var_name()

        if self.opcode == "NOT":
            try:
                check_is_existing_variable(runtime_environment, var1_frame, var1_name)
                arg2_value = self.get_arg_val_two_operands(runtime_environment)
            except InvalidXMLFormat:
                raise
            except VariableNotExist:
                raise
            except FrameNotExist:
                raise

            if isinstance(arg2_value, bool):
                res = not arg2_value
            else:
                raise InvalidOperandType
        else:
            try:
                check_is_existing_variable(runtime_environment, var1_frame, var1_name)
                arg2_value, arg3_value = self.get_args_vals_three_operands(runtime_environment)
            except InvalidXMLFormat:
                raise
            except VariableNotExist:
                raise
            except FrameNotExist:
                raise

            if isinstance(arg2_value, bool) and isinstance(arg3_value, bool):
                if self.opcode == "AND":
                    res = arg2_value and arg3_value
                elif self.opcode == "OR":
                    res = arg2_value or arg3_value
                else:
                    raise UnexpectedInstructionError
            else:
                raise InvalidOperandType

        save_var_to_frame(runtime_environment, var1_frame, var1_name, res)

    def jump_instruction(self, runtime_environment):
        # JUMP nebo JUMPIFEQ nebo JUMPIFNEQ

        arg1_value = get_arg_val(runtime_environment, self.arg1)
        run_env_labels = runtime_environment["labels"]
        label_position = run_env_labels[arg1_value]

        if self.opcode == "JUMP":
            try:
                # Skok na instrukci nasledujici za instrukci LABEL
                runtime_environment["position"] = int_str_2_int(label_position + 1)
            except ValueError:
                raise InvalidOperandValue

        elif self.opcode == "JUMPIFEQ" or self.opcode == "JUMPIFNEQ":
            try:
                arg2_value, arg3_value = self.get_args_vals_three_operands(runtime_environment)
            except InvalidXMLFormat:
                raise
            except VariableNotExist:
                raise
            except FrameNotExist:
                raise

            if arg2_value == "nil":
                arg2_value = None
            if arg3_value == "nil":
                arg3_value = None

            if arg2_value is not None and \
                    arg3_value is not None and \
                    type(arg2_value) != type(arg3_value):
                raise InvalidOperandType

            if isinstance(arg2_value, int) or \
                    isinstance(arg2_value, str) or \
                    isinstance(arg2_value, bool) or \
                    arg2_value is None:

                if self.opcode == "JUMPIFEQ":
                    if arg2_value == arg3_value:
                        try:
                            # Skok na instrukci nasledujici za instrukci LABEL
                            runtime_environment["position"] = int_str_2_int(label_position + 1)
                        except ValueError:
                            raise InvalidOperandValue
                else:
                    # JUMPIFNEQ
                    if arg2_value != arg3_value:
                        try:
                            # Skok na instrukci nasledujici za instrukci LABEL
                            runtime_environment["position"] = int_str_2_int(label_position + 1)
                        except ValueError:
                            raise InvalidOperandValue

            else:
                raise InvalidOperandType

        else:
            raise UnexpectedInstructionError

    def convert_instruction(self, runtime_environment):
        # INT2CHAR nebo STRI2INT
        var1_frame = self.arg1.get_var_frame()
        var1_name = self.arg1.get_var_name()

        if self.opcode == "INT2CHAR":
            try:
                check_is_existing_variable(runtime_environment, var1_frame, var1_name)
                arg2_value = self.get_arg_val_two_operands(runtime_environment)
            except InvalidXMLFormat:
                raise
            except VariableNotExist:
                raise
            except FrameNotExist:
                raise

            if not isinstance(arg2_value, int):
                raise InvalidOperandType

            try:
                res_value = chr(arg2_value)
            except ValueError:
                raise InvalidUnicodeValue
        elif self.opcode == "STRI2INT":
            try:
                check_is_existing_variable(runtime_environment, var1_frame, var1_name)
                arg2_value, arg3_value = self.get_args_vals_three_operands(runtime_environment)
            except InvalidXMLFormat:
                raise
            except VariableNotExist:
                raise
            except FrameNotExist:
                raise

            if isinstance(arg2_value, str) and isinstance(arg3_value, int):
                if arg3_value < 0 or arg3_value >= len(arg2_value):
                    raise InvalidStringIndex

                try:
                    res_value = ord(arg2_value[arg3_value])
                except TypeError:
                    raise InvalidUnicodeValue
            else:
                raise InvalidOperandType
        else:
            raise UnexpectedInstructionError

        save_var_to_frame(runtime_environment, var1_frame, var1_name, res_value)

    def execute(self, runtime_environment, input_handler):
        try:
            if self.opcode == "MOVE":
                if self.arg2.get_type() == "label":
                    raise InvalidXMLFormat

                var1_frame = self.arg1.get_var_frame()
                var1_name = self.arg1.get_var_name()

                arg2_value = get_arg_val(runtime_environment, self.arg2)

                save_var_to_frame(runtime_environment, var1_frame, var1_name, arg2_value)

            # elif self.opcode == "CREATEFRAME":
            # elif self.opcode == "PUSHFRAME":
            # elif self.opcode == "POPFRAME":
            elif self.opcode == "DEFVAR":
                var_frame = self.arg1.get_var_frame()
                var_name = self.arg1.get_var_name()
                save_var_to_frame(runtime_environment, var_frame, var_name, None)

            # elif self.opcode == "CALL":
            # elif self.opcode == "RETURN":
            # elif self.opcode == "PUSHS":
            # elif self.opcode == "POPS":
            elif self.opcode == "ADD":
                self.arithmetic(runtime_environment)

            elif self.opcode == "SUB":
                self.arithmetic(runtime_environment)

            elif self.opcode == "MUL":
                self.arithmetic(runtime_environment)

            elif self.opcode == "IDIV":
                self.arithmetic(runtime_environment)

            elif self.opcode == "LT":
                self.relational(runtime_environment)

            elif self.opcode == "GT":
                self.relational(runtime_environment)

            elif self.opcode == "EQ":
                self.relational(runtime_environment)

            elif self.opcode == "AND":
                self.boolean(runtime_environment)

            elif self.opcode == "OR":
                self.boolean(runtime_environment)

            elif self.opcode == "NOT":
                self.boolean(runtime_environment)

            elif self.opcode == "INT2CHAR":
                self.convert_instruction(runtime_environment)

            elif self.opcode == "STRI2INT":
                self.convert_instruction(runtime_environment)

            elif self.opcode == "READ":
                # TODO u promennych kde je to resene ulozeni aktualniho datoveho typu asi
                # datove typy jsou urceny dynamicky obsazenou hodnotou a implicitni konverze,
                # pokud neni receno jinak jsou zakazany viz zadani
                input_line = input_handler.readline()

                if input_line[-1] == '\n':
                    input_line = input_line[:-1]

                var1_frame = self.arg1.get_var_frame()
                var1_name = self.arg1.get_var_name()

                try:
                    check_is_existing_variable(runtime_environment, var1_frame, var1_name)
                    arg2_value = self.get_arg_val_two_operands(runtime_environment)
                except InvalidXMLFormat:
                    raise
                except VariableNotExist:
                    raise
                except FrameNotExist:
                    raise

                if arg2_value == "int":
                    try:
                        input_line = int_str_2_int(input_line)
                    except ValueError:
                        # TODO zkontrolovat ulozeni nil@nil viz zadani
                        input_line = None
                elif arg2_value == "string":
                    if not isinstance(input_line, str):
                        # input_line = ""
                        input_line = None
                elif arg2_value == "bool":
                    input_line = input_line.lower()

                    if input_line == "true":
                        input_line = True
                    else:
                        input_line = False
                else:
                    raise InvalidXMLFormat

                save_var_to_frame(runtime_environment, var1_frame, var1_name, input_line)

            elif self.opcode == "WRITE":
                val = get_arg_val(runtime_environment, self.arg1)

                # TODO zkontrolovat vypis nil@nil jako prazdny retezec
                # atd viz zadani

                if val is None:
                    val = ""
                elif val is True:
                    val = "true"
                elif val is False:
                    val = "false"
                else:
                    val = str(val)

                print(val, end='', flush=True)

            # elif self.opcode == "CONCAT":
            # elif self.opcode == "STRLEN":
            # elif self.opcode == "GETCHAR":
            # elif self.opcode == "SETCHAR":
            elif self.opcode == "TYPE":
                var1_frame = self.arg1.get_var_frame()
                var1_name = self.arg1.get_var_name()

                try:
                    check_is_existing_variable(runtime_environment, var1_frame, var1_name)
                    arg2_value = self.get_arg_val_two_operands(runtime_environment)
                except InvalidXMLFormat:
                    raise
                except VariableNotExist:
                    raise
                except FrameNotExist:
                    raise

                if isinstance(arg2_value, int):
                    save_var_to_frame(runtime_environment,
                                      self.arg1.get_var_frame(),
                                      self.arg1.get_var_name(),
                                      "int")

                elif isinstance(arg2_value, bool):
                    save_var_to_frame(runtime_environment,
                                      self.arg1.get_var_frame(),
                                      self.arg1.get_var_name(),
                                      "bool")

                elif isinstance(arg2_value, str):
                    var_type = None

                    if arg2_value == "nil":
                        var_type = "nil"
                    else:
                        var_type = "string"

                    save_var_to_frame(runtime_environment,
                                      self.arg1.get_var_frame(),
                                      self.arg1.get_var_name(),
                                      var_type)

                elif arg2_value is None:
                    save_var_to_frame(runtime_environment,
                                      self.arg1.get_var_frame(),
                                      self.arg1.get_var_name(),
                                      "nil")

                else:
                    raise InvalidOperandType

            elif self.opcode == "JUMP":
                self.jump_instruction(runtime_environment)

            elif self.opcode == "JUMPIFEQ":
                self.jump_instruction(runtime_environment)

            elif self.opcode == "JUMPIFNEQ":
                self.jump_instruction(runtime_environment)

            elif self.opcode == "EXIT":
                try:
                    arg1_value = get_arg_val(runtime_environment, self.arg1)
                except InvalidXMLFormat:
                    raise
                except VariableNotExist:
                    raise
                except FrameNotExist:
                    raise

                if not isinstance(arg1_value, int):
                    raise InvalidOperandType

                if arg1_value < 0 or arg1_value > 49:
                    raise ValueNotInRange
                else:
                    sys.exit(arg1_value)

            elif self.opcode == "DPRINT":
                try:
                    arg1_value = get_arg_val(runtime_environment, self.arg1)
                except InvalidXMLFormat:
                    raise
                except VariableNotExist:
                    raise
                except FrameNotExist:
                    raise

                sys.stderr.write(arg1_value)

            elif self.opcode == "BREAK":
                sys.stderr.write("Global frame content:")
                sys.stderr.write("")

                global_frame_content = runtime_environment["global_frame"]

                for key, value in global_frame_content.items():
                    sys.stderr.write(key + " : " + value)

                stack_size = len(runtime_environment["local_frames_stack"])

                sys.stderr.write("")
                sys.stderr.write("Local frames stack actual size:" + str(stack_size))

        except InvalidXMLFormat:
            raise
        except VariableNotExist:
            raise
        except FrameNotExist:
            raise
        except InvalidOperandType:
            raise
        except InvalidOperandValue:
            raise
        except ZeroDivision:
            raise
        except UnexpectedInstructionError:
            raise

        return
