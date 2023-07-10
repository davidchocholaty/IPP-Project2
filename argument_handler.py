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

from argument_parser import ArgumentParser
from handler import Creator, Handler


# Trida pro vytvareni obsluhy argumentu dle navrhoveho vzoru Tovarni metoda.
class ArgumentCreator(Creator):
    def _factory_method(self, arg):
        return ArgumentHandler(arg)


# Trida pro obsluhu argumentu.
class ArgumentHandler(Handler):
    # Vytvoreni argumentu.
    def __init__(self, help_action):
        self.parser = ArgumentParser(add_help=False)
        self.parser.add_argument('-h', '--help', dest="help", action=help_action)
        self.parser.add_argument("-s", "--source", dest="source")
        self.parser.add_argument("-i", "--input", dest="input")

    # Metoda pro ziskani vstupnich uzivatelskych argumentu.
    def handler_interface(self):
        return self.parser.parse_known_args()
