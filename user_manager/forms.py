from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from datetime import datetime


class SignupForm(UserCreationForm):
    email = forms.EmailField(label='эл. почта', max_length=200, help_text='обязательно к заполнению')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='Имя')
    last_name = forms.CharField(max_length=30, required=False, label='Фамилия')

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'b_date', 'phone', 'address', 'photo','b_date_last_change',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
        if self.instance.pk:
            self.fields['b_date_last_change'].initial = kwargs['instance'].b_date_last_change
            self.fields['b_date_last_change'].widget.attrs['disabled'] = 'disabled'


    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        if commit:
            profile.save()
            user = profile.prof
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
        return profile

