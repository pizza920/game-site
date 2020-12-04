from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class UserCreationForm(DjangoUserCreationForm):
    above_age_restriction = forms.BooleanField(required=True, label='This website requires you to be 18 or older to register and enter. By checking this box you are confirming you are 18 or older.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'temperament']


TEMPERAMENT_CHOICES = (
    (None, '----'),
    ('Shy', 'Shy'),
    ('Outgoing', 'Outgoing'),
)


class UserSearchForm(forms.Form):
    age = forms.IntegerField(min_value=18, required=False)
    temperament = forms.ChoiceField(choices=TEMPERAMENT_CHOICES, required=False, )
    email = forms.EmailField(required=False)
    username = forms.CharField(required=False)


class UserSelectForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.none())

    def __init__(self, *args, users=None, **kwargs):
        super(UserSelectForm, self).__init__(*args, **kwargs)
        if users:
            self.fields['users'].queryset = users
        else:
            self.fields['users'].queryset = User.objects.all()