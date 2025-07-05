import os
import csv
import tempfile
import shutil
from typing import List, Tuple, Union
import sys

class OrdenacaoExterna:
    """
    Classe para implementar ordenação externa usando Merge-Sort
    para arquivos CSV grandes que não cabem na memória RAM.
    """
    
    def __init__(self, tamanho_buffer: int = 1000):
        """
        Inicializa a classe de ordenação externa.
        
        Args:
            tamanho_buffer: Número máximo de registros que podem ser carregados
                          na memória por vez (simula o limite de RAM)
        """
        self.tamanho_buffer = tamanho_buffer
        self.arquivos_temporarios = []
        self.diretorio_temp = None
        self.coluna_chave_atual = None
    
    def ordenar_arquivo(self, nome_arquivo: str, coluna_chave: Union[str, int], 
                       ordem: str = 'asc', arquivo_saida: str = None) -> str:
        """
        Ordena um arquivo CSV usando ordenação externa.
        
        Args:
            nome_arquivo: Caminho para o arquivo CSV de entrada
            coluna_chave: Nome da coluna ou índice (0-based) da chave de ordenação
            ordem: 'asc' para ascendente ou 'desc' para descendente
            arquivo_saida: Nome do arquivo de saída (opcional)
            
        Returns:
            Caminho do arquivo ordenado
        """
        print(f"Iniciando ordenação externa do arquivo: {nome_arquivo}")
        print(f"Coluna chave: {coluna_chave}, Ordem: {ordem}")
        
        # Criar diretório temporário
        self.diretorio_temp = tempfile.mkdtemp(prefix="mergesort_")
        
        try:
            # Fase 1: Dividir o arquivo em runs ordenados
            runs = self._dividir_em_runs(nome_arquivo, coluna_chave, ordem)
            print(f"Arquivo dividido em {len(runs)} runs")
            
            # Fase 2: Merge externo dos runs
            arquivo_final = self._merge_externo(runs, coluna_chave, ordem)
            
            # Definir arquivo de saída
            if arquivo_saida is None:
                base_name = os.path.splitext(nome_arquivo)[0]
                arquivo_saida = f"{base_name}_ordenado.csv"
            
            # Mover arquivo final para destino
            shutil.move(arquivo_final, arquivo_saida)
            
            print(f"Ordenação concluída. Arquivo salvo em: {arquivo_saida}")
            return arquivo_saida
            
        finally:
            # Limpar arquivos temporários
            self._limpar_arquivos_temporarios()
    
    def _dividir_em_runs(self, nome_arquivo: str, coluna_chave: Union[str, int], 
                        ordem: str) -> List[str]:
        """
        Divide o arquivo original em runs menores ordenados.
        
        Args:
            nome_arquivo: Arquivo CSV original
            coluna_chave: Coluna de ordenação
            ordem: Ordem de classificação
            
        Returns:
            Lista com caminhos dos arquivos de runs
        """
        runs = []
        
        with open(nome_arquivo, 'r', encoding='utf-8', newline='') as arquivo:
            reader = csv.reader(arquivo)
            
            # Ler cabeçalho
            try:
                cabecalho = next(reader)
                print(f"Cabeçalho encontrado: {cabecalho}")
            except StopIteration:
                raise ValueError("Arquivo CSV está vazio")
            
            # Determinar índice da coluna chave
            if isinstance(coluna_chave, str):
                try:
                    indice_chave = cabecalho.index(coluna_chave)
                except ValueError:
                    raise ValueError(f"Coluna '{coluna_chave}' não encontrada no cabeçalho")
            else:
                indice_chave = coluna_chave
                if indice_chave >= len(cabecalho):
                    raise ValueError(f"Índice da coluna {indice_chave} está fora do intervalo")
            
            print(f"Usando coluna índice {indice_chave} como chave de ordenação")
            
            buffer = []
            run_numero = 0
            
            for linha in reader:
                if len(linha) <= indice_chave:
                    continue  # Pular linhas com dados insuficientes
                
                buffer.append(linha)
                
                # Quando o buffer está cheio, ordena e salva como run
                if len(buffer) >= self.tamanho_buffer:
                    run_arquivo = self._salvar_run(buffer, cabecalho, indice_chave, 
                                                 ordem, run_numero)
                    runs.append(run_arquivo)
                    buffer = []
                    run_numero += 1
            
            # Salvar último run se houver dados restantes
            if buffer:
                run_arquivo = self._salvar_run(buffer, cabecalho, indice_chave, 
                                             ordem, run_numero)
                runs.append(run_arquivo)
        
        return runs
    
    def _salvar_run(self, buffer: List[List[str]], cabecalho: List[str], 
                   indice_chave: int, ordem: str, run_numero: int) -> str:
        """
        Ordena um buffer de dados e salva como arquivo de run.
        
        Args:
            buffer: Lista de registros a serem ordenados
            cabecalho: Cabeçalho do CSV
            indice_chave: Índice da coluna chave
            ordem: Ordem de classificação
            run_numero: Número do run para nomenclatura
            
        Returns:
            Caminho do arquivo de run salvo
        """
        # Ordenar buffer usando merge sort interno
        buffer_ordenado = self._merge_sort_interno(buffer, indice_chave, ordem)
        
        # Salvar run ordenado
        if self.diretorio_temp is None:
            raise ValueError("Diretório temporário não foi criado")
        run_arquivo = os.path.join(self.diretorio_temp, f"run_{run_numero}.csv")
        
        with open(run_arquivo, 'w', encoding='utf-8', newline='') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(cabecalho)
            writer.writerows(buffer_ordenado)
        
        self.arquivos_temporarios.append(run_arquivo)
        return run_arquivo
    
    def _merge_sort_interno(self, dados: List[List[str]], indice_chave: int, 
                           ordem: str) -> List[List[str]]:
        """
        Implementa merge sort para dados em memória.
        
        Args:
            dados: Lista de registros
            indice_chave: Índice da coluna chave
            ordem: Ordem de classificação
            
        Returns:
            Lista ordenada de registros
        """
        if len(dados) <= 1:
            return dados
        
        meio = len(dados) // 2
        esquerda = self._merge_sort_interno(dados[:meio], indice_chave, ordem)
        direita = self._merge_sort_interno(dados[meio:], indice_chave, ordem)
        
        return self._merge_interno(esquerda, direita, indice_chave, ordem)
    
    def _merge_interno(self, esquerda: List[List[str]], direita: List[List[str]], 
                      indice_chave: int, ordem: str) -> List[List[str]]:
        """
        Faz o merge de duas listas ordenadas.
        
        Args:
            esquerda: Lista ordenada da esquerda
            direita: Lista ordenada da direita
            indice_chave: Índice da coluna chave
            ordem: Ordem de classificação
            
        Returns:
            Lista mesclada e ordenada
        """
        resultado = []
        i = j = 0
        
        while i < len(esquerda) and j < len(direita):
            if self._comparar_registros(esquerda[i], direita[j], indice_chave, ordem):
                resultado.append(esquerda[i])
                i += 1
            else:
                resultado.append(direita[j])
                j += 1
        
        # Adicionar elementos restantes
        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])
        
        return resultado
    
    def _merge_externo(self, runs: List[str], coluna_chave: Union[str, int], 
                      ordem: str) -> str:
        """
        Realiza o merge externo dos runs ordenados.
        
        Args:
            runs: Lista de arquivos de runs
            coluna_chave: Coluna de ordenação
            ordem: Ordem de classificação
            
        Returns:
            Caminho do arquivo final ordenado
        """
        while len(runs) > 1:
            novos_runs = []
            
            # Processar runs em pares
            for i in range(0, len(runs), 2):
                if i + 1 < len(runs):
                    # Merge de dois runs
                    run_mesclado = self._merge_dois_runs(runs[i], runs[i + 1], ordem)
                    novos_runs.append(run_mesclado)
                else:
                    # Run ímpar - apenas renomear
                    novos_runs.append(runs[i])
            
            runs = novos_runs
            print(f"Merge externo: {len(runs)} runs restantes")
        
        return runs[0]
    
    def _merge_dois_runs(self, run1: str, run2: str, ordem: str) -> str:
        """
        Faz o merge de dois arquivos de runs.
        
        Args:
            run1: Caminho do primeiro run
            run2: Caminho do segundo run
            ordem: Ordem de classificação
            
        Returns:
            Caminho do arquivo mesclado
        """
        if self.diretorio_temp is None:
            raise ValueError("Diretório temporário não foi criado")
        arquivo_mesclado = os.path.join(self.diretorio_temp, 
                                       f"merged_{len(self.arquivos_temporarios)}.csv")
        
        with open(run1, 'r', encoding='utf-8', newline='') as f1, \
             open(run2, 'r', encoding='utf-8', newline='') as f2, \
             open(arquivo_mesclado, 'w', encoding='utf-8', newline='') as saida:
            
            reader1 = csv.reader(f1)
            reader2 = csv.reader(f2)
            writer = csv.writer(saida)
            
            # Ler cabeçalhos
            cabecalho1 = next(reader1)
            cabecalho2 = next(reader2)
            writer.writerow(cabecalho1)  # Assumindo que são iguais
            
            # Determinar índice da coluna chave
            coluna_chave = self._get_coluna_chave()
            if isinstance(coluna_chave, str):
                indice_chave = cabecalho1.index(coluna_chave)
            else:
                indice_chave = coluna_chave if coluna_chave is not None else 0
            
            # Ler primeira linha de cada arquivo
            try:
                linha1 = next(reader1)
                tem_linha1 = True
            except StopIteration:
                tem_linha1 = False
                linha1 = []
            
            try:
                linha2 = next(reader2)
                tem_linha2 = True
            except StopIteration:
                tem_linha2 = False
                linha2 = []
            
            # Merge das linhas
            while tem_linha1 and tem_linha2:
                if self._comparar_registros(linha1, linha2, indice_chave, ordem):
                    writer.writerow(linha1)
                    try:
                        linha1 = next(reader1)
                    except StopIteration:
                        tem_linha1 = False
                else:
                    writer.writerow(linha2)
                    try:
                        linha2 = next(reader2)
                    except StopIteration:
                        tem_linha2 = False
            
            # Escrever linhas restantes
            if tem_linha1:
                writer.writerow(linha1)
                writer.writerows(reader1)
            
            if tem_linha2:
                writer.writerow(linha2)
                writer.writerows(reader2)
        
        self.arquivos_temporarios.append(arquivo_mesclado)
        return arquivo_mesclado
    
    def _comparar_registros(self, reg1: List[str], reg2: List[str], 
                           indice_chave: int, ordem: str) -> bool:
        """
        Compara dois registros baseado na chave de ordenação.
        
        Args:
            reg1: Primeiro registro
            reg2: Segundo registro
            indice_chave: Índice da coluna chave
            ordem: Ordem de classificação
            
        Returns:
            True se reg1 deve vir antes de reg2
        """
        if indice_chave >= len(reg1) or indice_chave >= len(reg2):
            return False
        
        chave1 = reg1[indice_chave]
        chave2 = reg2[indice_chave]
        
        # Tentar conversão numérica
        try:
            chave1_num = float(chave1)
            chave2_num = float(chave2)
            comparacao = chave1_num <= chave2_num
        except ValueError:
            # Comparação como string
            comparacao = chave1 <= chave2
        
        return comparacao if ordem == 'asc' else not comparacao
    
    def _get_coluna_chave(self):
        """Método auxiliar para obter a coluna chave (usado no merge externo)"""
        return self.coluna_chave_atual
    
    def _limpar_arquivos_temporarios(self):
        """Remove todos os arquivos temporários criados durante o processo."""
        if self.diretorio_temp and os.path.exists(self.diretorio_temp):
            shutil.rmtree(self.diretorio_temp)
            print("Arquivos temporários removidos")


