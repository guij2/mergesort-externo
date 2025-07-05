#!/usr/bin/env python3
"""
Arquivo de exemplo para testar a implementação do Merge Sort Externo.
Este script cria um arquivo CSV de teste e demonstra o uso da ordenação externa.
"""

import csv
import random
import os
from mergesort_externo import OrdenacaoExterna

def criar_arquivo_teste(nome_arquivo: str, num_registros: int = 5000):
    """
    Cria um arquivo CSV de teste com dados aleatórios.
    
    Args:
        nome_arquivo: Nome do arquivo CSV a ser criado
        num_registros: Número de registros a serem gerados
    """
    print(f"Criando arquivo de teste: {nome_arquivo} com {num_registros} registros")
    
    # Gerar dados aleatórios
    nomes = ["João", "Maria", "Pedro", "Ana", "Carlos", "Lucia", "Fernando", "Beatriz"]
    sobrenomes = ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira"]
    
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        
        # Escrever cabeçalho
        writer.writerow(['id', 'nome', 'idade', 'salario', 'departamento'])
        
        # Gerar registros
        for i in range(num_registros):
            id_registro = i + 1
            nome = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
            idade = random.randint(18, 65)
            salario = round(random.uniform(2000, 15000), 2)
            departamento = random.choice(['TI', 'RH', 'Vendas', 'Marketing', 'Financeiro'])
            
            writer.writerow([id_registro, nome, idade, salario, departamento])
    
    print(f"Arquivo {nome_arquivo} criado com sucesso!")

def testar_ordenacao_externa():
    """
    Testa a implementação da ordenação externa.
    """
    print("=== TESTE DE ORDENAÇÃO EXTERNA ===")
    
    # Criar arquivo de teste
    arquivo_teste = "dados_teste.csv"
    criar_arquivo_teste(arquivo_teste, 3000)
    
    # Criar instância do ordenador com buffer pequeno para simular limitação de memória
    ordenador = OrdenacaoExterna(tamanho_buffer=100)
    
    # Testar diferentes tipos de ordenação
    testes = [
        ("id", "asc", "dados_ordenados_por_id_asc.csv"),
        ("id", "desc", "dados_ordenados_por_id_desc.csv"),
        ("nome", "asc", "dados_ordenados_por_nome_asc.csv"),
        ("idade", "desc", "dados_ordenados_por_idade_desc.csv"),
        ("salario", "desc", "dados_ordenados_por_salario_desc.csv"),
    ]
    
    for coluna, ordem, arquivo_saida in testes:
        print(f"\n--- Testando ordenação por {coluna} ({ordem}) ---")
        try:
            # Configurar coluna chave
            ordenador.coluna_chave_atual = coluna
            
            # Executar ordenação
            resultado = ordenador.ordenar_arquivo(arquivo_teste, coluna, ordem, arquivo_saida)
            
            # Verificar resultado
            if os.path.exists(resultado):
                with open(resultado, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    cabecalho = next(reader)
                    primeiras_linhas = [next(reader) for _ in range(min(5, 3000))]
                    
                print(f"✓ Ordenação concluída: {resultado}")
                print(f"  Cabeçalho: {cabecalho}")
                print(f"  Primeiras 5 linhas:")
                for i, linha in enumerate(primeiras_linhas, 1):
                    print(f"    {i}: {linha}")
            else:
                print(f"✗ Erro: arquivo {resultado} não foi criado")
                
        except Exception as e:
            print(f"✗ Erro durante teste: {e}")
    
    # Limpeza
    print(f"\n--- Limpeza ---")
    arquivos_para_remover = [arquivo_teste] + [teste[2] for teste in testes]
    for arquivo in arquivos_para_remover:
        if os.path.exists(arquivo):
            os.remove(arquivo)
            print(f"Arquivo {arquivo} removido")

def verificar_ordenacao(arquivo: str, coluna: str, ordem: str):
    """
    Verifica se um arquivo está corretamente ordenado.
    
    Args:
        arquivo: Caminho do arquivo CSV
        coluna: Nome da coluna de ordenação
        ordem: 'asc' ou 'desc'
    """
    print(f"Verificando ordenação do arquivo {arquivo}...")
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        cabecalho = next(reader)
        
        try:
            indice_coluna = cabecalho.index(coluna)
        except ValueError:
            print(f"Coluna '{coluna}' não encontrada")
            return False
        
        linhas = list(reader)
        
        # Verificar ordenação
        for i in range(len(linhas) - 1):
            valor_atual = linhas[i][indice_coluna]
            valor_proximo = linhas[i + 1][indice_coluna]
            
            # Tentar conversão numérica
            try:
                valor_atual = float(valor_atual)
                valor_proximo = float(valor_proximo)
            except ValueError:
                pass  # Manter como string
            
            if ordem == 'asc':
                if valor_atual > valor_proximo:
                    print(f"✗ Erro na ordenação na linha {i+2}: {valor_atual} > {valor_proximo}")
                    return False
            else:  # desc
                if valor_atual < valor_proximo:
                    print(f"✗ Erro na ordenação na linha {i+2}: {valor_atual} < {valor_proximo}")
                    return False
        
        print(f"✓ Arquivo está corretamente ordenado por {coluna} ({ordem})")
        return True

if __name__ == "__main__":
    testar_ordenacao_externa() 