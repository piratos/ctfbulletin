from django.contrib import admin
from blog.models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'date_post')
    fieldsets = (
        (
            'None',
            {'fields': ('author', 'title', 'content')}
        ),
    )
admin.site.register(Article, ArticleAdmin)
admin.site.register(BlogComment)