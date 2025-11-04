"""
Fachada principal do sistema de pedidos.
"""
from .pedido import Pedido
from typing import Optional


class SistemaPedidos:
    """Fachada que simplifica todas as operações do pedido."""
    
    def __init__(self):
        self._pedidos_processados = []

    def processar_pedido(self, pedido: Pedido) -> bool:
        """Processa um pedido aplicando descontos, frete e pagamento."""
        print("=========================================")
        print("INICIANDO PROCESSAMENTO DO PEDIDO...")

        # 1. Aplicar regras de desconto baseadas no pedido
        if isinstance(pedido.metodo_pagamento.__class__.__name__, str) and \
           pedido.metodo_pagamento.__class__.__name__ == 'PagamentoPix':
            pedido.adicionar_desconto("PIX", 5)
        
        if pedido.valor_base > 500:
            pedido.adicionar_desconto("Pedido Grande", 10)

        # 2. Calcular valor com descontos
        valor_com_descontos = pedido.calcular_valor_com_descontos()

        # 3. Calcular frete
        valor_frete = pedido.tipo_frete.calcular(valor_com_descontos)

        # 4. Adicionar taxa de embalagem se necessário
        valor_final = valor_com_descontos + valor_frete
        if pedido.tem_embalagem_presente:
            taxa = 5.00
            valor_final += taxa
            print(f"Adicionando R${taxa:.2f} de Embalagem de Presente.")

        print(f"\nValor a Pagar: R${valor_final:.2f}")

        # 5. Processar pagamento
        sucesso = pedido.metodo_pagamento.processar(valor_final)

        if sucesso:
            self._registrar_pedido(pedido, valor_final)
            print("\nSUCESSO: Pedido finalizado e registrado.")
            self._emitir_nota_fiscal(valor_final)
            return True
        else:
            print("\nFALHA: Transação abortada.")
            return False

    def _registrar_pedido(self, pedido: Pedido, valor: float) -> None:
        """Registra o pedido no sistema (simulado)."""
        self._pedidos_processados.append((pedido, valor))
        print("Pedido registrado no sistema.")

    def _emitir_nota_fiscal(self, valor: float) -> None:
        """Emite nota fiscal (simulado)."""
        print(f"Emitindo nota fiscal no valor de R${valor:.2f}")