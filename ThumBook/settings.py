
from pathlib import Path
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",
    "articles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "rest_framework.authtoken",
    "six",
    "drf_yasg",
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS' : 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE' : 10,
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ThumBook.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, 'templates'),
            ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ThumBook.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

SIMPLE_JWT = {
    # 토근으로 로그인이 유지되는 시간
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=500),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_L10N = True

USE_I18N = True

USE_TZ = False

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = 'users.User'
CORS_ALLOW_ALL_ORIGINS = True


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' # 메일 호스트 서버
EMAIL_PORT = '587' # gmail과 통신하는 포트
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER") # 발신할 이메일
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD") # 발신할 메일의 비밀번호
EMAIL_USE_TLS = True # TLS 보안 방법
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# URL_FRONT = 'http://****' # 공개적인 웹페이지가 있다면 등록
ACCOUNT_CONFIRM_EMAIL_ON_GET = True # 유저가 받은 링크를 클릭하면 회원가입 완료되게끔
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# ACCOUNT_EMAIL_VERIFICATION = "none"
EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '127.0.0.1:5500/' # 사이트와 관련한 자동응답을 받을 이메일 주소,'webmaster@localhost'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
# 이메일에 자동으로 표시되는 사이트 정보
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Thumbook]"

SITE_ID = 1
REST_USE_JWT = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username" # username 필드 사용 x
ACCOUNT_USERNAME_REQUIRED = True        # username 필드 사용 x
ACCOUNT_AUTHENTICATION_METHOD = 'email'

