# Camada Bronze para Camada Silver

A *Camada Silver* representa a "Single Source of Truth" (Fonte Única da Verdade). Aqui, os dados oriundos da camada Bronze passam por um processo rigoroso de limpeza, padronização e qualidade de dados.

## Regras de Qualidade e Limpeza

O notebook 03_silver.ipynb aplica transformações estruturais para garantir que os dados estejam prontos para modelagem. O processamento PySpark executa as seguintes etapas:

1. *Remoção de Artefatos da Origem:* A coluna _id (pertencente ao MongoDB) é descartada, pois não tem valor analítico.
2. *Deduplicação e Tratamento de Nulos:* Remoção de registros totalmente duplicados e exclusão de linhas com valores nulos em colunas de negócio.
3. *Padronização de Strings:* Todas as colunas de texto são limpas usando funções de trim (remover espaços vazios) e upper (caixa alta).
4. *Renomeação de Colunas:* Os prefixos técnicos do TSE são traduzidos para nomes amigáveis:
   * DT_ → DATA_
   * CD_ → CODIGO_
   * NM_ → NOME_
   * SG_ → SIGLA_
5. *Metadados de Processamento:* Adição da coluna data_hora_silver para rastreabilidade da camada.

### Exemplo do Pipeline de Limpeza:
```python
def limpar(df: DataFrame) -> DataFrame:
    df = remover_id(df)               # Remove '_id'
    df = padronizar_strings(df)       # Aplica UPPER e TRIM
    df = remover_duplicatas(df)       # Drop Duplicates
    df = tratar_nulos(df)             # Drop NA
    df = adicionar_timestamp_silver(df)
    df = renomear_colunas(df)         # Traduz prefixos do TSE
    return df
```