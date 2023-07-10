##########################################################################
#                                                                        #
# Soubor: argument_parser.py                                             #
# Vytvoren: 2022-03-28                                                   #
# Posledni zmena: 2022-03-28                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Skript pro vytvoreni vlastni verze ArgumentParser               #
#                                                                        #
##########################################################################

import argparse
from exit_code import ExitCode


# Vlastni trida ArgumentParser pro zmenu funkcionality argparse.ArgumentParser.
class ArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        self.exit(ExitCode.WRONG_OPTION.value)
