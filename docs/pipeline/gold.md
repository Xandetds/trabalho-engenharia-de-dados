# Camada Silver para Camada Gold

A *Camada Gold* é o destino final do processamento. O foco desta etapa é estruturar os dados de forma agregada e otimizada para o consumo direto pelas ferramentas de visualização (neste caso, o Dashboard em Streamlit).

## Modelagem Dimensional (Star Schema)

O notebook 04_gold.ipynb lê os dados limpos da camada Silver e os remodela em um formato de Tabelas Fato e Dimensão, facilitando as agregações e filtros de negócio.

### Tabelas Fato:
Concentram as métricas numéricas e as chaves estrangeiras (FKs).
* *fato_candidatura_dashboard:* Tabela principal contendo as chaves do candidato, cargo, partido, município, grau de instrução, ocupação, gênero e raça.
* *fato_bem_candidato_dashboard:* Tabela associativa com a descrição detalhada e o valor (double) dos bens declarados pelos candidatos.

### Tabelas Dimensão:
Concentram os atributos descritivos que serão usados nos filtros do dashboard.
* *dim_cargo:* Código e descrição do cargo (Ex: Prefeito, Vereador).
* *dim_partido:* Número, sigla e nome dos partidos.
* *dim_municipio:* Sigla da UF, código e nome do município.

### Exemplo de Estruturação (Dimensão Partido):
```python
dim_partido = (
    partido
    .select(
        F.col("id_partido").alias("numero_partido"),
        F.col("sigla").alias("sigla_partido"),
        F.col("nome").alias("nome_partido")
    )
)

dim_partido.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .save("s3a://gold/tse/dim_partido")
```