import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Customer Churn Analytics Dashboard")

df = pd.read_csv("Cleaned_Churn.csv")

st.subheader("Churn Overview")
st.dataframe(df.head())

churn_count = df['Churn Value'].value_counts()
fig = px.bar(churn_count, title="Churn Distribution")
st.plotly_chart(fig)