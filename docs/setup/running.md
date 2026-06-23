#  Executando o Projeto

Com os pré-requisitos configurados e o arquivo `.env` preenchido, o ecossistema está pronto para ser inicializado. Esta página detalha os comandos de execução e o fluxo de inicialização da nossa infraestrutura.

---


## Inicializando a Stack de Containers

No terminal, execute o comando na raiz do projeto para construir as imagens e subir os serviços em segundo plano:

!!! info "Nota sobre o ambiente (Sistemas Operacionais)"
* Windows / macOS: Geralmente é necessário que o aplicativo do Docker Desktop esteja iniciado em segundo plano para que os comandos respondam no terminal.
* Linux: O comando pode ser executado diretamente, dado que o Docker costuma rodar nativamente como um serviço de sistema em background.

```bash
docker-compose up -d --build
```
A partir daí, o Jupyter Lab já está disponível em ```http://localhost:8888``` para manipulação e utilização dos notebooks Jupyter.

## Monitoramento dos Serviços
Após a inicialização dos serviços, você poderá acessar os consoles administrativos através das portas locais mapeadas:

- MinIO Console: ```http://localhost:9001```

- Apache Airflow Webserver: ```http://localhost:8080```
