from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
        'username',
        'email',
        ]


YEARS= [x for x in range(1940,2021)]
R_CHOICES=[('single','Single'),
         ('married','Married'),('widow','Widow'),('seprated','Seprated'),('commited','Commited')]

CHOICES=[('male','Male'),
         ('female','Female')]

class ProfileUpdateForm(forms.ModelForm):
    birthdate = forms.DateField(label='DOB', widget=forms.SelectDateWidget(attrs={'rows':2, 'cols':5},years=YEARS ))
    phone_no = forms.CharField(required=True)
    facebook =forms.URLField(required=False)
    twitter =forms.URLField(required=False)
    instagram =forms.URLField(required=False)
    google_plus =forms.URLField(required=False)
    name = forms.CharField(required=True)
    status = forms.ChoiceField(choices=R_CHOICES,widget=forms.RadioSelect)
    gender = forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect)
    address = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows':2, 'cols':15}),)
    bio = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows':2, 'cols':15}),)
    class Meta:
        model = Profile
        fields = [
        'name','age','address','status','gender','bio','phone_no','image','birthdate',
        'facebook','twitter','instagram','google_plus',
        ]
