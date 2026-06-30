# Landing para Camada Bronze

A *Camada Bronze* é onde os dados brutos da Landing Zone são convertidos para um formato colunar de alta performance (*Delta Lake*) e recebem os primeiros metadados essenciais para rastreabilidade e governança.

## Transformações e Metadados

O notebook 02_bronze.ipynb utiliza o *PySpark* para processar os arquivos JSON. O schema original é mantido, mas as seguintes colunas de metadados são injetadas em todas as tabelas:

* data_hora_bronze: Timestamp exato do momento em que o dado foi processado nesta camada.
* fonte_dados: String indicando a origem exata do dado (ex: landing.tse.candidatura).

### Exemplo de Processamento:
```python
from pyspark.sql.functions import current_timestamp, lit
```
#### Leitura do JSON bruto
```python
df_candidatura = spark.read.option("multiline", "true").json("s3a://landing/tse/candidatura.json")
```
#### Adição de metadados de governança
```python
df_candidatura = df_candidatura \
    .withColumn("data_hora_bronze", current_timestamp()) \
    .withColumn("fonte_dados", lit("landing.tse.candidatura"))
```
#### Escrita em formato Delta Lake
```python
df_candidatura.write.format("delta").mode("overwrite").save("s3a://bronze/tse/candidatura")
```