from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Q
from articles.models import Article, Comment, Book
from articles.serializers import ArticleSerializer, ArticleCreateSerializer, ArticleDetailSerializer, CommentCreateSerializer, BookSerializer,BookRecommendSerializer, ArticleAddSerializer
from rest_framework.generics import get_object_or_404
from django.db.models import Count
from articles import crowling
import json
from itertools import chain

# 파일 저장
import random
import json , csv, os, requests
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onepaper.settings")
import django
django.setup()

# crowling.function()



class ArticleView(APIView): #게시글 불러오기(인기글로) main1
    def get(self, request):
        best_list = Book.objects.all()
        serializer = BookSerializer(best_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserArticleView(APIView): #추천머신러닝을 통한 결과물 메인페이지에 보여줄거
    def get(self, request):
        if request.user.is_authenticated:
            test = request.data.get('select_books')
            userbook_list = Book.objects.filter(id__in=test)
            book_name_list = []
            for book in userbook_list:
                book_name_list.append(book.book_title)
            recommend_list = function.select_recommendations(book_name_list)
            result_list =[]
            for result in recommend_list:
                result_book = Book.objects.get(book_title = result)
                result_list.append(result_book)
            serializer = BookSerializer(result_list, many=True)
        else:
            book = Book.objects.all()
            random_book = random.sample(book, 3)
            serializer = BookSerializer(random_book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ArticleListView(APIView): # 피드페이지
    def get(self, request):
        articles_list = Article.objects.all()
        serializer = ArticleSerializer(articles_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleDetailView(APIView):
    def get(self, request, article_id): # 게시글&댓글 보여주기
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def delete(self, request, article_id): # 게시글 삭제하기
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("작성자가 아닙니다!", status=status.HTTP_403_FORBIDDEN)
    def post(self, request, article_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            serializer = ArticleCreateSerializer(article, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("작성자가 아닙니다!", status=status.HTTP_403_FORBIDDEN)

class CreateArticleView(APIView):
    def get(self, request, book_id):
        book_id = get_object_or_404(Book, id=book_id)
        print(book_id.book_title)
        serializer = BookRecommendSerializer(book_id)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        title = book.book_title
        book_id = book.id
        serializer = ArticleAddSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, select_book_id=book_id, title=title)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookSearchView(APIView): #무슨책 있는지 검색하는 곳
    def get(self, request):
        print(request.data)
        search_title = request.data.get('search_content')
        search_title = search_title.replace(" ","")
        if search_title == None :
            book = Book.objects.all()
        elif search_title:
            book = Book.objects.filter(Q(book_title__icontains=search_title))
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request): # 게시글 작성
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)



class CommentEditView(APIView):
    def put(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("작성자가 아닙니다!", status=status.HTTP_403_FORBIDDEN)
    def delete(self, request, comment_id, article_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("작성자가 아닙니다!", status=status.HTTP_403_FORBIDDEN)


class LikeView(APIView): #좋아요
    def post(self, request, article_id):
        article = get_object_or_404(Article, id = article_id)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response({"message":"좋아요 취소 완료!"}, status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response({"message":"좋아요 등록 완료!"}, status=status.HTTP_200_OK)

# csv 만들기
# with open('bookdata.csv', 'w', newline='') as csvfile:
#     fieldnames = ['book_id','book_title']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     writer.writeheader()

#     for book in Book.objects.all():
#         writer.writerow({'book_id':book.id, "book_title":book.book_title,})


