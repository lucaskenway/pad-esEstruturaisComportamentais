# -*- coding: utf-8 -*-

"""
Este módulo exemplifica o uso do padrão de projeto Composite.

O padrão Composite permite que você componha objetos em estruturas de árvore
e, em seguida, trabalhe com essas estruturas como se fossem objetos individuais.
"""

from abc import ABC, abstractmethod


class ComponenteSistemaArquivos(ABC):
    """
    A interface Componente declara um método para executar uma operação.
    """

    @abstractmethod
    def exibir(self, nivel=0):
        """
        Define a operação que será implementada por todos os componentes.
        """
        pass


class Arquivo(ComponenteSistemaArquivos):
    """
    A classe Folha (Leaf) representa os objetos finais de uma composição.
    Uma folha não pode ter filhos.
    """

    def __init__(self, nome):
        """
        Inicializa o arquivo com um nome.
        """
        self.nome = nome

    def exibir(self, nivel=0):
        """
        Exibe o nome do arquivo com indentação para representar a hierarquia.
        """
        print("  " * nivel + f"Arquivo: {self.nome}")


class Pasta(ComponenteSistemaArquivos):
    """
    A classe Composite representa os componentes complexos que podem ter filhos.
    Normalmente, os objetos Composite delegam o trabalho real para seus filhos
    e, em seguida, "resumem" o resultado.
    """

    def __init__(self, nome):
        """
        Inicializa a pasta com um nome e uma lista de componentes filhos.
        """
        self.nome = nome
        self.componentes = []

    def adicionar(self, componente):
        """
        Adiciona um componente (arquivo ou pasta) a esta pasta.
        """
        self.componentes.append(componente)

    def exibir(self, nivel=0):
        """
        Exibe o nome da pasta e, em seguida, chama o método exibir de cada
        componente filho, aumentando o nível de indentação.
        """
        print("  " * nivel + f"Pasta: {self.nome}/")
        for componente in self.componentes:
            componente.exibir(nivel + 1)


# Criando a estrutura de arquivos e pastas
# A estrutura em árvore é criada:
# MeuDrive/
#   Documentos/
#     relatorio.pdf
raiz = Pasta("MeuDrive")
docs = Pasta("Documentos")
docs.adicionar(Arquivo("relatorio.pdf"))
raiz.adicionar(docs)

# Exibindo a estrutura de arquivos a partir da raiz
# O cliente não precisa saber se está interagindo com um arquivo ou uma pasta.
raiz.exibir()
