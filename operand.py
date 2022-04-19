##########################################################################
#                                                                        #
# Soubor: operand.py                                                     #
# Vytvoren: 2022-04-02                                                   #
# Posledni zmena: 2022-04-19                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Skript obsahujici tridu reprezentujici operand instrukce        #
#                                                                        #
##########################################################################

from re import search
from xml.etree.ElementTree import ParseError
from custom_exception import InvalidOperandValue, InvalidXMLFormat


# Tovarni funkce pro vytroreni noveho operandu.
def create_operand(arg):
    if arg is not None:
        operand = Operand(arg)
    else:
        raise InvalidXMLFormat

    try:
        operand.parse_operand()
    except InvalidOperandValue:
        raise
    except InvalidXMLFormat:
        raise
    except MissingValueError:
        raise

    return operand


# Trida reprezentujici operand instrukce.
class Operand:
    def __init__(self, arg):
        self.arg = arg
        self.op_val = None
        self.type = None
        self.var_frame = None
        self.var_name = None

    # Nastaveni hodnoty operandu.
    def set_op_val(self):
        try:
            self.op_val = self.arg.text
        except ParseError:
            raise InvalidOperandValue

    # Nastaveni ramce promenne.
    def set_var_frame(self):
        self.var_frame = search(r'.*(?=@)', self.op_val).group(0)

    # Nastaveni jmena promenne.
    def set_var_name(self):
        self.var_name = search(r'(?<=@).*', self.op_val).group(0)

    # Ziskani typu operandu.
    def get_type(self):
        return self.type

    # Ziskani ramce promenne.
    def get_var_frame(self):
        return self.var_frame

    # Ziskani jmena promenne.
    def get_var_name(self):
        return self.var_name

    # Ziskani hodnoty operandu.
    def get_val(self):
        return self.op_val

    # Funkce pro zpracovani operandu a nastaveni atributu.
    def parse_operand(self):
        try:
            self.type = self.arg.attrib['type']
        except ParseError:
            raise MissingValueError

        try:
            if self.type == "var":
                self.set_op_val()

                if "@" in self.op_val:
                    self.set_var_frame()
                    self.set_var_name()

            elif self.type == "string":
                self.set_op_val()

                if self.op_val is None:
                    self.op_val = ""
                elif "#" in self.op_val or search(r"\s", self.op_val):
                    raise InvalidXMLFormat

            elif self.type == "type":
                self.set_op_val()

            elif self.type == "bool":
                self.set_op_val()

            elif self.type == "nil":
                self.set_op_val()

            elif self.type == "int":
                self.set_op_val()

            elif self.type == "label":
                self.set_op_val()

            else:
                raise InvalidXMLFormat

        except InvalidOperandValue:
            raise
        except InvalidXMLFormat:
            raise
