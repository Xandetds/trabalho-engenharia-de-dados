# Projeto Pipeline de Dados Eleitorais - TSE (Arquitetura Medalhão Local)

Projeto desenvolvido para a disciplina de Engenharia de Dados, focado na construção de um ecossistema de dados completo, automatizado e conteinerizado utilizando a **Arquitetura Medalhão (Lakehouse)**. O pipeline realiza a extração de dados brutos de uma base NoSQL na nuvem (**MongoDB Atlas**), processa e limpa os fluxos de forma distribuída via **Apache Spark (PySpark)** e consolida uma modelagem dimensional em um Data Lake local (**MinIO**) para alimentar um **Dashboard Analítico** interativo.

---

## Funcionalidades

* **Extração NoSQL para JSON:** Conexão nativa e segura com o MongoDB Atlas via `pymongo`, convertendo coleções transacionais brutas diretamente para formato JSON estruturado.
* **Esteira de Dados Medalhão:** Implementação física completa e distribuída das camadas **Landing, Bronze, Silver e Gold** utilizando tabelas **Delta Lake**.
* **Orquestração Inteligente (Airflow + Papermill):** Controle absoluto do pipeline feito por uma DAG no Apache Airflow, rodando e monitorando os Jupyter Notebooks de forma sequencial com injeção automática de parâmetros e logs.
* **Modelagem Dimensional Otimizada:** Construção de um modelo *Star Schema* (Fatos e Dimensões) na camada Gold, maximizando a performance das queries.
* **Entrega em One Page View:** Interface rica em Dark Mode construída em **Streamlit**, gerando relatórios de candidatos por cargo e patrimônio por partido através de leitura direta e rápida da camada Gold.
* **Documentação Viva:** Portal de documentação interna centralizado e gerado via **MkDocs**.

---

## Arquitetura do Ecossistema

O fluxo de dados foi desenhado para garantir isolamento e qualidade da informação em cada etapa da jornada analítica:

```mermaid
graph LR
    %% Fontes e Destinos
    Origem[(MongoDB Atlas <br> Origem NoSQL)]
    Landing[Landing Zone <br> JSON Bruto]
    Bronze[Camada Bronze <br> Delta Lake]
    Silver[Camada Silver <br> Delta Lake]
    Gold[Camada Gold <br> Star Schema]
    Dash[Dashboard <br> Streamlit]

    %% Conexões e Processamento
    Origem -->|01_landing.ipynb| Landing
    Landing -->|02_bronze.ipynb <br> Tipagem e Metadados| Bronze
    Bronze -->|03_silver.ipynb <br> Limpeza e Padronização| Silver
    Silver -->|04_gold.ipynb <br> Agregação e Relacionamento| Gold
    Gold -.->|Leitura Direta| Dash

    %% Estilos para Dark Mode
    style Origem fill:#1B5E20,stroke:#4CAF50,stroke-width:2px,color:#FFF
    style Landing fill:#303030,stroke:#9E9E9E,stroke-width:2px,color:#FFF
    style Bronze fill:#4E342E,stroke:#A1887F,stroke-width:2px,color:#FFF
    style Silver fill:#37474F,stroke:#90A4AE,stroke-width:2px,color:#FFF
    style Gold fill:#F9A825,stroke:#FFF176,stroke-width:2px,color:#111
    style Dash fill:#B71C1C,stroke:#E57373,stroke-width:2px,color:#FFF
```

## Tecnologias Utilizadas
- **Apache Spark (PySpark):** Engine principal de processamento distribuído das transformações.

- **Delta Lake:** Formato de armazenamento transacional ACID adotado a partir da Bronze.

- **Apache Airflow & Papermill:** Orquestrador de dependências e executor programático de notebooks.

- **MongoDB Atlas:** Banco de dados transacional na nuvem utilizado como origem (NoSQL).

- **MinIO:** Storage de objetos local (S3-compatible) simulando nosso Data Lake corporativo.

- **Streamlit:** Framework Python focado em aplicações de dados para construção do dashboard.

- **Docker & Docker Compose:** Isolamento, reprodutibilidade e gerenciamento de rede de toda a stack.

- **Poetry & MkDocs:** Gerenciador de ambientes virtuais e gerador do portal estático.

## Como Executar o Projeto
Antes de começar, certifique-se de ter o Docker e o Docker Compose instalados na sua máquina de desenvolvimento.

