from django.contrib import admin
from challenges.models import *


class WriteUpAdmin(admin.ModelAdmin):
    list_display = ('author', 'challenge', 'date_writeup')

admin.site.register(CategoryChallenge)
admin.site.register(Challenger)
admin.site.register(Challenge)
admin.site.register(WriteUp, WriteUpAdmin)