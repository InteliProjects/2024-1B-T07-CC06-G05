"""
Módulo que lida com caminhos de diretórios e de execução.
"""
from os import walk
from os.path import abspath, join, exists

def find_abs(dir : str, extra_to_join : str = "") -> str:
    """
    Encontra o caminho absoluto para o diretório especificado retrocedendo até a pasta raíz do caminho
    absoluto do diretório atual e procurando pelo alvo em cada um dos diretórios percorridos.

    Parâmetros:
    - dir : str -> diretório alvo
    - extra_to_join : str -> caminho extra a ser concatenado ao fim do caminho absoluto encontrado (por padrão, uma string vazia)

    Retorno:
    - caminho absoluto para o diretório alvo com o caminho extra concatenado : str
    """
    current_dir = abspath("")
    target = ""

    while (target == ""):
        for root, dirs, files in walk(current_dir):
            for d in dirs:
                if d == dir:
                    target = abspath(join(root, d + extra_to_join))
        current_dir = current_dir[:current_dir.rindex("\\")]
    return target


def get_current_abs_path() -> str:
    """
    Retorna o caminho absoluto do diretório atual.
    """
    return abspath("")


def path_exists(path : str) -> bool:
    """
    Checa se o caminho especificado existe.

    Parâmetros:
    - path : str -> caminho a ser checado

    Retorno:
    - "True" se o caminho existe, "False" caso contrário : bool
    """
    return exists(path)