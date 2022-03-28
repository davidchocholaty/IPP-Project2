##########################################################################
#                                                                        #
# Soubor: xml_parser.py                                                  #
# Vytvoren: 2022-03-28                                                   #
# Posledni zmena: 2022-03-28                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Skript pro zpracovani uzivatelskych argumentu                   #
#                                                                        #
##########################################################################

import czech_argparse as argparse
from argparse import ArgumentParser


class ArgumentHandler:
    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument("-s", "--source", dest="source", help="vstupni soubor s XML reprezentaci zdrojoveho kodu IPPcode22", metavar="ZDROJ")
        self.parser.add_argument("-i", "--input", dest="input", help="soubor se vstupy pro samotnou interpretaci zadaneho zdrojoveho kodu", metavar="VSTUP")

    def parse_args(self):
        return self.parser.parse_args()

