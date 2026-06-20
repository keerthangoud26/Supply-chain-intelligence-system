import streamlit as st
from dashboard.utils.queries import get_inventory_risk

st.title("📦 Inventory Risk Monitoring")

df = get_inventory_risk()

st.warning("Products with low stock")

st.dataframe(df, use_container_width=True)