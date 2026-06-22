# Camada Landing (Raw)

A *Landing Zone* é a porta de entrada do nosso Data Lake. O objetivo desta camada é extrair os dados diretamente do sistema transacional de origem (*MongoDB Atlas*) e armazená-los em seu formato bruto, sem nenhuma transformação de negócio.

## Ingestão de Dados

O notebook 01_landing.ipynb conecta-se ao MongoDB e varre todas as coleções do banco (como bens, candidatura, partido, etc.).

Como o requisito do projeto determina a passagem de NoSQL para *JSON*, utilizamos um MongoEncoder customizado para lidar com tipos específicos do MongoDB (como ObjectId e datetime) antes de salvar os arquivos no MinIO.

### Fluxo de Extração:
1. Conexão ao MongoDB via pymongo.
2. Listagem das 10 coleções eleitorais disponíveis.
3. Conversão de cada coleção para uma string JSON (com suporte a caracteres UTF-8).
4. Upload direto para o bucket landing usando o cliente do MinIO.

### Exemplo do Serializador Customizado:
```python
class MongoEncoder(json.JSONEncoder):
    """Serializa tipos do MongoDB que o json padrão não suporta."""
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)
```