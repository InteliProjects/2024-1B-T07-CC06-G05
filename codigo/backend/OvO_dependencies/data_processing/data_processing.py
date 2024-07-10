"""
Módulo para tratamento, processamento e clusterização dos dados para sequenciamento de rotas na aplicação pelos algoritmos.
"""
from os import remove, mkdir
from os.path import exists
import pandas as pd
import re as regex
from custom_exceptions.custom_exception import CustomException
from typing import IO
from sklearn.cluster import KMeans
from numpy import unique
import numpy as np
from math import ceil
import random
generated_files = []


def IO_as_dataframe(file : IO, sep : str = ",") -> pd.DataFrame:
    """
    Recebe um objeto de arquivo CSV e retorna um pandas DataFrame correspondente.

    Parâmetros:
    - file: IO -> objeto de arquivo CSV.
    - sep: str -> separador (por padrão, vírgula ",")

    Retorno:
    - pandas DataFrame correspondente ao parâmetro.
    """
    try:
        df = pd.read_csv(file, sep=sep, index_col=False)
        return df
    except Exception as e:
        raise CustomException("Formato de arquivo inválido (impossível converter para CSV).") from e


def df_to_IO(df : pd.DataFrame, tmp_file_name : str) -> IO:
    """
    Recebe um pandas DataFrame e retorna um objeto
    de arquivo CSV correspondente.

    Parâmetros:
    - df: pandas.DataFrame -> pandas DataFrame.
    - tmp_file_name: str -> nome do arquivo temporário a ser gerado.

    Retorno:
    - objeto de arquivo CSV correspondente ao parâmetro.
    """
    global generated_files
    try:
        if not exists("./data"): mkdir("./data")
        generated_files.append(tmp_file_name)
        tmp = open(f"./data/{tmp_file_name}", "a+")
        tmp.write(df.to_csv(index=False, lineterminator="\n"))
        tmp.seek(0)

        return tmp
    except Exception as e:
        raise CustomException(f"Erro ao escrever dados no arquivo temporário ({tmp_file_name})") from e


def write_to_tmp_file(data : IO) -> str:
    """Cria um arquivo CSV temporário, o fecha e retorna o nome do arquivo."""
    global generated_files
    try:
        data.seek(0)
        tmp_file_name = "tmp.csv"
        tmp = open(f"./data/{tmp_file_name}", "w")
        tmp.write(data.read())
        tmp.close()
        generated_files.append(tmp_file_name)
        return tmp_file_name
    except Exception as e:
        raise CustomException("Erro ao criar de um arquivo CSV temporário com os dados") from e

def remove_generated_files():
    """Remove os arquivos temporários gerados no processamento."""
    global generated_files
    try:
        while (len(generated_files) > 0):
            remove(f"./data/{generated_files.pop()}")
    except Exception as e:
        raise CustomException("Erro ao apagar os arquivos temporários criados") from e

def prepare_initial_data(file : IO) -> IO:
    """
    Recebe um arquivo CSV dos dados enviados pelo parceiro de
    projeto salvo em memória (objeto de arquivo) para processar
    e retornar um novo objeto de arquivo com os dados iniciais
    tratados e conservados ao máximo.

    Parâmetros:
    - file: IO -> objeto de arquivo CSV dos dados do parceiro de projeto.

    Retorno:
    - objeto de arquivo CSV aberto (necessário fechar ao fim do manuseio)
    contendo os dados tratados e conservados.
    """
    try:
        df = _client_IO_as_dataframe(file)
    
        _initial_data_pipeline(df)

        return df_to_IO(df, "initial.csv")
    except:
        raise # Exceções específicas tratadas nas funções acima chamadas


def prepare_algorithm_data(file : IO, days : int, leituristas: int) -> IO:
    """
    Recebe um arquivo CSV dos dados enviados pelo parceiro de
    projeto salvo em memória (objeto de arquivo) para processar
    e retornar um novo objeto de arquivo com os dados iniciais
    tratados e otimizados para utilização como input para o
    algoritmo desenvolvido.

    Parâmetros:
    - file: IO -> objeto de arquivo CSV dos dados do parceiro de projeto.
    - days: int -> restrição de máximo de dias para realizar todas as leituras.
    Usada na clusterização.
    - leituristas: int -> restrição de máximo de leituristas. Usada na clusterização.

    Retorno:
    - objeto de arquivo CSV aberto (necessário fechar ao fim do manuseio)
    contendo os dados tratados e otimizados.
    """
    try:
        df = _client_IO_as_dataframe(file)

        df = _algorithm_data_pipeline(df, days, leituristas)

        return df_to_IO(df, "algdata.csv")
    except:
        raise # Exceções específicas tratadas nas funções acima chamadas

