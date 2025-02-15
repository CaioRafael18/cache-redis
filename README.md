# Projeto de Cache com PostgreSQL e Redis

Este projeto é uma aplicação construída com Flask que utiliza PostgreSQL como banco de dados e Redis como cache para otimizar o tempo de resposta.

## Arquivos Principais:
- **app.py**: Arquivo principal da aplicação.
- **database.py**: Configuração das conexões com PostgreSQL e Redis.
- **inserir-dados.py**: Script para inserir dados no banco a partir de um arquivo CSV.
- **Dockerfile**: Configuração do Docker para a aplicação.
- **docker-compose.yml**: Configuração do Docker Compose para gerenciar os serviços.
- **requirements.txt**: Lista de dependências do projeto.
- **.env**: Arquivo de variáveis de ambiente.

O Dockerfile define a imagem da aplicação, e o docker-compose.yml gerencia os serviços do PostgreSQL, Redis e da aplicação.

## Passo a Passo:
1. Clone o repositório.
2. Navegue até o diretório do projeto.
3. Execute o comando abaixo para iniciar os serviços:
    ```sh
    docker-compose up
    ```
4. A aplicação estará disponível em: http://localhost:5000
5. Execute o comando abaixo para inserir os dados no banco a partir do arquivo CSV:
    ```sh
    python inserir-dados.py
    ```
