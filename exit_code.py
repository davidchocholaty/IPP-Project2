##########################################################################
#                                                                        #
# Soubor: exit_code.py                                                   #
# Vytvoren: 2022-03-28                                                   #
# Posledni zmena: 2022-04-19                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Skript s chybovymi kody interpreteru                            #
#                                                                        #
##########################################################################

from enum import Enum

# Chybove kody interpreteru.
class ExitCode(Enum):
    EXIT_SUCCESS = 0
    WRONG_OPTION = 10
    OPEN_INPUT_FILE_ERROR = 11
    OPEN_OUTPUT_FILE_ERROR = 12
    WRONG_XML_FORMAT = 31
    WRONG_XML_STRUCTURE = 32
    SEMANTIC_CHECK_ERROR = 52
    RUNTIME_WRONG_OPERAND_TYPE = 53
    RUNTIME_VAR_NOT_EXISTS = 54
    RUNTIME_FRAME_NOT_EXISTS = 55
    RUNTIME_MISSING_VALUE = 56
    RUNTIME_WRONG_OPERAND_VAL = 57
    RUNTIME_WRONG_STRING_OPERATION = 58
    INTERN_ERROR = 99
