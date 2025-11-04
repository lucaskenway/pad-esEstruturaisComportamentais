class Cafe:
    def get_custo(self):
        raise NotImplementedError

    def get_descricao(self):
        raise NotImplementedError


class CafeSimples(Cafe):
    def get_custo(self):
        return 5.0

    def get_descricao(self):
        return "Café Simples"


class DecoradorCafe(Cafe):
    def __init__(self, cafe):
        self._cafe = cafe


class Leite(DecoradorCafe):
    def get_custo(self):
        return self._cafe.get_custo() + 2.0

    def get_descricao(self):
        return self._cafe.get_descricao() + ", com Leite"


class Acucar(DecoradorCafe):
    def get_custo(self):
        return self._cafe.get_custo() + 0.5

    def get_descricao(self):
        return self._cafe.get_descricao() + ", com Açúcar"


# Composição em cascata
meu_cafe = CafeSimples()
meu_cafe = Leite(meu_cafe)
meu_cafe = Acucar(meu_cafe)

print(f"{meu_cafe.get_descricao()}: R${meu_cafe.get_custo():.2f}")

# Saída: Café Simples, com Leite, com Açúcar: R$7.50