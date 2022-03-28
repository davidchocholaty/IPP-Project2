##########################################################################
#                                                                        #
# Soubor: file_handler.py                                                #
# Vytvoren: 2022-03-28                                                   #
# Posledni zmena: 2022-03-28                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Skript pro vytvoreni ukazatele na vstupni data (soubor / stdin) #
#                                                                        #
##########################################################################

import sys
from handler import Creator, Handler


class FileCreator(Creator):
    def _factory_method(self, arg):
        return FileHandler(arg)


class FileHandler(Handler):
    def __init__(self, source):
        if source:
            self.source_handler = open(source)
        else:
            self.source_handler = sys.stdin

    def handler_interface(self):
        return self.source_handler
