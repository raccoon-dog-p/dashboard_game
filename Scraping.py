import pandas as pd
import requests
from bs4 import BeautifulSoup

df = pd.read_csv('data/steam_top_100.csv')

# steam 의 비디오 url 가져오기
# 1-1 URL 리스트를 먼저 만들고 가져와야겠다.
# 'https://store.steampowered.com/app/steam_id/title 의 형식으로 스팀은
# 홈페이지 url 을 저장한다. 따라서 데이터 프레임에 있는 steam id 와 game 컬럼을
# 이용해줘 리스트를 만든다.
steam_id_list = list(df['Steam id'])
title_list = list(df['Game'])
url_list = []
for steam_id in steam_id_list:
    url_list.append('https://store.steampowered.com/app/'+str(steam_id))
for i in range(100):
    url_list[i] = url_list[i]+title_list[i]
video_url_list=[]
for url in url_list:
    res = requests.get(url)
    soup = BeautifulSoup(res.content,'html.parser')
    # 스팀 홈페이지의 f12를 눌러보면 비디오가 들어있는 div class를 확인할 수 있다.
    soup_find = soup.find('div',{'class':'highlight_player_item highlight_movie'})
    # soup_find 을 문자열로 바꾼뒤 가공
    soup_find = str(soup_find).split()
    # 데이터가 있는 경우에는 더하고  
    if len(soup_find)>10:
        video_url = []
        for i in soup_find:
            # 최신 나온 게임의 경우 data-hd-src에 url 저장하고 
            # 옛날에 나온 게임은 data-mp4-hd-source에 저장하므로 둘 다 가져옴
            if ('data-mp4-hd-source' or 'data-hd-src') in i:
                video_url.append(i)
                video_url_list.append(video_url[0].split('"')[1])
            else:
                pass
    # 없는경우는 Nan을 추가해서 원본 데이터에 그대로 붙일 수 있게 만듬.
    else:
        video_url_list.append('Nan')
# 잘 됐는지 개수 확인
print(len(video_url_list))
# Nan이 있는 데이터의 경우 스팀 서비스를 종료한 게임들이다.
describe_list = []
for url in url_list:
    res = requests.get(url)
    soup = BeautifulSoup(res.content,'html.parser')
    soup_find = soup.find('div',{'class':'game_description_snippet'})
    soup_find = str(soup_find)
    if len(soup_find)>5:
        # soup_find[48:-13]을 사용한 이유는?
        # soup_find 자체를 어펜드 해버리면 다음과 같이 저장한다.
        # '<div class="game_description_snippet">\r\n\t\t\t\t\t\t\t\tExplore a thrilling, open-world MMO filled with danger and opportunity where you\'ll forge a new destiny 
        #  on the supernatural island of Aeternum.\t\t\t\t\t\t\t</div>'
        # 조건을 이용해서 빼는것도 좋지만 앞에서부터 뒤까지 슬라이싱 하는게 나을거 같다.
        # len(<div class="game_description_snippet">\r\n\t\t\t\t\t\t\t\t) 과
        # len(\t\t\t\t\t\t\t</div>) 으로 길이를 구하고 앞에서 부터 뒤까지 추출한다.
        describe_list.append(soup_find[48:-13])
            
    else:
        describe_list.append('Nan')
# 개수 확인하고
print(len(describe_list))
# 컬럼 추가하고
df['video_url']= video_url_list
df['describe'] = describe_list
# 저장해준다.
df.to_csv('data/new_steam.csv')