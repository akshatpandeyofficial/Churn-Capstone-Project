import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Customer Churn Analytics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).parent

DATA_FILE = BASE_DIR / "Cleaned_Churn.csv"
PART1_IMAGE = BASE_DIR / "Customer Churn Dashboard (Part1).png"
PART2_IMAGE = BASE_DIR / "Customer Churn Dashboard (Part2).png"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 38px;
    font-weight: 700;
    color: #1F497D;
    text-align: center;
    padding-top: 10px;
}

.sub-title {
    font-size: 15px;
    color: #888;
    text-align: center;
    margin-bottom: 10px;
}

.section-header {
    font-size: 20px;
    font-weight: 600;
    color: #1F497D;
    border-left: 5px solid #1F497D;
    padding-left: 12px;
    margin: 24px 0 12px;
}

.query-title {
    font-size: 15px;
    font-weight: 600;
    color: #ffffff;
    background: #1F497D;
    padding: 8px 14px;
    border-radius: 6px;
    margin-bottom: 4px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    if not DATA_FILE.exists():
        st.error(
            "Cleaned_Churn.csv was not found. "
            "Make sure it is uploaded to the same GitHub repository as app.py."
        )
        st.stop()

    return pd.read_csv(DATA_FILE)


df = load_data()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<p class="main-title">📊 Customer Churn Analytics Dashboard</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">'
    'End-to-end Data Analytics Capstone Project '
    '&nbsp;|&nbsp; Python · Pandas · MySQL · Power BI · Streamlit'
    '</p>',
    unsafe_allow_html=True
)

st.markdown("---")


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Overview",
    "🔍 Churn Analysis",
    "📊 Power BI Dashboard",
    "🗄️ SQL Queries",
    "📁 Project Info"
])


# ============================================================
# TAB 1 — OVERVIEW
# ============================================================

with tab1:

    st.markdown(
        '<p class="section-header">Key Business Metrics</p>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Customers",
        f"{len(df):,}"
    )

    col2.metric(
        "Churned Customers",
        f"{int(df['Churn Value'].sum()):,}"
    )

    col3.metric(
        "Overall Churn Rate",
        f"{round(df['Churn Value'].mean() * 100, 2)}%"
    )

    col4.metric(
        "Avg Monthly Charges",
        f"${round(df['Monthly Charges'].mean(), 2)}"
    )


    # Dataset Preview

    st.markdown(
        '<p class="section-header">Dataset Preview</p>',
        unsafe_allow_html=True
    )

    st.dataframe(
        df.head(10),
        width="stretch"
    )


    # Charts

    col_a, col_b = st.columns(2)

    with col_a:

        counts = df["Churn Label"].value_counts().reset_index()

        counts.columns = ["Status", "Count"]

        fig = px.pie(
            counts,
            values="Count",
            names="Status",
            title="Overall Churn Distribution",
            color_discrete_map={
                "Yes": "#E24B4A",
                "No": "#1D9E75"
            }
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )


    with col_b:

        fig2 = px.histogram(
            df,
            x="Tenure Months",
            color="Churn Label",
            title="Tenure Distribution by Churn Status",
            color_discrete_map={
                "Yes": "#E24B4A",
                "No": "#378ADD"
            },
            nbins=30
        )

        st.plotly_chart(
            fig2,
            width="stretch"
        )


# ============================================================
# TAB 2 — CHURN ANALYSIS
# ============================================================

