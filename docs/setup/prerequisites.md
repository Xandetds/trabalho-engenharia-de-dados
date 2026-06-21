# Pre-requisitos

Antes de rodar o projeto, instale:

- Docker Desktop ou Docker Engine com Docker Compose.
- Git, para clonar o repositorio.
- Acesso ao MongoDB Atlas usado como origem dos dados.

Crie um arquivo `.env` na raiz a partir do `.env.example`:

```bash
cp .env.example .env
```

Depois preencha:

```env
MONGO_URI=mongodb+srv://...
MONGO_DB_NAME=trabalho-final-engenharia-dados
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=...
MINIO_SECRET_KEY=...
AIRFLOW_ADMIN_USER=admin
AIRFLOW_ADMIN_PASSWORD=admin
```

O endpoint do MinIO deve usar `http://minio:9000`, pois Spark, notebooks e Airflow acessam o servico pela rede interna do Docker Compose.
