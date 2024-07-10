"""
Módulo para execução do algoritmo Ant Colony escrito em Java.
"""
from pathfinder import pathfinder
from subprocess import Popen, PIPE

dir = pathfinder.get_current_abs_path()
ant_colony_path = pathfinder.find_abs("java", "\\ant_colony\\bin")

def execute(file_name : str, route_code : int, args : list, with_2opt : bool) -> str:
    """
    Executa o algoritmo Ant Colony escrito em Java.

    Parâmetros:
    - file_name : str -> nome do arquivo CSV contendo os dados a serem enviados ao algoritmo
    - route_code : int -> código da rota sendo sequenciada
    - args : list -> lista de argumentos para execução do algoritmo Ant Colony
    - with_2opt : bool -> booleano para dizer se deve ou não refinar os resultados com o algoritmo 2-Opt

    Retorno:
    - String em formato CSV contendo output do algoritmo : str
    """
    global ant_colony_path
    global dir
    if with_2opt:
        process = Popen([f'java', '-cp', ant_colony_path, "antcolony.AntColony", f'{dir}\\data\\{file_name}', f"{route_code}", str(args[0]), str(args[1]), str(args[2]), str(args[3])], stdout=PIPE, universal_newlines=True)
    else:
        process = Popen([f'java', '-cp', ant_colony_path, "antcolony.AntColony", f'{dir}\\data\\{file_name}', f"{route_code}", str(args[0]), str(args[1]), str(args[2])], stdout=PIPE, universal_newlines=True)
    (stdout, stderr) = process.communicate()
    return stdout.strip()