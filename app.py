import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Customer Churn Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load data
df = pd.read_csv("Cleaned_Churn.csv")

st.title("📊 Customer Churn Analysis Dashboard")
st.markdown("Telco Customer Churn Analytics")

# KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", len(df))
col2.metric("Churned Customers", df["Churn Label"].eq("Yes").sum())
col3.metric(
    "Churn Rate",
    f"{df['Churn Label'].eq('Yes').mean() * 100:.2f}%"
)
col4.metric(
    "Avg Tenure",
    f"{df['Tenure Months'].mean():.1f} Months"
)

st.divider()

# Churn by Contract
contract_churn = pd.crosstab(
    df["Contract"],
    df["Churn Label"]
)

fig1 = px.bar(
    contract_churn,
    barmode="group",
    title="Churn by Contract"
)

st.plotly_chart(fig1, use_container_width=True)

# Churn by Payment Method
payment_churn = pd.crosstab(
    df["Payment Method"],
    df["Churn Label"]
)

fig2 = px.bar(
    payment_churn,
    barmode="group",
    title="Churn by Payment Method"
)

st.plotly_chart(fig2, use_container_width=True)

# Churn by Internet Service
internet_churn = pd.crosstab(
    df["Internet Service"],
    df["Churn Label"]
)

fig3 = px.bar(
    internet_churn,
    barmode="group",
    title="Churn by Internet Service"
)

st.plotly_chart(fig3, use_container_width=True)

# Data
st.subheader("Customer Data")

st.dataframe(
    df,
    use_container_width=True
)