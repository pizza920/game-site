from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django import forms


class UserCreationForm(DjangoUserCreationForm):
    above_age_restriction = forms.BooleanField(required=True, label='This website requires you to be 18 or older to register and enter. By checking this box you are confirming you are 18 or older.')
