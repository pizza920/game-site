from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile, TEMPERAMENT_CHOICES, INTELLIGENCE_CHOICES, EDUCATION_CHOICES, PERSONALITY_TYPE_CHOICES
from django.db.models.query import QuerySet


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
        fields = [
            'age', 'temperament', 'intelligence', 'education',
            'personality_type', 'temperament_preference', 'intelligence_preference',
            'education_preference', 'personality_type_preference', 'picture'
        ]


TEMPERAMENT_FORM_CHOICES = ((None, '----'),) + TEMPERAMENT_CHOICES
INTELLIGENCE_FORM_CHOICES = ((None, '----'),) + INTELLIGENCE_CHOICES
EDUCATION_FORM_CHOICES = ((None, '----'),) + EDUCATION_CHOICES
PERSONALITY_TYPE_FORM_CHOICES = ((None, '----'),) + PERSONALITY_TYPE_CHOICES


class UserSearchForm(forms.Form):
    age = forms.IntegerField(min_value=18, required=False)
    temperament = forms.ChoiceField(choices=TEMPERAMENT_FORM_CHOICES, required=False, )
    email = forms.EmailField(required=False)
    username = forms.CharField(required=False)
    intelligence = forms.ChoiceField(required=False, choices=INTELLIGENCE_FORM_CHOICES)
    personality_type = forms.ChoiceField(required=False, choices=PERSONALITY_TYPE_FORM_CHOICES)
    education = forms.ChoiceField(required=False, choices=EDUCATION_FORM_CHOICES)


class UserSelectForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.none(), widget=forms.CheckboxSelectMultiple())

    def __init__(self, *args, users=None, **kwargs):
        super(UserSelectForm, self).__init__(*args, **kwargs)
        if isinstance(users, QuerySet):
            self.fields['users'].queryset = users
        else:
            self.fields['users'].queryset = User.objects.all()

