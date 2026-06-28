import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ── Page config ──────────────────────────────────────────────
st.set_page_config(page_title="European Bank Customer Churn", layout="wide")
st.title("🏦 European Bank Customer Churn Dashboard")

# ── Load Data ─────────────────────────────────────────────────
df = pd.read_csv(r"Customer_churn.csv")
st.success(f"✅ File loaded! {df.shape[0]:,} rows × {df.shape[1]} columns")

# ── Sidebar Filters ───────────────────────────────────────────
st.sidebar.header("🔍 Filters")

# Geography filter (only if column exists)
if "Geography" in df.columns:
    all_geos = ["All"] + sorted(df["Geography"].dropna().unique().tolist())
    selected_geo = st.sidebar.selectbox("Geography", all_geos)
    if selected_geo != "All":
        df = df[df["Geography"] == selected_geo]

# Gender filter
if "Gender" in df.columns:
    all_genders = ["All"] + sorted(df["Gender"].dropna().unique().tolist())
    selected_gender = st.sidebar.selectbox("Gender", all_genders)
    if selected_gender != "All":
        df = df[df["Gender"] == selected_gender]

# Age range filter
if "Age_Group" in df.columns:
    all_age_group = ["All"] + sorted(df["Age_Group"].dropna().unique().tolist())
    selected_age = st.sidebar.selectbox("Age Group", all_age_group)

    if selected_age != "All":
        df = df[df["Age_Group"] == selected_age]

# Has Credit Card
credit = st.sidebar.selectbox(
    "Has Credit Card",
    ["All", "Yes", "No"]
)

if credit == "Yes":
    df = df[df["HasCrCard"] == 1]
elif credit == "No":
    df = df[df["HasCrCard"] == 0]

#active status
active = st.sidebar.selectbox("Customer Status",["All","Active","Inactive"])
if active == "Active":
    df = df[df["IsActiveMember"] == 1]
elif active == "Inactive":
    df = df[df["IsActiveMember"] == 0]

#balance segment filter
Balance = st.sidebar.selectbox("Balance Segment",["All"]+sorted(df["Balance_Value"].unique()))
if Balance !="All":
    df = df[df["Balance_Value"] == Balance]
	
st.markdown(f"**Showing {len(df):,} customers after filters**")

# ── Section 1: Raw Data Preview ───────────────────────────────

with st.expander("📋 Preview Raw Data"):
    st.dataframe(df.head(20), use_container_width=True)

# ── Section 2: Key Metrics ────────────────────────────────────

st.subheader("📊 Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)

total = len(df)
col1.metric("Total Customers", f"{total:,}")

if "Exited" in df.columns:
    churned = int(df["Exited"].sum())
    churn_rate = churned / total * 100 if total > 0 else 0
    col2.metric("Churned", f"{churned:,}")
    col3.metric("Churn Rate", f"{churn_rate:.1f}%")
    col4.metric("Retained", f"{total - churned:,}")
    inactive_churn = df[df['IsActiveMember'] == 0]['Exited'].mean() * 100
    active_churn = df[df['IsActiveMember'] == 1]['Exited'].mean() * 100
    engagement_gap = inactive_churn - active_churn
    col5.metric("Engagement Gap", f"{engagement_gap:.2f}%")

# ── Section 3: Charts ─────────────────────────────────────────

st.subheader("📈 Charts")
chart_col1, chart_col2 = st.columns(2)

# Chart 1: Churn by Geography

if "Geography" in df.columns and "Exited" in df.columns:
    with chart_col1:
        st.markdown("**Churn Count by Geography**")
        churn_geo = df.groupby("Geography")["Exited"].sum().sort_values(ascending=False)
        fig, ax = plt.subplots()
        churn_geo.plot(kind="bar", ax=ax, color="tomato", edgecolor="white")
        ax.set_xlabel("Geography")
        ax.set_ylabel("Number of Churned Customers")
        ax.set_xticklabels(churn_geo.index, rotation=0)
        st.pyplot(fig)

# Chart 2: Age Distribution

if "Age" in df.columns:
    with chart_col2:
        st.markdown("**Age Distribution**")
        fig2, ax2 = plt.subplots()
        df["Age"].plot(kind="hist", bins=20, ax=ax2, color="steelblue", edgecolor="white")
        ax2.set_xlabel("Age")
        ax2.set_ylabel("Count")
        st.pyplot(fig2)

chart_col3, chart_col4 = st.columns(2)

# Chart 3: Churn by Gender

if "Gender" in df.columns and "Exited" in df.columns:
    with chart_col3:
        st.markdown("**Churn Rate by Gender**")
        gender_churn = df.groupby("Gender")["Exited"].mean() * 100
        fig3, ax3 = plt.subplots()
        gender_churn.plot(kind="bar", ax=ax3, color=["orchid", "cornflowerblue"], edgecolor="white")
        ax3.set_ylabel("Churn Rate (%)")
        ax3.set_xticklabels(gender_churn.index, rotation=0)
        st.pyplot(fig3)

# Chart 4: Balance Distribution

if "Balance" in df.columns:
    with chart_col4:
        st.markdown("**Balance Distribution**")
        fig4, ax4 = plt.subplots()
        df["Balance"].plot(kind="hist", bins=20, ax=ax4, color="mediumseagreen", edgecolor="white")
        ax4.set_xlabel("Balance")
        ax4.set_ylabel("Count")
        st.pyplot(fig4)

# ── Section 4: Summary Stats ──────────────────────────────────

with st.expander("📐 Summary Statistics"):
    st.dataframe(df.describe(), use_container_width=True)

# ── Section 5: Download Filtered Data ────────────────────────
st.subheader("💾 Download Filtered Data")
csv_data = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download as CSV",
    data=csv_data,
    file_name="filtered_churn_data.csv",
    mime="text/csv",
)
