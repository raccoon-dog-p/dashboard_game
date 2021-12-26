from altair.vegalite.v4.schema.channels import Color, Column
from altair.vegalite.v4.schema.core import Scale
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from vega_datasets import data
import numpy as np
from datetime import datetime
from dateutil.parser import parse

from run_eda import sql_insert, sql_selcet

def run_history():
    df = pd.read_csv('data/new_steam.csv',index_col=0)
    # url 같은 경우 길이가 길기 때문에 따로 옵션을 설정해줘야
    # 온전히 가지고 올 수 있다.
    df['Release date'] = pd.to_datetime(df['Release date'])
    pd.set_option('display.max_colwidth', 1000) 
    df.dropna(axis=0,inplace=True)
    view_df = df.drop(['Steam id','video_url'],axis=1)
    st.title('Welcome Steam TOP 100!')
    col1, col2 = st.columns(2)
    user_input = col1.text_input('이름이나 장르로 검색하기')
    user_condition = col2.radio('게임 평으로 정렬',['All','Very Positive','Mostly Positive','Mixed','Overwhelmingly Positive'])
    search_df = view_df[(view_df['Game'].str.lower().str.contains(user_input.lower())) | (view_df['Tags'].str.lower().str.contains(user_input.lower())) ]
    if user_condition == 'All':
        user_choice_df = search_df
    else:
        user_choice_df= search_df[(search_df['Review summary'] == user_condition)]
    st.dataframe(user_choice_df)
    user_choice = st.selectbox('보고 싶은 게임 선택',user_choice_df['Game'])
    condition_df = df[df['Game'] == user_choice]
    url = list(condition_df['video_url'])
    describe = list(condition_df['describe'])
    col3, col4 = st.columns(2)
    if len(url[0]) > 5:
        col3.video(url[0])
    else:
        col3.write('이 게임은 현재 스팀에서 서비스 하고 있지 않습니다.')
    col4.subheader('Describe')
    col4.write(describe[0])
    condition_df_num = condition_df[['Game','Current players','Peak players today','Total reviews','Release date']]
    df_num = df[['Current players','Peak players today','Total reviews','Release date']]
    # 평균 날짜 구한ㄴ 함수 => 결과 2017-07-30
    # df_num['Release date']= df_num['Release date'].apply(str)
    # df_num['Release date']= df_num['Release date'].str.slice(0,11)

    # print(df_num['Release date'])
    # df_num['Release date'] = df_num['Release date'].map(
    # lambda date: pd.datetime(*tuple(map(lambda x: int(x), date.split("-"))))
    # )
    # print(df_num['Release date'].mean())
    oo = datetime(year=2017,month=7,day=30)
    print(oo)
    df_average=pd.DataFrame([{'Game':'Average','Current players':40062.4796,'Peak players today':52450.2755,'Total reviews':272358.6633,'Release date':oo}])
    df_chart = pd.concat([condition_df_num,df_average])
    # 확인결과 game 글자 수가 너무 길면 차트가 짤린다.
    # 글자가 너무 긴 건 짤라준다.
    df_chart['Game']=df_chart['Game'].str[:15]+'..'
    compare_df = view_df.drop(['Tags','describe'],axis=1)
    compare_df.loc[(compare_df['Game'] != user_choice,'Game')] = 'Others'
    compare_df.loc[(compare_df['Game'] != 'Others','Game')] = (user_choice[:15]+'..').lower()
    a=(compare_df[compare_df['Game'] == (user_choice[:15]+'..').lower()])
    compare_df= pd.concat([compare_df,a,a])
    # compare all 차트
    cp_chart1 = alt.Chart(compare_df).mark_point().encode(
        x="Current players",color='Game:N'
    ).properties(width=300,
    height=100
    )
    cp_chart2 = alt.Chart(compare_df).mark_point().encode(
        x="Peak players today",color='Game:N'
    ).properties(width=300,
    height=100
    )

    cp_chart3 = alt.Chart(compare_df).mark_point().encode(
        x="Total reviews",color='Game:N'
    ).properties(width=300,
    height=100
    )

    cp_chart4 = alt.Chart(compare_df).mark_point().encode(
        x='Release date',color='Game:N'
    ).properties(width=300,
    height=100
    )

    
    col5,col7 = st.columns(2)
    col5.header('Compare Average')
    col7.header('Comapre All data')
    col7.altair_chart(cp_chart1)
    col7.altair_chart(cp_chart2)
    col7.altair_chart(cp_chart3)
    col7.altair_chart(cp_chart4)
    chart1 = (
    alt.Chart(df_chart)
    .mark_bar()
    .encode(x="Current players", y="Game",color=alt.Color('Game',legend=None))
    ).properties(
    width= 300,
    height=100
    )
    col5.altair_chart(chart1)
    chart2 = (
    alt.Chart(df_chart)
    .mark_bar()
    .encode(x="Peak players today", y="Game",color=alt.Color('Game',legend=None))
    ).properties(
    width= 300,
    height=100
    )
    col5.altair_chart(chart2)
    chart3 = (
    alt.Chart(df_chart)
    .mark_bar()
    .encode(x="Total reviews", y="Game",color=alt.Color('Game',legend=None))
    ).properties(
    width= 300,
    height=100
    )
    col5.altair_chart(chart3)
    domain_pd = pd.to_datetime(['2000-11-01','2021-11-09']).astype(int) / 10 ** 6
    chart4 = (
    alt.Chart(df_chart)
    .mark_point()
    .encode(
        x=alt.X('Release date:T',timeUnit='yearmonthdate',scale=alt.Scale(domain=list(domain_pd))), y="Game",color=alt.Color('Game',legend=None))
    ).properties(
    width= 300,
    height=100
    )
    col5.altair_chart(chart4)
    st.write('Current players: 현재 게임을 플레이하고 있는 유저들을 의미합니다.')
    st.write('Peek players today: 당일 가장 많이 접속했던 유저수를 의미합니다.')
    st.write('Total reviews: 지금까지 받은 리뷰수를 의미합니다.')
    st.write('Release date: 게임 출시 날짜를 의미합니다.')
    if st.checkbox('describe'):
        st.dataframe(df_chart)
    sql_insert(user_choice)
    history = set(sql_selcet())
    st.subheader('최근 본 게임')
    st.selectbox('',history)
    st.subheader('비슷한 게임 추천')
    
    # 비슷한 게임 추천
    # 유저가 현재 보고있는 게임과 비슷한 게임을 추천할것
    # tag를 이용하여 split으로 쪼개준 후 set으로 저장 (중복 안되게)
    # 각 데이터 리스트 tag에 단어가 들어있을때마다 count 컬럼을 만들어 1씩 추가
    # 그렇게 추가 된 count 컬럼으로 정렬 후 위에서 부터 5개 순위로 가져온 후
    # 셀렉트 박스를 이용하여 고를 수 있게 만듬.

