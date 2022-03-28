##########################################################################
#                                                                        #
# Soubor: handler.py                                                     #
# Vytvoren: 2022-03-28                                                   #
# Posledni zmena: 2022-03-28                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis:                                                                 #
#                                                                        #
##########################################################################

from abc import ABC, abstractmethod

# https://sourcemaking.com/design_patterns/factory_method/python/1
# https://refactoring.guru/design-patterns/factory-method/python/example


class Creator(ABC):
    def __init__(self, arg):
        self._handler = self._factory_method(arg)

    @abstractmethod
    def _factory_method(self, arg):
        pass

    @property
    def handler(self):
        return self._handler.handler_interface()


class Handler(ABC):
    @abstractmethod
    def handler_interface(self):
        pass
