# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Visão geral

Trabalho final da disciplina de Engenharia de Dados (Unisatc). O objetivo é um pipeline
Apache Spark usando **Delta Lake**, **MinIO** (object storage compatível com S3) e **MongoDB**.
Código e documentação estão em português.

O repositório está, no momento, **focado na infraestrutura** — ele provisiona um ambiente
containerizado de Jupyter Lab + PySpark com Delta Lake e um MinIO já integrado. Os notebooks de
ETL/análise e o serviço de MongoDB ainda não estão no projeto; partes disso estão em outras
branches de feature.

## Executando o ambiente

O fluxo previsto é inteiramente via Docker — não há execução local.

```bash
docker compose up --build      # build da imagem + sobe o Jupyter Lab
docker compose up -d           # sobe em background
docker compose down            # para
```

Serviços expostos:

- **Jupyter Lab** — http://localhost:8888, **sem token/senha** (acesso aberto, apenas para dev).
  O diretório raiz dele é `notebook/`.
- **MinIO** — API S3 em http://localhost:9020 e console web em http://localhost:9021.

Antes de subir, é preciso um arquivo **`.env`** na raiz (não versionado) com `MINIO_ENDPOINT`,
`MINIO_ACCESS_KEY` e `MINIO_SECRET_KEY` — sem elas o serviço MinIO não autentica e o kernel
falha no startup (veja abaixo). O `MINIO_ENDPOINT` usado pelo Spark/boto3 aponta para o serviço
dentro da rede do compose (ex.: `http://minio:9000`), não para a porta publicada no host.

As dependências são gerenciadas com **Poetry** (`package-mode = false`, ou seja, não há pacote
a instalar — só dependências). Elas são instaladas *dentro* da imagem no build, com
`virtualenvs.create false`. Para adicionar/alterar uma dependência, edite o `pyproject.toml` e
refaça o build (`docker compose up --build`); regenere o `poetry.lock` com `poetry lock` se
necessário.

## Arquitetura

- **`docker-compose.yml`** — define dois serviços: `spark-lab` (o container do Jupyter/PySpark,
  buildado a partir de `docker/Dockerfile`) e `minio` (object storage, com dados persistidos no
  volume nomeado `minio-data`). As credenciais do MinIO vêm das variáveis `MINIO_ACCESS_KEY` /
  `MINIO_SECRET_KEY` do `.env`.
- **`docker/Dockerfile`** — base `python:3.11-slim`, instala um JRE headless (necessário para o
  Spark), o Poetry e então as dependências do projeto. Copia a pasta `startup/` para
  `/root/.ipython/profile_default/startup/`.
- **`startup/`** — scripts de bootstrap do IPython. Todo arquivo `.py` colocado aqui roda
  automaticamente a **cada** início de kernel IPython/Jupyter (graças à cópia para o profile
  de startup no Dockerfile), em **ordem alfabética** pelo nome — por isso o prefixo numérico
  (`00_`, `01_`, ...). Use essa pasta para preparar o ambiente de todo notebook (ex.: criar a
  sessão Spark, carregar variáveis, registrar conexões). Como roda dentro da imagem, qualquer
  alteração aqui exige rebuild (`docker compose up --build`) para ter efeito.
  - **`startup/00_startup.py`** — carrega o `.env` (`load_dotenv`), valida que as variáveis
    `MINIO_*` existem (senão levanta `RuntimeError`) e expõe três globais em todo notebook, sem
    precisar de imports:
    - `spark` — a `SparkSession` (`local[*]`), já com a extensão do **Delta Lake**
      (`DeltaSparkSessionExtension` + `DeltaCatalog`) e o conector **S3A** apontado para o MinIO
      (`spark.hadoop.fs.s3a.*`: endpoint, chaves, `path.style.access`, SSL desligado). Os pacotes
      `delta-spark` e `hadoop-aws` são puxados via `spark.jars.packages`. Com isso dá para
      ler/gravar tabelas Delta direto em `s3a://...`.
    - `sc` — o `SparkContext` subjacente.
    - `minio` — um cliente **boto3 S3** apontado para o MinIO, para operações de bucket/objeto
      fora do Spark.

    As versões de Spark/Delta precisam ficar em sincronia com o `pyproject.toml`
    (`pyspark 3.5.3`, `delta-spark 3.2.0`). Após montar tudo, o script faz `del` nas variáveis de
    credencial — isso só evita exposição acidental no namespace do notebook, **não** é proteção
    real (o segredo continua recuperável via `os.environ`, pela config do Spark ou pelo próprio
    cliente `minio`). A proteção de fato é o `.env` não ser versionado.
- **`notebook/`** — diretório de trabalho do Jupyter e onde os notebooks devem ficar.
- **`data/`** — montado no container em `/app/data`; guarda os dados das tabelas Delta Lake.

## Convenções

- Branches e commits seguem convenção em português, numerada pela issue
  (ex.: `14-provisionar-ambiente-jupyter-com-pyspark-configurado`); as mensagens de commit usam
  Conventional Commits com `feat(infrastructure): ...`, `style: ...`, etc. Os PRs vão para a
  branch `master`.
- Novos notebooks vão em `notebook/` e podem assumir que `spark`, `sc` e `minio` já existem.
