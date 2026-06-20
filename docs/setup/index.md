#  Guia de Setup do Ambiente

Bem-vindo ao guia oficial de implantação e configuração do ecossistema de Engenharia de Dados. Este espaço centraliza os procedimentos necessários para orquestrar e rodar toda a nossa infraestrutura de dados local e em nuvem.

---


##  Sumário de Configuração

Utilize os links abaixo para navegar pelas etapas sequenciais e obrigatórias de instalação:

* [**Etapa 1: Pré-requisitos e Credenciais**](prerequisites.md) – Configuração do arquivo `.env`, gerenciamento de chaves e acessos individuais ao MongoDB Atlas.
* [**Etapa 2: Executando o Projeto**](running.md) – Instruções de comandos do Docker, inicialização dos containers e verificação dos serviços (MinIO, Spark, Airflow).

---

##  Visão Geral da Infraestrutura

O nosso pipeline foi desenhado de forma modular, rodando sob containers isolados para garantir a reprodutibilidade. Configurando este setup, você terá acesso local a:

* **Apache Spark:** Processamento distribuído das camadas Bronze, Silver e Gold.
* **Apache Airflow:** Orquestração programática dos DAGs de ingestão.
* **MinIO:** Armazenamento de objetos simulando nosso Data Lake S3 (camadas de transição).
* **MongoDB Atlas:** Camada final de persistência analítica em nuvem.

Espero que esse novo visual da documentação e os slides ajudem muito o grupo! Qualquer outro ajuste que precisar, é só chamar.