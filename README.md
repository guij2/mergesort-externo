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

## Uso

### Uso Básico via Linha de Comando

```bash
python mergesort_externo.py <arquivo_csv> <coluna_chave> [ordem] [arquivo_saida]
```

**Parâmetros:**
- `arquivo_csv`: Caminho para o arquivo CSV a ser ordenado
- `coluna_chave`: Nome da coluna ou índice (0-based) para ordenação
- `ordem`: 'asc' para ascendente ou 'desc' para descendente (padrão: 'asc')
- `arquivo_saida`: Nome do arquivo de saída (opcional)

**Exemplos:**
```bash
# Ordenar por nome em ordem ascendente
python mergesort_externo.py dados.csv nome asc dados_ordenados.csv

# Ordenar por idade em ordem descendente
python mergesort_externo.py dados.csv idade desc

# Ordenar pela primeira coluna (índice 0)
python mergesort_externo.py dados.csv 0 asc
```

### Uso Programático

```python
from mergesort_externo import OrdenacaoExterna

# Criar instância com buffer de 1000 registros
ordenador = OrdenacaoExterna(tamanho_buffer=1000)

# Configurar coluna chave
ordenador.coluna_chave_atual = "nome"

# Ordenar arquivo
resultado = ordenador.ordenar_arquivo(
    nome_arquivo="dados.csv",
    coluna_chave="nome",
    ordem="asc",
    arquivo_saida="dados_ordenados.csv"
)

print(f"Arquivo ordenado salvo em: {resultado}")
```

## Teste

Para testar a implementação, execute:

```bash
python exemplo_teste.py
```

Este script irá:
1. Criar um arquivo CSV de teste com 3000 registros
2. Testar ordenação por diferentes colunas
3. Verificar se os resultados estão corretos
4. Limpar os arquivos temporários

## Características Técnicas

### Complexidade
- **Tempo**: O(n log n) onde n é o número de registros
- **Espaço**: O(B) onde B é o tamanho do buffer em memória

### Estruturas de Dados Utilizadas
- **Listas**: Para armazenar registros no buffer
- **Arquivos temporários**: Para armazenar runs ordenados
- **Readers/Writers CSV**: Para manipulação eficiente de arquivos

### Parâmetros Configuráveis
- **tamanho_buffer**: Controla quantos registros são processados por vez na memória
- **coluna_chave**: Define qual coluna será usada para ordenação
- **ordem**: Ascendente ou descendente

## Vantagens

1. **Escalabilidade**: Pode processar arquivos maiores que a RAM disponível
2. **Eficiência**: Usa o algoritmo Merge Sort, que é estável e eficiente
3. **Flexibilidade**: Permite ordenação por qualquer coluna
4. **Robustez**: Trata diferentes tipos de dados (numéricos e texto)

## Limitações

1. **Espaço em disco**: Requer espaço adicional para arquivos temporários
2. **I/O intensivo**: Muitas operações de leitura/escrita em disco
3. **Dependência de memória**: O tamanho do buffer afeta a performance

## Exemplo de Arquivo CSV

```csv
id,nome,idade,salario,departamento
1,João Silva,25,5000.00,TI
2,Maria Santos,30,6500.00,RH
3,Pedro Oliveira,28,5500.00,Vendas
```

## Requisitos

- Python 3.6 ou superior
- Módulos padrão: `csv`, `os`, `tempfile`, `shutil`, `typing`, `sys`

## Observações

- O algoritmo preserva a estabilidade da ordenação
- Arquivos temporários são criados em diretório temporário do sistema
- Limpeza automática dos arquivos temporários após conclusão
- Suporte a ordenação tanto numérica quanto alfabética
- Tratamento de erros para arquivos malformados