from controllers.Strategy import Strategy

class Copelia(Strategy):
    def rotacionar_torre(self, graus: int) -> bool:
        return True
    
    def mover_ferramenta(self, centimentros: int) -> bool:
        return True
    
    def zerar_posicao(self) -> bool:
        return True

    def valor_sensores(self) -> dict:
        return {}

    def atuar_ferramenta(self, status: bool) -> bool:
        return True