import json
import streamlit as st
import streamlit.components.v1 as components

from gold_reader import (
    inspect_expected_gold_paths,
    list_gold_objects,
    read_gold_sample,
    read_gold_table_records,
)
from kpis import calculate_total_candidates
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
    total_candidates = calculate_total_candidates(candidate_records)

    components.html(
        f"""
        <script>
        console.log("Conexão com MinIO realizada com sucesso.");
        console.log("Buckets encontrados:", {json.dumps(buckets)});
        console.log("Caminhos esperados da camada Gold:", {json.dumps(gold_paths)});
        console.log("Objetos encontrados na camada Gold:", {json.dumps(gold_objects)});
        console.log("Amostra lida da camada Gold:", {json.dumps(gold_sample)});
        console.log("Total de candidatos:", {json.dumps(total_candidates)});
        </script>
        """,
        height=0,
    )

    st.subheader("KPIs")

    if total_candidates:
        st.metric("Total de candidatos", f"{total_candidates:,}".replace(",", "."))
    else:
        st.warning("Tabela `fato_candidatura_dashboard` ainda não possui dados legíveis para calcular o KPI.")
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