with tab2:

    st.markdown(
        '<p class="section-header">Churn Rate by Contract Type</p>',
        unsafe_allow_html=True
    )

    c1 = (
        df.groupby("Contract")
        .agg(
            Total=("Churn Value", "count"),
            Churned=("Churn Value", "sum")
        )
        .reset_index()
    )

    c1["Churn Rate %"] = round(
        c1["Churned"] / c1["Total"] * 100,
        2
    )

    fig = px.bar(
        c1,
        x="Contract",
        y="Churn Rate %",
        color="Churn Rate %",
        color_continuous_scale="Reds",
        text="Churn Rate %",
        title="Churn Rate by Contract Type"
    )

    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


    # --------------------------------------------------------
    # Internet Service + Payment Method
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            '<p class="section-header">By Internet Service</p>',
            unsafe_allow_html=True
        )

        c2 = (
            df.groupby("Internet Service")
            .agg(
                Total=("Churn Value", "count"),
                Churned=("Churn Value", "sum")
            )
            .reset_index()
        )

        c2["Churn Rate %"] = round(
            c2["Churned"] / c2["Total"] * 100,
            2
        )

        fig2 = px.bar(
            c2,
            x="Internet Service",
            y="Churn Rate %",
            color="Churn Rate %",
            color_continuous_scale="Blues",
            text="Churn Rate %"
        )

        fig2.update_traces(
            texttemplate="%{text}%",
            textposition="outside"
        )

        st.plotly_chart(
            fig2,
            width="stretch"
        )


    with col2:

        st.markdown(
            '<p class="section-header">By Payment Method</p>',
            unsafe_allow_html=True
        )

        c3 = (
            df.groupby("Payment Method")
            .agg(
                Total=("Churn Value", "count"),
                Churned=("Churn Value", "sum")
            )
            .reset_index()
        )

        c3["Churn Rate %"] = round(
            c3["Churned"] / c3["Total"] * 100,
            2
        )

        fig3 = px.bar(
            c3,
            x="Payment Method",
            y="Churn Rate %",
            color="Churn Rate %",
            color_continuous_scale="Oranges",
            text="Churn Rate %"
        )

        fig3.update_traces(
            texttemplate="%{text}%",
            textposition="outside"
        )

        st.plotly_chart(
            fig3,
            width="stretch"
        )


    # --------------------------------------------------------
    # Monthly Charges vs Churn
    # --------------------------------------------------------

    st.markdown(
        '<p class="section-header">Monthly Charges vs Churn</p>',
        unsafe_allow_html=True
    )

    fig5 = px.box(
        df,
        x="Churn Label",
        y="Monthly Charges",
        color="Churn Label",
        color_discrete_map={
            "Yes": "#E24B4A",
            "No": "#1D9E75"
        },
        title="Monthly Charges vs Churn"
    )

    st.plotly_chart(
        fig5,
        width="stretch"
    )


    # --------------------------------------------------------
    # High Risk Customers
    # --------------------------------------------------------

    st.markdown(
        '<p class="section-header">'
        'High Risk Customers (Not yet churned but likely to)'
        '</p>',
        unsafe_allow_html=True
    )

    high_risk = df[
        (df["Churn Label"] == "No") &
        (df["Churn Score"] >= 70) &
        (df["Contract"] == "Month-to-month")
    ][
        [
            "CustomerID",
            "City",
            "Contract",
            "Monthly Charges",
            "Churn Score",
            "CLTV"
        ]
    ].sort_values("CLTV")

    st.write(
        f"**{len(high_risk)} high-risk customers identified** "
        "— Churn Score ≥ 70, Month-to-Month contract"
    )

    st.dataframe(
        high_risk.head(20),
        width="stretch"
    )


# ============================================================
# TAB 3 — POWER BI DASHBOARD
# ============================================================

with tab3:

    st.markdown(
        '<p class="section-header">Power BI Dashboard</p>',
        unsafe_allow_html=True
    )

    st.info(
        "Built using Power BI Desktop with DAX measures, "
        "Power Query transformations, and dynamic filters."
    )


    # --------------------------------------------------------
    # PART 1
    # --------------------------------------------------------

    st.markdown(
        "#### Part 1 — Overview & Contract Analysis"
    )

    if PART1_IMAGE.exists():

        st.image(
            str(PART1_IMAGE),
            width="stretch"
        )

    else:

        st.error(
            "Power BI Part 1 image not found: "
            "Customer Churn Dashboard (Part1).png"
        )


    st.markdown("---")


    # --------------------------------------------------------
    # PART 2
    # --------------------------------------------------------

    st.markdown(
        "#### Part 2 — Regional & Payment Analysis"
    )

    if PART2_IMAGE.exists():

        st.image(
            str(PART2_IMAGE),
            width="stretch"
        )

    else:

        st.error(
            "Power BI Part 2 image not found: "
            "Customer Churn Dashboard (Part2).png"
        )


# ============================================================
# TAB 4 — SQL QUERIES
# ============================================================

