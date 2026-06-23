from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core import api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('account/', include('allauth.urls')),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Auth
    path('api/signup/', api_views.signup_api, name='api_signup'),
    path('api/auth/google/', api_views.google_auth_api, name='google_auth_api'),

    # Profile
    path('api/profile/', api_views.profile_api, name='api_profile'),

    # Connected accounts
    path('api/connected-accounts/', api_views.connected_accounts_api, name='connected_accounts'),

    # Connect platforms
    path('api/connect/instagram/', api_views.instagram_connect_api, name='instagram_connect'),
    path('api/connect/facebook/', api_views.facebook_connect_api, name='facebook_connect'),

    # Create post
    path('api/create-post/', api_views.create_post_api, name='create_post'),

    # Dev only
    path('__reload__/', include('django_browser_reload.urls')),
]