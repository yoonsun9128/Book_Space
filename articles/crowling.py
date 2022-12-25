import requests, bs4
import pandas as pd
from articles.models import Book
import time

def function():
    a = []
    # book = Book()
    for j in range(1,7): #1페이지 당 80개의 데이터
        url = f"http://www.yes24.com/24/category/bestseller?CategoryNumber=001&sumgb=06&PageNumber={j}&FetchSize=80"
        response = requests.get(url).text.encode('utf-8')
        response = bs4.BeautifulSoup(response, 'html.parser')

        target = response.find('table', {'id':'category_layout', 'class':'list'})
        T = target.find_all('div', {'class' : 'goodsImgW'})

        text_list = [str(x).split('\n') for x in T]

        book_info = {
            "book_title":"",
            "book_img":"",
            "book_url":"",
            "book_content":""
        }
        for i in range(0,80): #79로 설정해야 80개의 데이터가 나옴
            book = Book()
            book_info["book_title"] = text_list[i][2].split('"')[1]
            book_info["book_img"] =  text_list[i][2].split('"')[3].replace("S", "XL")
            book_info["book_url"] = text_list[i][1].split('"')[1]
            each_raw = requests.get("http://www.yes24.com"+book_info["book_url"],
                    headers = {"User-Agent" : "Mozilla/5.0"})

            each_html = bs4.BeautifulSoup(each_raw.text, 'html.parser')

            genre_html = each_html.select('#infoset_goodsCate > div.infoSetCont_wrap > dl > dd > ul > li:nth-child(1) > a:nth-child(4)')
            

            try:
                contents = each_html.select("textarea.txtContentText")[0]
                genre= genre_html[0].text
                if genre == "자연과학" or genre == "인문" or genre == "역사" or genre == "종교" or genre == "사회 정치" or genre == "예술" :
                    genre = "교육"
                elif genre == "수험서 자격증" or genre == "국어 외국어 사전":
                    genre = "자격증시험"
                elif genre == "유아" or genre == "어린이" or genre == "청소년":
                    genre = "어린이"
                elif genre == "건강 취미" or genre == "자기계발" or genre == "가정 살림":
                    genre = "자기계발"
                else:
                    genre = "기타"                
            except IndexError:
                contents = ''
                genre = ''
            content_list = [x.get_text().replace('\r\n',"") for x in contents]
            book_info["book_content"] = ''.join(s for s in content_list)

            book.book_title = book_info["book_title"]
            book.img_url = book_info["book_img"]
            book.book_link = "http://www.yes24.com"+book_info["book_url"]
            book.book_content = book_info["book_content"]
            book.book_genre = genre
            book.save()






