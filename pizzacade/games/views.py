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
from django.db.models import Q
from django.contrib import messages
from .forms import UserCreationForm, ProfileForm, UserSearchForm, UserSelectForm

load_dotenv()
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')


# Create your views here.
def index(request):
    return render(request, 'games/project.html', {'user': request.user})


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
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
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
    friends = request.user.profile.friends.all()
    age = request.GET.get('age', None)
    if age:
        try:
            age = int(age)
        except ValueError:
            age = None
    temperament = request.GET.get('temperament', None)
    email = request.GET.get('email', None)
    username = request.GET.get('username', None)
    print('AGE: ', age)
    print('temperament: ', temperament)
    print('email: ', email)
    print('username: ', username)

    sort_params = {
        # 'profile__age': age,
        # 'profile__temperament': temperament,
        # 'email': email,
        # 'username': username
    }
    if age:
        sort_params['profile__age'] = age
    if temperament:
        sort_params['profile__temperament'] = temperament
    if email:
        sort_params['email'] = email
    if username:
        sort_params['username'] = username
    users = User.objects.filter(username=username).exclude(id__in=friends)
    user_select_form = UserSelectForm(users=users)
    return render(request, 'games/people.html', {'user_search_form': user_search_form, 'user_select_form': user_select_form})


@login_required()
def add_friends(request):
    if request.method == 'POST':
        form = UserSelectForm(request.POST)
        print(form.errors)
        if form.is_valid():
            users = form.cleaned_data['users']
            request.user.profile.friends.set(users)
            request.user.profile.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully added friends!')
            return redirect('people')

    else:
        return redirect('people')