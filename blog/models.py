from django.db import models
from django.contrib.auth.models import User
from talk.models import Challenger


class Article(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=128)
    content = models.TextField(blank=True)
    date_post = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title + " by " + self.author.username


class BlogComment(models.Model):
    article = models.ForeignKey(Article)
    commenter = models.ForeignKey(Challenger)
    comment = models.TextField(blank=True)
    date_comment = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'comment from '+self.commenter.user.username