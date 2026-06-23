# O que é o Dashboard?

O Dashboard é uma aplicação web interativa construída em **Streamlit** que atua como a camada de entrega final (**One Page View**) do projeto. Ele foi projetado para consumir diretamente as tabelas fato e dimensão agregadas que passaram por todo o processo de extração, limpeza e enriquecimento ao longo da nossa esteira de dados.

### Principais Objetivos do Painel:
* **Facilidade de Acesso:** Apresentar uma visão unificada dos dados eleitorais sem a necessidade de interações diretas com os bancos de dados por parte do usuário final.
* **Decisões Baseadas em Dados:** Permitir a filtragem dinâmica de candidaturas, partidos e faturamentos para análise de cenários eleitorais.
* **Consumo Eficiente:** Ler de forma otimizada os arquivos estruturados gerados pelo ecossistema de processamento distribuído.

---

## Estrutura da Documentação

Para facilitar a navegação e o entendimento do projeto pelos desenvolvedores e membros da equipe, a documentação foi dividida nos seguintes módulos:

- [Apresentação](index.md): Visão geral da ferramenta e proposta de valor do painel.
- [Explicação Negócio e Contexto Eleitoral](business.md):** Análise do contexto eleitoral, lógica de consolidação de métricas e detalhamento das regras de negócio aplicadas.
- [Documentação Técnica](technical.md):** Detalhamento da arquitetura de software, estrutura de desenvolvimento baseada em *branches* isoladas, configuração do ambiente Docker, integração do Jupyter Notebook e guia de execução unificada via Compose.  

---

## Tecnologias Principais da Solução

O ecossistema que suporta este dashboard é composto pelas seguintes tecnologias integradas:

* **Streamlit:** Framework em Python utilizado para a criação rápida da interface web e renderização dos gráficos analíticos.
* **Docker:** Tecnologia de conteinerização utilizada para isolar a aplicação, garantindo que o dashboard rode com o mesmo comportamento em qualquer máquina de desenvolvimento.
* **MinIO:** Servidor de armazenamento de objetos de alta performance que simula nosso Data Lake local, guardando os arquivos estruturados da camada Gold.
* **MongoDB Atlas:** Banco de dados NoSQL baseado em nuvem utilizado para armazenar e consultar metadados cruciais e coleções dinâmicas do projeto.