##########################################################################
#                                                                        #
# Soubor: handler.py                                                     #
# Vytvoren: 2022-03-28                                                   #
# Posledni zmena: 2022-04-19                                             #
# Autor: David Chocholaty <xchoch09@stud.fit.vutbr.cz>                   #
# Projekt: Uloha 2 pro predmet IPP                                       #
# Popis: Trida obsahujici zakladni tridni strukturu                      #
#        dle navrhoveho vzoru Tovarni metoda                             #
#                                                                        #
##########################################################################

from abc import ABC, abstractmethod


# Trida Creator dle navrhoveho vzoru Tovarni metoda.
#
# Tato trida deklaruje tovarni metodu, ktera vraci objekt dane tridy.
class Creator(ABC):    
    def __init__(self, arg):
        self._handler = self._factory_method(arg)

    # Tovarni metoda pro navraceni objektu dane tridy.
    @abstractmethod
    def _factory_method(self, arg):
        pass
    
    # Ziskani obsluhy.
    @property
    def handler(self):
        return self._handler.handler_interface()


# Trida Handler dle navrhoveho vzoru Tovarni metoda.
#
# Trida deklaruje metodu pro ziskani obsluhy (souboru / argumentu) dle konkretni tridy.
class Handler(ABC):
    @abstractmethod
    def handler_interface(self):
        pass
