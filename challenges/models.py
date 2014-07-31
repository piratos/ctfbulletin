from django.db import models
from django.contrib.auth.models import User
from time import time
import os
# Create your models here.

choices = (
    ('A', 'Apprentice'),
    ('C', 'Craftsman'),
    ('Me', 'Mentor'),
    ('Ma', 'Master'),
    ('G', 'Guru'),
)


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
    cv = models.FileField(upload_to=upload_renamed('cvs'), blank=True)
    website = models.URLField(blank=True, null=True)
    solved = models.CommaSeparatedIntegerField(max_length=128, null=True, blank=True)

    def get_solved_id(self):
        list_ids = [int(i) for i in self.solved.split(',')]
        return list_ids

    def add_solved(self, challenge1):
        id1 = str(challenge1.id)
        self.solved += ','+id1

    def is_solved(self, chal):
        if chal.id in self.get_solved_id():
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
        return self.name + ' from ' + self.category.name


class WriteUp(models.Model):
    author = models.ForeignKey(Challenger)
    challenge = models.ForeignKey(Challenge)
    content = models.TextField()
    date_writeup = models.DateTimeField(auto_created=True)

    def __unicode__(self):
        return 'for '+self.challenge.name+' by '+self.author.user.username