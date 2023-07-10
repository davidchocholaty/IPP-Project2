##########################################################################
#                                                                        #
# Soubor: interpret_util.py                                              #
# Vytvoren: 2022-03-28                                                   #
# Posledni zmena: 2022-04-19                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Skript obsahujici tridu reprezentujici interpret                #
#                                                                        #
##########################################################################

from custom_exception import MultipleOccurenceError, InvalidOperandValue, InvalidXMLFormat, VariableNotExist, \
    FrameNotExist, ZeroDivision, InvalidOperandType, UnexpectedInstructionError, ValueNotInRange, InvalidUnicodeValue, \
    InvalidStringIndex, MissingValueError, InvalidStringOperation
from xml.etree.ElementTree import ParseError
from instruction import Instruction


# Trida reprezentujici interpret.
class Interpret:
    def __init__(self, root):
        self.root = root
        self.input_handler = None
        self.order = {}
        self.runtime_environment = {
            "position": 0,
            "labels": {},
            "global_frame": {},
            "local_frames_stack": [],
            "tmp_frame": None,
            "call_stack": [],
            "data_stack": []
        }

    # Test nazvu jazyka definovaneho v xml reprezentaci programu.
    def is_valid_lang(self):
        lang = self.root.attrib['language']

        return lang.upper() == "IPPCODE22"

    # Ulozeni vsech navesti programu.
    def set_labels(self):
        try:
            for i in range(0, len(self.root)):
                if self.root[i].attrib['opcode'] == "LABEL":
                    for child in self.root[i]:
                        if child.text in self.runtime_environment["labels"]:
                            raise MultipleOccurenceError

                        self.runtime_environment["labels"].update(
                            {child.text: int(self.root[i].attrib['order'])})
        except ParseError:
            raise
        except KeyError:
            raise

    # Ulozeni poradi vsech instrukci v xml reprezentaci programu.
    def set_order(self):
        root_order = 0

        try:
            for i in self.root:
                attr_order = int(i.attrib['order'])

                if attr_order in self.order.keys():
                    raise MultipleOccurenceError

                self.order.update({attr_order: root_order})
                root_order += 1

        except MultipleOccurenceError:
            raise
        except KeyError:
            raise
        except ValueError:
            raise
            
        # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
        self.order = dict(sorted(self.order.items(), key=lambda item: item[0]))

    # Nastaveni obsluhy vstupu.
    def set_input_handler(self, input_handler):
        self.input_handler = input_handler

    # Funkce pro spusteni a provadeni operaci interpretru.
    def run(self):
        keys = list(self.order.keys())
        idx = 0                
        length = len(keys)
        
        try:    
            last = max(self.order)
        except ValueError:
            return
        
        while idx < length:
            i = keys[idx]
            
            if i <= 0:
                raise KeyError

            self.runtime_environment["position"] = i

            try:
                inst_order = self.order[i]
                
            except KeyError:                
                raise

            try:          
                opcode = self.root[inst_order].attrib['opcode'].upper()                
                
                if self.root[inst_order].tag != "instruction":
                    raise InvalidXMLFormat
                
                instruction = Instruction(self.root, opcode)
            except KeyError:
                raise
            except ParseError:
                raise
            except InvalidXMLFormat:
                raise

            try:
                instruction.parse_instruction(inst_order)
            except InvalidOperandValue:
                raise
            except InvalidXMLFormat:
                raise
            except MissingValueError:
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
            except InvalidOperandValue:
                raise
            except ZeroDivision:
                raise
            except UnexpectedInstructionError:
                raise
            except ValueNotInRange:
                raise
            except InvalidUnicodeValue:
                raise
            except InvalidStringIndex:
                raise
            except InvalidStringOperation:
                raise
            except MissingValueError:
                raise

            # Zmena pozice v kodu na LABEL            

            if self.runtime_environment["position"] != i:
                if self.runtime_environment["position"] != last + 1:
                    i = self.runtime_environment["position"]
                    idx = keys.index(i)
                else:
                    idx = length
                    
            else:
                idx = idx + 1
                                     
