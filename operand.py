##########################################################################
#                                                                        #
# Soubor: interpret.py                                                   #
# Vytvoren: 2022-04-02                                                   #
# Posledni zmena: 2022-04-02                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Hlavni skript interpreteru pro jazyk IPPcode22                  #
#                                                                        #
##########################################################################

from re import search
from xml.etree.ElementTree import ParseError
from custom_exception import InvalidOperandValue, InvalidXMLFormat


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

    return operand


class Operand:
    def __init__(self, arg):
        self.arg = arg
        self.op_val = None
        self.type = None
        self.var_frame = None
        self.var_name = None

    def set_op_val(self):
        try:
            self.op_val = self.arg.text
        except ParseError:
            raise InvalidOperandValue

    def set_var_frame(self):
        self.var_frame = search(r'.*(?=@)', self.op_val).group(0)

    def set_var_name(self):
        self.var_name = search(r'(?<=@).*', self.op_val).group(0)

    def get_type(self):
        return self.type

    def get_var_frame(self):
        return self.var_frame

    def get_var_name(self):
        return self.var_name

    def parse_operand(self):
        try:
            self.type = self.arg.attrib['type']
        except ParseError:
            return False

        try:
            if self.type == "var":
                self.set_op_val()

                if "@" in self.op_val:
                    self.set_var_frame()
                    self.set_var_name()

            elif self.type == "string":
                self.set_op_val()
                # TODO jestli je potreba
                #if self.op_val is not None and "#" in self.op_val:
                    # TODO error
            elif self.type == "type":
                self.set_op_val()
            elif self.type == "bool":
                self.set_op_val()
            elif self.type == "nil":
                self.set_op_val()
            elif self.type == "int":
                self.set_op_val()
            elif self.type == "string":
                self.set_op_val()
            elif self.type == "label":
                self.set_op_val()
            else:
                raise InvalidXMLFormat

        except InvalidOperandValue:
            raise
        except InvalidXMLFormat:
            raise