def merge_data(initial : pd.DataFrame, algorithm_response : pd.DataFrame) -> list[dict[str,]]:
    """
    Função responsável por juntar os dados tratados e conservados
    e o output do algoritmo desenvolvido.

    Parâmetros:
    - initial: pandas.DataFrame -> pandas DataFrame dos dados tratados e conservados.
    - algorithm_response: pandas.DataFrame -> pandas DataFrame do output do algoritmo utilizado.

    Retorno:
    - lista de objetos contendo os dados mergeados : list[dict[str, Any]]
    """
    try:
        # Realiza a junção dos DataFrames utilizando as colunas especificadas
        merged_df = initial.merge(algorithm_response, "inner", ["LOGRADOURO", "NUMERO"]).sort_values(["SEQUENCIA"])
    
        result = []
        for i in range(len(merged_df)):
            result.append({"INDICE" : int(merged_df.INDICE.iloc[i]), "LOGRADOURO" : merged_df.LOGRADOURO.iloc[i], "NUMERO" : int(merged_df.NUMERO.iloc[i]), "SEQUENCIA" : int(merged_df.SEQUENCIA.iloc[i]), "LATITUDE" : merged_df.LATITUDE.iloc[i], "LONGITUDE" : merged_df.LONGITUDE.iloc[i]})

        return result
      
    except Exception as e:
        raise CustomException("Erro ao gerar os dados de saída") from e


def _client_IO_as_dataframe(file : IO) -> pd.DataFrame:
    """
    Recebe um objeto de arquivo CSV no formato dos dados enviados pelo cliente
    e retorna um pandas DataFrame correspondente.

    Parâmetros:
    - file: IO -> objeto de arquivo CSV.

    Retorno:
    - pandas DataFrame correspondente ao parâmetro.
    """
    try:
        df = pd.read_csv(file, sep=";", index_col=False)
        if _is_invalid_format(df):
            raise CustomException("Arquivo CSV inválido (não contém as colunas necessárias).")
        return df
    except Exception as e:
        match e:
            case CustomException():
                raise
            case Exception():
                raise Exception("Formato de arquivo inválido (impossível converter para CSV).") from e


def _is_invalid_format(df : pd.DataFrame) -> bool:
    """
    Recebe um um pandas DataFrame e verifica se está
    no formato dos dados do parceiro de projeto, retornando
    um booleano de acordo com o resultado da verificação.

    Parâmetros:
    - df: pandas.DataFrame -> pandas DataFrame.

    Retorno:
    - True se estiver na estrutura correta, False caso contrário.
    """
    try:
        cols = df.columns
        expected = ["INDICE", "LATITUDE", "LONGITUDE", "CODIGO_ROTA", "SEQUENCIA", "LOGRADOURO", "NUMERO"]
        if len(cols.intersection(expected)) < len(expected):
            return True

        return False
    except Exception as e:
        raise CustomException("Erro ao validar a estrutura dos dados (colunas)") from e


def _common_pipeline(df : pd.DataFrame) -> None:
    """
    Recebe um pandas DataFrame e executa a pipeline comum
    entre o tratamento dos dados iniciais e o tratamento
    dos dados para execução do algoritmo desenvolvido.

    Parâmetros:
    - df: pandas.DataFrame -> pandas DataFrame.

    Retorno:
    - None.
    """
    try:
        _drop_unnecessary_cols(df)

        _fill_null_vals(df)

        _clean_number_column(df)

        _convert_float_cols_to_int(df)
    except Exception as e:
        raise # Exceções específicas tratadas nas funções acima chamadas

def _initial_data_pipeline(df : pd.DataFrame) -> None:
    """
    Recebe um pandas DataFrame e executa a pipeline
    específica de tratamento dos dados iniciais.

    Parâmetros:
    - df: pandas.DataFrame -> pandas DataFrame.

    Retorno:
    - None.
    """
    try:
        _common_pipeline(df)

        _drop_coordinates_cols(df)
    except Exception as e:
        raise # Exceções específicas tratadas nas funções acima chamadas


def _algorithm_data_pipeline(df : pd.DataFrame, days : int, leituristas: int) -> pd.DataFrame:
    """
    Recebe um pandas DataFrame e executa a pipeline 
    específica de tratamento dos dados para execução
    do algoritmo desenvolvido.

    Parâmetros:
    - df: pandas.DataFrame -> pandas DataFrame.
    - days: int -> máximo de dias para realização das leituras.
    Usado na clusterização.
    - leituristas: int -> máximo de leituristas. Usado na clusterização.

    Retorno:
    - pandas DataFrame processado pela pipeline : pandas.DataFrame.
    """
    try:
        _common_pipeline(df)

        _drop_indice_col(df)

        df = _add_hydrometer_count_col(df)

        _clusterize(df, days, leituristas)

        return df
    except Exception as e:
        raise # Exceções específicas tratadas nas funções acima chamadas


