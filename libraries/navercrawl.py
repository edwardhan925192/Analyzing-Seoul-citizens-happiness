
import os
import sys
import urllib.request
import json
import string
from functools import reduce
import pandas as pd
import numpy as np
import string
from tqdm import tqdm
import re
from collections import Counter
# 함수로 다시 표현.....................
def naverCrawling(encText,kind = 'news',display=100,start=1,sort='sim'):
  client_id = 'ROzTdbEhF8zEFtqg2dbw'
  client_secret = 'gkqKs44TH4'
  encText = urllib.parse.quote(encText)
  url_ = f"https://openapi.naver.com/v1/search/{kind}"      
  url = f"{url_}?query={encText}&display={display}&start={start}&sort={sort}"  

  request = urllib.request.Request(url)
  request.add_header("X-Naver-Client-Id",client_id)
  request.add_header("X-Naver-Client-Secret",client_secret)
  with urllib.request.urlopen(request) as response:
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        datas = json.loads(response_body.decode('utf-8'))
        return datas['items']
    else:
        print("Error Code:" + rescode)



#display --> 100
#number_of_page --> 페이지수 
#sort --> 방법 
#data frame 형태로 변환해줌 
def news_list(display_num = 100, number_of_page = 2,sort_how = 'sim' ):
  encText = input("검색어 : ")
  df_list = []
  title_list, originallink_list,link_list, desription_list =[],[],[],[]

  for page in tqdm(range(1,number_of_page)):
    datas = naverCrawling(encText,start = page,display = display_num,sort = sort_how)
    for data in datas: 
      title_list.append(data['title'])
      originallink_list.append(data['originallink'])
      link_list.append(data['link'])
      desription_list.append(data['description']) 
  df2 = pd.DataFrame({'title':title_list, 'orignal':originallink_list,'link':link_list, 'desc':desription_list}) 
  
  df2['title'] = df[['title']].applymap(to_korean)
  df2['desc'] = df[['desc']].applymap(to_korean)
  #df = df.apply(to_korean, axis = 0)
  return(df2)

def to_korean(word):
  puch = string.punctuation
  # 한글 정규표현식 패턴
  hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
  return "".join([ hangul.sub('', i) for i in word if i not in puch ])

#dataframe 형태 
def korean_values_count(list_you_want):
  puch = string.punctuation
  df2 = pd.DataFrame({'title':list_you_want})
  temp = df2['title'].apply(lambda x: x.split())
  temp = [ i for i in temp.values]
  temp = reduce(lambda x,y : x+y, temp)  # 단일 리스트 형태로 변경
  word_list_cnt =  Counter( [ i for i in map(to_korean, temp) if len(i) > 1] )
  word_list_cnt = dict(word_list_cnt)
  word_list_cnt.values
  word_list_cnt = sorted(word_list_cnt.items(), key = lambda x : x[1],reverse=True)
  return word_list_cnt

