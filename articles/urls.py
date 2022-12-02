from django.urls import path, include
from articles import views

urlpatterns = [
    path("main/list/", views.ArticleListView.as_view(), name = "main_list")
]
