# trabalho-engenharia-de-dados

Repositorio voltado para o trabalho final da disciplina de Engenharia de Dados da Unisatc.

O projeto implementa um pipeline de dados em arquitetura medalhao usando MongoDB Atlas, Apache Spark, Delta Lake, MinIO e Airflow. Os notebooks ficam em `notebook/` e podem ser executados manualmente pelo Jupyter Lab ou orquestrados pelo Airflow com Papermill.

## Servicos

| Servico | URL | Uso |
|---|---|---|
| Jupyter Lab | http://localhost:8888 | Desenvolvimento e validacao dos notebooks |
| MinIO Console | http://localhost:9021 | Inspecao dos buckets `landing`, `bronze`, `silver` e `gold` |
| Airflow | http://localhost:8080 | Orquestracao da DAG `tse_medallion_papermill` |

## Execucao

1. Copie `.env.example` para `.env` e preencha as credenciais do MongoDB Atlas e do MinIO.
2. Suba o ambiente:

```bash
docker compose up --build
```

3. Acesse o Airflow em `http://localhost:8080`.
4. Entre com usuario `admin` e senha `admin`, a menos que tenha configurado outros valores em `AIRFLOW_ADMIN_USER` e `AIRFLOW_ADMIN_PASSWORD`.
5. Execute a DAG `tse_medallion_papermill`.

Os notebooks executados pelo Papermill sao salvos em `notebook/output/`, servindo como evidencia de execucao de cada etapa.
