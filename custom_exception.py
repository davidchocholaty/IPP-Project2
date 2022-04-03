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

class MultipleOccurenceError(Exception):
    def __init__(self, msg="Multiple label definition occurence"):
        self.msg = msg
        super().__init__(self.msg)


class InvalidOperandValue(Exception):
    def __init__(self, msg="Invalid operand value"):
        self.msg = msg
        super().__init__(self.msg)


class InvalidXMLFormat(Exception):
    def __init__(self, msg="Invalid XML format"):
        self.msg = msg
        super().__init__(self.msg)


class InvalidOperandType(Exception):
    def __init__(self, msg="Invalid operand type"):
        self.msg = msg
        super().__init__(self.msg)


class FrameNotExist(Exception):
    def __init__(self, msg="Frame not exist"):
        self.msg = msg
        super().__init__(self.msg)


class VariableNotExist(Exception):
    def __init__(self, msg="Variable not exist"):
        self.msg = msg
        super().__init__(self.msg)