### 1. Inicializando a Infraestrutura (Containers)
Crie um arquivo .env na raiz do projeto com base no .env.example inserindo suas credenciais do MongoDB Atlas e do MinIO. Em seguida, suba toda a stack executando:

```bash
docker-compose up -d --build
```

Isso inicializará de forma integrada:

- **Jupyter Lab (Spark-Lab):** Rodando em http://localhost:8888

- **MinIO Console:** Rodando em http://localhost:9021 (API na porta 9000)

- **Apache Airflow:** Rodando em http://localhost:8080

- **Dashboard Streamlit:** Rodando em http://localhost:8501

### 2. Executando a Esteira de Dados (Orquestração)

1. Acesse o painel do Airflow em http://localhost:8080 (Usuário e senha padrão configurados no seu .env).

2. Localize a DAG tse_medallion_papermill.

3. Ative a DAG (mude a chave para Unpause) e clique no botão de Trigger (Play) para rodar o pipeline completo.

4. O Airflow executará sequencialmente os notebooks do diretório notebook/, injetará os metadados e persistirá as evidências de execução no volume compartilhado papermill-output.

### 3. Visualizando o Dashboard Analítico
Assim que a DAG concluir com sucesso (ficar verde até a tarefa da Gold), os dados estruturados estarão prontos.

- Acesse http://localhost:8501 no navegador para interagir com os filtros eleitorais e gráficos consolidados do painel do TSE.

### 4. Visualizando a Documentação Local (MkDocs)
Para explorar as transformações exatas feitas campo a campo nas camadas Silver e Gold:

```bash
# Instalar dependências locais via Poetry
poetry install

# Inicializar o servidor do MkDocs
poetry run mkdocs serve
```

- Acesse http://127.0.0.1:8000 para ler o portal completo com diagramas interativos.

## Equipe

Abaixo encontra-se a estrutura de governança, ocupação e os links diretos para os perfis profissionais de cada integrante do time de Engenharia de Dados.

| Integrante | Ocupação | Links de Contato |
| :--- | :--- | :--- |
| **Alexandre Tibes da Silva** | Analista de Suporte e Implantação |  [GitHub](https://github.com/Xandetds) |
| **Bruno Monteiro Bonifacio** | Desenvolvedor JR |  [GitHub](https://github.com/brunomonteirobonifacio) \| [LinkedIn](https://www.linkedin.com/in/bruno-monteiro-bonif%C3%A1cio-257338272/) |
| **Gianluca Andrade Silvestre** | Desenvolvedor PL |  [GitHub](https://github.com/GiaNinWorld) \| [LinkedIn](https://www.linkedin.com/in/gianluca-andrade-silvestre-6205622b8/) |
| **Gustavo de Freitas Cardoso** | Produção de Persianas |  [GitHub](https://github.com/GustavodeFreitasCardoso) |
| **João Miguel Fortunato Rita** | Desenvolvedor JR |  [GitHub](https://github.com/JoaoMiguelRita) \| [LinkedIn](https://www.linkedin.com/in/jo%C3%A3o-miguel-fortunato-rita-623962219/) |
| **Luis Filipe Damiani Colombo** | Analista de Suporte |  [GitHub](https://github.com/luisfilipedm) \| [LinkedIn](https://www.linkedin.com/in/luis-filipe-damiani-colombo-b060572b6/) |
| **Murilo Salvan** | Manutenção Eletrônica |  [GitHub](https://github.com/omrl) \| [LinkedIn](https://www.linkedin.com/in/murilo-salvan-1605b9382/) |
| **Roger Balcevicz** | Desenvolvedor JR |  [GitHub](https://github.com/Roger-Balcevicz) \| [LinkedIn](https://www.linkedin.com/in/roger-balcevicz-426053381/) |

---

## Referências Técnicas

* **[Streamlit Docs](https://docs.streamlit.io/)**: Referência para componentes visuais e estados do app.
* **[Apache Spark Python API](https://spark.apache.org/docs/latest/api/python/index.html)**: Guia de funções distribuídas e manipulação de DataFrames.
* **[Delta Lake Core Guide](https://docs.delta.io/latest/index.html)**: Otimizações e gravações em formato ACID.
* **[Papermill Documentation](https://papermill.readthedocs.io/)**: Lógica de parametrização e execução de notebooks via terminal/Python.
* **[Apache Airflow Architecture](https://airflow.apache.org/docs/apache-airflow/stable/index.html)**: Melhores práticas para definição de DAGs e PythonOperators.