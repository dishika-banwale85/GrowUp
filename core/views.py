from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import requests
from urllib.parse import urlencode

from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, SocialLinkForm
from .models import SocialLink

# ------------------ BASIC PAGES ------------------
def home(request):
    return render(request, 'home.html')

def welcome(request):
    return render(request, 'welcome.html')

def contact(request):
    return render(request, 'contact.html')

def support(request):
    return render(request, 'support.html')

def exploring(request):
    return render(request, 'exploring.html')

def content(request):
    return render(request, 'content.html')

def help(request):
    return render(request, 'help.html')


# ------------------ AUTHENTICATION ------------------
def signup_view(request):
    """User Registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    """User Login"""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """User Logout"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


# ------------------ PROFILE ------------------
@login_required
def profile_view(request):
    """Show user profile and connected social accounts"""
    user = request.user
    connected_accounts = SocialAccount.objects.filter(user=user)
    connected_providers = [acc.provider for acc in connected_accounts]
    context = {
        'connected_accounts': connected_accounts,
        'connected_providers': connected_providers,
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    """Edit profile details"""
    user = request.user
    profile = user.profile  # via signals
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)
    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# ------------------ GOOGLE OAUTH ------------------
def google_login(request):
    """
    Redirect user to Google OAuth 2.0 consent page
    """
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": '792664826369-mu65ssejfl51hn72r6frefh01aummvu1.apps.googleusercontent.com',  # replace in settings.py
        "redirect_uri": 'https://arrythmical-meridith-unvenially.ngrok-free.dev/account/google/login/callback/',
       
    # must match urls.py
        "response_type": "code",
        "scope": "email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    url = f"{base_url}?{urlencode(params)}"
    return redirect(url)


def google_callback(request):
    """
    Handle callback from Google OAuth 2.0
    Exchanges code for access token and gets user info
    """
    code = request.GET.get('code')
    if not code:
        return HttpResponse("Authorization failed or cancelled.")

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": '792664826369-mu65ssejfl51hn72r6frefh01aummvu1.apps.googleusercontent.com',
        "client_secret": 'GOCSPX-zQQN5l1qURwNF3cZsettings.GOOGLE_REDIRECT_msnZjr9MAjBI',
        "redirect_uri": 'https://arrythmical-meridith-unvenially.ngrok-free.dev/account/google/login/callback/',
        "grant_type": "authorization_code"
    }

    # Exchange code for access token
    response = requests.post(token_url, data=data)
    token_data = response.json()
    access_token = token_data.get("access_token")
    if not access_token:
        return HttpResponse("Failed to obtain access token.")

    # Get user info
    user_info_response = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    user_info = user_info_response.json()

    # Store user info in session (or create user in DB)
    request.session['google_user'] = user_info
    messages.success(request, f"Google account connected: {user_info.get('email')}")
    return redirect('profile')


# ------------------ SOCIAL LINKS ------------------
@login_required
def add_social_link(request):
    """Manually add custom social links"""
    if request.method == 'POST':
        form = SocialLinkForm(request.POST)
        if form.is_valid():
            social_link = form.save(commit=False)
            social_link.user = request.user
            social_link.save()
            messages.success(request, 'Social account added successfully!')
            return redirect('profile')
    else:
        form = SocialLinkForm()
    return render(request, 'add_social_link.html', {'form': form})


# ------------------ INSTAGRAM OAUTH ------------------
def instagram_login(request):
    """Redirect user to Instagram authorization page"""
    auth_url = (
        f"https://www.instagram.com/oauth/authorize"
        f"?client_id={'4099924166924965'}"
        f"&redirect_uri={'https://arrythmical-meridith-unvenially.ngrok-free.dev/auth/instagram/callback/'}"
        f"&scope=instagram_business_basic,instagram_business_manage_messages,"
        f"instagram_business_manage_comments,instagram_business_content_publish,"
        f"instagram_business_manage_insights"
        f"&response_type=code"
        f"&force_reauth=true"
    )
    return redirect(auth_url)


@csrf_exempt
def instagram_callback(request):
    """Handle Instagram OAuth callback"""
    code = request.GET.get('code')
    if not code:
        return render(request, "error.html", {"message": "Authorization failed or cancelled."})
    data = {
        'client_id': "4099924166924965",
        'client_secret': "758405ee85889118b25bb756bbc3fd49",
        'grant_type': 'authorization_code',
        'redirect_uri': "https://arrythmical-meridith-unvenially.ngrok-free.dev/auth/instagram/callback/",
        'code': code,
    }
    response = requests.post(settings.INSTAGRAM_TOKEN_URL, data=data)
    result = response.json()
    access_token = result.get('access_token')
    user_id = result.get('user_id')
    if access_token:
        user_info = requests.get(
            f"{settings.INSTAGRAM_API_URL}/me?fields=id,username,account_type&access_token={access_token}"
        ).json()
        request.session['ig_user'] = user_info
        request.session['ig_token'] = access_token
        messages.success(request, "Instagram account connected successfully!")
        return redirect('profile')
    return render(request, "error.html", {"message": "Failed to get access token."})


@login_required
def instagram_profile_view(request):
    """Show Instagram info, media, followers, following"""
    ig_user = request.session.get('ig_user')
    ig_token = request.session.get('ig_token')
    if not ig_user or not ig_token:
        messages.error(request, "No Instagram account connected.")
        return redirect('profile')
    url = f"https://graph.facebook.com/v17.0/{ig_user['id']}?fields=business_discovery.username({ig_user['username']}){{followers_count,follows_count}}&access_token={ig_token}"
    response = requests.get(url)
    followers_info = response.json().get('business_discovery', {})
    media_url = f"https://graph.instagram.com/{ig_user['id']}/media?fields=id,caption,media_type,media_url,permalink&access_token={ig_token}"
    media_response = requests.get(media_url)
    media_data = media_response.json().get('data', [])
    context = {
        'ig_user': ig_user,
        'followers': followers_info.get('followers_count', 0),
        'following': followers_info.get('follows_count', 0),
        'ig_media': media_data,
    }
    return render(request, 'instagram_profile.html', context)


# ------------------ FACEBOOK CALLBACK ------------------
def facebook_callback(request):
    """Meta Webhook verification callback"""
    verify_token = "growup_verify_token_123"
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")
    if mode == "subscribe" and token == verify_token:
        return HttpResponse(challenge)
    else:
        return HttpResponse("Verification failed", status=403)