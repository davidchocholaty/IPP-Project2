##########################################################################
#                                                                        #
# Soubor: czech_argparse.py                                              #
# Vytvoren: 2022-03-28                                                   #
# Posledni zmena: 2022-03-28                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Skript pro preklad zprav argparse do ceskeho jazyka             #
#                                                                        #
##########################################################################

##
# Code is inspired of following source.
#
# Source: https://stackoverflow.com/questions/22951442/how-to-make-pythons-argparse-generate-non-english-text
# Author: Frederic (https://stackoverflow.com/users/2971847/frederic)
#

import gettext

__TRANSLATIONS = {
    'ambiguous option: %(option)s could match %(matches)s': 'ambiguous option: %(option)s could match %(matches)s',
    'argument "-" with mode %r': 'argument "-" with mode %r',
    'cannot merge actions - two groups are named %r': 'cannot merge actions - two groups are named %r',
    "can't open '%(filename)s': %(error)s": "can't open '%(filename)s': %(error)s",
    'dest= is required for options like %r': 'dest= is required for options like %r',
    'expected at least one argument': 'expected at least one argument',
    'expected at most one argument': 'expected at most one argument',
    'expected one argument': 'expected one argument',
    'ignored explicit argument %r': 'ignored explicit argument %r',
    'invalid choice: %(value)r (choose from %(choices)s)': 'invalid choice: %(value)r (choose from %(choices)s)',
    'invalid conflict_resolution value: %r': 'invalid conflict_resolution value: %r',
    'invalid option string %(option)r: must start with a character %(prefix_chars)r':
        'invalid option string %(option)r: must start with a character %(prefix_chars)r',
    'invalid %(type)s value: %(value)r': 'invalid %(type)s value: %(value)r',
    'mutually exclusive arguments must be optional': 'mutually exclusive arguments must be optional',
    'not allowed with argument %s': "not allowed with argument %s",
    'one of the arguments %s is required': 'one of the arguments %s is required',
    'optional arguments': 'volitelne argumenty',
    'positional arguments': 'positional arguments',
    "'required' is an invalid argument for positionals": "'required' is an invalid argument for positionals",
    'show this help message and exit': 'zobrazi tuto napovedu a ukonci program',
    'unrecognized arguments: %s': 'unrecognized arguments: %s',
    'unknown parser %(parser_name)r (choices: %(choices)s)': 'unknown parser %(parser_name)r (choices: %(choices)s)',
    'usage: ': 'napoveda: ',
    '%(prog)s: error: %(message)s\n': '%(prog)s: error: %(message)s\n',
    '%r is not callable': '%r is not callable',
}

gettext.gettext = lambda text: __TRANSLATIONS[text] or text

from argparse import *