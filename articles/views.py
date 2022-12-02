from .models import Article
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from articles.serializers import ArticleSerializer


class ArticleListView(APIView):
    def get(self, request):

        articles_list = Article.objects.all()
        serializer = ArticleSerializer(articles_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

