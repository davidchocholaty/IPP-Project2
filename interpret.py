##########################################################################
#                                                                        #
# Soubor: interpret.py                                                   #
# Vytvoren: 2022-03-28                                                   #
# Posledni zmena: 2022-03-28                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Hlavni skript interpreteru pro jazyk IPPcode22                  #
#                                                                        #
##########################################################################

from argument_handler import ArgumentCreator, ArgumentHandler
from file_handler import FileCreator, FileHandler


def handle_args():
    arg_handler = ArgumentCreator(False)
    args, leftovers = arg_handler.handler

    # TODO leftovers

    source_data = args.source
    input_data = args.input

    source_file = FileCreator(source_data)
    source_handler = source_file.handler

    input_file = FileCreator(input_data)
    input_handler = input_file.handler


def main():
    handle_args()


if __name__ == '__main__':
    main()