with tab4:

    st.markdown(
        '<p class="section-header">'
        'SQL Business Analysis — MySQL Queries'
        '</p>',
        unsafe_allow_html=True
    )

    st.info(
        "15+ SQL queries written in MySQL Workbench "
        "to extract actionable business insights from the cleaned dataset."
    )


    queries = [

        {
            "title": "1. Overall Churn Rate",
            "insight": "26.54% of total customers have churned.",
            "sql": """
SELECT
    COUNT(*) AS Total_Customers,
    SUM(`Churn Value`) AS Churned_Customers,
    ROUND(
        SUM(`Churn Value`) * 100 / COUNT(*),
        2
    ) AS Overall_Churn_Rate
FROM cleaned_churn;
"""
        },


        {
            "title": "2. Churn Rate by Contract Type",
            "insight": "Month-to-Month contracts have the highest churn rate.",
            "sql": """
SELECT
    Contract,
    COUNT(*) AS Total_Customers,
    SUM(`Churn Value`) AS Churned,
    ROUND(
        AVG(`Churn Value`) * 100,
        2
    ) AS Churn_Rate_By_Contract
FROM cleaned_churn
GROUP BY Contract
ORDER BY Churn_Rate_By_Contract DESC;
"""
        },


        {
            "title": "3. Churn Rate by Internet Service",
            "insight": "Compares churn rates across internet service types.",
            "sql": """
SELECT
    `Internet Service`,
    COUNT(*) AS Total_Customers,
    ROUND(
        AVG(`Churn Value`) * 100,
        2
    ) AS Churn_Rate
FROM cleaned_churn
GROUP BY `Internet Service`
ORDER BY Churn_Rate DESC;
"""
        },


        {
            "title": "4. Churn Rate by Payment Method",
            "insight": "Compares churn rates across payment methods.",
            "sql": """
SELECT
    `Payment Method`,
    COUNT(*) AS Total_Customers,
    ROUND(
        AVG(`Churn Value`) * 100,
        2
    ) AS Churn_Rate
FROM cleaned_churn
GROUP BY `Payment Method`
ORDER BY Churn_Rate DESC;
"""
        },


        {
            "title": "5. Churn by Gender and Senior Citizen",
            "insight": "Analyzes churn by gender and senior-citizen status.",
            "sql": """
SELECT
    Gender,
    `Senior Citizen`,
    COUNT(*) AS Total_Customers,
    ROUND(
        AVG(`Churn Value`) * 100,
        2
    ) AS Churn_Rate
FROM cleaned_churn
GROUP BY Gender, `Senior Citizen`
ORDER BY Churn_Rate DESC;
"""
        },


        {
            "title": "6. Top Cities with Highest Churn Rate",
            "insight": "Cities with at least 20 customers ranked by churn rate.",
            "sql": """
SELECT
    City,
    COUNT(*) AS Total_Customers,
    SUM(`Churn Value`) AS Churned,
    ROUND(
        AVG(`Churn Value`) * 100,
        2
    ) AS Churn_Rate
FROM cleaned_churn
GROUP BY City
HAVING COUNT(*) >= 20
ORDER BY Churn_Rate DESC
LIMIT 10;
"""
        },


        {
            "title": "7. High Risk Customers (Not Yet Churned)",
            "insight": "Identifies retained customers with high churn scores.",
            "sql": """
SELECT
    CustomerID,
    City,
    Contract,
    `Monthly Charges`,
    `Churn Score`,
    CLTV
FROM cleaned_churn
WHERE `Churn Label` = 'No'
  AND `Churn Score` >= 70
  AND Contract = 'Month-to-month'
ORDER BY CLTV;
"""
        },


        {
            "title": "8. Churn by Paperless Billing",
            "insight": "Compares churn between paperless-billing groups.",
            "sql": """
SELECT
    `Paperless Billing`,
    COUNT(*) AS Total_Customers,
    SUM(`Churn Value`) AS Churned,
    ROUND(
        AVG(`Churn Value`) * 100,
        2
    ) AS Churn_Rate
FROM cleaned_churn
GROUP BY `Paperless Billing`;
"""
        },


        {
            "title": "9. Churn by Contract and Internet",
            "insight": "Combines contract type and internet service for deeper analysis.",
            "sql": """
SELECT
    Contract,
    `Internet Service`,
    COUNT(*) AS Total_Customers,
    ROUND(
        AVG(`Churn Value`) * 100,
        2
    ) AS Churn_Rate
FROM cleaned_churn
GROUP BY Contract, `Internet Service`
ORDER BY Churn_Rate DESC;
"""
        },


        {
            "title": "10. Contracts with Above Average Churn",
            "insight": "Uses a subquery to identify contracts above the overall average churn.",
            "sql": """
SELECT
    Contract,
    COUNT(*) AS Total_Customers,
    SUM(`Churn Value`) AS Churned,
    ROUND(
        AVG(`Churn Value`) * 100,
        2
    ) AS Churn_Rate
FROM cleaned_churn
GROUP BY Contract
HAVING AVG(`Churn Value`) > (
    SELECT AVG(`Churn Value`)
    FROM cleaned_churn
);
"""
        },


        {
            "title": "11. CTE — Churn Rank by City",
            "insight": "Uses a CTE and window function to rank cities.",
            "sql": """
WITH city_churn AS (

    SELECT
        City,
        COUNT(*) AS Total_Customers,
        ROUND(
            AVG(`Churn Value`) * 100,
            2
        ) AS Churn_Rate_Pct

    FROM cleaned_churn

    GROUP BY City

    HAVING COUNT(*) >= 20
)

SELECT
    City,
    Total_Customers,
    Churn_Rate_Pct,
    RANK() OVER (
        ORDER BY Churn_Rate_Pct DESC
    ) AS Churn_Rank

FROM city_churn

LIMIT 10;
"""
        },


        {
            "title": "12. CTE — Churn Rank by State",
            "insight": "Uses a CTE and window function for state-level churn analysis.",
            "sql": """
WITH state_churn AS (

    SELECT
        State,
        COUNT(*) AS Total_Customers,
        ROUND(
            AVG(`Churn Value`) * 100,
            2
        ) AS Churn_Rate_Pct

    FROM cleaned_churn

    GROUP BY State
)

SELECT
    State,
    Total_Customers,
    Churn_Rate_Pct,
    RANK() OVER (
        ORDER BY Churn_Rate_Pct DESC
    ) AS Churn_Rank

FROM state_churn;
"""
        }

    ]


    # Display SQL queries

    for q in queries:

        with st.expander(
            f"🔍 {q['title']}"
        ):

            st.markdown(
                f"**💡 Business Insight:** {q['insight']}"
            )

            st.code(
                q["sql"],
                language="sql"
            )


