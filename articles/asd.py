import pandas as pd 
import numpy as np
from math import sqrt

# 데이터 읽어오기 
books=pd.read_csv("../articles/database/bookdata.csv", encoding='CP949')
ratings=pd.read_csv("../articles/database/ratings.csv", encoding='CP949')

data=pd.merge(ratings, books, on="bookId")
column=['userId','bookId','rating','book_title']
data=data[column]
data
 
bookdata=data.pivot_table(index="bookId",  columns='userId')['rating']
print(bookdata)
bookdata.fillna(-1, inplace=True)


def sim_distance(data, n1, n2):
    sum=0
    #두 사용자가 모두 본 영화를 기준으로 해야해서 i로 변수 통일(j따로 안 써줌)
    for i in data.loc[n1,data.loc[n1,:]>=0].index:
         if data.loc[n2,i]>=0:
            sum+=pow(data.loc[n1,i]-data.loc[n2,i],2) #누적합 
    return sqrt(1/(sum+1)) #유사도 형식으로 출력 

def top_match(data, name, rank = 5, simf = sim_distance):
    simList = []
    for i in data.index[-10:]:
        if name != i:
            simList.append((simf(data, name, i), i))
    simList.sort()
    simList.reverse()    
    return simList[:rank]

def recommendation(data, person, simf = sim_distance):
    res = top_match(data, person, len(data))
    score_dic = {}
    sim_dic = {}
    myList = []
    for sim, name in res:
        if sim < 0:
            continue
        for movie in data.loc[person, data.loc[person, :] < 0].index:
            simSum = 0
            if data.loc[name, movie] >= 0:
                simSum += sim * data.loc[name, movie]
                
                score_dic.setdefault(movie, 0)
                score_dic[movie] += simSum
                
                sim_dic.setdefault(movie, 0)
                sim_dic[movie] += sim                
    for key in score_dic:
        myList.append((score_dic[key] / sim_dic[key], key))
    myList.sort()
    myList.reverse()
    
    return myList

# 25번 user가 안본 영화중에서 
#추천 점수가 가장 높은 순으로 예상평점과 영화제목을 추천 (10개까지)
movieList = []
for rate, b_id in recommendation(bookdata, 25):
    movieList.append((rate, books.loc[books['bookId'] == b_id, 'book_title'].values[0]))

movieList[:3]
print(movieList[:3])