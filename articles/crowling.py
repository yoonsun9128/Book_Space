import requests, bs4
import pandas as pd
from articles.models import Book
import time

def function():
    # book = Book()
    for j in range(1,5):
        url = f"http://www.yes24.com/24/category/bestseller?CategoryNumber=001&sumgb=06&PageNumber={j}&FetchSize=80"
        response = requests.get(url).text.encode('utf-8')
        response = bs4.BeautifulSoup(response, 'html.parser')


        target = response.find('table', {'id':'category_layout', 'class':'list'})
        T = target.find_all('div', {'class' : 'goodsImgW'})

        text_list = [str(x).split('\n') for x in T]
        print("너뭐야",text_list[0][2])
        book_info = {
            "book_title":"",
            "book_img":"",
            "book_url":"",
            "book_content":""
        }
        for i in range(0,5):
            book = Book()
            book_info["book_title"] = text_list[i][2].split('"')[1]
            print(book_info["book_title"])
            print("---------------------------")
            book_info["book_img"] =  text_list[i][2].split('"')[3]
            print("---------------------------")
            book_info["book_url"] = text_list[i][1].split('"')[1]
            
            print("---------------------------")
            target2 = response.find('table', {'id':'category_layout', 'class':'list'})
            T2 = target.find_all('')

            book_info["book_url"] = text_list[i][1].split('"')[1]
            each_raw = requests.get("http://www.yes24.com"+book_info["book_url"],
                    headers = {"User-Agent" : "Mozilla/5.0"})

            each_html = bs4.BeautifulSoup(each_raw.text, 'html.parser')
            contents = each_html.select("textarea.txtContentText")[0]
            content_list = [x.get_text().replace('\r\n',"") for x in contents]
            book_info["book_content"] = ''.join(s for s in content_list)
            # time.sleep(2)
            book.book_title = book_info["book_title"]
            book.img_url = book_info["book_img"]
            book.book_link = "http://www.yes24.com"+book_info["book_url"]
            book.book_content = book_info["book_content"]
            book.save()


        



