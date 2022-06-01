from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Context():
    """
    The Context defines the interface of interest to clients.
    """

    def __init__(self, strategy: Strategy) -> None:
        """
        Usually, the Context accepts a strategy through the constructor, but
        also provides a setter to change it at runtime.
        """

        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It should work
        with all strategies via the Strategy interface.
        """

        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        """
        Usually, the Context allows replacing a Strategy object at runtime.
        """

        self._strategy = strategy
    
    def rotacionar_torre(self, graus: int) -> bool:
        return self._strategy.rotacionar_torre(graus)
    
    def mover_ferramenta(self, centimentros: int) -> bool:
        return self._strategy.mover_ferramenta(centimentros)
    
    def zerar_posicao(self) -> bool:
        return self._strategy.zerar_posicao()
    
    def valor_sensores(self) -> bool:
        return self._strategy.valor_sensores()
    
    def atuar_ferramenta(self, status) -> bool:
        return self._strategy.atuar_ferramenta(status)


class Strategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """
    
    @abstractmethod
    def rotacionar_torre(self, graus: int) -> bool:
        pass
    
    @abstractmethod
    def mover_ferramenta(self, centimentros: int) -> bool:
        pass
    
    @abstractmethod
    def zerar_posicao(self) -> bool:
        pass

    @abstractmethod
    def valor_sensores(self) -> dict:
        pass

    @abstractmethod
    def atuar_ferramenta(self, status: bool) -> bool:
        pass