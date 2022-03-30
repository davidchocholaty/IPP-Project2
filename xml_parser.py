##########################################################################
#                                                                        #
# Soubor: xml_parser.py                                                  #
# Vytvoren: 2022-03-28                                                   #
# Posledni zmena: 2022-03-30                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Skript pro zpracovani vstupnich XML dat                         #
#                                                                        #
##########################################################################

import xml.etree.ElementTree as ET


class XMLParser:
    def __init__(self, source):
        self.source = source

    def parse_xml(self):
        try:
            tree = ET.parse(self.source)
            root = tree.getroot()
        except ET.ParseError:
            raise

        return root
