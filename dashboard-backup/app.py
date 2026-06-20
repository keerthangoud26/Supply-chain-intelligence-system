import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Nexus Supply Chain AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
css = Path("dashboard/assets/style.css").read_text()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.markdown("""
<h1>⚡ Nexus Supply Chain Intelligence</h1>
<p style='color:#C4B5FD; font-size:18px;'>
AI Powered Logistics & Analytics Platform
</p>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 🚀 Navigation")
st.sidebar.success("Enterprise AI Dashboard")