import json
import streamlit as st
import streamlit.components.v1 as components

from minio_connection import list_buckets

st.set_page_config(
    page_title="Dashboard TSE",
    layout="wide",
)

st.title("Dashboard TSE")

try:
    buckets = list_buckets()
    components.html(
        f"""
        <script>
        console.log("Conexão com MinIO realizada com sucesso.");
        console.log("Buckets encontrados:", {json.dumps(buckets)});
        </script>
        """,
        height=0,
    )
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
