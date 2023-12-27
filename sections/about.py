import streamlit as st
import pandas as pd

def show():
    st.subheader("Gen AI Proficient - Team D")
    df = df1 = pd.DataFrame([['Samira Hammiche', '052046'], ['Abhijit Kulkarni', '002724'], ['Shoeb Sayyed', '049706']], columns=["Name", "Employee ID"], index=["1", "2", "3"])
    st.table(df)
