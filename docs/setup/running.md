# Rodando o Projeto

Suba todos os servicos:

```bash
docker compose up --build
```

Depois acesse:

| Ferramenta | URL |
|---|---|
| Jupyter Lab | http://localhost:8888 |
| MinIO Console | http://localhost:9021 |
| Airflow | http://localhost:8080 |

No Airflow, entre com o usuario e senha definidos em `.env` ou use `admin` / `admin` no ambiente local. A DAG principal e `tse_medallion_papermill`.

## Executando pelo Airflow

1. Abra `http://localhost:8080`.
2. Localize a DAG `tse_medallion_papermill`.
3. Despause a DAG.
4. Clique em executar manualmente.

A DAG executa os notebooks existentes em ordem:

1. `00_setup_buckets.ipynb`
2. `01_landing.ipynb`
3. `02_bronze.ipynb`, quando o arquivo existir
4. `03_silver.ipynb`, quando o arquivo existir
5. `04_gold.ipynb`, quando o arquivo existir

Cada execucao gera uma copia executada do notebook em `notebook/output/<nome-do-notebook>/`. Essa pasta nao e versionada porque contem artefatos de execucao.
