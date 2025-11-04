"""
CÓDIGO LEGADO - Sistema de Pedidos Monolítico (LMPT)
 Este código apresenta diversos problemas de design
 NÃO use este código - serve apenas para comparação

PROBLEMAS IDENTIFICADOS:
1. Baixa Coesão / Alto Acoplamento
2. Violação do SRP (Single Responsibility Principle)
3. Violação do OCP (Open/Closed Principle)
4. Complexidade Excessiva
"""


class SistemaPedidoAntigo:
    """
    CLASSE "DEUS" - Viola múltiplos princípios SOLID
    Esta classe centraliza TODAS as responsabilidades do sistema
    """
    
    def __init__(self, itens, valor_base):
        self.itens = itens
        self.valor_base = valor_base
        self.valor_total = valor_base
        self.metodo_pagamento = None
        self.tipo_frete = None
        self.tem_embalagem_presente = False
        self.estoque = {}  # Simula banco de dados
        
    def processar_pagamento(self, metodo):
        """
         VIOLAÇÃO DO OCP: Para adicionar novo método de pagamento,
        é necessário MODIFICAR este método (adicionar novo elif)
        """
        self.metodo_pagamento = metodo
        
        if metodo == "pix":
            print(f"Processando pagamento PIX de R$ {self.valor_total:.2f}")
            print("Gerando QR Code...")
            # Lógica específica do PIX
            return True
            
        elif metodo == "credito":
            print(f"Processando pagamento via Crédito de R$ {self.valor_total:.2f}")
            print("Validando cartão...")
            # Lógica específica do Crédito
            return True
            
        elif metodo == "boleto":
            print(f"Gerando boleto de R$ {self.valor_total:.2f}")
            print("Código de barras: 34191.79001...")
            # Lógica específica do Boleto
            return True
            
        elif metodo == "debito":
            print(f"Processando débito de R$ {self.valor_total:.2f}")
            # Lógica específica do Débito
            return True
        
        #  Para adicionar PayPal, teria que adicionar OUTRO elif aqui!
        # elif metodo == "paypal":
        #     ...
        
        else:
            print("Método de pagamento inválido!")
            return False
    
    def calcular_frete(self, tipo):
        """
        VIOLAÇÃO DO OCP: Para adicionar novo tipo de frete,
        é necessário MODIFICAR este método
        """
        self.tipo_frete = tipo
        
        if tipo == "normal":
            if self.valor_base > 200:
                frete = 0.0  # Frete grátis
            else:
                frete = 15.0
            print(f"Frete Normal: R$ {frete:.2f} (5-7 dias úteis)")
            
        elif tipo == "expresso":
            if self.valor_base > 500:
                frete = 20.0
            else:
                frete = 35.0
            print(f"Frete Expresso: R$ {frete:.2f} (1-2 dias úteis)")
            
        elif tipo == "retirada":
            frete = 0.0
            print("Retirada na loja (sem custo)")
        
        #  Para adicionar frete SEDEX, teria que adicionar OUTRO elif!
        # elif tipo == "sedex":
        #     ...
        
        else:
            print("Tipo de frete inválido!")
            frete = 0.0
        
        self.valor_total += frete
        return frete
    
    def aplicar_desconto(self, tipo_desconto):
        """
         VIOLAÇÃO DO SRP: Esta classe não deveria conhecer
        todos os tipos de desconto
         Modifica diretamente o valor_total (sem rastreabilidade)
        """
        if tipo_desconto == "pix":
            desconto = self.valor_total * 0.05
            self.valor_total -= desconto
            print(f"Desconto PIX aplicado: -R$ {desconto:.2f}")
            
        elif tipo_desconto == "primeira_compra":
            desconto = 50.0
            self.valor_total -= desconto
            print(f"Desconto primeira compra: -R$ {desconto:.2f}")
            
        elif tipo_desconto == "cupom_verao":
            desconto = self.valor_total * 0.10
            self.valor_total -= desconto
            print(f"Cupom de verão: -R$ {desconto:.2f}")
        
        #  Para novo desconto, modificar este método!
    
    def adicionar_embalagem_presente(self):
        """
         Modifica estado interno diretamente
         Sem possibilidade de "empilhar" múltiplas taxas
        """
        self.tem_embalagem_presente = True
        taxa = 10.0
        self.valor_total += taxa
        print(f"Taxa de embalagem para presente: +R$ {taxa:.2f}")
    
    def verificar_estoque(self):
        """
         VIOLAÇÃO DO SRP: Sistema de pedidos não deveria
        gerenciar estoque diretamente
        """
        print("Verificando estoque...")
        for item in self.itens:
            # Simula verificação de estoque
            print(f"  - {item['nome']}: Disponível")
        return True
    
    def reservar_itens(self):
        """
         VIOLAÇÃO DO SRP: Responsabilidade de estoque
        """
        print("Reservando itens...")
        for item in self.itens:
            print(f"  - {item['nome']}: Reservado")
        return True
    
    def baixar_estoque(self):
        """
         VIOLAÇÃO DO SRP: Responsabilidade de estoque
        """
        print("Baixando estoque...")
        return True
    
    def gerar_nota_fiscal(self, numero_pedido):
        """
         VIOLAÇÃO DO SRP: Sistema de pedidos não deveria
        gerar notas fiscais
        """
        print(f"Gerando Nota Fiscal para pedido #{numero_pedido}...")
        nota = f"NF-e: {numero_pedido}-2024"
        print(f"Nota Fiscal gerada: {nota}")
        return nota
    
    def enviar_email_confirmacao(self, email, numero_pedido):
        """
         VIOLAÇÃO DO SRP: Sistema de pedidos não deveria
        enviar e-mails
        """
        print(f"Enviando e-mail de confirmação para {email}...")
        print(f"Pedido #{numero_pedido} confirmado!")
        return True
    
    def finalizar_compra(self, metodo_pagamento, tipo_frete, email_cliente):
        """
         MÉTODO GIGANTE - Violação do SRP
         Alta Complexidade Ciclomática
         Cliente precisa conhecer TODA a sequência de operações
         Ordem errada = erro difícil de debugar
        """
        print("=" * 60)
        print("INICIANDO PROCESSO DE CHECKOUT (SISTEMA LEGADO)")
        print("=" * 60)
        
        # Passo 1: Verificar estoque
        if not self.verificar_estoque():
            print("ERRO: Itens indisponíveis!")
            return False
        
        # Passo 2: Reservar itens
        if not self.reservar_itens():
            print("ERRO: Falha ao reservar itens!")
            return False
        
        # Passo 3: Calcular frete
        self.calcular_frete(tipo_frete)
        
        # Passo 4: Aplicar descontos (lógica embutida)
        if metodo_pagamento == "pix":
            self.aplicar_desconto("pix")
        
        # Passo 5: Taxa de embalagem (se necessário)
        # self.adicionar_embalagem_presente()  # Comentado no exemplo
        
        # Passo 6: Processar pagamento
        print("\nProcessando pagamento...")
        if not self.processar_pagamento(metodo_pagamento):
            print("ERRO: Falha no pagamento!")
            return False
        
        # Passo 7: Baixar estoque
        self.baixar_estoque()
        
        # Passo 8: Gerar nota fiscal
        numero_pedido = "PED1000"  # Simulado
        self.gerar_nota_fiscal(numero_pedido)
        
        # Passo 9: Enviar confirmação
        self.enviar_email_confirmacao(email_cliente, numero_pedido)
        
        print("\n" + "=" * 60)
        print(f"COMPRA FINALIZADA! Valor total: R$ {self.valor_total:.2f}")
        print("=" * 60)
        
        return True


