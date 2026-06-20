import streamlit as st

st.markdown("## ⚠ AI Anomaly Detection Center")

col1, col2 = st.columns([1,2])

with col1:
    st.metric(
        "Detected Anomalies",
        10,
        "+3 Alerts"
    )

with col2:
    st.error("""
    🚨 High Cost Shipment Alerts Detected
    
    AI engine found abnormal logistics behavior.
    
    Manual review recommended.
    """)

st.info("Isolation Forest model continuously monitors shipment behavior.")