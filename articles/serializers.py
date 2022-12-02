from rest_framework import serializers
from articles.models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.email
    
    class Meta:
        model = Comment
        fields = ("user", "content", "created_at", "updated_at")


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("user", "content") 


class ArticleDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comment_set = CommentSerializer(many=True)

    
    def get_user(self, obj):
        return obj.user.email
    
    class Meta:
        model = Article
        fields = "__all__"
        
        
        


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class ArticleCreateSerializer(serializers.ModelSerializer): # 게시글 작성 시리얼라이즈
    class Meta:
        model = Article
        fields = ("title", "image", "content")

