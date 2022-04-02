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
from custom_exception import InvalidOperandValue, InvalidXMLFormat


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

    def one_arg(self, inst_arg):
        root_args = self.root[self.opcode]

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

    def two_args(self, inst_args):
        root_args = self.root[self.opcode]

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

    def three_args(self, inst_args):
        root_args = self.root[self.opcode]

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

    def parse_instruction(self):
        if self.opcode in inst_set:
            inst_args = inst_set[self.opcode]
            args_cnt = len(inst_args)
        else:
            raise InvalidXMLFormat

        try:
            if args_cnt == 0:
                self.no_arg()
            elif args_cnt == 1:
                self.one_arg(inst_args)
            elif args_cnt == 2:
                self.two_args(inst_args)
            elif args_cnt == 3:
                self.three_args(inst_args)
            else:
                raise InvalidXMLFormat

        except InvalidOperandValue:
            raise
        except InvalidXMLFormat:
            raise

    def execute(self):
        # TODO
        return
