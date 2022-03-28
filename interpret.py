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
import argparse
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


def handle_args(args, leftovers):
    if args.help:
        print_help()


def handle_user_input():
    arg_handler = ArgumentCreator("store_true")

    args, leftovers = arg_handler.handler

    handle_args(args, leftovers)

    # TODO leftovers

    source_data = args.source
    input_data = args.input

    source_file = FileCreator(source_data)
    source_handler = source_file.handler

    input_file = FileCreator(input_data)
    input_handler = input_file.handler

def main():
    handle_user_input()


if __name__ == '__main__':
    main()
