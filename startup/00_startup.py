import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName('Trabalho_Eng_Dados')
    .master('local[*]')
    .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension')
    .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog')
    .getOrCreate()
)

sc = spark.sparkContext

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