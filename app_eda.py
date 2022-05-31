import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

def run_eda() :
    df= pd.read_csv('data/pre_data.csv', index_col=0)
    st.dataframe(df)
    
    # 장르별 웹툰 수 
    fig1 = px.histogram(df, x = 'genre', color = 'genre',
                        title='장르별  웹툰 수')
    st.plotly_chart(fig1)

    # 장르별 평점 분포
    fig2 = px.scatter(df, x='genre', y = 'grade', color='genre',
                        title='장르별 평점 분포')
    st.plotly_chart(fig2)

    # 장르별 조회수 분포
    fig3 = px.histogram(df, x="view[M]",color = 'genre', 
                        nbins = 15, title='장르별 조회수 분포')
    st.plotly_chart(fig3)

    # 장르별 좋아요 분포
    fig4 = px.histogram(df, x="likes[M]",color = 'genre', 
                        nbins=15, title='장르별 좋아요 분포')
    st.plotly_chart(fig4)

    # 출시 년도별 작품, 장르 분포
    fig5 = px.histogram(df, x="released_year",
                        color = 'genre', title='출시 년도별 작품, 장르 분포')
    st.plotly_chart(fig5)

    # 년도별 조회수, 구독자수, 좋아요수 평균
    st.line_chart(df.groupby('released_year')[['view[M]']].mean())
    st.line_chart(df.groupby('released_year')[['subscribe[M]']].mean())
    st.line_chart(df.groupby('released_year')[['likes[M]']].mean())




    # 상관관계
    fig2 = plt.figure()
    sns.heatmap(df.corr(), annot=True, cmap='Blues')
    plt.title('Correlation')
    st.pyplot(fig2)



