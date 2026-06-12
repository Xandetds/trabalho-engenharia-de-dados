import pandas as pd
import numpy as np

print("--- Iniciando a geração de dados BRUTOS")

# Lendo os arquivos direto da pasta onde o script está rodando 
df_bruto = pd.read_csv('consulta_cand_2024_SP.csv', sep=';', encoding='latin1')
df_bens_bruto = pd.read_csv('bem_candidato_2024_SP.csv', sep=';', encoding='latin1')

print("Gerando as 10 tabelas com duplicatas, nulos e erros de formatacao...\n")

tabela_partido = df_bruto[['NR_PARTIDO', 'SG_PARTIDO', 'NM_PARTIDO']].copy()
tabela_partido['NM_PARTIDO'] = tabela_partido['NM_PARTIDO'].apply(
    lambda x: str(x).lower() if np.random.rand() > 0.5 else str(x).upper()
)
tabela_partido.columns = ['NR_PARTIDO', 'SG_PARTIDO', 'NM_PARTIDO']

tabela_cargo = df_bruto[['CD_CARGO', 'DS_CARGO']].copy()
tabela_cargo.columns = ['CD_CARGO', 'DS_CARGO']

tabela_instrucao = df_bruto[['CD_GRAU_INSTRUCAO', 'DS_GRAU_INSTRUCAO']].copy()
tabela_instrucao.columns = ['CD_GRAU_INSTRUCAO', 'DS_GRAU_INSTRUCAO']

tabela_ocupacao = df_bruto[['CD_OCUPACAO', 'DS_OCUPACAO']].copy()
tabela_ocupacao.columns = ['CD_OCUPACAO', 'DS_OCUPACAO']

tabela_municipio = df_bruto[['SG_UF', 'SG_UE', 'NM_UE']].copy()
tabela_municipio.columns = ['SG_UF', 'SG_UE', 'NM_UE']

colunas_candidato = [
    'SQ_CANDIDATO', 'NM_CANDIDATO', 'NM_URNA_CANDIDATO', 'CD_GENERO', 'DS_COR_RACA',
    'CD_CARGO', 'NR_PARTIDO', 'SG_UE', 'CD_GRAU_INSTRUCAO', 'CD_OCUPACAO'
]
tabela_candidato = df_bruto[colunas_candidato].copy()
tabela_candidato.columns = [
    'SQ_CANDIDATO', 'NM_CANDIDATO', 'NM_URNA_CANDIDATO', 'CD_GENERO', 'DS_COR_RACA', 
    'CD_CARGO', 'NR_PARTIDO', 'SG_UE', 'CD_GRAU_INSTRUCAO', 'CD_OCUPACAO'
]

tabela_tipo_bem = df_bens_bruto[['CD_TIPO_BEM_CANDIDATO', 'DS_TIPO_BEM_CANDIDATO']].copy()
tabela_tipo_bem.columns = ['CD_TIPO_BEM_CANDIDATO', 'DS_TIPO_BEM_CANDIDATO']

colunas_bens = ['SQ_CANDIDATO', 'CD_TIPO_BEM_CANDIDATO', 'DS_BEM_CANDIDATO', 'VR_BEM_CANDIDATO']
tabela_bens = df_bens_bruto[colunas_bens].copy()
tabela_bens.columns = ['SQ_CANDIDATO', 'CD_TIPO_BEM_CANDIDATO', 'DS_BEM_CANDIDATO', 'VR_BEM_CANDIDATO']

tabela_bens_estatistica = tabela_bens[['SQ_CANDIDATO', 'VR_BEM_CANDIDATO']].copy()

tabela_situacao = df_bruto[['SG_UF', 'SG_UE', 'NM_COLIGACAO']].copy()
tabela_situacao.columns = ['SG_UF', 'SG_UE', 'NM_COLIGACAO']

print("Salvando os arquivos")

tabela_partido.to_csv('1_dim_partido.csv', index=False, encoding='utf-8')
tabela_cargo.to_csv('2_dim_cargo.csv', index=False, encoding='utf-8')
tabela_instrucao.to_csv('3_dim_grau_instrucao.csv', index=False, encoding='utf-8')
tabela_ocupacao.to_csv('4_dim_ocupacao.csv', index=False, encoding='utf-8')
tabela_municipio.to_csv('5_dim_municipio.csv', index=False, encoding='utf-8')
tabela_candidato.to_csv('6_fato_candidato.csv', index=False, encoding='utf-8')
tabela_tipo_bem.to_csv('7_dim_tipo_bem.csv', index=False, encoding='utf-8')
tabela_bens.to_csv('8_fato_bem.csv', index=False, encoding='utf-8')
tabela_bens_estatistica.to_csv('9_agg_bens.csv', index=False, encoding='utf-8')
tabela_situacao.to_csv('10_dim_coligacao.csv', index=False, encoding='utf-8')

print("\nFeito! 10 tabelas geradas na pasta.")