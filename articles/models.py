from django.db import models

class Article(models.Model):
    #user = models.ForeignKey(User) 유저모델 생성후
    title = models.TextField()
    content = models.TextField()
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
