from django.urls import path, include, re_path
from rest_framework_simplejwt.views import ( TokenObtainPairView,TokenRefreshView, )
from users import views
from dj_rest_auth.registration.views import VerifyEmailView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('<int:user_id>/', views.MypageView.as_view(), name='MypageView'),
    path('<int:user_id>/image', views.MypageImage.as_view(), name='MypageImageView'),


    path('', views.RecommendView.as_view(), name='recommend_view'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # 유효한 이메일이 유저에게 전달
    re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # 유저가 클릭한 이메일(=링크) 확인
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', views.ConfirmEmailView.as_view(), name='account_confirm_email'),

]
