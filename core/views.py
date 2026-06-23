from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import requests
from urllib.parse import urlencode
import os
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


# FIX: logout must only act on POST to prevent CSRF-based logout via GET
# Update your logout button in templates to submit a POST form, not a link
@require_POST
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

    instagram_user = request.session.get('ig_user')
    instagram_connected = bool(instagram_user)
    instagram_username = instagram_user.get('username') if instagram_user else None

    context = {
        'connected_accounts': connected_accounts,
        'connected_providers': connected_providers,
        'instagram_connected': instagram_connected,
        'instagram_username': instagram_username,
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
    """Redirect user to Google OAuth 2.0 consent page"""
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        # FIX: read client_id from settings, never hardcode it
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    url = f"{base_url}?{urlencode(params)}"
    return redirect(url)


def google_callback(request):
    """Handle callback from Google OAuth 2.0"""
    code = request.GET.get('code')
    if not code:
        return HttpResponse("Authorization failed or cancelled.")

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        # FIX: use correct lowercase keys that Google expects
        # FIX: read from settings (which reads from env), not os.getenv() directly
        # FIX: corrected typo GOOGLE_REDIRCT_URI -> redirect_uri
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    # FIX: wrap in try/except with timeout — unhandled network errors returned 500
    try:
        response = requests.post(token_url, data=data, timeout=10)
        response.raise_for_status()
        token_data = response.json()
    except requests.RequestException as e:
        return render(request, 'error.html', {'message': f"Google token exchange failed: {str(e)}"})

    access_token = token_data.get("access_token")
    if not access_token:
        return render(request, 'error.html', {'message': "Failed to obtain access token from Google."})

    # Get user info
    try:
        user_info_response = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10
        )
        user_info_response.raise_for_status()
        user_info = user_info_response.json()
    except requests.RequestException as e:
        return render(request, 'error.html', {'message': f"Failed to fetch Google user info: {str(e)}"})

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
    client_id = settings.INSTAGRAM_CLIENT_ID
    redirect_uri = settings.INSTAGRAM_REDIRECT_URI
    scope = (
        "instagram_business_basic,"
        "instagram_business_manage_messages,"
        "instagram_business_manage_comments,"
        "instagram_business_content_publish,"
        "instagram_business_manage_insights"
    )

    auth_url = (
        f"https://www.instagram.com/oauth/authorize"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope}"
        f"&response_type=code"
        f"&force_reauth=true"
    )
    return redirect(auth_url)


# FIX: @csrf_exempt kept only because Meta's server hits this endpoint directly.
# If you want to also protect the user-facing redirect, split into two views.
@csrf_exempt
def instagram_callback(request):
    """Handle Instagram OAuth callback"""
    code = request.GET.get('code')
    if not code:
        return render(request, "error.html", {"message": "Authorization failed or cancelled."})

    client_id = settings.INSTAGRAM_CLIENT_ID
    client_secret = settings.INSTAGRAM_CLIENT_SECRET
    redirect_uri = settings.INSTAGRAM_REDIRECT_URI

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
        'code': code,
    }

    # FIX: wrapped in try/except with timeout
    try:
        response = requests.post(settings.INSTAGRAM_TOKEN_URL, data=data, timeout=10)
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as e:
        return render(request, "error.html", {"message": f"Instagram token exchange failed: {str(e)}"})

    access_token = result.get('access_token')
    user_id = result.get('user_id')

    if access_token:
        # Fetch Instagram user info
        try:
            user_info_url = f"{settings.INSTAGRAM_API_URL}/me"
            params = {
                "fields": "id,username,account_type",
                "access_token": access_token
            }
            user_info_response = requests.get(user_info_url, params=params, timeout=10)
            user_info_response.raise_for_status()
            user_info = user_info_response.json()
        except requests.RequestException as e:
            return render(request, "error.html", {"message": f"Failed to fetch Instagram user info: {str(e)}"})

        request.session['ig_user'] = user_info
        request.session['ig_token'] = access_token

        messages.success(request, f"Instagram account '{user_info.get('username')}' connected successfully!")
        return redirect('profile')

    error_message = result.get("error_message", "Failed to get access token.")
    return render(request, "error.html", {"message": error_message})


@login_required
def instagram_profile_view(request):
    """Show Instagram info, media, followers, following"""
    ig_user = request.session.get('ig_user')
    ig_token = request.session.get('ig_token')

    if not ig_user or not ig_token:
        messages.error(request, "No Instagram account connected.")
        return redirect('profile')

    # FIX: wrapped external calls in try/except with timeout
    try:
        url = (
            f"https://graph.facebook.com/v17.0/{ig_user['id']}"
            f"?fields=business_discovery.username({ig_user['username']})"
            f"{{followers_count,follows_count}}"
            f"&access_token={ig_token}"
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        followers_info = response.json().get('business_discovery', {})
    except requests.RequestException:
        followers_info = {}

    try:
        media_url = (
            f"https://graph.instagram.com/{ig_user['id']}/media"
            f"?fields=id,caption,media_type,media_url,permalink"
            f"&access_token={ig_token}"
        )
        media_response = requests.get(media_url, timeout=10)
        media_response.raise_for_status()
        media_data = media_response.json().get('data', [])
    except requests.RequestException:
        media_data = []

    context = {
        'ig_user': ig_user,
        'followers': followers_info.get('followers_count', 0),
        'following': followers_info.get('follows_count', 0),
        'ig_media': media_data,
    }
    return render(request, 'instagram_profile.html', context)


# ------------------ FACEBOOK WEBHOOK ------------------
def facebook_callback(request):
    """Meta Webhook verification callback"""
    # FIX: read verify token from settings, not hardcoded string
    verify_token = settings.FACEBOOK_VERIFY_TOKEN
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == verify_token:
        return HttpResponse(challenge)
    return HttpResponse("Verification failed", status=403)