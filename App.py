__author__ = 'Chunpu Tianlai Zhang, tianlaiz@unc.edu, Onyen = tianlaiz'

## Step 00 - Import packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

## Step 01 - Page config
st.set_page_config(
    page_title="Diabetes Data Dashboard 🏥",
    layout="centered",
    page_icon="🏥",
)

## Step 02 - Sidebar setup
st.sidebar.title("Diabetes Data Analysis 🏥")
page = st.sidebar.selectbox("Select Page", ["Introduction 📘", "Visualization 📊", "Automated Report 📑"])

## Step 03 - Header image
try:
    st.image("doc.png", width=400)
except FileNotFoundError:
    st.warning("⚠️ Image file 'doc.png' not found")

st.divider()

## Step 04 - Load dataset with caching
@st.cache_data
def load_data():
    return pd.read_csv("diabetes.csv")

df = load_data()

## Step 05 - Page: Introduction
if page == "Introduction 📘":
    st.subheader("01 Introduction 📘")

    st.markdown("##### Data Preview")
    rows = st.slider("Select a number of rows to display", 5, 20, 5)
    st.dataframe(df.head(rows))

    st.markdown("##### Missing Values")
    missing = df.isnull().sum()
    st.write(missing)

    if missing.sum() == 0:
        st.success("✅ No missing values found")
    else:
        st.warning("⚠️ You have missing values")

    st.markdown("##### 📈 Summary Statistics")
    if st.button("Show Describe Table"):
        st.dataframe(df.describe())

## Step 06 - Page: Visualization
elif page == "Visualization 📊":
    st.subheader("02 Data Visualization 📊")

    col_x = st.selectbox("Select X-axis variable", df.columns, index=0)
    col_y = st.selectbox("Select Y-axis variable", df.columns, index=1)

    tab1, tab2, tab3, tab4 = st.tabs(["Scatter Plot 🔵", "Bar Chart 📊", "Line Chart 📈", "Correlation Heatmap 🔥"])

    with tab1:
        st.subheader("Scatter Plot")
        fig_scatter, ax_scatter = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x=col_x, y=col_y, hue="Outcome", palette="coolwarm", ax=ax_scatter)
        ax_scatter.set_title(f"{col_x} vs {col_y}")
        st.pyplot(fig_scatter)

    with tab2:
        st.subheader("Bar Chart")
        st.bar_chart(df[[col_x, col_y]].sort_values(by=col_x), use_container_width=True)

    with tab3:
        st.subheader("Line Chart")
        st.line_chart(df[[col_x, col_y]].sort_values(by=col_x), use_container_width=True)

    with tab4:
        st.subheader("Correlation Matrix")
        df_numeric = df.select_dtypes(include=np.number)
        fig_corr, ax_corr = plt.subplots(figsize=(12, 8))
        sns.heatmap(df_numeric.corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax_corr)
        st.pyplot(fig_corr)

## Step 07 - Page: Automated Report
elif page == "Automated Report 📑":
    st.subheader("03 Automated Report 📑")
    if st.button("Generate Report"):
        try:
            with st.spinner("Generating report..."):
                profile = ProfileReport(df, title="Diabetes Data Report", explorative=True, minimal=True)
                st_profile_report(profile)

            export = profile.to_html()
            st.download_button(
                label="📥 Download Full Report",
                data=export,
                file_name="diabetes_report.html",
                mime="text/html",
            )
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")
            st.info("Make sure ydata-profiling and streamlit-pandas-profiling are installed")
