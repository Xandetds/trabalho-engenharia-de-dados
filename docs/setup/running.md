#  Executando o Projeto

Com os pré-requisitos configurados e o arquivo `.env` preenchido, o ecossistema está pronto para ser inicializado. Esta página detalha os comandos de execução e o fluxo de inicialização da nossa infraestrutura.

---


## Inicializando a Stack de Containers

Certifique-se de que o Docker Desktop esteja aberto. No terminal, execute o comando na raiz do projeto para construir as imagens e subir os serviços em segundo plano:
```bash
docker-compose up -d --build
```

## Monitoramento dos Serviços
Após a inicialização do container, você poderá acessar os consoles administrativos através das portas locais mapeadas:

- MinIO Console: ```http://localhost:9001```

- Apache Airflow Webserver: ```http://localhost:8080```

- Spark Master UI: ```http://localhost:4040```