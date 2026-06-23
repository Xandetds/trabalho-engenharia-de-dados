# Engenharia de Dados · SATC

<div class="grid cards" markdown>

-   :material-lightning-bolt:{ .lg .middle } **Pipeline End-to-End**

    ---

    Ingestão, transformação e disponibilização de dados usando Apache Spark, Delta Lake e MinIO com arquitetura medalhão.

    [:octicons-arrow-right-24: Ver arquitetura](architecture/index.md)

-   :material-layers-triple:{ .lg .middle } **Arquitetura Medalhão**

    ---

    Dados organizados em camadas Landing, Bronze, Silver e Gold com controle de qualidade em cada etapa.

    [:octicons-arrow-right-24: Ver camadas](architecture/medallion.md)

-   :material-chart-bar:{ .lg .middle } **Dashboard**

    ---

    4 KPIs e 2 métricas visualizados em painel One Page View consumindo direto da camada Gold.

    [:octicons-arrow-right-24: Ver dashboard](dashboard.md)

-   :material-account-group:{ .lg .middle } **Equipe**

    ---

    Projeto desenvolvido por 8 integrantes como trabalho final da disciplina de Engenharia de Dados.

    [:octicons-arrow-right-24: Ver equipe](team.md)

</div>

## Tecnologias utilizadas

| Categoria | Tecnologia |
|---|---|
| Processamento | Apache Spark / PySpark |
| Formato de dados | Delta Lake |
| Object Storage | MinIO |
| Banco de origem | MongoDB Atlas |
| Orquestração | Airflow |
| Ambiente | Docker / JupyterLab |
| Documentação | MkDocs Material |

## Estrutura do projeto

```
trabalho-engenharia-de-dados/
├── docker/             # Dockerfiles da infraestrutura
├── docker-compose.yml  # Sobe todos os serviços
├── notebook/           # Notebooks PySpark por camada
├── docs/               # Documentação (MkDocs)
└── pyproject.toml      # Dependências do projeto
```
