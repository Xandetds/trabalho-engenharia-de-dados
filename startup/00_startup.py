import os
import boto3
from botocore.client import Config
from pyspark.sql import SparkSession
from dotenv import load_dotenv

load_dotenv(override=True)

MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')

if not all([MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY]):
    raise RuntimeError('Variáveis MINIO_* não definidas — confira o .env')

minio = boto3.client(
    's3',
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

spark = (
    SparkSession.builder
    .appName('Trabalho_Eng_Dados')
    .master('local[*]')
    .config('spark.jars.packages', 'io.delta:delta-spark_2.12:3.2.0,org.apache.hadoop:hadoop-aws:3.3.4')
    .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension')
    .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog')
    # MinIO / S3A
    .config('spark.hadoop.fs.s3a.endpoint', MINIO_ENDPOINT)
    .config('spark.hadoop.fs.s3a.access.key', MINIO_ACCESS_KEY)
    .config('spark.hadoop.fs.s3a.secret.key', MINIO_SECRET_KEY)
    .config('spark.hadoop.fs.s3a.path.style.access', 'true')
    .config('spark.hadoop.fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
    .config('spark.hadoop.fs.s3a.connection.ssl.enabled', 'false')
    .getOrCreate()
)

sc = spark.sparkContext

del MINIO_ENDPOINT
del MINIO_ACCESS_KEY
del MINIO_SECRET_KEY