"""
Exemplo de uso do checkout com PIX mas sem aplicar o desconto PIX.
"""

from checkout_refatorado import (
    Pedido, PagamentoPix, FreteNormal, CheckoutFacade
)


def exemplo_pix_sem_desconto():
    # Criando um pedido simples
    itens = [
        {'nome': 'Poção de Cura', 'valor': 100.0}
    ]

    # Criar pedido usando PIX como pagamento, mas SEM aplicar o decorator
    # de desconto PIX. Note que não usamos DescontoPix aqui.
    pedido = Pedido(
        itens=itens,
        estrategia_pagamento=PagamentoPix(),
        estrategia_frete=FreteNormal(),
        tem_embalagem_presente=False
    )

    # Usar a fachada para processar o pedido
    facade = CheckoutFacade()
    facade.concluir_transacao(pedido)


if __name__ == "__main__":
    print("=== Exemplo: Pagamento PIX sem Desconto ===")
    exemplo_pix_sem_desconto()