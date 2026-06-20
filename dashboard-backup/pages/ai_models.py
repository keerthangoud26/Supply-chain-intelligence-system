import streamlit as st
import pandas as pd

st.title("🤖 AI Prediction Models")

data = {
    "Metric": ["MAE", "R2 Score"],
    "Value": [2.231, -0.050]
}

df = pd.DataFrame(data)

st.subheader("Shipping Cost Prediction Model")

st.dataframe(df)

st.info("Baseline Random Forest model for shipping cost prediction.")