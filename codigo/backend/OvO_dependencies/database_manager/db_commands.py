"""
Módulo para inicialização, consulta e alteração do banco de dados da aplicação.
"""
from sqlite3 import connect, Connection
import sqlite3
from custom_exceptions.custom_exception import CustomException
from pathfinder import pathfinder

db_folder_path = pathfinder.find_abs("banco")

DB_FILE_PATH = db_folder_path + "\\database.db"
DB_SQL_PATH = db_folder_path + "\\database.sql"


def generate_db() -> None:
    """
    Checa se o banco de dados já existe e, se não existir, cria o arquivo vazio "database.db".
    """
    global DB_FILE_PATH
    global DB_SQL_PATH
    try:
        if not pathfinder.path_exists(DB_FILE_PATH):
            open(DB_FILE_PATH, "a").close()

            # Se conecta ao banco de dados
            connection = _connect_to_db()

            # Executa o script SQL para construir o banco de dados
            with open(DB_SQL_PATH) as sql:
                connection.executescript(sql.read())

            # Finaliza o processo
            connection.commit()
    except Exception as e:
        print(e)
        raise CustomException("Erro ao gerar o banco de dados.") from e
    finally:
        if "connection" in locals():
            connection.close()

def retrieve_data(query_string : str, params : tuple = None) -> list:
    """
    Executa uma query em SQL com comando SELECT no banco de dados para retornar
    os dados consultados.

    Parâmetros:
    - query_string : str -> texto SQL da query
    - params : tuple -> sequência de parâmetros para completar a query (por padrão, None)
    
    Retorno:
    - lista de resultados : list
    """
    try:
        con = _connect_to_db()
        if params == None:
            result = con.execute(query_string).fetchall()
        else:
            result = con.execute(query_string, params).fetchall()

        return result
    except Exception as e:
        raise CustomException("Erro ao consultar o banco de dados. SQL:\n" + query_string) from e
    finally:
        if "con" in locals():
            con.close()

def alter_data(query_string : str, params : tuple = None) -> int:
    """
    Executa uma query em SQL com comando DELETE, INSERT ou UPDATE no banco de dados para alterar
    registros existentes ou inserir novos.

    Parâmetros:
    - query_string : str -> texto SQL da query
    - params : tuple -> sequência de parâmetros para completar a query (por padrão, None)
    """
    try:
        con = _connect_to_db()
        if params == None:
            cursor = con.execute(query_string)
        else:
            cursor = con.execute(query_string, params)
        con.commit()
        return cursor.lastrowid
    except Exception as e:
        raise CustomException("Erro ao alterar dados do banco de dados. SQL:\n" + query_string) from e
    finally:
        if "con" in locals():
            con.close()

def _connect_to_db() -> Connection:
    """
    Estabelece conexão com o banco de dados.

    Retorno:
    - Objeto da conexão com o banco : sqlite3.Connection
    """
    global DB_FILE_PATH
    return connect(DB_FILE_PATH)