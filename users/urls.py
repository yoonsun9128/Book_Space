from django.urls import path
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView, )
from users import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('signup/', views.UserView.as_view(), name='UserView'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<int:user_id>/', views.MypageView.as_view(), name='MypageView'),
    path('<int:user_id>/likes/', views.LikeArticlesView.as_view(), name="LikeArticlesView"), #좋아요 게시글 보기
    path('<int:user_id>/image', views.MypageImage.as_view(), name='MypageImageView'),
    path('most-numberous/', views.MostNumberousBook.as_view(), name='most_numberous'),
    path('user-choice/', views.UserChoiceBook.as_view(), name='user_choice'),
    path('', views.RecommendView.as_view(), name='recommend_view'),
    path('inquiry/', views.InquiryView.as_view(), name='inquiry_view'),
    path('activate/<str:uidb64>/<str:token>/', views.UserActivate.as_view(), name='activate'),
    # 비밀번호 변경 파트
    path('password_reset/', views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