def _drop_unnecessary_cols(df : pd.DataFrame) -> None:
    """
    Recebe um pandas DataFrame e descarta as
    colunas irrelevantes para a solução do problema
    (CODIGO_ROTA e SEQUENCIA, que terão seus valores
    atribuídos na execução do algoritmo e, por isso, são
    desnecessárias antes de sua execução).

    Parâmetros:
    - df: pandas.DataFrame -> pandas DataFrame.

    Retorno:
    - None.
    """
    try:
        cols = ["CODIGO_ROTA", "SEQUENCIA"]
        df.drop(cols, axis=1, inplace=True)
    except Exception as e:
        raise CustomException('Erro ao excluir as colunas "CODIGO_ROTA" e "SEQUENCIA"') from e


def _fill_null_vals(df : pd.DataFrame) -> None:
    """
    Recebe um pandas DataFrame e substitui registros
    nulos por 0. Essa abordagem se dá principalmente
    pela concentração de registros nulos unicamente
    na coluna "NUMERO" do dataset e pela confiança de
    que as coordenadas geográficas, que são os únicos
    dados de fato insubstituíveis por novos valores e que
    não dependem de input humano para serem coletadas (ou
    seja, estão pouco sujeitas a erro), não apresentarão
    registros nulos.

    Parâmetros:
    - df: pandas.DataFrame -> pandas DataFrame.

    Retorno:
    - None.
    """
    try:
        df.fillna(0, inplace=True)
    except Exception as e:
        raise CustomException("Erro ao tratar dados nulos") from e


def _clean_number_column(df : pd.DataFrame) -> None:
    """
    Recebe um pandas DataFrame e limpa caracteres
    não-numéricos da coluna "NUMERO" do dataset,
    conservando o número (caso existente, senão ele
    se torna 0).

    Parâmetros:
    - df: pandas.DataFrame -> pandas DataFrame.

    Retorno:
    - None.
    """
    try:
        if df["NUMERO"].dtype == "object":
            df["NUMERO"] = df["NUMERO"].astype(str)
            df["NUMERO"] = df["NUMERO"].apply(_get_adress_number)
    except Exception as e:
        match e:
            case CustomException():
                raise
            case Exception():
                raise CustomException('Erro ao tratar a coluna "NUMERO"') from e


def _convert_float_cols_to_int(df : pd.DataFrame) -> None:
    """
    Recebe um pandas DataFrame e converte as colunas
    NUMERO e INDICE, que podem ser do tipo float inicialmente,
    para o tipo int.

    Parâmetros:
    - df: pandas.DataFrame -> pandas DataFrame.

    Retorno:
    - None.
    """
    try:
        df["NUMERO"] = df["NUMERO"].astype(int)
        df["INDICE"] = df["INDICE"].astype(int)
    except Exception as e:
        raise CustomException('Erro ao converter as colunas "NUMERO" e "INDICE" para valores numéricos') from e


def _drop_coordinates_cols(df : pd.DataFrame) -> None:
    """
    Recebe um pandas DataFrame descarta as colunas
    "LATITUDE" e "LONGITUDE".

    Parâmetros:
    - df: pandas.DataFrame -> pandas DataFrame.

    Retorno:
    - None.
    """
    try:
        cols = ["LATITUDE", "LONGITUDE"]
        df.drop(cols, axis=1, inplace=True)
    except Exception as e:
        raise CustomException('Erro ao excluir as colunas "LATITUDE" e "LONGITUDE"') from e


def _drop_indice_col(df : pd.DataFrame) -> None:
    """
    Recebe um pandas DataFrame e descarta a coluna
    "INDICE".

    Parâmetros:
    - df: pandas.DataFrame -> pandas DataFrame.

    Retorno:
    - None.
    """
    try:
        df.drop("INDICE", axis=1, inplace=True)
    except Exception as e:
        raise CustomException('Erro ao excluir a coluna "INDICE"') from e


def _add_hydrometer_count_col(df : pd.DataFrame) -> pd.DataFrame:
    """
    Recebe um pandas DataFrame e adiciona uma coluna
    que registra quantos hidrômetros existem em cada
    endereço nos dados (ou seja, conta endereços duplicados).

    Parâmetros:
    - df: pandas.DataFrame -> pandas DataFrame.

    Retorno:
    - pandas DataFrame com a coluna adicionada : pandas.DataFrame.
    """
    try:
        hydrometer_count = df.groupby(["LOGRADOURO", "NUMERO"]).size().reset_index().rename(columns={0: "QUANTIDADE_HIDROMETROS"})

        duplicated_mask = df[["LOGRADOURO", "NUMERO"]].duplicated(keep="last") == True
        return df.drop(df[duplicated_mask].index).merge(hydrometer_count, "inner", ["LOGRADOURO", "NUMERO"])

    except Exception as e:
        raise CustomException("Erro ao adicionar a quantidade de hidrômetros em cada endereço aos dados") from e

