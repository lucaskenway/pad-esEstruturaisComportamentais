class NovaAPIEnvio:
    def enviar_dados(self, dados):
        raise NotImplementedError


class APIAntigaEnvio:
    def enviar_dados_legado(self, dados_antigos):
        print(f"Enviando: {dados_antigos}")


class AdaptadorEnvio(NovaAPIEnvio):
    def __init__(self, api_antiga):
        self._api_antiga = api_antiga

    def enviar_dados(self, dados):
        dados_antigos = f"LEGADO_{dados}"
        self._api_antiga.enviar_dados_legado(dados_antigos)


# Uso
api_antiga = APIAntigaEnvio()
adaptador = AdaptadorEnvio(api_antiga)
adaptador.enviar_dados("Dados novos")