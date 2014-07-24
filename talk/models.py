from django.db import models
from challenges.models import Challenger, CategoryChallenge


class Thread(models.Model):
    question = models.CharField(max_length=300)
    start_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    category = models.ForeignKey(CategoryChallenge)

    def __unicode__(self):
        return self.title


class Message(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=False)
    sender = models.ForeignKey(Challenger)
    thread = models.ForeignKey(Thread)

    def __unicode__(self):
        return 'message from '+self.sender.user.username