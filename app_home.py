import streamlit as st
import pandas as pd

def run_home() :
    df1 = pd.read_csv('data/pre_data.csv', index_col=0)
    df2 = pd.read_csv('data/X.csv', index_col=0)
    
    search = st.text_input('웹툰명이나 장르 검색')
    search_result = df1.loc[df1['title'].str.lower().str.contains(search) | 
            df1['genre'].str.lower().str.contains(search),]


    search_list = search_result['title'].values
    if len(search_list) != 0 :
        selected = st.selectbox('검색 결과 리스트', search_list)
        st.subheader(selected)
    else :
        st.text('검색 결과가 없습니다.')

