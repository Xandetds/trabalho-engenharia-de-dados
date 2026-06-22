import json
import streamlit as st
import streamlit.components.v1 as components

from gold_reader import (
    inspect_expected_gold_paths,
    list_gold_objects,
    read_gold_sample,
    read_gold_table_records,
)
from kpis import (
    calculate_total_candidates,
    calculate_total_declared_assets,
    calculate_total_municipalities,
    calculate_total_parties,
)
from minio_connection import list_buckets

st.set_page_config(
    page_title="Dashboard TSE",
    layout="wide",
)

st.title("Dashboard TSE")

try:
    buckets = list_buckets()
    gold_objects = list_gold_objects()
    gold_paths = inspect_expected_gold_paths()
    gold_sample = read_gold_sample()
    candidate_records = read_gold_table_records("fato_candidatura_dashboard")
    asset_records = read_gold_table_records("fato_bem_candidato_dashboard")
    total_candidates = calculate_total_candidates(candidate_records)
    total_parties = calculate_total_parties(candidate_records)
    total_municipalities = calculate_total_municipalities(candidate_records)
    total_declared_assets = calculate_total_declared_assets(asset_records)

    components.html(
        f"""
        <script>
        console.log("Conexão com MinIO realizada com sucesso.");
        console.log("Buckets encontrados:", {json.dumps(buckets)});
        console.log("Caminhos esperados da camada Gold:", {json.dumps(gold_paths)});
        console.log("Objetos encontrados na camada Gold:", {json.dumps(gold_objects)});
        console.log("Amostra lida da camada Gold:", {json.dumps(gold_sample)});
        console.log("Total de candidatos:", {json.dumps(total_candidates)});
        console.log("Total de partidos:", {json.dumps(total_parties)});
        console.log("Total de municípios:", {json.dumps(total_municipalities)});
        console.log("Total de bens declarados:", {json.dumps(str(total_declared_assets))});
        </script>
        """,
        height=0,
    )

    st.subheader("KPIs")

    kpi_candidates, kpi_parties, kpi_municipalities, kpi_declared_assets = st.columns(4)

    if total_candidates:
        kpi_candidates.metric("Total de candidatos", f"{total_candidates:,}".replace(",", "."))
    else:
        st.warning("Tabela `fato_candidatura_dashboard` ainda não possui dados legíveis para calcular o KPI.")

    if total_parties:
        kpi_parties.metric("Total de partidos", f"{total_parties:,}".replace(",", "."))
    else:
        st.warning("Tabela `fato_candidatura_dashboard` ainda não possui partidos legíveis para calcular o KPI.")

    if total_municipalities:
        kpi_municipalities.metric("Total de municípios", f"{total_municipalities:,}".replace(",", "."))
    else:
        st.warning("Tabela `fato_candidatura_dashboard` ainda não possui municípios legíveis para calcular o KPI.")

    if total_declared_assets:
        formatted_assets = f"R$ {total_declared_assets:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        kpi_declared_assets.metric("Bens declarados", formatted_assets)
    else:
        st.warning("Tabela `fato_bem_candidato_dashboard` ainda não possui bens legíveis para calcular o KPI.")
except Exception as error:
    components.html(
        f"""
        <script>
        console.error("Erro ao conectar no MinIO.");
        console.error({json.dumps(str(error))});
        </script>
        """,
        height=0,
    )
