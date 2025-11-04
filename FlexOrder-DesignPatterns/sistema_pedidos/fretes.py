"""
Implementações das estratégias de frete.
"""
from .pedido import EstrategiaFrete


class FreteNormal(EstrategiaFrete):
    """Frete padrão: 5% do valor do pedido."""
    
    def calcular(self, valor: float) -> float:
        custo = valor * 0.05
        print(f"Frete Normal: R${custo:.2f}")
        return custo


class FreteExpresso(EstrategiaFrete):
    """Frete expresso: 10% do valor + taxa fixa."""
    
    def calcular(self, valor: float) -> float:
        custo = valor * 0.10 + 15.00
        print(f"Frete Expresso (com taxa): R${custo:.2f}")
        return custo


class FreteTeletransporte(EstrategiaFrete):
    """Frete VIP: valor fixo premium."""
    
    def calcular(self, valor: float) -> float:
        custo = 50.00
        print(f"Frete Teletransporte: R${custo:.2f}")
        return custo