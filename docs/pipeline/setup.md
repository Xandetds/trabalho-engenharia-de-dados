# Setup da Infraestrutura

A primeira etapa do nosso pipeline garante que a infraestrutura de armazenamento (Data Lake) esteja pronta para receber os dados. O script de setup conecta-se ao *MinIO* e cria os buckets necessários para cada camada da arquitetura Medallion.

## Inicialização dos Buckets

O script utiliza a biblioteca boto3 (ou cliente similar do MinIO) para verificar a existência dos buckets e criá-los caso não existam.

```python
def ensure_bucket(bucket_name):
    try:
        minio.head_bucket(Bucket=bucket_name)
        print(f'Bucket [{bucket_name}] já existe')
    except:
        minio.create_bucket(Bucket=bucket_name)
        print(f'Bucket [{bucket_name}] criado!')
```


### Criação das 4 camadas base
```python
ensure_bucket('landing')
ensure_bucket('bronze')
ensure_bucket('silver')
ensure_bucket('gold')
```