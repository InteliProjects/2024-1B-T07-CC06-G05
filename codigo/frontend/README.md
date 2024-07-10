# OvO

Este é o aplicativo frontend do OvO baseado em React, utilizando o React Router para navegação e estilizado com CSS modular. O projeto é construído com Vite e inclui ESLint para garantir a qualidade do código.

## Pré-requisitos

Antes de iniciar, você precisará ter as seguintes ferramentas instaladas em seu computador:

- [Node.js](https://nodejs.org/en/) (que inclui `npm`)
- Um editor de código de sua preferência (recomendamos [VSCode](https://code.visualstudio.com/))

## Instalação

Para começar com este projeto, clone o repositório e execute os seguintes comandos:

```bash
npm install       # Instalar dependências
npm run dev       # Executar o servidor de desenvolvimento
```

## Scripts Disponíveis

Neste projeto, você pode executar os seguintes scripts:

- `npm run dev` - Inicia o servidor de desenvolvimento usando Vite.
- `npm run build` - Constrói os arquivos estáticos prontos para produção.
- `npm run lint` - Analisa os arquivos do projeto em busca de problemas potenciais.
- `npm run preview` - Serve os arquivos estáticos construídos.

## Estrutura do Projeto

Abaixo está o mapa de arquivos do projeto detalhando a finalidade de cada diretório e arquivo:

```
/frontend
│
├── /node_modules            # Módulos e dependências do Node
├── /public                  # Ativos públicos como imagens e fontes
├── /src                     # Arquivos fonte
│   ├── /components          # Componentes de interface de usuário reutilizáveis
│   │   ├── /data-form       # Componente para formulários de entrada de dados
│   │   ├── /export-routes   # Componente para  exportação de rotas
│   │   ├── /header          # Componente de cabeçalho da interface de usuário
│   │   ├── /routes          # Componente para roteamento
│   │   ├── /table           # Componente de tabela para exibição de dados
│   │   └── /white-background # Componente para fundo branco
│   ├── /data                # Arquivos de dados
│   ├── /pages               # Páginas do React Router
│   │   └── /dashboard       # Página do painel de controle
│   ├── /services            # Serviços para manipulação de comunicação com o backend
│   │   └── send-data.service.js # Serviço para enviar dados ao servidor
│   ├── /utils               # Funções de utilidade
│   │   ├── download-csv-file.js  # Utilitário para baixar arquivos CSV
│   │   └── generate-csv-content.js # Utilitário para gerar conteúdo CSV
│   ├── main.jsx             # Ponto de entrada principal
│   ├── reset.css            # Reset CSS
│   └── routes.jsx           # Definições de roteamento
│   └── styles.css           # Estilos globais
│
├── .eslintrc.cjs            # Configuração do ESLint
├── .stylelintrc.json        # Configuração do StyleLint
├── index.html               # Página HTML principal
├── .gitignore               # Especifica arquivos não rastreados intencionalmente para ignorar
├── package.json             # Manifesto do projeto com dependências e scripts
├── README.md                # Documentação do projeto (este arquivo)
└── vite.config.js           # Configuração do Vite

```

## Dependências

- React e ReactDOM para a interface de usuário.
- React Router para navegação.
- Vite para construir e servir a aplicação.
- ESLint e StyleLint para linting do código.

## Linting

ESLint e StyleLint estão configurados para garantir a qualidade do código e a consistência do estilo. Para verificar se há erros de lint no seu código, execute `npm run lint`.

Para mais informações sobre como configurar ou estender este projeto, consulte a documentação oficial das dependências listadas no `package.json`.
