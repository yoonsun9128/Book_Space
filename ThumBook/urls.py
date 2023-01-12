
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="TO-DO API",  # 타이틀
        default_version='v1',   # 버전
        description="Swagger 정복기",   # 설명
        terms_of_service="https://azalea-keep-in-mind.tistory.com/1",
        contact=openapi.Contact(email="bristol9128@naver.com")
),
    validators=['flex'],
    public=True,
    permission_classes=(permissions.AllowAny,)
)


urlpatterns = [
    # swagger
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("articles/", include("articles.urls")),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)