def _balancing_kmeans(data : pd.DataFrame, ponts_qtd : int, days : int) -> None:
    """
    Recebe um pandas DataFrame e adiciona colunas de cluster
    por dia e por leiturista.

    Parâmetros:
    - data (pd.DataFrame): pandas DataFrame contendo os dados com atribuições de cluster.
    - points_qtd (int): Quantidade máxima de pontos por dia permitida em um cluster.
    - days (int): Número de dias ao longo dos quais os pontos estão distribuídos.

    Retorno:
    - None.
    """
    grouped = data.groupby('cluster_leiturista')
    excess = 0
    excess_list = []
    excess_index =[]
   
    for _, group in grouped:
    
        clusters = group.groupby('cluster_dia')
       
        qtd_points = group.shape[0]
        
        if qtd_points/days > (ponts_qtd +50):
            if qtd_points/days - ponts_qtd > 0.5 * ponts_qtd:
                excess += 1
                excess_list.append({"cluster":group['cluster_leiturista'].values[0],"excess_per_day":qtd_points/days - ponts_qtd ,"points_quantity":qtd_points/22})
                excess_index.append(group['cluster_leiturista'].values[0])

                kmeans3 = KMeans(n_clusters=2)
                clusters_index = group["cluster_leiturista"].values[0]
                group_data = data.loc[data["cluster_leiturista"]==clusters_index].iloc[:,2:4].values
                group_coords = group.iloc[:,2:4].values
                kmeans3.fit(group_coords)
                pred = kmeans3.predict(group_data)
                pred = pred+100 + int(10*random.random())
             
                data.loc[data["cluster_leiturista"]==clusters_index,'cluster_leiturista'] = pred
                for i in np.unique(pred):
                    X = data.loc[data["cluster_leiturista"]==i].iloc[:,2:4].values
                    kmeans4 = KMeans(n_clusters=days)
                    pred2=kmeans4.fit_predict(X)
                    data.loc[data["cluster_leiturista"]==i,'cluster_dia']=pred2

             
                excess_list.remove(excess_list[-1])
                excess_index.remove(excess_index[-1])
                
def _clusterize(df : pd.DataFrame, days : int, leituras: int) -> None:
    """
    Recebe um pandas DataFrame e adiciona colunas de cluster
    por dia e por leiturista.

    Parâmetros:
    - df: pandas.DataFrame -> pandas DataFrame.
    - days: int -> máximo de dias para realização das leituras.
    Serve para definir clusters de rotas por leiturista por dia.
    - leituras: int -> máximo de leituras. Serve para definir
    clusters de rotas por leiturista.

    Retorno:
    - None.
    """
    try:
        kmeans = KMeans(n_clusters=ceil(df.shape[0]/(leituras*days)))
        
        X = df.iloc[:, 0:2].values
        kmeans.fit(X)
        pred = kmeans.predict(X)

        df["cluster_leiturista"] = pred
        
        dias_leitura = days
        df['cluster_dia'] = 0
        for i in unique(kmeans.labels_):
            X = df[df["cluster_leiturista"]==i].iloc[:, 0:2].values
            kmeans2 = KMeans(n_clusters=dias_leitura)
            pred2 = kmeans2.fit_predict(X)
            df.loc[df["cluster_leiturista"] == i, 'cluster_dia'] = pred2
        _balancing_kmeans(df, leituras, days)
    except Exception as e:
        raise CustomException("Erro ao clusterizar os dados por latitude e longitude") from e


def _get_adress_number(s : str) -> str:
    """
    Recebe um registro do dataset da coluna "NUMERO" e retorna o número devidamente
    processado (ou seja, com letras e caracteres não-numéricos retirados). Caso não
    haja caracteres numéricos no registro, retorna "0".

    Parâmetros:
    - s: string -> registro da coluna "NUMERO".

    Retorno:
    - número sem caracteres não-numéricos ou "0".
    """
    try:
        if len(s) <= 0:
            return '0'
        s = s.strip()

        if s.isnumeric():
            return s

        return _get_number_within_str(s)
    except Exception as e:
        match e:
            case CustomException():
                raise
            case Exception():
                raise CustomException("Erro ao encontrar valor numérico de registro da coluna número") from e


def _get_number_within_str(s : str) -> str:
    """
    Recebe uma string e tenta retornar um número nela contido.
    Caso não encontre um número, retorna "0".

    Parâmetros:
    - s: string que supostamente contém um número.

    Retorno:
    - número contido na string enviada como parâmetro ou "0".
    """
    try:
        number = regex.findall(r'\d+', s)

        if len(number) > 0:
            return number[0]

        return '0'
    except Exception as e:
        raise CustomException("Erro ao encontrar valor numérico de registro da coluna número") from e