import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ────────────────────────────────────────────────────────────────
#  Page configuration & basic styling
# ────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Student Performance Dashboard | TITAN SUKKUR",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS – modern, clean, professional look
st.markdown("""
    <style>
    .stApp {
        background-color: #f8fafc;
    }
    .header-title {
        font-size: 2.4rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.4rem;
    }
    .header-subtitle {
        font-size: 1.1rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f1f5f9;
        border-radius: 6px 6px 0 0;
        gap: 1rem;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: white !important;
    }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        text-align: center;
    }
    hr {
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────
#  Data loading (cached)
# ────────────────────────────────────────────────────────────────

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("StudentsPerformance.csv")
        # Standardize column names (in case of small inconsistencies)
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        return df
    except FileNotFoundError:
        st.error("Dataset 'StudentsPerformance.csv' not found in the current directory.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

df = load_data()

# ────────────────────────────────────────────────────────────────
#  Sidebar – Filters & Controls
# ────────────────────────────────────────────────────────────────

with st.sidebar:
    st.header("🎯 Filters")
    st.markdown("Narrow down the data:")

    # Gender
    gender_options = ["All"] + sorted(df["gender"].unique().tolist())
    selected_gender = st.multiselect(
        "Gender",
        options=gender_options,
        default=["All"],
        help="Select one or more genders"
    )

    # Test preparation course
    test_options = ["All"] + sorted(df["test_preparation_course"].unique().tolist())
    selected_test = st.multiselect(
        "Test Preparation Course",
        options=test_options,
        default=["All"],
        help="Did the student complete a test preparation course?"
    )

    # Parental level of education
    education_options = ["All"] + sorted(df["parental_level_of_education"].unique().tolist())
    selected_education = st.multiselect(
        "Parental Education Level",
        options=education_options,
        default=["All"],
        help="Highest education level of parents"
    )

    # Lunch type (bonus filter)
    lunch_options = ["All"] + sorted(df["lunch"].unique().tolist())
    selected_lunch = st.multiselect(
        "Lunch Type",
        options=lunch_options,
        default=["All"],
        help="Type of lunch provided"
    )

    # Reset button
    if st.button("↺ Reset Filters", use_container_width=True):
        st.rerun()

    st.markdown("---")
    st.caption("Data source: StudentsPerformance.csv")
    st.caption(f"Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M PKT')}")

# ────────────────────────────────────────────────────────────────
#  Apply filters (handle "All" case)
# ────────────────────────────────────────────────────────────────

filtered_df = df.copy()

if "All" not in selected_gender:
    filtered_df = filtered_df[filtered_df["gender"].isin(selected_gender)]

if "All" not in selected_test:
    filtered_df = filtered_df[filtered_df["test_preparation_course"].isin(selected_test)]

if "All" not in selected_education:
    filtered_df = filtered_df[filtered_df["parental_level_of_education"].isin(selected_education)]

if "All" not in selected_lunch:
    filtered_df = filtered_df[filtered_df["lunch"].isin(selected_lunch)]

# ────────────────────────────────────────────────────────────────
#  Main Page Header
# ────────────────────────────────────────────────────────────────

st.markdown('<div class="header-title">Student Performance Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">TITAN SUKKUR – Interactive Analysis of Student Exam Scores</div>', unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────
#  KPI Cards
# ────────────────────────────────────────────────────────────────

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

avg_math    = filtered_df["math_score"].mean()
avg_read    = filtered_df["reading_score"].mean()
avg_write   = filtered_df["writing_score"].mean()
avg_total   = (avg_math + avg_read + avg_write) / 3

prev_math   = df["math_score"].mean()    # overall average as reference
prev_read   = df["reading_score"].mean()
prev_write  = df["writing_score"].mean()

with col1:
    st.metric("Avg Math Score", f"{avg_math:.1f}", 
              delta=f"{avg_math - prev_math:.1f}", delta_color="normal")

with col2:
    st.metric("Avg Reading Score", f"{avg_read:.1f}", 
              delta=f"{avg_read - prev_read:.1f}", delta_color="normal")

with col3:
    st.metric("Avg Writing Score", f"{avg_write:.1f}", 
              delta=f"{avg_write - prev_write:.1f}", delta_color="normal")

with col4:
    st.metric("Overall Average", f"{avg_total:.1f}", 
              help="Average of Math + Reading + Writing")

# ────────────────────────────────────────────────────────────────
#  Tabs – better organization
# ────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Score Overview",
    "📊 Distributions",
    "🔥 Correlations & Relationships",
    "📋 Raw Data"
])

# ── Tab 1: Score Overview ────────────────────────────────────────
with tab1:
    st.subheader("Average Scores by Category")

    col_left, col_right = st.columns([3, 2])

    with col_left:
        fig, ax = plt.subplots(figsize=(10, 5.5))
        sns.barplot(
            data=filtered_df.melt(id_vars=["gender"], value_vars=["math_score", "reading_score", "writing_score"]),
            x="gender", y="value", hue="variable",
            palette="viridis", errorbar=None, ax=ax
        )
        ax.set_title("Average Scores by Gender", fontsize=14, pad=15)
        ax.set_ylabel("Score")
        ax.set_xlabel("")
        ax.legend(title="Subject")
        st.pyplot(fig)

    with col_right:
        st.markdown("**Quick Insights**")
        st.info(f"Total students shown: **{len(filtered_df)}**")
        st.write(f"• Highest average: **{filtered_df[['math_score','reading_score','writing_score']].mean().idxmax().replace('_score','').title()}**")
        if len(filtered_df) > 0:
            top_lunch = filtered_df.groupby("lunch")["math_score"].mean().idxmax()
            st.write(f"• Best performing lunch type: **{top_lunch}**")

# ── Tab 2: Distributions ─────────────────────────────────────────
with tab2:
    st.subheader("Score Distributions")

    colA, colB = st.columns(2)

    with colA:
        fig, ax = plt.subplots()
        sns.histplot(filtered_df["math_score"], bins=20, kde=True, color="#4ade80", ax=ax)
        ax.set_title("Math Score Distribution")
        st.pyplot(fig)

    with colB:
        fig, ax = plt.subplots()
        sns.histplot(filtered_df["reading_score"], bins=20, kde=True, color="#60a5fa", ax=ax)
        ax.set_title("Reading Score Distribution")
        st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 4.5))
    sns.boxplot(data=filtered_df[["math_score","reading_score","writing_score"]], palette="Set2", ax=ax)
    ax.set_title("Score Comparison – Box Plot")
    st.pyplot(fig)

# ── Tab 3: Correlations ──────────────────────────────────────────
with tab3:
    st.subheader("Correlation Between Scores")

    fig, ax = plt.subplots(figsize=(7, 6))
    corr = filtered_df[["math_score", "reading_score", "writing_score"]].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title("Score Correlation Heatmap")
    st.pyplot(fig)

    st.info("**Strongest correlation** is usually between **Reading** and **Writing** scores.")

# ── Tab 4: Raw Data & Export ─────────────────────────────────────
with tab4:
    st.subheader("Filtered Dataset")

    st.dataframe(
        filtered_df.style.format(precision=1),
        use_container_width=True,
        hide_index=True
    )

    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv,
        file_name="student_performance_filtered.csv",
        mime="text/csv",
        help="Download current filtered view"
    )

# ────────────────────────────────────────────────────────────────
#  Footer
# ────────────────────────────────────────────────────────────────

st.markdown("---")

footer_col1, footer_col2 = st.columns([3,1])

with footer_col1:
    st.markdown("""
    **Student Performance Dashboard**  
    Built for TITAN SUKKUR • Data source: StudentsPerformance.csv  
    Created with ❤️ using Streamlit, Pandas, Matplotlib & Seaborn
    """)

with footer_col2:
    st.markdown(f"""
    **Last refreshed**  
    {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M PKT')}
    """)
