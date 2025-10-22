"""Refatoração do checkout_monolitico usando Strategy, Decorator e Facade.

Este arquivo implementa:
- Estratégias de pagamento (Strategy)
- Estratégias de frete (Strategy)
- Descontos/taxas como Decorators aplicáveis ao pedido
- Uma fachada (CheckoutFacade) que orquestra o fluxo de finalização

O objetivo é permitir a extensibilidade sem modificar a classe Pedido.
"""

from abc import ABC, abstractmethod
from typing import List, Dict


class Pedido:
    def __init__(self, itens: List[Dict], estrategia_pagamento, estrategia_frete, tem_embalagem_presente: bool = False):
        self.itens = itens
        self.estrategia_pagamento = estrategia_pagamento
        self.estrategia_frete = estrategia_frete
        self.tem_embalagem_presente = tem_embalagem_presente
        self.valor_base = sum(item['valor'] for item in itens)

    def calcular_valor(self):
        # Valor base - descontos são aplicados via Decorator externo
        return self.valor_base


# ===== Strategy: Pagamento =====
class MetodoPagamento(ABC):
    @abstractmethod
    def processar(self, valor: float) -> bool:
        pass


class PagamentoCredito(MetodoPagamento):
    def processar(self, valor: float) -> bool:
        print(f"Processando R${valor:.2f} via Cartão de Crédito...")
        if valor < 1000:
            print("   -> Pagamento com Crédito APROVADO.")
            return True
        else:
            print("   -> Pagamento com Crédito REJEITADO (limite excedido).")
            return False


class PagamentoPix(MetodoPagamento):
    def processar(self, valor: float) -> bool:
        print(f"Processando R${valor:.2f} via PIX...")
        print("   -> Pagamento com PIX APROVADO (QR Code gerado).")
        return True


class PagamentoMana(MetodoPagamento):
    def processar(self, valor: float) -> bool:
        print(f"Processando R${valor:.2f} via Transferência de Mana...")
        print("   -> Pagamento com Mana APROVADO (requer 10 segundos de espera).")
        return True


# ===== Strategy: Frete =====
class EstrategiaFrete(ABC):
    @abstractmethod
    def calcular(self, valor: float) -> float:
        pass


class FreteNormal(EstrategiaFrete):
    def calcular(self, valor: float) -> float:
        custo = valor * 0.05
        print(f"Frete Normal: R${custo:.2f}")
        return custo


class FreteExpresso(EstrategiaFrete):
    def calcular(self, valor: float) -> float:
        custo = valor * 0.10 + 15.00
        print(f"Frete Expresso (com taxa): R${custo:.2f}")
        return custo


class FreteTeletransporte(EstrategiaFrete):
    def calcular(self, valor: float) -> float:
        custo = 50.00
        print(f"Frete Teletransporte: R${custo:.2f}")
        return custo


# ===== Decorator: Descontos / Taxas =====
class PedidoDecorator(Pedido, ABC):
    def __init__(self, pedido: Pedido):
        self._pedido = pedido

    def calcular_valor(self):
        return self._pedido.calcular_valor()

    def __getattr__(self, name):
        # Delegar atributos desconhecidos para o pedido encapsulado.
        # Isso permite encadear decorators e ainda acessar campos como
        # estrategia_pagamento, estrategia_frete e tem_embalagem_presente.
        return getattr(self._pedido, name)


class DescontoPix(PedidoDecorator):
    def calcular_valor(self):
        valor = self._pedido.calcular_valor()
        print("Aplicando 5% de desconto PIX.")
        return valor * 0.95


class DescontoPedidoGrande(PedidoDecorator):
    def calcular_valor(self):
        valor = self._pedido.calcular_valor()
        if valor > 500:
            print("Aplicando 10% de desconto para pedidos grandes.")
            return valor * 0.90
        return valor


class TaxaEmbalagemPresente(PedidoDecorator):
    def calcular_valor(self):
        valor = self._pedido.calcular_valor()
        if self._pedido.tem_embalagem_presente:
            taxa = 5.00
            print(f"Adicionando R${taxa:.2f} de Embalagem de Presente.")
            return valor + taxa
        return valor


