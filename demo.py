#!/usr/bin/env python3
"""
Script de demonstração simples para a ordenação externa.
"""

import csv
import os
from mergesort_externo import OrdenacaoExterna

def criar_dados_exemplo():
    """Cria um arquivo CSV de exemplo para demonstração."""
    dados = [
        ['id', 'nome', 'idade', 'salario'],
        [3, 'Carlos Silva', 28, 5500.00],
        [1, 'Ana Santos', 25, 4800.00],
        [4, 'Bruno Costa', 32, 6200.00],
        [2, 'Diana Oliveira', 29, 5100.00],
        [5, 'Eduardo Lima', 26, 4900.00],
    ]
    
    with open('exemplo.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(dados)
    
    print("Arquivo exemplo.csv criado com os dados:")
    for linha in dados:
        print(f"  {linha}")

def demonstrar_ordenacao():
    """Demonstra o uso da ordenação externa."""
    print("\n=== DEMONSTRAÇÃO DE ORDENAÇÃO EXTERNA ===\n")
    
    # Criar dados de exemplo
    criar_dados_exemplo()
    
    # Criar instância do ordenador
    ordenador = OrdenacaoExterna(tamanho_buffer=2)  # Buffer pequeno para demonstração
    
    # Configurar coluna chave
    ordenador.coluna_chave_atual = "nome"
    
    print("\n1. Ordenando por nome (ascendente):")
    resultado1 = ordenador.ordenar_arquivo('exemplo.csv', 'nome', 'asc', 'exemplo_ordenado_nome.csv')
    
    print("\n2. Ordenando por idade (descendente):")
    ordenador.coluna_chave_atual = "idade"
    resultado2 = ordenador.ordenar_arquivo('exemplo.csv', 'idade', 'desc', 'exemplo_ordenado_idade.csv')
    
    # Mostrar resultados
    print("\n=== RESULTADOS ===")
    
    print(f"\nArquivo ordenado por nome:")
    with open(resultado1, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for linha in reader:
            print(f"  {linha}")
    
    print(f"\nArquivo ordenado por idade:")
    with open(resultado2, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for linha in reader:
            print(f"  {linha}")
    
    # Limpeza
    print("\n=== LIMPEZA ===")
    arquivos = ['exemplo.csv', 'exemplo_ordenado_nome.csv', 'exemplo_ordenado_idade.csv']
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            os.remove(arquivo)
            print(f"Arquivo {arquivo} removido")

if __name__ == "__main__":
    demonstrar_ordenacao() 