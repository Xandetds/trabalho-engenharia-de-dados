import streamlit as st
import plotly.express as px
import pandas as pd

from gold_reader import read_gold_table_records
from kpis import (
    calculate_assets_by_party,
    calculate_candidates_by_office,
    calculate_total_candidates,
    calculate_total_declared_assets,
    calculate_total_municipalities,
    calculate_total_parties,
)

st.set_page_config(
    page_title="Dashboard TSE",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 0rem;
        }
        header[data-testid="stHeader"] {
            display: none;
        }
        div[data-testid="stMetric"] {
            background-color: rgba(81, 45, 168, 0.08);
            border: 1px solid #7c4dff;
            border-radius: 0.5rem;
            padding: 0.8rem 1rem;
            text-align: center;
        }
        div[data-testid="stMetric"] label {
            color: #b39ddb !important;
            font-size: 0.85rem;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-size: 1.4rem;
        }
        .dashboard-title {
            font-size: 1.6rem;
            font-weight: 700;
            color: #b39ddb;
            margin-bottom: 0.3rem;
        }
        .dashboard-subtitle {
            font-size: 0.9rem;
            color: #9e9e9e;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="dashboard-title">Dashboard TSE</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="dashboard-subtitle">Panorama dos dados eleitorais — Camada Gold</div>',
    unsafe_allow_html=True,
)


def format_brl(value) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


@st.cache_data(ttl=300)
def load_data():
    candidate_records = read_gold_table_records("fato_candidatura_dashboard")
    asset_records = read_gold_table_records("fato_bem_candidato_dashboard")
    office_records = read_gold_table_records("dim_cargo")
    party_records = read_gold_table_records("dim_partido")

    return {
        "total_candidates": calculate_total_candidates(candidate_records),
        "total_parties": calculate_total_parties(candidate_records),
        "total_municipalities": calculate_total_municipalities(candidate_records),
        "total_declared_assets": calculate_total_declared_assets(asset_records),
        "candidates_by_office": calculate_candidates_by_office(candidate_records, office_records),
        "assets_by_party": calculate_assets_by_party(candidate_records, asset_records, party_records),
    }


try:
    data = load_data()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de candidatos", f"{data['total_candidates']:,}".replace(",", "."))
    col2.metric("Total de partidos", f"{data['total_parties']:,}".replace(",", "."))
    col3.metric("Total de municipios", f"{data['total_municipalities']:,}".replace(",", "."))
    col4.metric("Bens declarados", format_brl(data["total_declared_assets"]))

    chart_left, chart_right = st.columns(2)

    with chart_left:
        st.markdown("**Candidatos por cargo**")
        if data["candidates_by_office"]:
            df_office = pd.DataFrame(data["candidates_by_office"])
            fig_office = px.bar(
                df_office,
                x="total_candidatos",
                y="cargo",
                orientation="h",
                color_discrete_sequence=["#7c4dff"],
            )
            fig_office.update_layout(
                xaxis_title="",
                yaxis_title="",
                margin=dict(l=0, r=10, t=10, b=0),
                height=340,
                yaxis=dict(autorange="reversed"),
                bargap=0.3,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e0e0e0",
            )
            fig_office.update_traces(
                texttemplate="%{x:,.0f}",
                textposition="outside",
                textfont_size=11,
                textfont_color="#e0e0e0",
            )
            st.plotly_chart(fig_office, use_container_width=True, config={"displayModeBar": False})

    with chart_right:
        st.markdown("**Patrimonio por partido**")
        if data["assets_by_party"]:
            top_parties = data["assets_by_party"][:10]
            df_party = pd.DataFrame([
                {"partido": item["partido"], "patrimonio": float(item["patrimonio_declarado"])}
                for item in top_parties
            ])
            fig_party = px.bar(
                df_party,
                x="patrimonio",
                y="partido",
                orientation="h",
                color_discrete_sequence=["#00e5ff"],
            )
            fig_party.update_layout(
                xaxis_title="",
                yaxis_title="",
                margin=dict(l=0, r=10, t=10, b=0),
                height=340,
                yaxis=dict(autorange="reversed"),
                bargap=0.3,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e0e0e0",
            )
            fig_party.update_traces(
                texttemplate="R$ %{x:,.2f}",
                textposition="outside",
                textfont_size=11,
                textfont_color="#e0e0e0",
            )
            fig_party.update_xaxes(tickprefix="R$ ", tickformat=",.2f")
            st.plotly_chart(fig_party, use_container_width=True, config={"displayModeBar": False})

except Exception as error:
    st.error(f"Erro ao carregar dados: {error}")
