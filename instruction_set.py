##########################################################################
#                                                                        #
# Soubor: interpret.py                                                   #
# Vytvoren: 2022-03-30                                                   #
# Posledni zmena: 2022-03-30                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Hlavni skript interpreteru pro jazyk IPPcode22                  #
#                                                                        #
##########################################################################

inst_set = {
    # Prace s ramci, volani funkci
    'MOVE': ['var', 'symb'],
    'CREATEFRAME': [],
    'PUSHFRAME': [],
    'POPFRAME': [],
    'DEFVAR': ['var'],
    'CALL': ['label'],
    'RETURN': [],
    # Prace s datovym zasobnikem */
    'PUSHS': ['symb'],
    'POPS': ['var'],
    # Aritmeticke, relacni, booleovske a konverzni instrukce */
    'ADD': ['var', 'symb', 'symb'],
    'SUB': ['var', 'symb', 'symb'],
    'MUL': ['var', 'symb', 'symb'],
    'IDIV': ['var', 'symb', 'symb'],
    'LT': ['var', 'symb', 'symb'],
    'GT': ['var', 'symb', 'symb'],
    'EQ': ['var', 'symb', 'symb'],
    'AND': ['var', 'symb', 'symb'],
    'OR': ['var', 'symb', 'symb'],
    'NOT': ['var', 'symb'],
    'INT2CHAR': ['var', 'symb'],
    'STRI2INT': ['var', 'symb', 'symb'],
    # Vstupne vystupni instrukce */
    'READ': ['var', 'type'],
    'WRITE': ['symb'],
    # Prace s retezci */
    'CONCAT': ['var', 'symb', 'symb'],
    'STRLEN': ['var', 'symb'],
    'GETCHAR': ['var', 'symb', 'symb'],
    'SETCHAR': ['var', 'symb', 'symb'],
    # Prace s typy */
    'TYPE': ['var', 'symb'],
    # Instrukce pro rizeni toku programu */
    'LABEL': ['label'],
    'JUMP': ['label'],
    'JUMPIFEQ': ['label', 'symb', 'symb'],
    'JUMPIFNEQ': ['label', 'symb', 'symb'],
    'EXIT': ['symb'],
    # Ladici instrukce */
    'DPRINT': ['symb'],
    'BREAK': []
}
