# Ordenação Externa com Merge Sort

Este projeto implementa um algoritmo de **ordenação externa** baseado no **Merge Sort** para ordenar arquivos CSV grandes que não cabem na memória RAM.

## Descrição

A ordenação externa é uma técnica utilizada para ordenar dados que são muito grandes para serem carregados completamente na memória principal. O algoritmo implementado utiliza o conceito de "divisão e conquista" do Merge Sort, mas adaptado para trabalhar com arquivos em disco.

## Funcionamento

O algoritmo funciona em duas fases principais:

### Fase 1: Divisão em Runs
1. O arquivo original é dividido em pequenos blocos (runs) que cabem na memória
2. Cada run é carregado na memória, ordenado usando Merge Sort interno
3. Cada run ordenado é salvo como um arquivo temporário

### Fase 2: Merge Externo
1. Os runs ordenados são mesclados par a par
2. O processo continua até que reste apenas um arquivo final ordenado
3. Os arquivos temporários são removidos

## Estrutura do Projeto

```
mergesort/
├── mergesort_externo.py    # Implementação principal
├── exemplo_teste.py        # Arquivo de teste e demonstração
├── README.md              # Este arquivo
└── orientação.md          # Especificações do trabalho
```


## Requisitos

- Python 3.6 ou superior
- Módulos padrão: `csv`, `os`, `tempfile`, `shutil`, `typing`, `sys`
