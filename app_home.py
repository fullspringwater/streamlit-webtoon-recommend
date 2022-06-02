import streamlit as st
import pandas as pd
from PIL import Image
import webbrowser
import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objects as go
def run_home() :
    df1 = pd.read_csv('data/pre_data.csv', index_col=0)
    X = pd.read_csv('data/X.csv', index_col=0)
    y = pd.read_csv('data/y.csv', index_col=0)
    kn = joblib.load('data/kn.pkl')


    search = st.text_input('웹툰명이나 장르 검색')
    search_result = df1.loc[df1['title'].str.lower().str.contains(search) | 
            df1['genre'].str.lower().str.contains(search),]
    search_list = search_result['title'].values

    if len(search_list) != 0 :
        selected = st.selectbox('검색 결과 리스트', search_list)
        st.markdown("---")
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #9EE681;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">{}</p>'.format(selected), unsafe_allow_html=True)
        # st.subheader(selected)
        col1, col2 = st.columns([3, 1])

        

        with col1:
            st.subheader('장르')
            st.text(df1.loc[df1['title'] == selected,'genre'].values[0])
          
            st.subheader('회차 수')
            st.text(df1.loc[df1['title'] == selected,'episodes'].values[0])
          
            st.subheader('줄거리')
            st.write(df1.loc[df1['title'] == selected,'summary'].values[0])

            
        with col2:
            st.subheader('조회수')
            st.text('{}M'.format(df1.loc[
                    df1['title'] == selected,'view[M]'].values[0]))
            
            st.subheader('구독자 수')
            st.text('{}M'.format(df1.loc[
                    df1['title'] == selected,'subscribe[M]'].values[0]))

            st.subheader('좋아요 수')
            st.text('{}M'.format(df1.loc[
                    df1['title'] == selected,'likes[M]'].values[0]))
            
            st.subheader('출시일')
            st.text(df1.loc[df1['title'] == selected,'released_date'].values[0])

        


        url = df1.loc[df1['title'] == selected,'url'].values[0]
        st.subheader('[보러가기]({})'.format(url))

        st.markdown("---")
        st.subheader('다른 추천 웹툰')

        # 추천기능
        distances, indices = kn.kneighbors(
                    np.array(X.loc[selected]).reshape(1,21))
        nearest_webtoons = [
            y.loc[i][0] for i in indices.flatten()][1:]
        sim_rates = []
        summary = []
        genre = []
        recommended_url = []

        for webtoon in nearest_webtoons :
            summary.append(df1.loc[df1['title'] == webtoon]['summary'].reset_index().values[0,1])
            genre.append(df1.loc[df1['title'] == webtoon]['genre'].reset_index().values[0,1])
            recommended_url.append(df1.loc[df1['title'] == webtoon]['url'].reset_index().values[0,1])
            sim = cosine_similarity(np.array(X.loc[selected]).reshape(1,21),
                                    np.array(X.loc[webtoon]).reshape(1,21)).flatten()
            sim_rates.append(sim[0])
        
        # 추천웹툰 데이터프레임 생성
        recommended_webtoons = pd.DataFrame({'추천 웹툰' : nearest_webtoons,
                                     '유사도' : sim_rates,
                                     '장르' : genre,
                                     '줄거리' : summary,
                                     'url' : recommended_url} )
        recommended_webtoons.sort_values('유사도', ascending =False, inplace = True)
        
        for i in range(4) :

            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #9EE681;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">{}</p>'.format(recommended_webtoons.iloc[i,0]), unsafe_allow_html=True)    

             #유사도
            st.subheader(recommended_webtoons.columns[1])
            st.text('{} %'.format(round(recommended_webtoons.iloc[i,1]*100)))
            
            # 장르
            st.subheader(recommended_webtoons.columns[2])
            st.write(recommended_webtoons.iloc[i,2])
           
            #줄거리
            st.subheader(recommended_webtoons.columns[3])
            st.write(recommended_webtoons.iloc[i,3])

            st.subheader('[보러가기]({})'.format(recommended_webtoons.iloc[i,4]))
            
            st.markdown('---')

        


    else :
        st.text('검색 결과가 없습니다.')

