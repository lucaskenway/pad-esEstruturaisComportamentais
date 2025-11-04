"""
Implementações das estratégias de pagamento.
"""
from .pedido import MetodoPagamento


class PagamentoCredito(MetodoPagamento):
    """Pagamento via cartão de crédito com limite de R$1000."""
    
    def processar(self, valor: float) -> bool:
        print(f"Processando R${valor:.2f} via Cartão de Crédito...")
        if valor < 1000:
            print("   -> Pagamento com Crédito APROVADO.")
            return True
        else:
            print("   -> Pagamento com Crédito REJEITADO (limite excedido).")
            return False


class PagamentoPix(MetodoPagamento):
    """Pagamento via PIX (sempre aprovado)."""
    
    def processar(self, valor: float) -> bool:
        print(f"Processando R${valor:.2f} via PIX...")
        print("   -> Pagamento com PIX APROVADO (QR Code gerado).")
        return True


class PagamentoMana(MetodoPagamento):
    """Pagamento via transferência de Mana (sempre aprovado)."""
    
    def processar(self, valor: float) -> bool:
        print(f"Processando R${valor:.2f} via Transferência de Mana...")
        print("   -> Pagamento com Mana APROVADO (requer 10 segundos de espera).")
        return True