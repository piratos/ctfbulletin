from django.db import models
from challenges.models import Challenger
from uuid import uuid4  # for generating unique id's


class Team(models.Model):
    name = models.CharField(max_length=128, unique=True)                # TODO add country to Team to display coutrey
    score = models.IntegerField(default=0)
    user_admin = models.ForeignKey(Challenger, related_name='user_admin', unique=True)
    user2 = models.ForeignKey(Challenger, null=True, related_name='user2', unique=True)
    user2_key = models.CharField(max_length=128)
    user3 = models.ForeignKey(Challenger, null=True, related_name='user3', unique=True)
    user3_key = models.CharField(max_length=128)
    user4 = models.ForeignKey(Challenger, null=True, related_name='user4', unique=True)
    user4_key = models.CharField(max_length=128)

    @classmethod
    def create(cls, name, user_admin):
        team = cls(name=name, user_admin=user_admin)
        team.score = 0
        team.user2_key = 'challenger2{'+str(uuid4())+'}'
        team.user3_key = 'challenger3{'+str(uuid4())+'}'
        team.user4_key = 'challenger4{'+str(uuid4())+'}'
        return team

    def get_keys(self):
        keys = [self.user2_key,
                self.user3_key,
                self.user4_key,
                ]
        return keys

    def __unicode__(self):
        return self.name