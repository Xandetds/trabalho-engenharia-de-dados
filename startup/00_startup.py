import os
import boto3
from pymongo import MongoClient
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from botocore.client import Config

load_dotenv(override=True)

MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')

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

del MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY

##

load_dotenv()

def testar_conexao():
    print("Iniciando teste de conexão com MongoDB Atlas...")
    
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME")
    
    if not uri or not db_name:
        print("ERRO: Variáveis de ambiente MONGO_URI ou MONGO_DB_NAME não encontradas.")
        return

    try:
        client = MongoClient(uri)
        db = client[db_name]
        
        client.admin.command('ping')
        print("Ping bem-sucedido! Conectado ao MongoDB Atlas.\n")
        
        print(f"Buscando um documento de teste na collection 'partido'...")
        documento_teste = db['partido'].find_one()
        
        if documento_teste:
            print("Sucesso! Documento encontrado:")
            print(documento_teste)
        else:
            print("A collection 'partido' está vazia ou não existe.")
            
    except Exception as e:
        print(f"Erro ao conectar ou consultar o banco: {e}")

if __name__ == "__main__":
    testar_conexao()