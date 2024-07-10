"""
Módulo para execução dos algoritmos da aplicação, que são:

- 1. Ant Colony
- 2. Flower Pollination
"""
import pandas as pd
import numpy as np
from os import remove as remove_dir
from json import loads as as_dict, dumps as as_string
from haversine import haversine, Unit
from typing import IO
from database_manager import db_commands as db
from algorithms.pollination.FPA import FPA
from algorithms.ant_colony import ant_colony_executer
from data_processing.data_processing import IO_as_dataframe, df_to_IO, write_to_tmp_file, remove_generated_files, merge_data

def run_algorithm(algorithm : int, data_to_run : IO, initial_data : IO, db_row_id : int, args : list) -> None:
    """
    Função para rodar qualquer um dos algoritmos disponíveis na aplicação. Ao fim da execução, o valor é guardado na base de dados para consulta futura.

    Parâmetros:
    - algorithm : int -> id no banco de dados do algoritmo a ser executado (1 == Ant Colony / 2 == Pollination)
    - data_to_run : IO -> objeto de arquivo CSV para ser enviado ao algoritmo para execução
    - initial_data : IO -> objeto de arquivo CSV para ser mergeado ao output do algoritmo
    - db_row_id : int -> id do registro desta execução no banco de dados
    - args : list -> lista de argumentos a serem passados para os algoritmos
    """
    try:
        initial_df = IO_as_dataframe(initial_data)
        initial_data.close()

        df = IO_as_dataframe(data_to_run)
        data_to_run.close()

        result = open("./data/result.json", "a+")

        match algorithm:
            case 1: # Ant Colony
                _solve_ant_colony(df, result, args, False)
            
            case 2: # Flower Pollination
                _solve_pollination(df, result, args, False)
            
            case 3: # Ant Colony + 2-Opt
                _solve_ant_colony(df, result, args, True)

            case 4: # Pollination + 2-Opt
                _solve_pollination(df, result, args, True)
        
        FINISHED_STATUS = 2
        result.seek(0)
        
        result_string = result.read()
        result_string = result_string[:len(result_string) - 3] + "\n}"
        
        result_dict = as_dict(result_string)
        times_exceeded_limit = 0
        MAX_HOURS = 6
        for i in range(1, len(result_dict) + 1):
            hours = result_dict[f"Rota {i}"]["Tempo"]
            if float(hours[:len(hours) - 1]) > MAX_HOURS:
                times_exceeded_limit += 1
            
            result_dict[f"Rota {i}"]["Pontos"] = merge_data(initial_df, pd.DataFrame(result_dict[f"Rota {i}"]["Pontos"]))
            

        db.alter_data("UPDATE EXECUTIONS SET status=?, end_time=datetime(), result=?, times_exceeded_limit=? WHERE id=?;", (FINISHED_STATUS, as_string(result_dict), times_exceeded_limit, db_row_id))
        result.close()
        remove_dir("./data/result.json")
    except Exception as e:
        ERROR_STATUS = 3
        db.alter_data("UPDATE EXECUTIONS SET status=?, end_time=datetime(), result=? WHERE id=?;", (ERROR_STATUS, e.__str__(), db_row_id))
        raise e
    finally:
        if "result" in locals():
            result.close()
            remove_dir("./data/result.json")
        initial_data.close()


def _solve_ant_colony(clusterized_df : pd.DataFrame, file_to_write : IO, args : list, with_2opt : bool) -> None:
    """
    Executa o algoritmo Ant Colony para sequenciamento das rotas.

    Parâmetros:
    - clusterized_df : pandas.DataFrame -> pandas DataFrame clusterizado para execução do algoritmo
    - file_to_write : IO -> objeto de arquivo JSON para escrita do output
    - args : list -> lista de argumentos para execução do algoritmo Ant Colony
    - with_2opt : bool -> booleano para dizer se deve ou não refinar os resultados com o algoritmo 2-Opt
    """
    route_code = 0
    file_to_write.write("{")
    for leiturista in clusterized_df["cluster_leiturista"].unique():
        for dia in clusterized_df["cluster_dia"].unique():
            route_code += 1
            grouped_leiturista = clusterized_df[clusterized_df["cluster_leiturista"] == leiturista]
            grouped_dia = grouped_leiturista[grouped_leiturista["cluster_dia"] == dia]
            
            temp = df_to_IO(grouped_dia, f"tmp{leiturista}.csv")
            tmp_file_name = write_to_tmp_file(temp)
            temp.close()
            file_to_write.write(ant_colony_executer.execute(tmp_file_name, route_code, args, with_2opt))
            remove_generated_files()
    
    file_to_write.write("\n}")

        

