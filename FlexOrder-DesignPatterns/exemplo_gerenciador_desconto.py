"""
Exemplo de uso do checkout com o GerenciadorDesconto
"""

from checkout_refatorado import (
    Pedido, PagamentoPix, FreteNormal, CheckoutFacade
)
from gerenciador_desconto import GerenciadorDesconto


def exemplo_checkout_com_gerenciador():
    # 1. Pedido pequeno com PIX
    print("\n=== Pedido 1: R$100 com PIX ===")
    itens_p1 = [
        {'nome': 'Poção de Cura', 'valor': 100.0}
    ]
    
    pedido1 = Pedido(
        itens=itens_p1,
        estrategia_pagamento=PagamentoPix(),
        estrategia_frete=FreteNormal(),
        tem_embalagem_presente=False
    )
    
    # Sobrescrever o valor base com desconto
    valor_original = pedido1.valor_base
    pedido1.valor_base = GerenciadorDesconto.calcular_valor_com_desconto(
        valor_original,
        desconto_pix=True  # aplica 5% de desconto
    )

    facade = CheckoutFacade()
    facade.concluir_transacao(pedido1)

    # 2. Pedido grande com PIX
    print("\n=== Pedido 2: R$600 com PIX ===")
    itens_p2 = [
        {'nome': 'Varinha Mágica Premium', 'valor': 600.0}
    ]
    
    pedido2 = Pedido(
        itens=itens_p2,
        estrategia_pagamento=PagamentoPix(),
        estrategia_frete=FreteNormal(),
        tem_embalagem_presente=False
    )
    
    # Aplica ambos os descontos (PIX + pedido grande)
    valor_original = pedido2.valor_base
    pedido2.valor_base = GerenciadorDesconto.calcular_valor_com_desconto(
        valor_original,
        desconto_pix=True,     # 5% de desconto
        pedido_grande=True     # +10% se valor > 500
    )

    facade.concluir_transacao(pedido2)


if __name__ == "__main__":
    exemplo_checkout_com_gerenciador()