class CustomException(Exception):
    """
    Usado para gerar exceções customizadas manualmente. Exemplo de uso:
    
    ```
    except Exception as e:
        raise CustomException("Exceção personalizada") from e
    ```
    """
    pass