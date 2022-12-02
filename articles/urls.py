from django.urls import path
from articles import views

urlpatterns = [
    path('<int:article_id>/', views.ArticleDetailView.as_view(), name='article_detail_view'),
    path('<int:article_id>/edit/', views.ArticleEditView.as_view(), name='article_edit_view'),
    path('<int:article_id>/<int:comment_id>', views.CommentEditView.as_view(), name='comment_edit_view'),
]