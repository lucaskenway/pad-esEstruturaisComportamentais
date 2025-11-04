## Disciplina: Engenharia de Software
## Contexto: Sistemas Legados e Manutenção de Software 

**Objetivo:** Aplicar Padrões de Projeto Estruturais e Comportamentais para refatorar um código monolítico, melhorando o acoplamento, a coesão e a aderência aos princípios SOLID, especificamente o SRP (Single Responsibility Principle) e o OCP (Open/Closed Principle).

**Cenário:** O Sistema de Processamento de Pedidos (LMPT)
Você recebeu o código-fonte de um módulo de processamento de pedidos (fornecido no arquivo checkout_monolitico.py). Esta classe, SistemaPedidoAntigo, encapsula todas as responsabilidades do checkout: cálculo de valor, aplicação de descontos, lógica de frete, e a própria finalização da transação.

## Análise do Código Legado (checkout_monolitico.py):

1. Baixa Coesão / Alto Acoplamento: A classe SistemaPedidoAntigo é uma "classe deus" que viola o SRP, centralizando diferentes lógicas (pagamento, frete, descontos).

2. Violação do OCP: Para adicionar um novo método de pagamento ou um novo tipo de frete, é necessário modificar diretamente os métodos processar_pagamento() ou calcular_frete(), introduzindo novos blocos elif.

3. Complexidade na Interação: O método finalizar_compra() expõe uma série de etapas complexas que deveriam ser simplificadas para o código cliente.

## Instruções: Refatoração e Aplicação de Padrões
Seu trabalho é criar um novo conjunto de classes, utilizando o repositório FlexOrder-DesignPatterns no GitHub, que substitua a funcionalidade da classe monolítica, aplicando os seguintes Padrões de Projeto para resolver os problemas identificados:

1. Padrão Comportamental: Strategy (Estratégia)
    - Problema a Resolver: A rigidez na escolha e execução do método de pagamento (processar_pagamento) e o cálculo de frete (calcular_frete).

    - **Implementação:**

        - Refatore as lógicas de pagamento e frete. Crie as interfaces abstratas (EstrategiaPagamento e EstrategiaFrete) e classes concretas para cada variação (ex: PagamentoPix, PagamentoCredito, FreteNormal, FreteExpresso).

        - Crie uma classe Pedido que atue como Contexto, mantendo referências às interfaces de Estratégia, permitindo que o comportamento de pagamento/frete seja trocado em tempo de execução via composição.

2. Padrão Estrutural: Decorator (Decorador)
    - Problema a Resolver: A lógica de descontos e a adição da taxa de embalagem de presente estão embutidas e exigem modificação de métodos existentes.

    - **Implementação:**

        - Defina uma interface base para o Pedido (ou um CálculoValor).

        - Implemente o DescontoPix e a TaxaEmbalagemPresente como Decorators Concretos. Eles devem envolver o objeto base do pedido, adicionando ou modificando o valor de forma dinâmica e em camadas, sem alterar a classe Pedido fundamental.

3. Padrão Estrutural: Facade (Fachada)
    - Problema a Resolver: Simplificar a orquestração do processo de checkout contido em finalizar_compra().

    - **Implementação:**

        - Crie classes separadas para subsistemas (ex: SistemaEstoque, GeradorNotaFiscal).

        - Implemente a classe CheckoutFacade. Esta Fachada deve fornecer uma interface de alto nível e simplificada (ex: concluir_transacao(pedido)) que orquestra as chamadas para as Estratégias (pagamento, frete) e os subsistemas, substituindo a complexidade do método legado.

## Requisitos de Entrega
1. Repositório GitHub: Crie um repositório público (FlexOrder-DesignPatterns).

2. Código Funcional: O código refatorado deve ser funcional e demonstrar o uso dos três padrões obrigatórios (Strategy, Decorator, Facade).

3. Documentação Técnica (README.md): O README.md deve conter:

     - Uma breve descrição da sua nova arquitetura orientada a objetos.

    - A explicação técnica de como e por que cada padrão foi utilizado para resolver os problemas do código legado, referenciando as violações de SRP/OCP corrigidas.


## Avaliação
A avaliação será focada na aderência correta aos princípios de cada Padrão, na clareza do código e na sua capacidade de demonstrar a flexibilidade e a manutenibilidade alcançadas pela refatoração.

# Ponto Extra
**O Aluno que entregar todos os Items corretamente terá 1 extra no bimestre corrente.**