# ============================================================================
# EXEMPLO DE USO DO CÓDIGO LEGADO
# ============================================================================

def exemplo_codigo_legado():
    """
    Demonstra os problemas do código legado
    """
    print("\n" + "█" * 60)
    print("EXEMPLO: USO DO SISTEMA LEGADO")
    print("█" * 60)
    
    # Cliente precisa conhecer MUITOS detalhes internos
    itens = [
        {"nome": "Notebook", "quantidade": 1, "preco": 2500.00},
        {"nome": "Mouse", "quantidade": 2, "preco": 50.00}
    ]
    valor_base = 2600.00
    
    # Cria o sistema monolítico
    sistema = SistemaPedidoAntigo(itens, valor_base)
    
    # Cliente precisa chamar finalizar_compra conhecendo:
    # - Método de pagamento
    # - Tipo de frete
    # - E-mail
    # E AINDA assim, muita lógica fica escondida/acoplada
    resultado = sistema.finalizar_compra(
        metodo_pagamento="pix",
        tipo_frete="normal",
        email_cliente="cliente@email.com"
    )
    
    return resultado


# ============================================================================
# PROBLEMAS DEMONSTRADOS
# ============================================================================

def demonstrar_problemas():
    """
    Demonstra os problemas específicos do código legado
    """
    print("\n" + "▼" * 60)
    print("DEMONSTRAÇÃO DOS PROBLEMAS DO CÓDIGO LEGADO")
    print("▼" * 60)
    
    sistema = SistemaPedidoAntigo(
        [{"nome": "Produto", "quantidade": 1, "preco": 100.0}],
        100.0
    )
    
    print("\n PROBLEMA 1: Violação do OCP")
    print("-" * 40)
    print("Para adicionar 'PayPal', preciso MODIFICAR processar_pagamento()")
    print("Código atual:")
    print("""
    def processar_pagamento(self, metodo):
        if metodo == "pix":
            ...
        elif metodo == "credito":
            ...
        #  PRECISO ADICIONAR AQUI:
        # elif metodo == "paypal":
        #     ...
    """)
    
    print("\n PROBLEMA 2: Violação do SRP")
    print("-" * 40)
    print("SistemaPedidoAntigo tem MÚLTIPLAS responsabilidades:")
    print("  1. Gerenciar pagamento")
    print("  2. Calcular frete")
    print("  3. Aplicar descontos")
    print("  4. Gerenciar estoque")
    print("  5. Gerar nota fiscal")
    print("  6. Enviar e-mails")
    print("  7. Orquestrar todo o processo")
    
    print("\n PROBLEMA 3: Alta Complexidade")
    print("-" * 40)
    print("Método finalizar_compra() tem:")
    print("  - 9 passos sequenciais")
    print("  - Múltiplos pontos de falha")
    print("  - Lógica de negócio espalhada")
    print("  - Difícil de testar isoladamente")
    
    print("\n PROBLEMA 4: Baixa Flexibilidade")
    print("-" * 40)
    print("Impossível:")
    print("  - Combinar múltiplos descontos dinamicamente")
    print("  - Trocar estratégia de pagamento em runtime")
    print("  - Adicionar novo comportamento sem modificar código")
    
    print("\n" + "▲" * 60)


if __name__ == "__main__":
    # Executa exemplo do código legado
    exemplo_codigo_legado()
    
    print("\n\n")
    
    # Demonstra problemas específicos
    demonstrar_problemas()
    
    print("\n\n")
    print("=" * 60)
    print(" SOLUÇÃO: Ver flexorder_refactored.py")
    print("=" * 60)
    print("O código refatorado resolve TODOS estes problemas usando:")
    print("  ✓ Strategy Pattern (pagamento e frete)")
    print("  ✓ Decorator Pattern (descontos e taxas)")
    print("  ✓ Facade Pattern (simplificação do checkout)")
    print("=" * 60)