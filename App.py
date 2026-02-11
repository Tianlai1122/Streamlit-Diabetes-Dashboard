# App.py

## Step 00 - Import packages
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

## Step 01 - Page config
st.set_page_config(
    page_title="Diabetes Data Dashboard 🏥",
    layout="centered",
    page_icon="🏥",
)

## Step 02 - Sidebar setup
st.sidebar.title("Diabetes Data Analysis 🏥")
page = st.sidebar.selectbox("Select Page", ["Introduction 📘", "Visualization 📊"])

## Step 03 - Header image
try:
    st.image("doc.png", width=400)
except FileNotFoundError:
    pass

st.write(" ")
st.write(" ")

## Step 04 - Load dataset with caching
@st.cache_data
def load_data():
    return pd.read_csv("diabetes.csv")

df = load_data()

## Step 05 - Pages
if page == "Introduction 📘":
    st.subheader("01 Introduction 📘")

    st.markdown("##### Data Preview")
    rows = st.slider("Select a number of rows to display", 5, 50, 10)
    st.dataframe(df.head(rows), use_container_width=True)

    st.markdown("##### Missing Values")
    missing = df.isnull().sum()
    st.write(missing)

    if missing.sum() == 0:
        st.success("✅ No missing values found")
    else:
        st.warning("⚠️ You have missing values")

    st.markdown("##### 📈 Summary Statistics")
    if st.button("Show Describe Table"):
        st.dataframe(df.describe(), use_container_width=True)

elif page == "Visualization 📊":
    st.subheader("02 Data Visualization 📊")

    df_num = df.select_dtypes(include=np.number)

    col_x = st.selectbox("Select X-axis variable", df_num.columns, index=0)
    col_y = st.selectbox("Select Y-axis variable", df_num.columns, index=1)

    tab1, tab2, tab3 = st.tabs(["Scatter Plot 🔵", "Line Chart 📈", "Correlation Heatmap 🔥"])

    with tab1:
        st.subheader("Scatter Plot")
        fig_scatter, ax_scatter = plt.subplots(figsize=(10, 6))

        if "Outcome" in df.columns:
            sns.scatterplot(data=df, x=col_x, y=col_y, hue="Outcome", ax=ax_scatter)
        else:
            sns.scatterplot(data=df, x=col_x, y=col_y, ax=ax_scatter)

        ax_scatter.set_title(f"{col_x} vs {col_y}")
        st.pyplot(fig_scatter)

    with tab2:
        st.subheader("Line Chart")
        st.line_chart(df_num[[col_x, col_y]].sort_values(by=col_x), use_container_width=True)

    with tab3:
        st.subheader("Correlation Matrix")
        fig_corr, ax_corr = plt.subplots(figsize=(12, 8))
        sns.heatmap(df_num.corr(), annot=True, fmt=".2f", ax=ax_corr)
        st.pyplot(fig_corr)