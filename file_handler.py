##########################################################################
#                                                                        #
# Soubor: file_handler.py                                                #
# Vytvoren: 2022-03-28                                                   #
# Posledni zmena: 2022-04-19                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Skript pro vytvoreni ukazatele na vstupni data (soubor / stdin) #
#                                                                        #
##########################################################################

import sys
from handler import Creator, Handler


# Trida pro vytvareni obsluhy souboru dle navrhoveho vzoru Tovarni metoda.
class FileCreator(Creator):
    def _factory_method(self, arg):
        return FileHandler(arg)

# Trida pro obsluhu souboru.
class FileHandler(Handler):
    # Vytvoreni obsluhy souboru.
    def __init__(self, source):
        if source:
            try:
                self.source_handler = open(source, "r")
            except FileNotFoundError:
                self.source_handler = None
        else:
            self.source_handler = sys.stdin

    # Metoda pro ziskani obsluhy souboru.
    def handler_interface(self):
        return self.source_handler
