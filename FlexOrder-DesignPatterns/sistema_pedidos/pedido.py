"""
Modelo base do pedido e interfaces de estratégia.
"""
from abc import ABC, abstractmethod
from typing import List, Dict


class MetodoPagamento(ABC):
    """Interface para estratégias de pagamento."""
    @abstractmethod
    def processar(self, valor: float) -> bool:
        """Processa o pagamento e retorna se foi aprovado."""
        pass


class EstrategiaFrete(ABC):
    """Interface para estratégias de cálculo de frete."""
    @abstractmethod
    def calcular(self, valor: float) -> float:
        """Calcula o valor do frete baseado no valor do pedido."""
        pass


class Pedido:
    """Classe principal que representa um pedido."""
    
    def __init__(self, 
                 itens: List[Dict], 
                 metodo_pagamento: MetodoPagamento,
                 tipo_frete: EstrategiaFrete,
                 tem_embalagem_presente: bool = False):
        self.itens = itens
        self.metodo_pagamento = metodo_pagamento
        self.tipo_frete = tipo_frete
        self.tem_embalagem_presente = tem_embalagem_presente
        self.valor_base = sum(item['valor'] for item in itens)
        self._descontos_aplicados = []

    def adicionar_desconto(self, nome: str, percentual: float) -> None:
        """Adiciona um desconto ao pedido."""
        self._descontos_aplicados.append((nome, percentual))

    def calcular_valor_com_descontos(self) -> float:
        """Calcula o valor após aplicar todos os descontos registrados."""
        valor = self.valor_base
        for nome, percentual in self._descontos_aplicados:
            desconto = valor * (percentual / 100)
            valor -= desconto
            print(f"Aplicando {percentual}% de desconto {nome}.")
        return valor