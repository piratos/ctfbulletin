__author__ = 'piratos'
from django import forms
from django.forms import widgets
from talk.models import *


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)