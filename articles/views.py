from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from articles.models import Article
from articles.serializers import ArticleSerializer, ArticleCreateSerializer, ArticleCreateSerializer
class ArticleView(APIView): #게시글 불러오기(인기글로)
    def get(self, request):
        popular_articles = Article.objects.all().order_by('likes')[:2]
        serializer = ArticleSerializer(popular_articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request): # 게시글 작성
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)       



class ArticleListView(APIView):
    def get(self, request):

        articles_list = Article.objects.all()
        serializer = ArticleSerializer(articles_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        



    

