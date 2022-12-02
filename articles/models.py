from django.db import models
from users.models import User

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    image = models.ImageField()
    likes = models.ManyToManyField(User, related_name="likes_articles")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)