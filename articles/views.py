from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from articles.models import Article, Comment
from articles.serializers import ArticleDetailSerializer, ArticleCreateSerializer, CommentCreateSerializer
from rest_framework.generics import get_object_or_404


# Create your views here.

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
        
        
class ArticleEditView(APIView):
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