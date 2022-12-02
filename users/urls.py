from django.urls import path
from rest_framework_simplejwt.views import ( TokenObtainPairView,TokenRefreshView, )
from users import views


urlpatterns = [
    path('signup/', views.UserView.as_view(), name='UserView'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<int:user_id>/', views.UserMypageView.as_view(), name='user_mypage_view'),
    # path('<int:user_id>/edit/', views.UserDetailView.as_view(), name='user_edit_view'),
]
