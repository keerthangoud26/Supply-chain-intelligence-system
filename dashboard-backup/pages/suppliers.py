import streamlit as st
import plotly.express as px
from dashboard.utils.queries import get_supplier_defects

st.title("🏭 Supplier Intelligence")

df = get_supplier_defects()

fig = px.bar(
    df,
    x="supplier_name",
    y="avg_defect_rate",
    title="Supplier Defect Rate Analysis"
)

st.plotly_chart(fig, use_container_width=True)
st.dataframe(df)