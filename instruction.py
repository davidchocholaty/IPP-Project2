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


class Instruction:
    def __init__(self, root, opcode):
        self.root = root
        self.opcode = opcode

    def no_arg(self):
        root_args = self.root[self.opcode]

        if len(root_args) >= 0:
            #TODO error

    def one_arg(self, inst_arg):
        root_args = self.root[self.opcode]

        if len(root_args) == 1:
            if root_args.find("arg1"):

        else:
            #TODO error

    def two_args(self, inst_args):


    def three_args(self, inst_args):

    def execute(self):
        if self.opcode in inst_set:
            inst_args = inst_set[self.opcode]
            args_cnt = len(inst_args)
        else:
            # TODO error

        if args_cnt == 0:
            no_arg()
        elif args_cnt == 1:
            arg1 = one_arg(inst_args)
        elif args_cnt == 2:
            arg1, arg2 = two_args(inst_args)
        elif args_cnt == 3:
            arg1, arg2, arg3 = three_args(inst_args)
        else:
            #TODO error