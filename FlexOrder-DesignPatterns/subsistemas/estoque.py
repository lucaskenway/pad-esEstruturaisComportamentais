class SistemaEstoque:
    """Subsistema responsável por operações de estoque (simulado).

    Não impõe tipos concretos para evitar dependências circulares.
    """

    def registrar_pedido(self, pedido) -> None:
        # Aqui poderíamos atualizar um banco de dados, reservar itens, etc.
        print("Pedido registrado no sistema de estoque (simulado).")
