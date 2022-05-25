from controllers.Strategy import Strategy
from typing import List

class ConcreteStrategyA(Strategy):
    def do_algorithm(self, data: List) -> List:
        return sorted(data)