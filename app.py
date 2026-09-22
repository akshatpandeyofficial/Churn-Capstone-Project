import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

st.title("Customer Churn Capstone Project")
st.markdown("End-to-end DA project — Data Cleaning, EDA, SQL Analysis, Power BI Dashboard")

# Data section
st.header("Cleaned Dataset")
df = pd.read_csv("Cleaned_Churn.csv")
st.write(f"Total records: {len(df)}")
st.dataframe(df.head(10))

# Key stats
st.header("Key Insights")
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", len(df))
col2.metric("Churned", df['Churn Value'].sum())
col3.metric("Churn Rate", f"{round(df['Churn Value'].mean()*100, 2)}%")

# Power BI screenshots
st.header("Power BI Dashboard")
img1 = Image.open("Customer Churn Dashboard (Part1).png")
img2 = Image.open("Customer Churn Dashboard (Part2).png")
st.image(img1, use_column_width=True)
st.image(img2, use_column_width=True)