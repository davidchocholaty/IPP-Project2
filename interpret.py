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

import sys

from argument_handler import ArgumentCreator, ArgumentHandler
from file_handler import FileCreator, FileHandler
from exit_code import ExitCode


def print_help():
    print("napoveda: interpret.py [-h] [-s ZDROJ] [-i VSTUP]\n")
    print("\n")
    print("volitelne argumenty:\n")
    print("\t-h, --help\n")
    print("\t-s ZDROJ, --source ZDROJ\n")
    print("\t-i VSTUP, --input VSTUP\n")

    sys.exit(ExitCode.EXIT_SUCCESS.value)


def handle_args(arg_handler):
    args, leftovers = arg_handler.handler

    # Na vstupu zadany nezname parametry
    if len(leftovers) > 0:
        sys.exit(ExitCode.WRONG_OPTION.value)

    # Napoveda
    if args.help:
        if args.input is None and args.source is None:
            print_help()
        else:
            # S parametrem help byl zadan i nektery z dalsich volitelnych parametry
            sys.exit(ExitCode.WRONG_OPTION.value)

    # Alespon jeden z parametru musi byt vzdy zadan
    if args.source is None and args.input is None:
        sys.exit(ExitCode.WRONG_OPTION.value)

    return args.source, args.input


def handle_user_input():
    arg_handler = ArgumentCreator("store_true")

    source_data, input_data = handle_args(arg_handler)

    source_file = FileCreator(source_data)
    source_handler = source_file.handler

    input_file = FileCreator(input_data)
    input_handler = input_file.handler

    if source_handler is None or input_handler is None:
        sys.exit(ExitCode.OPEN_INPUT_FILE_ERROR.value)

    return source_handler, input_handler


def main():
    source_handler, input_handler = handle_user_input()


if __name__ == '__main__':
    main()
