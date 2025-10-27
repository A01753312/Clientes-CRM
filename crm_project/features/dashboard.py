"""Tab de Dashboard con métricas y gráficas"""
import streamlit as st
import pandas as pd
import altair as alt
from crm_project.config.settings import ESTATUS_OPCIONES


def render(df: pd.DataFrame):
    st.subheader("📊 Dashboard")
    if df is None or df.empty:
        st.info("No hay clientes con los filtros seleccionados")
        return
    conteo = df["estatus"].value_counts().reindex(ESTATUS_OPCIONES, fill_value=0)
    cols = st.columns(4)
    for i, (estatus, count) in enumerate(conteo.items()):
        with cols[i % 4]:
            st.metric(estatus, int(count))
    chart_data = pd.DataFrame({"estatus": conteo.index, "conteo": conteo.values})
    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X("estatus:N", sort="-y"),
        y="conteo:Q",
        color="estatus:N",
        tooltip=["estatus", "conteo"]
    ).properties(height=400)
    st.altair_chart(chart, use_container_width=True)
