import streamlit as st
import plotly.express as px
from dashboard.utils.queries import get_transport_cost

st.title("🚚 Logistics Analytics")

df = get_transport_cost()

fig = px.pie(
    df,
    names="transportation_mode",
    values="avg_shipping_cost",
    hole=0.5,
    title="Shipping Cost by Transport Mode"
)

st.plotly_chart(fig, use_container_width=True)
st.dataframe(df)