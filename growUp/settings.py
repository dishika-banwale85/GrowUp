from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv() 

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-rr8awn*9-lh9p6n7g(errkbipapj1qlqzqti_d97)rk8)t07zk'
DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "arrythmical-meridith-unvenially.ngrok-free.dev"
]
CSRF_TRUSTED_ORIGINS = [
    "https://arrythmical-meridith-unvenially.ngrok-free.dev"
]
# ----------------------------------------------------------
# INSTALLED APPS
# ----------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Required for allauth
    'django.contrib.sites',
    # Django allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.instagram',
    # 'allauth.socialaccount.providers.youtube',
    'allauth.socialaccount.providers.facebook',
    # Your apps
    'core.apps.CoreConfig',
    'tailwind',
    'curvy',
    'django_browser_reload',
]

SITE_ID = 1
TAILWIND_APP_NAME = 'curvy'

# ----------------------------------------------------------
# AUTHENTICATION BACKENDS
# ----------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# ----------------------------------------------------------
# LOGIN / LOGOUT SETTINGS
# ----------------------------------------------------------
LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/profile/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# ----------------------------------------------------------
# DJANGO-ALLAUTH ACCOUNT SETTINGS
# ----------------------------------------------------------
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_DEBUG = True

# ----------------------------------------------------------
# Instagram OAuth Settings
# ----------------------------------------------------------
INSTAGRAM_CLIENT_ID = str(os.getenv('INSTAGRAM_CLIENT_ID'))
INSTAGRAM_CLIENT_SECRET = str(os.getenv('INSTAGRAM_CLIENT_SECRET'))
INSTAGRAM_REDIRECT_URI = str(os.getenv('INSTAGRAM_REDIRECT_URI'))
INSTAGRAM_AUTH_URL = str(os.getenv('INSTAGRAM_AUTH_URL'))
INSTAGRAM_TOKEN_URL = str(os.getenv('INSTAGRAM_TOKEN_URL'))
INSTAGRAM_API_URL = str(os.getenv('INSTAGRAM_API_URL'))
#-----------------------------------------------------------

# Allow secure cookies through ngrok
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# So Django knows it’s behind a proxy
USE_X_FORWARDED_HOST = True
# ----------------------------------------------------------
# Google OAuth Settings
# ----------------------------------------------------------
GOOGLE_CLIENT_ID = str(os.getenv('GOOGLE_CLIENT_ID'))
GOOGLE_CLIENT_SECRET = str(os.getenv('GOOGLE_CLIENT_SECRET'))
GOOGLE_REDIRECT_URI = str(os.getenv('GOOGLE_REDIRECT_URI'))

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id':os.getenv('GOOGLE_CLIENT_ID'),
            'secret':os.getenv('GOOGLE_CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}

# ----------------------------------------------------------
# MIDDLEWARE
# ----------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Allauth
    'allauth.account.middleware.AccountMiddleware',
    # Optional for dev reload
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

# ----------------------------------------------------------
# TEMPLATES
# ----------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # required by allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'growUp.urls'
WSGI_APPLICATION = 'growUp.wsgi.application'

# ----------------------------------------------------------
# DATABASE
# ----------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ----------------------------------------------------------
# PASSWORD VALIDATORS
# ----------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ----------------------------------------------------------
# INTERNATIONALIZATION
# ----------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ----------------------------------------------------------
# STATIC FILES
# ----------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

