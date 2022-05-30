import streamlit as st
import pandas as pd

def run_home() :
    df1 = pd.read_csv('data/pre_data.csv', index_col=0)
    df2 = pd.read_csv('data/X.csv', index_col=0)
    search = st.text_input('웹툰명이나 장르 검색')
    
    df1['title'].str.lower().str.contains(search)
    st.dataframe(df1)

    
    st.dataframe(df2)
