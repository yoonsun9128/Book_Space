import pandas as pd
from tqdm import tqdm_notebook
import re
from urllib.request import urlopen
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

books = pd.read_csv('articles/database/bookdata.csv', encoding='UTF-8')

books['합침'] = (books['book_title']) + (books['book_content'])
books['합침'] = books['합침'].fillna('')
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(books['book_content'].values.astype('U'))
cosine_a = cosine_similarity(tfidf_matrix, tfidf_matrix)
indices = pd.Series(books.index, index=books['book_title']).drop_duplicates()
title_to_index = dict(zip(books['book_title'], books.index))


def select_recommendations(check_list):
    total_book_list = []
    for a in check_list:
        one_book = a
        index_no = title_to_index[one_book]
        # 해당 가게와 모든 가게의 유사도를 가져온다.
        sim_scores = list(enumerate(cosine_a[index_no]))
        # 유사도에 따라 가게들을 정렬한다.
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # 가장 유사한 10개의 가게 받아온다.유사도 검사결과
        sim_scores = sim_scores[1:2]
        # 가장 유사한 10개의 가게 인덱스를 얻는다.
        store_indices = [idx[0] for idx in sim_scores]
        store_result = []
        for x in store_indices:
            data = books['book_title'].iloc[x]
            store_result.append(data)
        total_book_list.append(store_result)
        print("비교",store_result)
    print(total_book_list)