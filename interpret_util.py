##########################################################################
#                                                                        #
# Soubor: interpret.py                                                   #
# Vytvoren: 2022-03-28                                                   #
# Posledni zmena: 2022-03-30                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Hlavni skript interpreteru pro jazyk IPPcode22                  #
#                                                                        #
##########################################################################

from custom_exception import MultipleOccurenceError, InvalidOperandValue, InvalidXMLFormat, VariableNotExist, \
    FrameNotExist, ZeroDivision, InvalidOperandType, UnexpectedInstructionError
from xml.etree.ElementTree import ParseError
from instruction import Instruction


class Interpret:
    def __init__(self, root):
        self.root = root
        self.input_handler = None
        self.labels = {}
        self.order = {}
        self.runtime_environment = {
            "global_frame": {},
            "local_frames_stack": []
        }

    def is_valid_lang(self):
        lang = self.root.attrib['language']

        return lang.upper() == "IPPCODE22"

    def set_labels(self):
        try:
            for i in range(0, len(self.root)):
                if self.root[i].attrib['opcode'] == "LABEL":
                    for child in self.root[i]:
                        if child.text in self.labels:
                            raise MultipleOccurenceError

                        self.labels.update({child.text: int(self.root[i].attrib['order'])})
        except ParseError:
            raise

    def set_order(self):
        root_order = 0

        for i in self.root:
            attr_order = int(i.attrib['order'])

            if attr_order in self.order.keys():
                raise MultipleOccurenceError

            self.order.update({attr_order: root_order})
            root_order += 1

    def set_input_handler(self, input_handler):
        self.input_handler = input_handler

    def run(self):
        for i in range(1, len(self.root) + 1):
            try:
                inst_order = self.order[i]
                opcode = self.root[inst_order].attrib['opcode'].upper()
                instruction = Instruction(self.root, opcode)
            except KeyError:
                raise
            except ParseError:
                raise

            try:
                instruction.parse_instruction(inst_order)
            except InvalidOperandValue:
                raise
            except InvalidXMLFormat:
                raise

            try:
                instruction.execute(self.runtime_environment, self.input_handler)
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

