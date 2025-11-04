"""Refatoração do checkout_monolitico usando Strategy, Decorator e Facade.

Mantém funcionalidades do monolítico mas com melhor estrutura:
- Estratégias de pagamento (Strategy)
- Estratégias de frete (Strategy)
- Descontos/taxas como Decorators  
- Fachada (CheckoutFacade) que orquestra o fluxo
- ProcessadorPedido que centraliza regras
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime
try:
    from .processador_pedido import ProcessadorPedido
except ImportError:
    from processador_pedido import ProcessadorPedido


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


# Observação: os subsistemas `SistemaEstoque` e `GeradorNotaFiscal` foram
# extraídos para o pacote `subsistemas`.


# ===== Facade: CheckoutFacade =====
class CheckoutFacade:
    """Fachada que simplifica o fluxo de checkout.

    Expondo um método de alto nível `concluir_transacao(pedido)` que:
      - calcula valor com descontos (pedido pode ser decorado)
      - calcula frete via estratégia
      - processa pagamento via estratégia
      - registra no estoque e emite nota fiscal em caso de sucesso
    """

    def __init__(self, estoque: Optional[Any] = None, gerador_nf: Optional[Any] = None):
        # Se os subsistemas não puderem ser importados (execução em ambiente atípico),
        # usamos implementações locais simples como fallback.
        if SistemaEstoque is None:
            class _FallbackEstoque:
                def registrar_pedido(self, pedido):
                    print("Pedido registrado (fallback de estoque).")

            self.estoque = estoque or _FallbackEstoque()
        else:
            self.estoque = estoque or SistemaEstoque()

        if GeradorNotaFiscal is None:
            class _FallbackNF:
                def emitir(self, pedido, valor: float):
                    print(f"Emitindo nota fiscal R${valor:.2f} (fallback).")

            self.gerador_nf = gerador_nf or _FallbackNF()
        else:
            self.gerador_nf = gerador_nf or GeradorNotaFiscal()

    def concluir_transacao(self, pedido: Pedido) -> bool:
        """Orquestra o fluxo de finalização de forma simplificada."""
        print("=========================================")
        print("INICIANDO CHECKOUT (FACADE)...")

        # 1. Valor após descontos/taxas (decorators) — pedido pode ser decorado
        valor_apos_descontos = pedido.calcular_valor()

        # 2. Calcular frete usando a estratégia fornecida no pedido
        custo_frete = pedido.estrategia_frete.calcular(valor_apos_descontos)

        valor_final = valor_apos_descontos + custo_frete

        # 3. Compatibilidade: se o pedido não foi decorado com taxa de embalagem,
        #    aplicamos aqui a taxa quando necessário.
        if not isinstance(pedido, PedidoDecorator) and pedido.tem_embalagem_presente:
            taxa = 5.00
            print(f"Adicionando R${taxa:.2f} de Embalagem de Presente.")
            valor_final += taxa

        print(f"\nValor a Pagar: R${valor_final:.2f}")

        # 4. Processar pagamento via estratégia
        sucesso = pedido.estrategia_pagamento.processar(valor_final)

        # 5. Em caso de sucesso, disparar ações nos subsistemas
        if sucesso:
            self.estoque.registrar_pedido(pedido)
            self.gerador_nf.emitir(pedido, valor_final)
            print("\nSUCESSO: Pedido finalizado.")
            return True
        else:
            print("\nFALHA: Transação abortada.")
            return False

    # Mantemos um wrapper para compatibilidade com código que usava
    # `finalizar_compra(pedido)` anteriormente.
    def finalizar_compra(self, pedido: Pedido) -> bool:
        return self.concluir_transacao(pedido)


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
    # Usando a Fachada pelo método de alto-nível `concluir_transacao`.
    facade.concluir_transacao(pedido1)

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

    # Segundo pedido usando a mesma fachada
    facade.concluir_transacao(pedido2)


if __name__ == "__main__":
    main()
