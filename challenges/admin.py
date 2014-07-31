from django.contrib import admin
from challenges.models import *


class WriteUpAdmin(admin.ModelAdmin):
    list_display = ('author', 'challenge', 'date_writeup')


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'score', 'flag')
admin.site.register(CategoryChallenge)
admin.site.register(Challenger)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(WriteUp, WriteUpAdmin)