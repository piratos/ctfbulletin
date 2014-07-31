__author__ = 'piratos'
from django import forms
from challenges.models import *
from django.forms import widgets


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

    def clean_password(self):
        if self.data['password'] != self.data['password_confirmation']:
            raise forms.ValidationError("passwords don't match !")
        return self.data['password']

    def clean(self, *args, **kwargs):
        self.clean_password()
        return super(UserForm, self).clean(*args, **kwargs)


class HiddenTextField(models.TextField):
    def formfield(self, **kwargs):
        defaults = {'widget': widgets.Textarea({'hidden': ''}), 'initial': 'A'}
        defaults.update(kwargs)
        return super(HiddenTextField, self).formfield(**defaults)


class ChallengerProfile(forms.ModelForm):
    points = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    member = forms.CharField(widget=forms.HiddenInput(), initial=" ")
    badge = forms.CharField(widget=forms.HiddenInput(), initial="A")

    class Meta:
        model = Challenger
        fields = ('picture', 'born', 'cv', 'website')