def _solve_pollination(clusterized_df : pd.DataFrame, file_to_write : IO, args : list, with_2opt : bool) -> None:
    """
    Executa o algoritmo Flower Pollination para sequenciamento das rotas.

    Parâmetros:
    - clusterized_df : pandas.DataFrame -> pandas DataFrame clusterizado para execução do algoritmo
    - file_to_write : IO -> objeto de arquivo JSON para escrita do output
    - args : list -> lista de argumentos para execução do algoritmo Pollination
    - with_2opt : bool -> booleano para dizer se deve ou não refinar os resultados com o algoritmo 2-Opt
    """
    grouped = clusterized_df.groupby('cluster_leiturista')
    route_code = 0
    flowers = args[0]
    switch_prob = args[1]
    radius = args[2]
    file_to_write.write("{")
    for _, group in grouped:
        clusters = group.groupby('cluster_dia')
        for label, cluster in clusters:
            route_code += 1
            coords = cluster[['LATITUDE', 'LONGITUDE']].to_numpy()
            n = len(coords)
            distance_matrix = np.zeros((n, n))

            for i in range(n):
                for j in range(i + 1, n):
                    distance_matrix[i, j] = distance_matrix[j, i] = haversine(coords[i], coords[j], unit=Unit.KILOMETERS)

            fpa = FPA(distance_matrix, switch_prob, len(distance_matrix), flowers)
            solution = fpa.main_loop(cluster.QUANTIDADE_HIDROMETROS.values, radius)

            if with_2opt:
                solution = _two_opt(solution['sequence'], distance_matrix, cluster.QUANTIDADE_HIDROMETROS.values, args[3]) 

            file_to_write.write(f'\n"Rota {route_code}": {"{"}\n"Tempo": "{solution["time"]}h",\n"Tamanho": "{solution["distance"]}km",\n"Pontos": [')
            
            cluster["SEQUENCIA"] = pd.Series(solution["sequence"]).values
            cluster.sort_values(["SEQUENCIA"], inplace=True)
            
            for i in range(len(solution["sequence"])):
                if i == len(solution["sequence"]) - 1:
                    file_to_write.write(f'\n{"{"}\n"LOGRADOURO": "{cluster.LOGRADOURO.values[i]}",\n"NUMERO": {cluster.NUMERO.values[i]},\n"SEQUENCIA": {cluster.SEQUENCIA[i]},\n"LATITUDE": {cluster.LATITUDE.values[i]},\n"LONGITUDE": {cluster.LONGITUDE.values[i]}\n{"}"}')
                    break
                file_to_write.write(f'\n{"{"}\n"LOGRADOURO": "{cluster.LOGRADOURO.values[i]}",\n"NUMERO": {cluster.NUMERO.values[i]},\n"SEQUENCIA": {cluster.SEQUENCIA[i]},\n"LATITUDE": {cluster.LATITUDE.values[i]},\n"LONGITUDE": {cluster.LONGITUDE.values[i]}\n{"}"},')
            
            file_to_write.write("\n]\n},")

    file_to_write.write("\n}")


def _two_opt(path, distances, qtd_matrix, max_iterations):
    """
    Executa o algoritmo 2-Opt para refinamento do sequenciamento das rotas.

    Parâmetros:
    - path : list -> lista de pontos sequenciados
    - distances : list -> matriz de distância entre os pontos
    - qtd_matrix : list -> matriz de quantidade de hidrômetros em cada ponto
    - max_iterations : int -> máximo de iterações que o algoritmo deve executar
    """
    # Flag para controlar se houve melhoria no caminho
    improved = True
    # Contador para controlar o número de iterações
    iteration_count = 0

    # Loop continua enquanto houver melhoria e o número de iterações for menor que o máximo
    while improved and iteration_count < max_iterations:
        improved = False
        # Testa todas as possíveis trocas de segmentos não consecutivos
        for i in range(1, len(path) - 2):
            for j in range(i + 1, len(path) - 1):
                if j - i == 1:  # Ignora se i e j são consecutivos
                    continue
                # Verifica se a troca resulta em uma distância menor
                if distances[path[i - 1]][path[i]] + distances[path[j]][path[j + 1]] > distances[path[i - 1]][path[j]] + distances[path[i]][path[j + 1]]:
                    # Realiza a troca invertendo o segmento
                    path[i:j + 1] = path[i:j + 1][::-1]
                    improved = True

        # Incrementa o contador de iterações
        iteration_count += 1

    # Recalcula distância e tempo após a otimização 2-opt
    dist = 0
    time = 0
    for k in range(1, len(path)):
        dist += distances[path[k - 1]][path[k]]
        time += distances[path[k - 1]][path[k]] / 5 + (0.5 / 60) * qtd_matrix[path[k - 1]]

    # Retorna o caminho otimizado, a distância total e o tempo estimado
    return {'sequence': path, 'distance': dist, 'time': time}