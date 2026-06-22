# Explicação Negócio e Contexto Eleitoral

O dashboard consolida os indicadores finais sobre o panorama das candidaturas eleitorais brasileiras. A lógica de negócio consiste em extrair os dados brutos de registros e prestações de contas, validar as informações transacionais contra as coleções armazenadas no MongoDB Atlas, e estruturar métricas agregadas por partido, cargo e região. 

Esses dados limpos e enriquecidos são armazenados na camada **Gold** do Data Lake (MinIO) no formato Parquet, permitindo que o painel Streamlit realize consultas analíticas rápidas de alto desempenho sem sobrecarregar os sistemas operacionais originais.
---

## Tabelas Gold consumidas

| Tabela | Tipo | Descrição |
|---|---|---|
| `fato_candidatura_dashboard` | Fato | Cada registro representa uma candidatura, com chaves para cargo, partido, municipio, grau de instrução, ocupação, genero e cor/raça |
| `fato_bem_candidato_dashboard` | Fato | Bens declarados por candidato, com tipo do bem, descrição e valor monetário |
| `dim_cargo` | Dimensão | Código e descrição dos cargos eletivos |
| `dim_partido` | Dimensão | Número, sigla e nome dos partidos |
| `dim_municipio` | Dimensão | Sigla da UF, código e nome do municipio (disponível na Gold, não consumida pelo dashboard atual) |

Todas as tabelas são gravadas em formato **Delta Lake** no bucket `gold` do MinIO,
sob o prefixo `tse/` (ex.: `gold/tse/fato_candidatura_dashboard/`).

---

## KPIs (cards superiores)

O dashboard exibe quatro KPIs no topo da página:

### 1. Total de candidatos

- **Descrição:** quantidade de candidatos distintos registrados.
- **Fórmula:** contagem de valores distintos de `sq_candidato` na tabela `fato_candidatura_dashboard`.
- **Código:** `kpis.calculate_total_candidates`

### 2. Total de partidos

- **Descrição:** quantidade de partidos distintos com pelo menos uma candidatura.
- **Fórmula:** contagem de valores distintos de `numero_partido` na tabela `fato_candidatura_dashboard`.
- **Código:** `kpis.calculate_total_parties`

### 3. Total de municipios

- **Descrição:** quantidade de municipios distintos que possuem candidaturas.
- **Fórmula:** contagem de valores distintos de `sigla_ue` na tabela `fato_candidatura_dashboard`.
- **Código:** `kpis.calculate_total_municipalities`

### 4. Total de bens declarados

- **Descrição:** soma do patrimônio declarado por todos os candidatos.
- **Fórmula:** `SUM(valor_bem_candidato)` sobre todos os registros da tabela `fato_bem_candidato_dashboard`. Valores nulos ou inválidos são tratados como zero.
- **Formato:** moeda brasileira (`R$ X.XXX,XX`).
- **Código:** `kpis.calculate_total_declared_assets`

---

## Métricas (gráficos)

Abaixo dos KPIs o dashboard exibe dois gráficos de barras horizontais:

### 1. Candidatos por cargo

- **Descrição:** distribuição de candidatos por cargo eletivo, ordenada do cargo com mais candidatos para o com menos.
- **Fórmula:**
    1. Para cada registro de `fato_candidatura_dashboard`, associa `codigo_cargo` ao `sq_candidato`.
    2. Agrupa por `codigo_cargo` e conta candidatos distintos (`COUNT(DISTINCT sq_candidato)`).
    3. Faz *join* com `dim_cargo` para obter `descricao_cargo`.
    4. Ordena por total de candidatos decrescente.
- **Tabelas:** `fato_candidatura_dashboard` + `dim_cargo`
- **Código:** `kpis.calculate_candidates_by_office`

### 2. Patrimônio por partido

- **Descrição:** soma do patrimônio declarado por partido, exibindo os 10 partidos com maior patrimônio.
- **Fórmula:**
    1. Associa cada candidato ao seu partido via `fato_candidatura_dashboard` (`sq_candidato` → `numero_partido`).
    2. Para cada registro de `fato_bem_candidato_dashboard`, identifica o partido do candidato e soma `valor_bem_candidato` por partido (`SUM(valor_bem_candidato) GROUP BY partido`).
    3. Faz *join* com `dim_partido` para obter `sigla_partido`.
    4. Ordena por patrimônio decrescente e exibe os 10 primeiros.
- **Tabelas:** `fato_candidatura_dashboard` + `fato_bem_candidato_dashboard` + `dim_partido`
- **Formato:** moeda brasileira (`R$ X.XXX,XX`).
- **Código:** `kpis.calculate_assets_by_party`

---

## Como executar o dashboard

### Via Docker Compose (recomendado)

O dashboard é um serviço do `docker-compose.yml` e sobe junto com o MinIO:

```bash
docker compose up --build
```

Após a inicialização, acesse **http://localhost:8501**.

**Pré-requisitos:**

- O arquivo `.env` na raiz do projeto deve conter `MINIO_ACCESS_KEY` e `MINIO_SECRET_KEY`.
- O MinIO deve estar acessível e o bucket `gold` deve conter as tabelas listadas acima. Para isso, execute os notebooks na ordem (`00_setup_buckets` → `01_landing` → `02_bronze` → `03_silver` → `04_gold`) antes de acessar o dashboard.

### Variáveis de ambiente

| Variável | Descrição | Valor padrão |
|---|---|---|
| `MINIO_ACCESS_KEY` | Chave de acesso do MinIO | *(obrigatória)* |
| `MINIO_SECRET_KEY` | Chave secreta do MinIO | *(obrigatória)* |
| `MINIO_DASHBOARD_ENDPOINT` | URL da API S3 do MinIO | `http://localhost:9020` (local) / `http://minio:9000` (compose) |
| `MINIO_GOLD_BUCKET` | Nome do bucket Gold | `gold` |
| `MINIO_GOLD_PREFIX` | Prefixo das tabelas dentro do bucket | `tse` |

---

## Como validar o dashboard

1. **Pipeline completo:** execute todos os notebooks (`00` a `04`) no Jupyter Lab para garantir que as tabelas Gold existem no MinIO.
2. **Verificar tabelas no MinIO:** acesse o console do MinIO em http://localhost:9021 e confirme que o bucket `gold` contém as pastas `tse/fato_candidatura_dashboard/`, `tse/fato_bem_candidato_dashboard/`, `tse/dim_cargo/`, `tse/dim_partido/` e `tse/dim_municipio/`.
3. **Abrir o dashboard:** acesse http://localhost:8501 e verifique:
    - Os 4 KPIs no topo exibem valores numéricos (não zero e sem erros).
    - O gráfico "Candidatos por cargo" mostra barras com os cargos eletivos.
    - O gráfico "Patrimônio por partido" mostra barras com os 10 maiores partidos.
4. **Validação cruzada:** compare os valores dos KPIs com a contagem de registros obtida na célula de validação do notebook `04_gold.ipynb` (seção 8).