# ===== Subsystem simples: Estoque e NotaFiscal =====
class Estoque:
    def registrar_pedido(self, pedido: Pedido):
        print("Pedido registrado no estoque (simulado).")


class NotaFiscal:
    def emitir(self, pedido: Pedido, valor: float):
        print(f"Emitindo nota fiscal para R${valor:.2f} (simulado).")


# ===== Facade: CheckoutFacade =====
class CheckoutFacade:
    def __init__(self, estoque: Estoque = None, nota_fiscal: NotaFiscal = None):
        self.estoque = estoque or Estoque()
        self.nota_fiscal = nota_fiscal or NotaFiscal()

    def finalizar_compra(self, pedido: Pedido) -> bool:
        print("=========================================")
        print("INICIANDO CHECKOUT (FACADE)...")

        # 1. Aplicar descontos/taxas via decorator - assumimos que o pedido
        #    já pode ser um objeto decorado. Para compatibilidade, usamos
        #    o método calcular_valor.
        valor_apos_descontos = pedido.calcular_valor()

        # 2. Calcular frete via estratégia
        custo_frete = pedido.estrategia_frete.calcular(valor_apos_descontos)

        valor_final = valor_apos_descontos + custo_frete

        # 3. Se o pedido não for decorado para embalar, aplicamos a taxa aqui
        #    (para manter compatibilidade com objetos Pedido simples).
        if not isinstance(pedido, PedidoDecorator) and pedido.tem_embalagem_presente:
            taxa = 5.00
            print(f"Adicionando R${taxa:.2f} de Embalagem de Presente.")
            valor_final += taxa

        print(f"\nValor a Pagar: R${valor_final:.2f}")

        # 4. Processar pagamento via estratégia
        sucesso = pedido.estrategia_pagamento.processar(valor_final)

        if sucesso:
            self.estoque.registrar_pedido(pedido)
            self.nota_fiscal.emitir(pedido, valor_final)
            print("\nSUCESSO: Pedido finalizado.")
            return True
        else:
            print("\nFALHA: Transação abortada.")
            return False


# ===== Exemplo de uso =====
def main():
    itens_p1 = [
        {'nome': 'Capa da Invisibilidade', 'valor': 150.0},
        {'nome': 'Poção de Voo', 'valor': 80.0}
    ]

    # Pedido 1: PIX + Frete Normal + desconto Pix
    pedido1_base = Pedido(itens_p1, PagamentoPix(), FreteNormal(), tem_embalagem_presente=False)
    # Aplicamos decorator de desconto PIX
    pedido1 = DescontoPix(pedido1_base)
    # Propagar campos necessários para a fachada
    pedido1.estrategia_pagamento = pedido1_base.estrategia_pagamento
    pedido1.estrategia_frete = pedido1_base.estrategia_frete
    pedido1.tem_embalagem_presente = pedido1_base.tem_embalagem_presente

    facade = CheckoutFacade()
    facade.finalizar_compra(pedido1)

    print("\n--- Próximo Pedido ---\n")

    # Pedido 2: Grande + Crédito + Frete Expresso + embalagem presente
    itens_p2 = [
        {'nome': 'Cristal Mágico', 'valor': 600.0}
    ]
    pedido2_base = Pedido(itens_p2, PagamentoCredito(), FreteExpresso(), tem_embalagem_presente=True)
    # Aplicar desconto para pedido grande e taxa de embalagem como decorators encadeados
    pedido2 = TaxaEmbalagemPresente(DescontoPedidoGrande(pedido2_base))
    pedido2.estrategia_pagamento = pedido2_base.estrategia_pagamento
    pedido2.estrategia_frete = pedido2_base.estrategia_frete
    pedido2.tem_embalagem_presente = pedido2_base.tem_embalagem_presente

    facade.finalizar_compra(pedido2)


if __name__ == "__main__":
    main()
