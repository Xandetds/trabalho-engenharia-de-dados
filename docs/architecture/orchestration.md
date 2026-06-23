# Orquestração com Apache Airflow

Este documento detalha como o Apache Airflow é utilizado no projeto para automatizar e monitorar a execução da nossa esteira de dados (Medallion Architecture).

Em vez de convertermos nossos Jupyter Notebooks em scripts Python puros, adotamos uma abordagem de orquestração direta utilizando a biblioteca **Papermill**. Isso nos permite manter a interatividade do desenvolvimento em notebooks enquanto garantimos a confiabilidade da execução em produção.

---

## A DAG: `tse_medallion_papermill`

A DAG (Directed Acyclic Graph) principal do projeto foi configurada para refletir exatamente a ordem lógica de dependência das camadas do nosso Data Lake. 

Ela executa os notebooks de forma estritamente sequencial. Se uma etapa falhar (por exemplo, a extração da Landing), as etapas subsequentes não serão iniciadas, protegendo a integridade das camadas Silver e Gold.

**Ordem de Execução:**
1. `run_00_setup_buckets`
2. `run_01_landing`
3. `run_02_bronze`
4. `run_03_silver`
5. `run_04_gold`

---

## O Papel do Papermill

O **Papermill** é a ferramenta que atua como ponte entre o Airflow e os notebooks. Ele parametriza e executa os arquivos `.ipynb` por baixo dos panos. 

As principais vantagens e configurações adotadas no nosso código (`dags/tse_medallion_papermill.py`) incluem:

* **Injeção de Parâmetros:** O Airflow passa automaticamente variáveis de contexto para os notebooks durante a execução, como o `airflow_run_id` e o `airflow_logical_date`.
* **Isolamento do Spark (`SPARK_SCRATCH`):** Para evitar que os arquivos temporários do Spark (como `spark-warehouse/` ou `metastore_db`) poluam o diretório principal do projeto, a execução do Papermill é direcionada para um diretório temporário isolado (`/tmp/spark-scratch`).
* **Geração de Evidências (`OUTPUT_DIR`):** Cada execução bem-sucedida ou falha gera uma cópia do notebook com as células executadas (contendo os logs e resultados). Esses arquivos são salvos em um volume nomeado (`/opt/airflow/papermill-output`), servindo como um histórico de auditoria perfeito para debug. O formato do arquivo de saída segue o padrão: `<data_logica>_<run_id>.ipynb`.

---

## Configuração do Container (Docker)

Para que o Airflow conseguisse executar notebooks que utilizam PySpark e Delta Lake, a imagem oficial do Apache Airflow precisou ser estendida (`docker/Dockerfile.airflow`).

As seguintes dependências foram incorporadas ao container do Airflow:

* **Java (JRE):** Necessário para a Máquina Virtual Java (JVM) executar as rotinas do Apache Spark.
* **Bibliotecas Python:** Instalação do `papermill`, `ipykernel`, `pyspark`, `delta-spark` e `pymongo` via arquivo `airflow-requirements.txt`, garantindo que o Airflow tenha o mesmo ambiente de execução do Jupyter Lab.

---

## Como Executar pelo Airflow

Com a stack do Docker Compose rodando, siga os passos abaixo para acionar o pipeline completo:

1. Acesse a interface web do Airflow no navegador: **`http://localhost:8080`**.
2. Faça login utilizando as credenciais definidas no seu arquivo `.env` (o padrão local geralmente é usuário `admin` e senha `admin`).
3. Na lista de DAGs, localize a **`tse_medallion_papermill`**.
4. Clique no botão de **"Unpause"** (o toggle switch no canto esquerdo) para ativar a DAG.
5. Clique no botão de **"Trigger DAG"** (ícone de play no canto direito) para iniciar a execução manual.
6. Clique no nome da DAG e vá na aba **Graph** ou **Grid** para acompanhar o progresso de cada notebook em tempo real.