import streamlit as st
import plotly.express as px
from dashboard.utils.queries import *

st.markdown("## 📊 Executive Overview")

revenue = get_total_revenue()
products = get_total_products()
suppliers = get_total_suppliers()
shipping = get_avg_shipping_cost()

# KPI Cards
c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Revenue", f"${revenue:,.0f}", "+14.2%")
c2.metric("📦 Products", products, "+5")
c3.metric("🏭 Suppliers", suppliers, "+2")
c4.metric("🚚 Shipping Cost", f"${shipping}", "-2.8%")

st.markdown("###")

# Charts
left, right = st.columns(2)

df = get_top_products()

with left:
    fig = px.bar(
        df,
        x="sku",
        y="total_units_sold",
        title="Top Selling Products"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )
    st.plotly_chart(fig, use_container_width=True)

supplier_df = get_supplier_defects()

with right:
    fig2 = px.bar(
        supplier_df,
        x="supplier_name",
        y="avg_defect_rate",
        title="Supplier Quality Risk"
    )
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )
    st.plotly_chart(fig2, use_container_width=True)