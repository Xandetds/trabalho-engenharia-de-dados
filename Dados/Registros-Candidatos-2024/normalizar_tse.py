import pandas as pd

# =========================================================
# ETAPA 1: PROCESSANDO OS CANDIDATOS (TABELAS 1 A 6 E 10)
# =========================================================
print("--- Iniciando a Primeira Etapa: Processando os Candidatos ---")
print("Carregando os dados brutos de candidatos...")

# Buscando o arquivo na pasta ao lado usando "../"
df_bruto = pd.read_csv('../consulta_cand_2024/consulta_cand_2024_SP.csv', sep=';', encoding='latin1')
print(f"Total de registros de candidatos carregados: {len(df_bruto)} linhas\n")

print("Iniciando a quebra em tabelas normalizadas de candidatos...")

# TABELA 1: Partido
tabela_partido = df_bruto[['NR_PARTIDO', 'SG_PARTIDO', 'NM_PARTIDO']].drop_duplicates().dropna()
tabela_partido.columns = ['id_partido', 'sigla', 'nome']

# TABELA 2: Cargo
tabela_cargo = df_bruto[['CD_CARGO', 'DS_CARGO']].drop_duplicates().dropna()
tabela_cargo.columns = ['id_cargo', 'descricao']

# TABELA 3: Grau de Instrução
tabela_instrucao = df_bruto[['CD_GRAU_INSTRUCAO', 'DS_GRAU_INSTRUCAO']].drop_duplicates().dropna()
tabela_instrucao.columns = ['id_grau_instrucao', 'descricao']

# TABELA 4: Ocupação
tabela_ocupacao = df_bruto[['CD_OCUPACAO', 'DS_OCUPACAO']].drop_duplicates().dropna()
tabela_ocupacao.columns = ['id_ocupacao', 'descricao']

# TABELA 5: Município
tabela_municipio = df_bruto[['SG_UF', 'SG_UE', 'NM_UE']].drop_duplicates().dropna()
tabela_municipio.columns = ['sigla_uf', 'id_municipio', 'nome']

# TABELA 6: Candidatos
colunas_candidato = [
    'SQ_CANDIDATO', 'NM_CANDIDATO', 'NM_URNA_CANDIDATO', 'CD_GENERO', 'DS_COR_RACA',
    'CD_CARGO', 'NR_PARTIDO', 'SG_UE', 'CD_GRAU_INSTRUCAO', 'CD_OCUPACAO'
]
tabela_candidato = df_bruto[colunas_candidato].drop_duplicates().dropna()
tabela_candidato.columns = [
    'id_candidatura', 'nome_completo', 'nome_urna', 'genero', 'cor_raca', 
    'id_cargo_fk', 'id_partido_fk', 'id_municipio_fk', 'id_grau_instrucao_fk', 'id_ocupacao_fk'
]

# TABELA 10: Coligações (Mais de 50 registros reais e dinâmicos do TSE)
tabela_situacao = df_bruto[['SG_UF', 'SG_UE', 'NM_COLIGACAO']].drop_duplicates().dropna()
tabela_situacao.columns = ['sigla_uf', 'id_municipio_fk', 'nome_coligacao']

# =========================================================
# ETAPA 2: PROCESSANDO OS BENS (TABELAS 7 A 9)
# =========================================================
print("\n--- Iniciando a Segunda Etapa: Processando os Bens ---")
print("Carregando os dados brutos de bens...")

# Lendo o arquivo de bens na pasta atual
df_bens_bruto = pd.read_csv('bem_candidato_2024_SP.csv', sep=';', encoding='latin1')
print(f"Total de registros de bens carregados: {len(df_bens_bruto)} linhas\n")

print("Iniciando a quebra em tabelas normalizadas de bens...")

# TABELA 7: Tipo de Bem
tabela_tipo_bem = df_bens_bruto[['CD_TIPO_BEM_CANDIDATO', 'DS_TIPO_BEM_CANDIDATO']].drop_duplicates().dropna()
tabela_tipo_bem.columns = ['id_tipo_bem', 'descricao']

# TABELA 8: Bens Detalhados
colunas_bens = ['SQ_CANDIDATO', 'CD_TIPO_BEM_CANDIDATO', 'DS_BEM_CANDIDATO', 'VR_BEM_CANDIDATO']
tabela_bens = df_bens_bruto[colunas_bens].dropna().copy()
tabela_bens['VR_BEM_CANDIDATO'] = tabela_bens['VR_BEM_CANDIDATO'].astype(str).str.replace(',', '.').astype(float)
tabela_bens.columns = ['id_candidatura_fk', 'id_tipo_bem_fk', 'descricao_detalhada', 'valor']

# TABELA 9: Estatísticas de Patrimônio
tabela_bens_estatistica = tabela_bens.groupby('id_candidatura_fk').agg(
    total_bens_declarados=('valor', 'count'),
    patrimonio_total=('valor', 'sum'),
    maior_bem_valor=('valor', 'max')
).reset_index()


# =========================================================
# SALVANDO TUDO
# =========================================================
print("\nSalvando todos os arquivos CSV normalizados...")

tabela_partido.to_csv('1_tabela_partido.csv', index=False, encoding='utf-8')
tabela_cargo.to_csv('2_tabela_cargo.csv', index=False, encoding='utf-8')
tabela_instrucao.to_csv('3_tabela_instrucao.csv', index=False, encoding='utf-8')
tabela_ocupacao.to_csv('4_tabela_ocupacao.csv', index=False, encoding='utf-8')
tabela_municipio.to_csv('5_tabela_municipio.csv', index=False, encoding='utf-8')
tabela_candidato.to_csv('6_tabela_candidatura.csv', index=False, encoding='utf-8')
tabela_tipo_bem.to_csv('7_tabela_tipo_bem.csv', index=False, encoding='utf-8')
tabela_bens.to_csv('8_tabela_bens.csv', index=False, encoding='utf-8')
tabela_bens_estatistica.to_csv('9_tabela_bens_estatistica.csv', index=False, encoding='utf-8')
tabela_situacao.to_csv('10_tabela_situacao.csv', index=False, encoding='utf-8')

print("\n¡PROJETO CONCLUÍDO COM SUCESSO!")
print("As 10 tabelas legítimas e normalizadas foram geradas com sucesso na sua pasta.")
print(f"Linhas em Candidaturas: {len(tabela_candidato)} | Linhas em Bens: {len(tabela_bens)} | Linhas em Coligações: {len(tabela_situacao)}")