# OvO

Este é o aplicativo backend do OvO, que utiliza Flask para o servidor API e SQLite para gerenciamento de dados de rotas e leituras de hidrômetros. O projeto é estruturado para maximizar a eficiência operacional e a segurança dos leituristas através da otimização das rotas.

## Pré-requisitos

Antes de iniciar, você precisará ter as seguintes ferramentas instaladas em seu computador:

- [Python](https://www.python.org/downloads/) (que inclui `pip`)
- [Java JDK](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html) (necessário para compilar e executar os algoritmos Java)
- PowerShell ou PowerShell Core (para usuários de MacOS ou Linux)
- Um editor de código de sua preferência (recomendamos [VSCode](https://code.visualstudio.com/))

Assegure-se de que o Python e o Java estejam corretamente configurados no PATH do seu sistema para permitir a execução dos scripts e comandos de compilação.

## Scripts Disponíveis

Neste projeto, você pode executar os seguintes scripts:

- `./build.ps1` - Configura o ambiente, instala dependências, compila algoritmos Java e inicia o servidor Flask.
- `pytest` - Executa os testes automatizados para garantir a qualidade do código.

## Estrutura do Projeto

Abaixo está o mapa de arquivos do projeto detalhando a finalidade de cada diretório e arquivo:

```
/backend
│
├── /banco                   # Scripts SQL e banco de dados SQLite
│   └── /database.sql        # Script SQL para criação do banco de dados
│
├── /flask                    # Código Flask para o servidor API
│   ├── /app.py               # Ponto de entrada do servidor Flask
│   └── /app.spec.py          # Especificações para testes do Flask
│
├── /OvO_dependencies         # Dependências customizadas do projeto
│   ├── /algorithms           # Algoritmos de otimização
│   │   ├── /ant_colony       # Algoritmo de colônia de formigas
│   │   ├── /general_executer # Execução de algoritmos
│   │   ├── /greedy           # Algoritmo guloso
│   │   ├── /pollination      # Algoritmo de polinização
│   │   └── /two_opt          # Algoritmo de 2-opt
│   ├── /custom_exceptions    # Exceções customizadas para o projeto
│   │   └── /custom_exception.py # Definição de exceções
│   ├── /data_processing      # Módulo para tratamento, processamento e clusterização dos dados para sequenciamento de rotas na aplicação pelos algoritmos.
│   │   ├── /data_processing.spec.py # Especificações para testes de processamento
│   │   └── /data_processing.py # Script de processamento
│   ├── /database_manager     # Módulo para inicialização, consulta e alteração do banco de dados da aplicação.
│   │   └── /db_commands.py   # Comandos de banco de dados
│   └── /pathfinder           # Módulo que lida com caminhos de diretórios e de execução.
│       └── /pathfinder.py    # Script de definição de caminhos
│
└── /tests                    # Testes para as funcionalidades do backend
    └── /test_routes.py       # Testes para as rotas da API
```

## Banco de Dados

Utilizamos SQLite para gerenciar dados relacionados às rotas e leituras de hidrômetros. O esquema e as migrações do banco de dados podem ser encontrados no diretório `/banco`.

## Testes

Para executar os testes e garantir a qualidade do código, use o comando:

```bash
pytest
```

Para mais informações sobre como configurar ou estender este projeto, consulte a documentação dos módulos Python listados no `requirements.txt`.
