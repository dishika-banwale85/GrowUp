from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------------
# SECURITY
# ----------------------------------------------------------
# Moved to .env — never hardcode this
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY is not set in environment variables.")

# Read from env — default False for safety
DEBUG = os.getenv('DEBUG', 'False') == 'True'

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
    'rest_framework',
    'corsheaders',
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

# FIX: was True — allows CSRF-based forced login via GET request
SOCIALACCOUNT_LOGIN_ON_GET = False

SOCIALACCOUNT_DEBUG = True

# ----------------------------------------------------------
# Instagram OAuth Settings
# FIX: removed str() wrapper — str(None) gives "None" not None,
#      silently hiding missing env vars
# ----------------------------------------------------------
INSTAGRAM_CLIENT_ID = os.getenv('INSTAGRAM_CLIENT_ID')
INSTAGRAM_CLIENT_SECRET = os.getenv('INSTAGRAM_CLIENT_SECRET')
INSTAGRAM_REDIRECT_URI = os.getenv('INSTAGRAM_REDIRECT_URI')
INSTAGRAM_AUTH_URL = os.getenv('INSTAGRAM_AUTH_URL')
INSTAGRAM_TOKEN_URL = os.getenv('INSTAGRAM_TOKEN_URL')
INSTAGRAM_API_URL = os.getenv('INSTAGRAM_API_URL')

# ----------------------------------------------------------
# Google OAuth Settings
# FIX: removed str() wrapper (same reason as above)
# ----------------------------------------------------------
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')

# ----------------------------------------------------------
# Facebook Webhook
# ----------------------------------------------------------
FACEBOOK_VERIFY_TOKEN = os.getenv('FACEBOOK_VERIFY_TOKEN')

# ----------------------------------------------------------
# Allauth Social Providers
# ----------------------------------------------------------
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}

# Allow secure cookies through ngrok
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# So Django knows it's behind a proxy
USE_X_FORWARDED_HOST = True

# ----------------------------------------------------------
# MIDDLEWARE
# ----------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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
                'django.template.context_processors.request',
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


CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
CORS_ALLOW_ALL_ORIGINS = True

import cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
)
