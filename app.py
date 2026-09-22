import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# Page config
st.set_page_config(
    page_title="Customer Churn Analytics",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main-title {font-size: 36px; font-weight: 700; color: #1F497D; text-align: center;}
.sub-title {font-size: 16px; color: #666; text-align: center; margin-bottom: 30px;}
.metric-card {background: #f0f4ff; border-radius: 10px; padding: 15px; text-align: center;}
.section-header {font-size: 22px; font-weight: 600; color: #1F497D; border-left: 4px solid #1F497D; padding-left: 10px; margin: 20px 0 10px;}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Cleaned_Churn.csv")
    return df

df = load_data()

# ── HEADER ──
st.markdown('<p class="main-title">📊 Customer Churn Analytics Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">End-to-end Data Analytics Capstone Project | Python · SQL · Power BI · Streamlit</p>', unsafe_allow_html=True)
st.markdown("---")

# ── NAVIGATION ──
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Overview",
    "🔍 Churn Analysis",
    "📊 Power BI Dashboard",
    "🗄️ SQL Queries",
    "📁 Project Info"
])

# ════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════
with tab1:
    st.markdown('<p class="section-header">Key Metrics</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    total = len(df)
    churned = df['Churn Value'].sum()
    churn_rate = round(df['Churn Value'].mean() * 100, 2)
    avg_monthly = round(df['Monthly Charges'].mean(), 2)

    col1.metric("Total Customers", f"{total:,}")
    col2.metric("Churned Customers", f"{churned:,}")
    col3.metric("Overall Churn Rate", f"{churn_rate}%")
    col4.metric("Avg Monthly Charges", f"${avg_monthly}")

    st.markdown('<p class="section-header">Dataset Preview</p>', unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        churn_counts = df['Churn Value'].value_counts().reset_index()
        churn_counts.columns = ['Churn', 'Count']
        churn_counts['Churn'] = churn_counts['Churn'].map({1: 'Churned', 0: 'Retained'})
        fig = px.pie(churn_counts, values='Count', names='Churn',
                     title='Overall Churn Distribution',
                     color_discrete_map={'Churned': '#E24B4A', 'Retained': '#1D9E75'})
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        tenure_fig = px.histogram(df, x='Tenure Months', color='Churn Label',
                                   title='Customer Tenure Distribution',
                                   color_discrete_map={'Yes': '#E24B4A', 'No': '#378ADD'},
                                   nbins=30)
        st.plotly_chart(tenure_fig, use_container_width=True)

# ════════════════════════════════════════
# TAB 2 — CHURN ANALYSIS
# ════════════════════════════════════════
with tab2:
    st.markdown('<p class="section-header">Churn Analysis by Key Factors</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # By Contract
        contract_churn = df.groupby('Contract').agg(
            Total=('Churn Value', 'count'),
            Churned=('Churn Value', 'sum')
        ).reset_index()
        contract_churn['Churn Rate %'] = round(contract_churn['Churned'] / contract_churn['Total'] * 100, 2)
        fig = px.bar(contract_churn, x='Contract', y='Churn Rate %',
                     title='Churn Rate by Contract Type',
                     color='Churn Rate %', color_continuous_scale='Reds',
                     text='Churn Rate %')
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # By Internet Service
        internet_churn = df.groupby('Internet Service').agg(
            Total=('Churn Value', 'count'),
            Churned=('Churn Value', 'sum')
        ).reset_index()
        internet_churn['Churn Rate %'] = round(internet_churn['Churned'] / internet_churn['Total'] * 100, 2)
        fig2 = px.bar(internet_churn, x='Internet Service', y='Churn Rate %',
                      title='Churn Rate by Internet Service',
                      color='Churn Rate %', color_continuous_scale='Blues',
                      text='Churn Rate %')
        fig2.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        # By Payment Method
        payment_churn = df.groupby('Payment Method').agg(
            Total=('Churn Value', 'count'),
            Churned=('Churn Value', 'sum')
        ).reset_index()
        payment_churn['Churn Rate %'] = round(payment_churn['Churned'] / payment_churn['Total'] * 100, 2)
        fig3 = px.bar(payment_churn, x='Payment Method', y='Churn Rate %',
                      title='Churn Rate by Payment Method',
                      color='Churn Rate %', color_continuous_scale='Oranges',
                      text='Churn Rate %')
        fig3.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        # By Gender and Senior Citizen
        gender_churn = df.groupby(['Gender', 'Senior Citizen'])['Churn Value'].mean().reset_index()
        gender_churn['Churn Rate %'] = round(gender_churn['Churn Value'] * 100, 2)
        fig4 = px.bar(gender_churn, x='Gender', y='Churn Rate %',
                      color='Senior Citizen',
                      title='Churn Rate by Gender & Senior Citizen',
                      barmode='group',
                      color_discrete_map={'Yes': '#E24B4A', 'No': '#378ADD'},
                      text='Churn Rate %')
        fig4.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig4, use_container_width=True)

    # Monthly Charges vs Churn
    st.markdown('<p class="section-header">Monthly Charges vs Churn</p>', unsafe_allow_html=True)
    fig5 = px.box(df, x='Churn Label', y='Monthly Charges',
                  title='Monthly Charges Distribution by Churn Status',
                  color='Churn Label',
                  color_discrete_map={'Yes': '#E24B4A', 'No': '#1D9E75'})
    st.plotly_chart(fig5, use_container_width=True)

    # High Risk Customers
    st.markdown('<p class="section-header">High Risk Customers (Churn Score ≥ 70, Month-to-Month)</p>', unsafe_allow_html=True)
    high_risk = df[
        (df['Churn Label'] == 'No') &
        (df['Churn Score'] >= 70) &
        (df['Contract'] == 'Month-to-month')
    ][['CustomerID', 'City', 'Contract', 'Monthly Charges', 'Churn Score', 'CLTV']].sort_values('CLTV')
    st.write(f"Total high-risk customers: {len(high_risk)}")
    st.dataframe(high_risk.head(20), use_container_width=True)

# ════════════════════════════════════════
# TAB 3 — POWER BI DASHBOARD
# ════════════════════════════════════════
with tab3:
    st.markdown('<p class="section-header">Power BI Dashboard</p>', unsafe_allow_html=True)
    st.info("Interactive Power BI dashboard built with DAX measures and dynamic filters.")

    try:
        img1 = Image.open("Customer Churn Dashboard (Part1).png")
        img2 = Image.open("Customer Churn Dashboard (Part2).png")
        st.image(img1, caption="Dashboard Part 1 — Overview & Contract Analysis", use_column_width=True)
        st.markdown("---")
        st.image(img2, caption="Dashboard Part 2 — Regional & Payment Analysis", use_column_width=True)
    except:
        st.warning("Dashboard images not found. Please ensure PNG files are in the same folder.")

# ════════════════════════════════════════
# TAB 4 — SQL QUERIES
# ════════════════════════════════════════
with tab4:
    st.markdown('<p class="section-header">SQL Analysis — Business Queries</p>', unsafe_allow_html=True)
    st.info("15+ SQL queries written in MySQL to extract business insights from cleaned data.")

    queries = {
        "Overall Churn Rate": """SELECT count(*) as Total_customers,
    sum(`Churn Value`) as Churned_customer,
    round(sum(`Churn Value`) *100/ count(*),2) as Overall_Churn_rate
FROM cleaned_churn;""",

        "Churn Rate By Contract": """SELECT contract, count(*) as total_Customer,
    sum(`Churn Value`) as Churn,
    round(avg(`Churn Value`)*100,2) as Churn_Rate_By_Contract
FROM cleaned_churn
GROUP BY contract
ORDER BY Churn_Rate_By_Contract;""",

        "Churn Rate By Internet Service": """SELECT `Internet Service`,
    COUNT(*) AS total_customers,
    ROUND(AVG(`Churn Value`) * 100, 2) AS churn_rate_by_IS
FROM cleaned_churn
GROUP BY `Internet Service`
ORDER BY churn_rate_by_IS;""",

        "Top Cities With Highest Churn": """SELECT City,
    count(*) as Total_Customers,
    round(avg(`Churn Value`)*100,2) as Churned_rate_by_City
FROM cleaned_churn
GROUP BY City
HAVING count(*) >= 20
ORDER BY Churned_rate_by_City DESC;""",

        "High Risk Customers": """SELECT CustomerID, City, Contract,
    `Monthly Charges`, `Churn Score`, CLTV
FROM cleaned_churn
WHERE `Churn Label` = 'No'
AND `Churn Score` >= 70
AND Contract = 'Month-to-Month'
ORDER BY CLTV;""",

        "CTE — Churn Rank By City": """WITH city_churn AS (
    SELECT City,
    count(*) AS total_customers,
    Round(AVG(`Churn Value`) * 100, 2) AS churn_rate_pct
    FROM cleaned_churn
    GROUP BY City
    HAVING Count(*) >= 20
)
SELECT City, total_customers, churn_rate_pct,
RANK() OVER (Order by churn_rate_pct DESC) AS churn_rank
FROM city_churn
LIMIT 10;""",
    }

    for title, query in queries.items():
        with st.expander(f"🔍 {title}"):
            st.code(query, language="sql")

# ════════════════════════════════════════
# TAB 5 — PROJECT INFO
# ════════════════════════════════════════
with tab5:
    st.markdown('<p class="section-header">About This Project</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
**Project:** Customer Churn Analytics Capstone

**Dataset:** Telco Customer Churn — 7,043 rows, 33 columns

**Workflow:**
1. 📥 Raw data collection from Kaggle
2. 🧹 Data cleaning using Python & Pandas
3. 🔍 EDA — patterns & insights
4. 🗄️ SQL analysis — 15+ business queries
5. 📊 Power BI dashboard with DAX
6. 🚀 Deployed on Streamlit

**Key Finding:** Month-to-month contracts have the highest churn rate at ~42%. Customers with Fiber optic internet churn more than DSL users.
        """)

    with col2:
        st.markdown("""
**Tools Used:**

| Tool | Purpose |
|------|---------|
| Python + Pandas | Data cleaning & EDA |
| MySQL | SQL business queries |
| Power BI (DAX) | Interactive dashboard |
| Streamlit + Plotly | Web deployment |
| Git + GitHub | Version control |

**Author:** Akshat Pandey

**GitHub:** [View Repository](https://github.com/akshatpandeyofficial/Churn-Capstone-Project)

**LinkedIn:** [Akshat Pandey](https://linkedin.com/in/akshatpandeyofficial)
        """)