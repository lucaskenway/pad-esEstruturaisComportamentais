"""
Exemplo de uso do sistema de pedidos.
"""
from sistema_pedidos.pedido import Pedido
from sistema_pedidos.pagamentos import PagamentoPix, PagamentoCredito
from sistema_pedidos.fretes import FreteNormal, FreteExpresso
from sistema_pedidos.sistema import SistemaPedidos


def exemplo_principal():
    # Criar o sistema
    sistema = SistemaPedidos()

    # Pedido 1: PIX + Frete Normal
    print("\n=== Pedido 1: Itens Mágicos Básicos ===")
    itens_p1 = [
        {'nome': 'Capa da Invisibilidade', 'valor': 150.0},
        {'nome': 'Poção de Voo', 'valor': 80.0}
    ]
    
    pedido1 = Pedido(
        itens=itens_p1,
        metodo_pagamento=PagamentoPix(),
        tipo_frete=FreteNormal(),
        tem_embalagem_presente=False
    )
    
    sistema.processar_pedido(pedido1)

    # Pedido 2: Crédito + Frete Expresso + Presente
    print("\n=== Pedido 2: Item Premium ===")
    itens_p2 = [
        {'nome': 'Cristal Mágico', 'valor': 600.0}
    ]
    
    pedido2 = Pedido(
        itens=itens_p2,
        metodo_pagamento=PagamentoCredito(),
        tipo_frete=FreteExpresso(),
        tem_embalagem_presente=True
    )
    
    sistema.processar_pedido(pedido2)


if __name__ == "__main__":
    print("Sistema de Pedidos - E-commerce Mágico")
    print("======================================")
    exemplo_principal()