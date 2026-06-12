from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName('Trabalho_Eng_Dados')
    .master('local[*]')
    .config('spark.jars.packages', 'io.delta:delta-spark_2.12:3.2.0,org.apache.hadoop:hadoop-aws:3.3.4')
    .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension')
    .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog')
    .getOrCreate()
)

sc = spark.sparkContext
