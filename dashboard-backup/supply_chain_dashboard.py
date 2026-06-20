import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

st.set_page_config(layout="wide", page_title="Supply Chain Dashboard")
st.title("📊 Real-Time Supply Chain Dashboard")

# Auto-refresh every 10 seconds
st.markdown("""
    <meta http-equiv="refresh" content="10">
""", unsafe_allow_html=True)

# Connect to PostgreSQL
engine = create_engine('postgresql://admin:admin123@localhost:5432/supplychain')

# Remove cache to force fresh data
def load_data():
    df = pd.read_sql("""
        SELECT product, quantity, price, location, timestamp 
        FROM realtime_sales 
        ORDER BY id DESC 
        LIMIT 200
    """, engine)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

df = load_data()

if len(df) > 0:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sales", len(df))
    col2.metric("Products", df['product'].nunique())
    col3.metric("Avg Quantity", round(df['quantity'].mean(), 1))
    col4.metric("Avg Price", f"₹{df['price'].mean():.0f}")
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(df.groupby('product')['quantity'].sum().reset_index(), 
                     x='product', y='quantity', title='Sales by Product', color='product')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(df, names='location', title='Sales by Location', hole=0.3)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🔄 Recent Sales")
    st.dataframe(df.head(20), use_container_width=True)
    
    # Show last update time
    st.caption(f"Last updated: {pd.Timestamp.now().strftime('%H:%M:%S')}")
else:
    st.warning("No data yet. Run kafka_producer.py to send data.")