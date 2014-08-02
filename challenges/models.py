from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from time import time
import os
import ast
# Create your models here.

choices = (
    ('A', 'Apprentice'),
    ('Me', 'Mentor'),
    ('Ma', 'Master'),
    ('G', 'Guru'),
)


class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


def upload_renamed(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        new_name = str(time()).replace('.', '_') + '.' + ext
        return os.path.join(path, new_name)
    return wrapper


class Challenger(models.Model):
    user = models.OneToOneField(User)
    badge = models.CharField(choices=choices, default='A', max_length=128)
    score = models.IntegerField(default=0)
    member = models.CharField(max_length=128, blank=True, null=True)
    picture = models.ImageField(upload_to=upload_renamed('profile_pics'), blank=True)
    born = models.DateField(blank=True)
    country = CountryField()
    cv = models.FileField(upload_to=upload_renamed('cvs'), blank=True)
    website = models.URLField(blank=True, null=True)
    solved = ListField(blank=True, null=True)

    def did_solved(self, ch):
        for i in self.solved:
            if i == ch.id:
                return True
        return False

    def __unicode__(self):
        return self.user.username


class CategoryChallenge(models.Model):
    name = models.CharField(max_length=128)
    color = models.CharField(max_length=7)

    def __unicode__(self):
        return self.name


class Challenge(models.Model):
    name = models.CharField(max_length=128, unique=True)
    category = models.ForeignKey(CategoryChallenge)
    flag = models.CharField(max_length=128)
    hints = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    url = models.URLField()

    def __unicode__(self):
        return self.name


class WriteUp(models.Model):
    author = models.ForeignKey(Challenger)
    challenge = models.ForeignKey(Challenge)
    content = models.TextField()
    aproved = models.BooleanField(default=False)
    date_writeup = models.DateTimeField(auto_created=True)

    def __unicode__(self):
        return 'for '+self.challenge.name+' by '+self.author.user.username