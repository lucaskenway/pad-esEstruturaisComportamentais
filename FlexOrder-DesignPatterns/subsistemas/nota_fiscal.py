class GeradorNotaFiscal:
    """Subsistema responsável por emissão de nota fiscal (simulado)."""

    def emitir(self, pedido, valor: float) -> None:
        # Integração com serviço fiscal seria feita aqui.
        print(f"Emitindo nota fiscal para R${valor:.2f} (simulado).")
