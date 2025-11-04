"""
Gerenciador de descontos para simplificar a aplicação de descontos
sem necessidade de usar Decorators.
"""
from decimal import Decimal
from typing import Optional


class GerenciadorDesconto:
    """Classe que gerencia descontos de forma simples e direta."""

    @staticmethod
    def calcular_desconto_pix(valor: float) -> float:
        """Aplica 5% de desconto para pagamentos PIX."""
        return valor * 0.95

    @staticmethod
    def calcular_desconto_pedido_grande(valor: float) -> float:
        """Aplica 10% de desconto para pedidos acima de R$500."""
        if valor > 500:
            return valor * 0.90
        return valor

    @staticmethod
    def calcular_valor_com_desconto(
        valor_base: float,
        *,  # força parâmetros nomeados após este
        desconto_pix: bool = False,
        pedido_grande: bool = False
    ) -> float:
        """Calcula valor final aplicando os descontos solicitados.
        
        Args:
            valor_base: Valor inicial do pedido
            desconto_pix: Se True, aplica 5% de desconto
            pedido_grande: Se True, verifica e aplica desconto de 10% se valor > 500
            
        Returns:
            Valor com descontos aplicados
        """
        valor = valor_base

        if desconto_pix:
            print("Aplicando 5% de desconto PIX.")
            valor = GerenciadorDesconto.calcular_desconto_pix(valor)

        if pedido_grande:
            # Só aplica se o valor_base (antes de qualquer desconto) for > 500
            if valor_base > 500:
                print("Aplicando 10% de desconto para pedidos grandes.")
                # Aplica na sequência, após PIX se houver
                valor = GerenciadorDesconto.calcular_desconto_pedido_grande(valor)

        return valor


# Exemplo de uso direto
if __name__ == "__main__":
    # Teste com valor pequeno
    valor_teste = 100.0
    print(f"\nTestando com R${valor_teste:.2f}:")
    
    # Só PIX
    valor_pix = GerenciadorDesconto.calcular_valor_com_desconto(
        valor_teste, desconto_pix=True
    )
    print(f"Valor com desconto PIX: R${valor_pix:.2f}")

    # Teste com valor grande
    valor_teste = 600.0
    print(f"\nTestando com R${valor_teste:.2f}:")
    
    # PIX + Pedido Grande
    valor_final = GerenciadorDesconto.calcular_valor_com_desconto(
        valor_teste,
        desconto_pix=True,
        pedido_grande=True
    )
    print(f"Valor com PIX + desconto pedido grande: R${valor_final:.2f}")