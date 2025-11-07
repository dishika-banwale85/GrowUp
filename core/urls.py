from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/google/login/', views.google_login, name='google_login'),
    path('account/google/login/callback/', views.google_callback, name='google_callback'),

    path('welcome/', views.welcome, name='welcome'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('contact/', views.contact, name='contact'),
    path('exploring/', views.exploring, name='exploring'),
    path('support/', views.support, name='support'),
    path('content/', views.content, name='content'),
    path('help/', views.help, name='help'),
    path('profile/add-social/', views.add_social_link, name='add_social_link'),
    path('auth/instagram/login/', views.instagram_login, name='instagram_login'),
    path('auth/instagram/callback/', views.instagram_callback, name='instagram_callback'),
    path('accounts/facebook/callback/', views.facebook_callback, name='facebook_callback'),
    path('profile/instagram/', views.instagram_profile_view, name='instagram_profile'),
]