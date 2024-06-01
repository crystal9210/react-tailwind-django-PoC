from pathlib import Path
import os
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 環境変数を読み込む
env = environ.Env(
    DEBUG=(bool, False)
)

# デプロイ環境かローカル環境かを判定
if os.getenv('RENDER', 'False') == 'True':
    # デプロイ環境 (Render)
    DEBUG = env.bool('DEBUG', default=False)
    SECRET_KEY = env('SECRET_KEY')
    DATABASE_URL = env('DATABASE_URL')
    MYSITE_DOMAIN = env('MYSITE_DOMAIN')
    ALLOWED_HOSTS = ['*']  # 任意のユーザからのアクセスを許可；通常、きちんとした開発者なら許可しない
    # Render用に追加の設定があればここに記述
else:
    # ローカル環境
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
    DEBUG = env.bool('DEBUG', default=True)
    SECRET_KEY = env('SECRET_KEY')
    DATABASE_URL = env('DATABASE_URL')
    MYSITE_DOMAIN = env('MYSITE_DOMAIN')
    ALLOWED_HOSTS = ['react-tailwind-django-poc.onrender.com', '127.0.0.1', 'localhost']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY', default='')  # ローカル環境で存在しない場合のためのデフォルト設定

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = env('DEBUG')

# Application definition

INSTALLED_APPS = [
    'core.apps.CoreConfig',
    'accounts.apps.AccountsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'frontend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'work_sample1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'work_sample1.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': env.db(),
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
# デプロイ環境かローカル環境かで設定を分ける
if os.getenv('RENDER', 'False') == 'True':
    # デプロイ環境 (Render)
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "frontend/static"),
        os.path.join(BASE_DIR, "static"),
    ]
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
else:
    # ローカル環境
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "frontend/static"),
        os.path.join(BASE_DIR, "static"),
    ]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'

# ログイン・ログアウト用設定
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
