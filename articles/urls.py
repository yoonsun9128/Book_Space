
from django.urls import path, include

from django.urls import path

from articles import views

urlpatterns = [
    path('', views.ArticleView.as_view(), name='article_view'),
    path("main/list/", views.ArticleListView.as_view(), name = "main_list")
]
