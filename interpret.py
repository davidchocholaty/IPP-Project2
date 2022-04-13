##########################################################################
#                                                                        #
# Soubor: interpret.py                                                   #
# Vytvoren: 2022-03-28                                                   #
# Posledni zmena: 2022-03-30                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Hlavni skript interpreteru pro jazyk IPPcode22                  #
#                                                                        #
##########################################################################

import sys

from xml.etree.ElementTree import ParseError
from custom_exception import MultipleOccurenceError, InvalidOperandValue, InvalidXMLFormat, VariableNotExist, \
    FrameNotExist, InvalidOperandType, ZeroDivision, UnexpectedInstructionError, ValueNotInRange
from argument_handler import ArgumentCreator
from file_handler import FileCreator
from exit_code import ExitCode
from xml_parser import XMLParser
from interpret_util import Interpret


def print_help():
    print("napoveda: interpret.py [-h] [-s ZDROJ] [-i VSTUP]")
    print("\nInterpret jazyka IPPcode22.\n")
    print("volitelne argumenty:\n")
    print("\t-h, --help\t\t\tZobrazi tuto napovedu a ukonci program.")
    print("\t-s ZDROJ, --source ZDROJ\tVstupni soubor s XML reprezentaci zdrojoveho kodu IPPcode22.")
    print("\t-i VSTUP, --input VSTUP\t\tSoubor se vstupy pro samotnou interpretaci zadaneho zdrojoveho kodu.\n")

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


def parse_input_xml(source_handler):
    parser = XMLParser(source_handler)

    try:
        root = parser.parse_xml()
    except ParseError:
        sys.exit(ExitCode.WRONG_XML_FORMAT.value)

    return root


def init_interpret(root, input_handler):
    interpret = Interpret(root)

    if not interpret.is_valid_lang():
        sys.exit(ExitCode.WRONG_XML_STRUCTURE.value)

    try:
        interpret.set_labels()
    except MultipleOccurenceError:
        sys.exit(ExitCode.SEMANTIC_CHECK_ERROR.value)
    except ParseError:
        sys.exit(ExitCode.WRONG_XML_STRUCTURE.value)

    try:
        interpret.set_order()
    except MultipleOccurenceError:
        sys.exit(ExitCode.WRONG_XML_STRUCTURE.value)

    interpret.set_input_handler(input_handler)

    return interpret


def run_interpret(root, input_handler):
    interpret = init_interpret(root, input_handler)

    try:
        interpret.run()
    except InvalidOperandValue:
        sys.exit(ExitCode.SEMANTIC_CHECK_ERROR.value)
    except InvalidXMLFormat:
        sys.exit(ExitCode.WRONG_XML_STRUCTURE.value)
    except VariableNotExist:
        sys.exit(ExitCode.RUNTIME_VAR_NOT_EXISTS.value)
    except FrameNotExist:
        sys.exit(ExitCode.RUNTIME_FRAME_NOT_EXISTS.value)
    except InvalidOperandType:
        sys.exit(ExitCode.RUNTIME_WRONG_OPERAND_TYPE.value)
    except ValueNotInRange:
        sys.exit(ExitCode.RUNTIME_WRONG_OPERAND_VAL.value)
    except ZeroDivision:
        sys.exit(ExitCode.RUNTIME_WRONG_OPERAND_VAL.value)
    except UnexpectedInstructionError:
        sys.exit(ExitCode.INTERN_ERROR.value)
    # TODO

    # TODO kdyz nebudou sedet cisla order kde to je resene (bude cislo v poradi vynechane)


def close_files(source_handler, input_handler):
    source_handler.close()
    input_handler.close()


def main():
    source_handler, input_handler = handle_user_input()
    root = parse_input_xml(source_handler)

    run_interpret(root, input_handler)
    close_files(source_handler, input_handler)


if __name__ == '__main__':
    main()
