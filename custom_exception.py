##########################################################################
#                                                                        #
# Soubor: custom_exception.py                                            #
# Vytvoren: 2022-03-30                                                   #
# Posledni zmena: 2022-04-19                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Skript s vlastnimi vyjimkami pouzivanymi v interpreteru         #
#                                                                        #
##########################################################################

# Vicenasobny vyskyt.
class MultipleOccurenceError(Exception):
    def __init__(self, msg="Multiple label definition occurence"):
        self.msg = msg
        super().__init__(self.msg)


# Nespravna hodnota operandu.
class InvalidOperandValue(Exception):
    def __init__(self, msg="Invalid operand value"):
        self.msg = msg
        super().__init__(self.msg)


# Nespravny format XML souboru.
class InvalidXMLFormat(Exception):
    def __init__(self, msg="Invalid XML format"):
        self.msg = msg
        super().__init__(self.msg)


# Nespravny typ operandu.
class InvalidOperandType(Exception):
    def __init__(self, msg="Invalid operand type"):
        self.msg = msg
        super().__init__(self.msg)


# Nespravna unicode hodnota.
class InvalidUnicodeValue(Exception):
    def __init__(self, msg="Invalid unicode value"):
        self.msg = msg
        super().__init__(self.msg)


# Nespravny index v retezci.
class InvalidStringIndex(Exception):
    def __init__(self, msg="Invalid string index"):
        self.msg = msg
        super().__init__(self.msg)


# Zakazana operace s retezci.
class InvalidStringOperation(Exception):
    def __init__(self, msg="Invalid string index"):
        self.msg = msg
        super().__init__(self.msg)


# Hodnota neni v rozsahu.
class ValueNotInRange(Exception):
    def __init__(self, msg="Value is not in range"):
        self.msg = msg
        super().__init__(self.msg)


# Neexistujici ramec.
class FrameNotExist(Exception):
    def __init__(self, msg="Frame not exist"):
        self.msg = msg
        super().__init__(self.msg)


# Neexistujici promenna.
class VariableNotExist(Exception):
    def __init__(self, msg="Variable not exist"):
        self.msg = msg
        super().__init__(self.msg)


# Chybejici hodnota.
class MissingValueError(Exception):
    def __init__(self, msg="Missing value error"):
        self.msg = msg
        super().__init__(self.msg)


# Deleni nulou.
class ZeroDivision(Exception):
    def __init__(self, msg="Zero division"):
        self.msg = msg
        super().__init__(self.msg)


# Neocekavana instrukce.
class UnexpectedInstructionError(Exception):
    def __init__(self, msg="Unexpected instruction"):
        self.msg = msg
        super().__init__(self.msg)
