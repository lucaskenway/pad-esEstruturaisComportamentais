import os
import sys

# Ajusta sys.path para permitir importar o módulo mesmo com nomes de pasta contendo
# hífens quando rodado a partir da estrutura do repositório.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from checkout_refatorado import (
    Pedido, PagamentoPix, PagamentoCredito,
    FreteNormal, FreteExpresso, DescontoPix, DescontoPedidoGrande,
    TaxaEmbalagemPresente, CheckoutFacade
)


def test_checkout_sucesso_pix():
    itens = [{'nome': 'Item A', 'valor': 150.0}, {'nome': 'Item B', 'valor': 80.0}]
    pedido_base = Pedido(itens, PagamentoPix(), FreteNormal(), tem_embalagem_presente=False)
    pedido = DescontoPix(pedido_base)
    pedido.estrategia_pagamento = pedido_base.estrategia_pagamento
    pedido.estrategia_frete = pedido_base.estrategia_frete
    pedido.tem_embalagem_presente = pedido_base.tem_embalagem_presente

    facade = CheckoutFacade()
    assert facade.concluir_transacao(pedido) is True


def test_checkout_falha_credito_limite():
    itens = [{'nome': 'Item VIP', 'valor': 2000.0}]
    pedido = Pedido(itens, PagamentoCredito(), FreteExpresso(), tem_embalagem_presente=False)
    facade = CheckoutFacade()
    assert facade.concluir_transacao(pedido) is False


if __name__ == "__main__":
    # Runner simples para executar os testes sem pytest
    test_checkout_sucesso_pix()
    test_checkout_falha_credito_limite()
    print("Todos os testes manuais passaram.")
