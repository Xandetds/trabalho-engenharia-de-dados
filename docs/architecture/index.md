# Arquitetura

O projeto adota uma arquitetura Lakehouse: o Apache Spark (via PySpark) como motor de processamento, o Delta Lake como formato transacional das tabelas e o MinIO como armazenamento de objetos, tendo o MongoDB Atlas como origem dos dados.

O desenvolvimento acontece num ambiente containerizado com Jupyter Lab, onde os notebooks são criados e testados, e posteriormente convertidos em DAGs do Apache Airflow.

Esta seção descreve as decisões de arquitetura do projeto: as tecnologias que compõem o ambiente e como os dados fluem entre as camadas até chegarem ao dashboard.

## Nesta seção

- [Visão Geral](overview.md) — como Spark, Delta Lake e MinIO se combinam num ambiente Lakehouse e qual o fluxo dos dados de ponta a ponta.
- [Medalhão (Camadas)](medallion.md) — a organização dos dados em Landing, Bronze, Silver e Gold, com o papel e as transformações de cada camada.