def main():
    """Função principal para demonstrar o uso da ordenação externa."""
    
    # Criar instância da classe
    ordenador = OrdenacaoExterna(tamanho_buffer=1000)  # Buffer de 1000 registros
    
    # Exemplo de uso
    if len(sys.argv) < 3:
        print("Uso: python mergesort_externo.py <arquivo_csv> <coluna_chave> [ordem] [arquivo_saida]")
        print("Exemplo: python mergesort_externo.py dados.csv nome asc dados_ordenados.csv")
        return
    
    arquivo_entrada = sys.argv[1]
    coluna_chave = sys.argv[2]
    ordem = sys.argv[3] if len(sys.argv) > 3 else 'asc'
    arquivo_saida = sys.argv[4] if len(sys.argv) > 4 else None
    
    # Tentar converter coluna_chave para inteiro se possível
    try:
        coluna_chave = int(coluna_chave)
    except ValueError:
        pass  # Manter como string
    
    try:
        # Guardar coluna chave para uso no merge externo
        ordenador.coluna_chave_atual = coluna_chave
        
        # Executar ordenação
        resultado = ordenador.ordenar_arquivo(arquivo_entrada, coluna_chave, ordem, arquivo_saida)
        print(f"Sucesso! Arquivo ordenado salvo em: {resultado}")
        
    except Exception as e:
        print(f"Erro durante a ordenação: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 