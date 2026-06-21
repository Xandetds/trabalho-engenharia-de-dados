# Arquitetura

O projeto adota uma arquitetura Lakehouse: o Apache Spark via PySpark atua como motor de processamento, o Delta Lake como formato transacional das tabelas e o MinIO como armazenamento de objetos, tendo o MongoDB Atlas como origem dos dados.

O desenvolvimento acontece em um ambiente containerizado com Jupyter Lab, onde os notebooks sao criados e testados. A orquestracao fica no Apache Airflow: cada tarefa da DAG executa um notebook com Papermill e salva uma copia executada como evidencia da etapa.

Esta secao descreve as decisoes de arquitetura do projeto: as tecnologias que compoem o ambiente e como os dados fluem entre as camadas ate chegarem ao dashboard.

## Nesta secao

- [Visao Geral](overview.md) - como Spark, Delta Lake e MinIO se combinam em um ambiente Lakehouse e qual o fluxo dos dados de ponta a ponta.
- [Medalhao (Camadas)](medallion.md) - a organizacao dos dados em Landing, Bronze, Silver e Gold, com o papel e as transformacoes de cada camada.
