from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount as AllauthSocialAccount
from .models import SocialAccount, Post
import requests
from datetime import date
import cloudinary
import cloudinary.uploader


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}


# ------------------ AUTH ------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_api(request):
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '').strip()
    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=400)
    if len(password) < 8:
        return Response({'error': 'Password must be at least 8 characters.'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken.'}, status=400)
    user = User.objects.create_user(username=username, password=password)
    return Response({'message': f'Account created for {user.username}.'}, status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
def google_auth_api(request):
    credential = request.data.get('credential')
    if not credential:
        return Response({'error': 'Google credential is required.'}, status=400)
    try:
        google_response = requests.get(
            'https://oauth2.googleapis.com/tokeninfo',
            params={'id_token': credential}, timeout=10
        )
        google_data = google_response.json()
    except requests.RequestException:
        return Response({'error': 'Failed to verify Google token.'}, status=400)

    if 'error' in google_data:
        return Response({'error': 'Invalid Google token.'}, status=400)

    email = google_data.get('email')
    first_name = google_data.get('given_name', '')
    last_name = google_data.get('family_name', '')
    picture = google_data.get('picture', '')

    if not email:
        return Response({'error': 'Could not get email from Google.'}, status=400)

    username = email.split('@')[0]
    user, created = User.objects.get_or_create(
        email=email,
        defaults={'username': username, 'first_name': first_name, 'last_name': last_name}
    )
    if created and User.objects.filter(username=username).exclude(email=email).exists():
        user.username = f"{username}_{user.id}"
        user.save()

    tokens = get_tokens_for_user(user)
    return Response({
        'access': tokens['access'], 'refresh': tokens['refresh'],
        'email': email, 'username': user.username,
        'first_name': first_name, 'last_name': last_name,
        'picture': picture, 'is_new': created,
    })


# ------------------ PROFILE ------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_api(request):
    user = request.user
    joined_date = user.date_joined.date()
    days_since = (date.today() - joined_date).days
    is_new = days_since <= 7

    allauth_accounts = AllauthSocialAccount.objects.filter(user=user)
    connected_providers = [acc.provider for acc in allauth_accounts]

    # Our own SocialAccount (Instagram/Facebook tokens)
    our_accounts = SocialAccount.objects.filter(user=user)
    for acc in our_accounts:
        if acc.platform not in connected_providers:
            connected_providers.append(acc.platform)

    total_posts = Post.objects.filter(user=user).count()
    scheduled_posts = Post.objects.filter(user=user, status='scheduled').count()

    profile_picture = None
    google_account = allauth_accounts.filter(provider='google').first()
    if google_account:
        profile_picture = google_account.extra_data.get('picture')
    if not profile_picture and hasattr(user, 'profile') and user.profile.image:
        profile_picture = request.build_absolute_uri(user.profile.image.url)

    return Response({
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'joined_date': joined_date.strftime('%B %d, %Y'),
        'days_since_joined': days_since,
        'is_new': is_new,
        'profile_picture': profile_picture,
        'connected_providers': connected_providers,
        'total_posts': total_posts,
        'scheduled_posts': scheduled_posts,
    })


# ------------------ CONNECTED ACCOUNTS ------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def connected_accounts_api(request):
    """Returns which platforms are connected for the logged-in user"""
    accounts = SocialAccount.objects.filter(user=request.user)
    data = {}
    for acc in accounts:
        data[acc.platform] = {
            'connected': True,
            'username': acc.username,
            'account_id': acc.account_id,
        }
    return Response(data)


# ------------------ INSTAGRAM CONNECT ------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def instagram_connect_api(request):
    """
    Called after Instagram OAuth callback.
    Saves the access token to our SocialAccount model.
    """
    access_token = request.data.get('access_token')
    user_id = request.data.get('user_id')
    username = request.data.get('username', '')

    if not access_token or not user_id:
        return Response({'error': 'access_token and user_id are required.'}, status=400)

    SocialAccount.objects.update_or_create(
        user=request.user,
        platform='instagram',
        defaults={
            'access_token': access_token,
            'account_id': str(user_id),
            'username': username,
        }
    )
    return Response({'message': f'Instagram @{username} connected successfully!'})


# ------------------ FACEBOOK CONNECT ------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def facebook_connect_api(request):
    """
    Saves Facebook Page access token to SocialAccount model.
    """
    access_token = request.data.get('access_token')
    page_id = request.data.get('page_id')
    page_name = request.data.get('page_name', '')

    if not access_token or not page_id:
        return Response({'error': 'access_token and page_id are required.'}, status=400)

    SocialAccount.objects.update_or_create(
        user=request.user,
        platform='facebook',
        defaults={
            'access_token': access_token,
            'account_id': str(page_id),
            'username': page_name,
        }
    )
    return Response({'message': f'Facebook Page "{page_name}" connected successfully!'})


# ------------------ CREATE POST ------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_post_api(request):
    caption = request.data.get('caption', '').strip()
    file = request.FILES.get('file')
    platforms_raw = request.data.get('platforms', '[]')

    import json
    try:
        platforms = json.loads(platforms_raw)
    except:
        platforms = []

    if not caption:
        return Response({'error': 'Caption is required.'}, status=400)
    if not file:
        return Response({'error': 'Media file is required.'}, status=400)
    if not platforms:
        return Response({'error': 'Select at least one platform.'}, status=400)

    # Upload to Cloudinary
    try:
        upload_result = cloudinary.uploader.upload(file, resource_type='auto', folder='growup_posts')
        media_url = upload_result.get('secure_url')
    except Exception as e:
        return Response({'error': f'Media upload failed: {str(e)}'}, status=500)

    post = Post.objects.create(
        user=request.user,
        caption=caption,
        platforms=platforms,
        media_file=file,
        media_url=media_url,
        status='published',
    )

    errors = []
    success = []

    if 'instagram' in platforms:
        try:
            ig_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
            ig_user_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')

            # Step 1: Create container
            container_res = requests.post(
                f"https://graph.instagram.com/v19.0/{ig_user_id}/media",
                data={'image_url': media_url, 'caption': caption, 'access_token': ig_token},
                timeout=30
            )
            container_result = container_res.json()
            creation_id = container_result.get('id')

            if not creation_id:
                errors.append(f"Instagram error: {container_result.get('error', {}).get('message', 'Unknown')}")
            else:
                # Step 2: Publish
                publish_res = requests.post(
                    f"https://graph.instagram.com/v19.0/{ig_user_id}/media_publish",
                    data={'creation_id': creation_id, 'access_token': ig_token},
                    timeout=30
                )
                publish_result = publish_res.json()
                if publish_result.get('id'):
                    success.append('instagram')
                else:
                    errors.append(f"Instagram publish error: {publish_result.get('error', {}).get('message', 'Unknown')}")
        except Exception as e:
            errors.append(f'Instagram exception: {str(e)}')

    if success:
        post.status = 'published'
        from django.utils import timezone
        post.published_at = timezone.now()
    if errors:
        post.error_message = ' | '.join(errors)
        if not success:
            post.status = 'failed'
    post.save()

    return Response({
        'success': success,
        'errors': errors,
        'message': f"Posted to: {', '.join(success)}" if success else "Post failed.",
        'post_id': post.id,
    })

