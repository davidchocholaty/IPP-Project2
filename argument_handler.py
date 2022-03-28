##########################################################################
#                                                                        #
# Soubor: argument_handler.py                                            #
# Vytvoren: 2022-03-28                                                   #
# Posledni zmena: 2022-03-28                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Skript pro zpracovani uzivatelskych argumentu                   #
#                                                                        #
##########################################################################

from argparse import ArgumentParser
from handler import Creator, Handler


class ArgumentCreator(Creator):
    def _factory_method(self, arg):
        return ArgumentHandler(arg)


class ArgumentHandler(Handler):
    def __init__(self, help_action):
        self.parser = ArgumentParser(add_help=False)
        self.parser.add_argument('-h', '--help', dest="help", action=help_action)
        self.parser.add_argument("-s", "--source", dest="source")
        self.parser.add_argument("-i", "--input", dest="input")

    def handler_interface(self):
        return self.parser.parse_known_args()
