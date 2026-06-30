# Especificação Técnica do Dashboard (Camada de Visualização)

Este documento detalha a arquitetura técnica, as ferramentas de desenvolvimento e a estrutura de código utilizadas exclusivamente para a construção e execução do **Dashboard TSE**.

>  **Lembrete Importante:** Para que o dashboard funcione corretamente, é necessário que toda a infraestrutura conteinerizada tenha sido inicializada previamente através do comando `docker-compose up -d --build` na raiz do projeto. Após o deploy dos containers, o painel interativo estará disponível para visualização no endereço: **[http://localhost:8501](http://localhost:8501)**.

---

##  Stack Tecnológica do Dashboard

O aplicativo de visualização foi construído de forma isolada do pipeline de dados, utilizando as seguintes tecnologias:

* **Linguagem Base:** Python 3.11
* **Framework Web:** Streamlit (para renderização dos gráficos interativos e componentes de interface)
* **Gerenciamento de Pacotes:** Poetry (garantindo um ambiente virtual isolado com `pyproject.toml` e `poetry.lock`)
* **Consumo de Dados:** PyArrow / Pandas (para leitura rápida das tabelas Delta/Parquet já consolidadas)

---

##  Arquitetura e Modularização do Código

O código do dashboard foi componentizado dentro do diretório `dashboard/` para facilitar a manutenção e garantir uma boa organização de software:

* **`app.py`:** Ponto de entrada do aplicativo. Gerencia o layout principal da página (One Page View), as barras laterais de filtros e a renderização final dos blocos visuais.
* **`kpis.py`:** Módulo isolado responsável pelo cálculo e formatação dos 4 indicadores principais exibidos nos cards do topo (Total de Candidatos, Total de Partidos, Total de Municípios e Bens Declarados).
* **`gold_reader.py`:** Camada de acesso a dados que faz as consultas e queries nas tabelas da camada Gold, aplicando os filtros selecionados pelo usuário na interface.
* **`minio_connection.py`:** Gerencia a conexão segura do Streamlit com o servidor local do MinIO utilizando as credenciais contidas no arquivo `.env`.

---

##  Containerização e Portas

O dashboard roda dentro de um container Docker dedicado, configurado para subir automaticamente junto com a stack do projeto.

* **Porta Padrão:** `8501` (Acessível localmente em `http://localhost:8501`)
* **Mapeamento de Rede:** O container do dashboard conecta-se à rede interna do Compose para ler o MinIO diretamente através do endpoint configurado.
* **Volume:** O diretório de código do dashboard é montado em modo de leitura para permitir atualizações em tempo real durante o desenvolvimento (*hot reload*).

---

##  Estrutura de Consumo da Camada Gold

O dashboard não faz nenhum tratamento pesado ou limpeza de dados. Ele assume que os dados estão 100% limpos e consome diretamente as seguintes tabelas estruturadas do bucket `gold`:

1. **`fato_candidatura_dashboard`** e **`fato_bem_candidato_dashboard`** para gerar volumetrias e somatórios de patrimônio.
2. **`dim_cargo`**, **`dim_partido`** e **`dim_municipio`** para alimentar os componentes de filtros da barra lateral.