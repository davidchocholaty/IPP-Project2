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

import czech_argparse as argparse
from argparse import ArgumentParser
from handler import Creator, Handler


class ArgumentCreator(Creator):
    def _factory_method(self, arg):
        return ArgumentHandler(arg)


class ArgumentHandler(Handler):
    def __init__(self, add_help):
        self.parser = ArgumentParser(add_help)
        self.parser.add_argument("-s", "--source", dest="source",
                                 help="vstupni soubor s XML reprezentaci zdrojoveho kodu IPPcode22", metavar="ZDROJ")
        self.parser.add_argument("-i", "--input", dest="input",
                                 help="soubor se vstupy pro samotnou interpretaci zadaneho zdrojoveho kodu",
                                 metavar="VSTUP")

    def handler_interface(self):
        return self.parser.parse_known_args()
