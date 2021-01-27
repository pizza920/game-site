import os
import json
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from dotenv import load_dotenv
from django.contrib import messages
from .forms import UserCreationForm, ProfileForm, UserSearchForm, UserSelectForm, ProfileFriendsForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.signals import user_logged_out
from .models import Profile
from django.http import HttpResponseForbidden
from whitenoise.middleware import WhiteNoiseMiddleware


load_dotenv()
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')


def index(request):
    context = get_friends_user_and_preferences_context(request.user)
    return render(request, 'games/index.html', context)


def checkers(request):
    context = get_friends_user_and_preferences_context(request.user)
    return render(request, 'games/checkers.html', context)


@csrf_exempt
def login(request):
    json_body = json.loads(request.body)
    username = json_body["username"]
    if not username:
        return HttpResponse('Unauthorized', status=401)

    token = AccessToken(twilio_account_sid, twilio_api_key_sid,
                        twilio_api_key_secret, identity=username)
    token.add_grant(VideoGrant(room='My Room'))
    return JsonResponse({'token': token.to_jwt().decode()})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('profile_edit')
    else:
        form = UserCreationForm()
    return render(request, 'games/signup.html', {'form': form})


@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            edited_profile = form.save()
            picture = form.cleaned_data.get("picture")
            edited_profile.picture = picture
            edited_profile.save()
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'games/edit_profile.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'games/view_profile.html', {'user': request.user})


@login_required
def people(request):
    user_search_form = UserSearchForm(request.GET)
    change_friends_form = ProfileFriendsForm(instance=request.user.profile)
    friends = request.user.profile.friends.all()
    user_ids_to_exclude = [friend.id for friend in friends]
    user_ids_to_exclude.append(request.user.id)
    age = request.GET.get('age', None)
    if age:
        try:
            age = int(age)
        except ValueError:
            age = None
    temperament = request.GET.get('temperament', None)
    email = request.GET.get('email', None)
    username = request.GET.get('username', None)
    intelligence = request.GET.get('intelligence', None)
    personality_type = request.GET.get('personality_type', None)
    education = request.GET.get('education', None)

    filter_params = {}

    if age:
        filter_params['profile__age'] = age
    if temperament:
        filter_params['profile__temperament'] = temperament
    if email:
        filter_params['email'] = email
    if username:
        filter_params['username'] = username
    if intelligence:
        filter_params['profile__intelligence'] = intelligence
    if personality_type:
        filter_params['profile__personality_type'] = personality_type
    if education:
        filter_params['profile__education'] = education
    users = User.objects.exclude(id__in=user_ids_to_exclude).filter(**filter_params)
    if not users.exists():
        users = User.objects.none()
    user_select_form = UserSelectForm(users=users)
    return render(
        request,
        'games/people.html',
        {
            'user_search_form': user_search_form,
            'user_select_form': user_select_form,
            'change_friends_form': change_friends_form,
            'user': request.user,
        }
    )


@login_required()
def add_friends(request):
    if request.method == 'POST':
        form = UserSelectForm(request.POST)
        if form.is_valid():
            users = form.cleaned_data['users']
            request.user.profile.friends.add(*users)
            request.user.profile.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully added friends!')
            return redirect('people')
        else:
            return redirect('people')

    else:
        return redirect('people')


@login_required()
def change_friends(request):
    if request.method == 'POST':
        form = ProfileFriendsForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully saved friends!')
            return redirect('people')
        else:
            return redirect('people')

    else:
        return redirect('people')


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        profile = instance.profile
    except ObjectDoesNotExist:
        profile = Profile.objects.create(user=instance)
        profile.save()


@receiver(user_logged_out)
def set_user_status(sender, request, user, **kwargs):
    if user and user.profile:
        user.profile.online_count = 0
        user.profile.save()


def get_friends_user_and_preferences_context(user):
    friends = []
    preferences = {}
    if user.is_authenticated:
        friends = [friend.profile.as_dict() for friend in user.profile.friends.all()]
        preferences = user.profile.preferences_as_dict()
    return {'user': user, 'friends': friends, 'preferences': preferences, 'user_id': user.id}


# Restricting auth for static files
class ProtectedStaticFileMiddleware(WhiteNoiseMiddleware):
    def process_request(self, request):
        # check user authentication
        print("GOING THROUGH MIDDLE WARE")
        if request.user.is_authenticated:
            return super(WhiteNoiseMiddleware, self).process_request(request)
        # condition false
        return HttpResponseForbidden("you are not authorized")