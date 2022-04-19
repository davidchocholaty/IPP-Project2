##########################################################################
#                                                                        #
# Soubor: interpret.py                                                   #
# Vytvoren: 2022-03-30                                                   #
# Posledni zmena: 2022-04-19                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Skript se tridou reprezentujici instrukci                       #
#                                                                        #
##########################################################################

import sys

from instruction_set import inst_set
from operand import Operand, create_operand
from custom_exception import InvalidOperandValue, InvalidXMLFormat, FrameNotExist, VariableNotExist, \
    InvalidOperandType, ZeroDivision, UnexpectedInstructionError, ValueNotInRange, InvalidUnicodeValue, \
    InvalidStringIndex, MissingValueError, InvalidStringOperation
from instruction_util import save_var_to_frame, get_arg_val, check_is_existing_variable, int_str_2_int, \
    process_decimal_escape

# Trida reprezentujici instrukci.
class Instruction:
    def __init__(self, root, opcode):
        self.root = root
        self.opcode = opcode
        self.arg1 = None
        self.arg2 = None
        self.arg3 = None

    # Instrukce bez argumentu.
    def no_arg(self, inst_order):
        root_args = self.root[inst_order]

        if len(root_args) > 0:
            raise InvalidXMLFormat

    # Instrukce s jednim argumentem.
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
            except MissingValueError:
                raise

        else:
            raise InvalidXMLFormat

    # Instrukce se dvema argumenty.
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
            except MissingValueError:
                raise

        else:
            raise InvalidXMLFormat

    # Instrukce se tremi argumenty.
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
            except MissingValueError:
                raise

        else:
            raise InvalidXMLFormat

    # Zpracovani argumentu instrukce.
    def parse_instruction(self, inst_order):
        if self.opcode in inst_set:
            inst_args = inst_set[self.opcode]
            args_cnt = len(inst_args)
        else:
            raise InvalidXMLFormat

        try:
            if args_cnt == 0:
                self.no_arg(inst_order)
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
        except MissingValueError:
            raise

    # Ziskani hodnoty argumentu pro instrukci s jednim argumentem.
    def get_arg_val_one_operand(self, runtime_environment):
        try:
            arg1_value = get_arg_val(runtime_environment, self.arg1)
        except InvalidXMLFormat:
            raise
        except VariableNotExist:
            raise
        except FrameNotExist:
            raise

        return arg1_value

    # Ziskani hodnoty argumentu pro instrukci se dvema argumenty.
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

    # Ziskani hodnoty argumentu pro instrukci se tremi argumenty.
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

    # Zpracovani aritmetickych instrukci.
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

        if isinstance(arg2_value, bool) or isinstance(arg3_value, bool):
            raise InvalidOperandType

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

        try:
            save_var_to_frame(runtime_environment, var1_frame, var1_name, res)
        except FrameNotExist:
            raise
        except InvalidXMLFormat:
            raise

    # Zpracovani relacnich instrukci.
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
        try:
            save_var_to_frame(runtime_environment, var1_frame, var1_name, res)
        except FrameNotExist:
            raise
        except InvalidXMLFormat:
            raise

    # Zpracovani booleovskych instrukci.
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

        try:
            save_var_to_frame(runtime_environment, var1_frame, var1_name, res)
        except FrameNotExist:
            raise
        except InvalidXMLFormat:
            raise

    # Zpracovani skokovych instrukci.
    def jump_instruction(self, runtime_environment):
        # JUMP nebo JUMPIFEQ nebo JUMPIFNEQ
        try:
            arg1_value = get_arg_val(runtime_environment, self.arg1)
        except InvalidXMLFormat:
            raise
        except VariableNotExist:
            raise
        except FrameNotExist:
            raise

        run_env_labels = runtime_environment["labels"]

        try:
            label_position = run_env_labels[arg1_value]
        except KeyError:
            raise InvalidOperandValue

        if self.opcode == "JUMP":
            try:
                # Skok na LABEL
                runtime_environment["position"] = int_str_2_int(label_position)
            except ValueError:
                raise InvalidOperandValue

        elif self.opcode == "JUMPIFEQ" or self.opcode == "JUMPIFNEQ":
            arg2_value, arg3_value = self.get_args_vals_three_operands(runtime_environment)

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
                            # Skok na LABEL
                            runtime_environment["position"] = int_str_2_int(label_position)
                        except ValueError:
                            raise InvalidOperandValue
                else:
                    # JUMPIFNEQ
                    if arg2_value != arg3_value:
                        try:
                            # Skok na LABEL
                            runtime_environment["position"] = int_str_2_int(label_position)
                        except ValueError:
                            raise InvalidOperandValue

            else:
                raise InvalidOperandType

        else:
            raise UnexpectedInstructionError

    # Zpracovani prevodnich instrukci.
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

        try:
            save_var_to_frame(runtime_environment, var1_frame, var1_name, res_value)
        except FrameNotExist:
            raise
        except InvalidXMLFormat:
            raise

    # Vyhodnoceni a provedeni instrukce.
    def execute(self, runtime_environment, input_handler):    
        try:
            # MOVE ⟨var⟩ ⟨symb⟩
            if self.opcode == "MOVE":
                if self.arg2.get_type() == "label":
                    raise InvalidXMLFormat

                var1_frame = self.arg1.get_var_frame()
                var1_name = self.arg1.get_var_name()                
                arg2_value = get_arg_val(runtime_environment, self.arg2)               

                check_is_existing_variable(runtime_environment, var1_frame, var1_name)

                save_var_to_frame(runtime_environment, var1_frame, var1_name, arg2_value)

            # CREATEFRAME 
            elif self.opcode == "CREATEFRAME":
                runtime_environment["tmp_frame"] = {}

            # PUSHFRAME
            elif self.opcode == "PUSHFRAME":
                tmp_frame = runtime_environment["tmp_frame"]

                if tmp_frame is None:
                    raise FrameNotExist

                runtime_environment["local_frames_stack"].append(tmp_frame)
                runtime_environment["tmp_frame"] = None

            # POPFRAME
            elif self.opcode == "POPFRAME":
                if len(runtime_environment["local_frames_stack"]) == 0:
                    raise FrameNotExist

                runtime_environment["tmp_frame"] = runtime_environment["local_frames_stack"].pop()
            
            # DEFVAR <var>
            elif self.opcode == "DEFVAR":
                var_frame = self.arg1.get_var_frame()
                var_name = self.arg1.get_var_name()
                save_var_to_frame(runtime_environment, var_frame, var_name, None)                

            # CALL <label>
            elif self.opcode == "CALL":
                call_stack = runtime_environment["call_stack"]
                # Ulozi inkrementovanou aktualni pozici
                call_stack.append(runtime_environment["position"] + 1)

                run_env_labels = runtime_environment["labels"]

                arg1_value = get_arg_val(runtime_environment, self.arg1)

                if not isinstance(arg1_value, str):
                    raise InvalidXMLFormat

                try:
                    label_position = run_env_labels[arg1_value]
                except KeyError:
                    raise InvalidOperandValue

                try:
                    runtime_environment["position"] = int_str_2_int(label_position)

                except ValueError:
                    raise InvalidOperandValue

            # RETURN
            elif self.opcode == "RETURN":
                try:
                    runtime_environment["position"] = runtime_environment["call_stack"].pop()

                except ValueError:
                    raise MissingValueError
                except IndexError:
                    raise MissingValueError

            # PUSHS <symb>
            elif self.opcode == "PUSHS":
                if self.arg1.get_type() == "label":
                    raise InvalidXMLFormat

                arg1_value = self.get_arg_val_one_operand(runtime_environment)

                if arg1_value is None:
                    raise MissingValueError

                runtime_environment["data_stack"].append(arg1_value)

            # POPS <var>
            elif self.opcode == "POPS":
                var1_frame = self.arg1.get_var_frame()
                var1_name = self.arg1.get_var_name()

                if var1_frame is None or var1_name is None:
                    raise InvalidOperandValue

                check_is_existing_variable(runtime_environment, var1_frame, var1_name)

                if len(runtime_environment["data_stack"]) == 0:
                    raise MissingValueError

                stack_top = runtime_environment["data_stack"].pop()

                save_var_to_frame(runtime_environment, var1_frame, var1_name, stack_top)

            # ADD <var> <symb1> <symb2>
            elif self.opcode == "ADD":
                self.arithmetic(runtime_environment)

            # SUB <var> <symb1> <symb2>            
            elif self.opcode == "SUB":
                self.arithmetic(runtime_environment)

            # MUL <var> <symb1> <symb2>
            elif self.opcode == "MUL":
                self.arithmetic(runtime_environment)

            # IDIV <var> <symb1> <symb2>
            elif self.opcode == "IDIV":
                self.arithmetic(runtime_environment)

            # LT <var> <symb1> <symb2>
            elif self.opcode == "LT":
                self.relational(runtime_environment)

            # GT <var> <symb1> <symb2>
            elif self.opcode == "GT":
                self.relational(runtime_environment)

            # EQ <var> <symb1> <symb2>
            elif self.opcode == "EQ":
                self.relational(runtime_environment)

            # AND <var> <symb1> <symb2>
            elif self.opcode == "AND":
                self.boolean(runtime_environment)

            # OR <var> <symb1> <symb2>
            elif self.opcode == "OR":
                self.boolean(runtime_environment)

            # NOT <var> <symb1> <symb2>
            elif self.opcode == "NOT":
                self.boolean(runtime_environment)

            # INT2CHAR <var> <symb>
            elif self.opcode == "INT2CHAR":
                self.convert_instruction(runtime_environment)

            # STRI2INT <var> <symb1> <symb2>
            elif self.opcode == "STRI2INT":
                self.convert_instruction(runtime_environment)

            # READ <var> <type>
            elif self.opcode == "READ":
                input_line = input_handler.readline()

                try:
                    if input_line[-1] == '\n':
                        input_line = input_line[:-1]
                except IndexError:
                    input_line = "nil"

                var1_frame = self.arg1.get_var_frame()
                var1_name = self.arg1.get_var_name()

                check_is_existing_variable(runtime_environment, var1_frame, var1_name)
                arg2_value = self.get_arg_val_two_operands(runtime_environment)

                if arg2_value == "int":
                    if input_line == "nil":
                        input_line = None
                    else:                    
                        try:
                            input_line = int_str_2_int(input_line)
                        except ValueError:
                            input_line = None
                elif arg2_value == "string":
                    if not isinstance(input_line, str):
                        input_line = None
                elif arg2_value == "bool":
                    input_line = input_line.lower()

                    if input_line == "nil":
                        input_line = None
                    else:                    
                        if input_line == "true":
                            input_line = True
                        else:
                            input_line = False
                else:
                    raise InvalidXMLFormat

                save_var_to_frame(runtime_environment, var1_frame, var1_name, input_line)

            # WRITE <symb>
            elif self.opcode == "WRITE":
                val = get_arg_val(runtime_environment, self.arg1)

                if self.arg1.get_type() == "var" and val is None:
                    raise MissingValueError
                elif val is None:
                    val = ""                    
                elif val is True:
                    val = "true"
                elif val is False:
                    val = "false"
                elif val == "nil":
                    val = ""
                else:
                    val = str(val)
                    val = process_decimal_escape(val)

                print(val, end='', flush=True)

            # CONCAT <var> <symb1> <symb2>
            elif self.opcode == "CONCAT":
                var1_frame = self.arg1.get_var_frame()
                var1_name = self.arg1.get_var_name()

                check_is_existing_variable(runtime_environment, var1_frame, var1_name)
                arg2_value, arg3_value = self.get_args_vals_three_operands(runtime_environment)

                if not isinstance(arg2_value, str):
                    if self.arg2.get_type() == "var" and arg2_value is None:
                        raise MissingValueError
                    if arg2_value is None and isinstance(arg3_value, str):
                        concatenated = arg3_value
                    else:
                        raise InvalidOperandType

                elif not isinstance(arg3_value, str):
                    if self.arg3.get_type() == "var" and arg3_value is None:
                        raise MissingValueError
                    if arg3_value is None and isinstance(arg2_value, str):
                        concatenated = arg2_value
                    else:
                        raise InvalidOperandType
                else:
                    # Oba operandy jsou retezce.
                    concatenated = arg2_value + arg3_value

                save_var_to_frame(runtime_environment, var1_frame, var1_name, concatenated)

            # STRLEN <var> <symb>
            elif self.opcode == "STRLEN":
                var1_frame = self.arg1.get_var_frame()
                var1_name = self.arg1.get_var_name()

                check_is_existing_variable(runtime_environment, var1_frame, var1_name)
                arg2_value = self.get_arg_val_two_operands(runtime_environment)

                if isinstance(arg2_value, str):
                    arg2_value = process_decimal_escape(arg2_value)
                    length = len(arg2_value)
                elif arg2_value is None:
                    if self.arg2.get_type() != "string":
                        raise MissingValueError
                    else:
                        length = 0
                else:
                    raise InvalidOperandType

                save_var_to_frame(runtime_environment, var1_frame, var1_name, length)

            # GETCHAR <var> <symb1> <symb2>
            elif self.opcode == "GETCHAR":
                var1_frame = self.arg1.get_var_frame()
                var1_name = self.arg1.get_var_name()

                check_is_existing_variable(runtime_environment, var1_frame, var1_name)
                arg2_value, arg3_value = self.get_args_vals_three_operands(runtime_environment)

                if arg2_value is None or arg3_value is None:
                    raise MissingValueError

                if isinstance(arg2_value, str) and isinstance(arg3_value, int):
                    if arg3_value < 0 or arg3_value >= len(arg2_value):
                        raise InvalidStringIndex

                    character = arg2_value[arg3_value]

                else:
                    raise InvalidOperandType

                save_var_to_frame(runtime_environment, var1_frame, var1_name, character)

            # SETCHAR <var> <symb1> <symb2>
            elif self.opcode == "SETCHAR":
                var1_frame = self.arg1.get_var_frame()
                var1_name = self.arg1.get_var_name()

                check_is_existing_variable(runtime_environment, var1_frame, var1_name)
                var1_value = get_arg_val(runtime_environment, self.arg1)
                arg2_value, arg3_value = self.get_args_vals_three_operands(runtime_environment)

                if isinstance(var1_value, str):
                    if isinstance(arg2_value, int):
                        if isinstance(arg3_value, str):
                            if arg2_value < 0 or arg2_value >= len(var1_value):
                                raise InvalidStringIndex

                            try:
                                var1_value = list(var1_value)
                                var1_value[arg2_value] = arg3_value[0]
                                var1_value = "".join(var1_value)
                            except IndexError:
                                raise InvalidStringOperation

                        else:
                            if arg3_value is None or arg3_value == "":
                                raise InvalidStringOperation
                            else:
                                raise InvalidOperandType

                    else:
                        raise InvalidOperandType
                else:
                    raise InvalidOperandType

                save_var_to_frame(runtime_environment, var1_frame, var1_name, var1_value)

            # TYPE <var> <symb>
            elif self.opcode == "TYPE":
                var1_frame = self.arg1.get_var_frame()
                var1_name = self.arg1.get_var_name()

                check_is_existing_variable(runtime_environment, var1_frame, var1_name)
                arg2_value = self.get_arg_val_two_operands(runtime_environment)

                if isinstance(arg2_value, bool):
                    save_var_to_frame(runtime_environment,
                                      self.arg1.get_var_frame(),
                                      self.arg1.get_var_name(),
                                      "bool")

                elif isinstance(arg2_value, int):
                    save_var_to_frame(runtime_environment,
                                      self.arg1.get_var_frame(),
                                      self.arg1.get_var_name(),
                                      "int")                

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
                                      "")

                else:
                    raise InvalidOperandType

            # JUMP <label>
            elif self.opcode == "JUMP":
                self.jump_instruction(runtime_environment)

            # JUMPIFEQ <label> <symb1> <symb2>
            elif self.opcode == "JUMPIFEQ":
                self.jump_instruction(runtime_environment)

            # JUMPIFNEQ <label> <symb1> <symb2>
            elif self.opcode == "JUMPIFNEQ":
                self.jump_instruction(runtime_environment)

            # EXIT <symb>
            elif self.opcode == "EXIT":
                arg1_value = get_arg_val(runtime_environment, self.arg1)

                if arg1_value is None:
                    raise MissingValueError

                if not isinstance(arg1_value, int):
                    raise InvalidOperandType

                if arg1_value < 0 or arg1_value > 49:
                    raise ValueNotInRange
                else:
                    sys.exit(arg1_value)

            # DPRINT <symb>
            elif self.opcode == "DPRINT":
                arg1_value = get_arg_val(runtime_environment, self.arg1)

                sys.stderr.write(arg1_value)

            # BREAK
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
        except InvalidStringOperation:
            raise
        except InvalidStringIndex:
            raise
        except MissingValueError:
            raise

        return
