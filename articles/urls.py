
from django.urls import path
from articles import views

urlpatterns = [
    path('', views.ArticleView.as_view(), name='article_view'),
    path('user/', views.UserArticleView.as_view(), name='user_article_view'),
    path("list/", views.ArticleListView.as_view(), name = "main_list"),
    path('<int:article_id>/', views.ArticleDetailView.as_view(), name='article_detail_view'),
    path('<int:article_id>/edit/', views.ArticleEditView.as_view(), name='article_edit_view'),
    path('<int:article_id>/<int:comment_id>/', views.CommentEditView.as_view(), name='comment_edit_view'),
    path("like/<int:article_id>/", views.LikeView.as_view(), name="like_view"),
]


