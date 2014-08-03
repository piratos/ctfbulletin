from django.contrib import admin
from ctf.models import *


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_admin', 'user2', 'user3', 'user4', 'score')


class CtfChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'score', 'flag')
admin.site.register(Team, TeamAdmin)
admin.site.register(CtfChallenge, CtfChallengeAdmin)