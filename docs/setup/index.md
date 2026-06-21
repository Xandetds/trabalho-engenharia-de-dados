# Setup

O ambiente do projeto e executado com Docker Compose. A stack sobe tres partes principais:

| Servico | Funcao | Porta |
|---|---|---|
| `spark-lab` | Jupyter Lab com PySpark, Delta Lake e acesso ao MinIO | `8888` |
| `minio` | Object storage compativel com S3 | `9020` API / `9021` console |
| `airflow` | Orquestracao dos notebooks via Papermill | `8080` |

O arquivo `.env` na raiz concentra as credenciais do MongoDB Atlas, do MinIO e, opcionalmente, do usuario inicial do Airflow.