# ============================================================
# TAB 5 — PROJECT INFO
# ============================================================

with tab5:

    st.markdown(
        '<p class="section-header">About This Project</p>',
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # PROJECT INFORMATION
    # --------------------------------------------------------

    with col1:

        st.markdown("""
**Project:** Customer Churn Analytics — End-to-End Capstone

**Dataset:** Telco Customer Churn (Kaggle)

- 7,043 rows · 33 columns
- Real-world telecom company data

**Complete Workflow:**

1. 📥 Raw data from Kaggle
2. 🧹 Data cleaning — Python & Pandas
3. 🔍 EDA — patterns & visualizations
4. 🗄️ 12+ SQL queries — MySQL Workbench
5. 📊 Power BI dashboard — DAX measures
6. 🚀 Deployed on Streamlit Cloud

**Key Findings:**

- Month-to-month contracts: ~42% churn rate
- Fiber optic users churn more than DSL
- Electronic check payment = highest churn
- Senior citizens churn more than non-senior
""")


    # --------------------------------------------------------
    # TECHNOLOGIES
    # --------------------------------------------------------

    with col2:

        st.markdown("""
**Tools & Technologies:**

| Tool | Purpose |
|------|---------|
| Python 3.x | Core programming |
| Pandas | Data cleaning & EDA |
| Matplotlib / Seaborn | EDA visualizations |
| MySQL Workbench | SQL business queries |
| Power BI (DAX) | Interactive dashboard |
| Streamlit + Plotly | Web deployment |
| Git + GitHub | Version control |

---

**Author:** Akshat Pandey

🎓 B.Tech CSE · Vishwakarma University, Pune

🐙 [GitHub](https://github.com/akshatpandeyofficial)

💼 [LinkedIn](https://linkedin.com/in/akshatpandeyofficial)
""")