from django.db import models
from django.contrib.auth.models import User
# Create your models here.

choices = (
    ('A', 'Apprentice'),
    ('C', 'Craftsman'),
    ('Me', 'Mentor'),
    ('Ma', 'Master'),
    ('G', 'Guru'),
)


class Challenger(models.Model):
    user = models.OneToOneField(User)
    badge = models.TextField(choices=choices, default='A')
    score = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='./profile_pics', blank=True)
    born = models.DateField(blank=True)                                   # dirty hack to store solved challenges for
    cv = models.FileField(upload_to='./cvs', blank=True)                  # each challenger, solved will store the id's
    website = models.URLField(blank=True)                                 # of each solved challenge, each id is written
    solved = models.CharField(max_length=750, default="", null=True)      # in 3 characters, greater solutions are

                                                                          # appreciated :)
    def get_solved(self):
        list_challenges = []
        list_ids = [int(self.solved[3*i:3+3*i]) for i in range(len(self.solved)/3)]
        for id1 in list_ids:
            try:
                list_challenges.append(Challenge.objects.get(id=id1))
            except Challenge.DoesNotExist:
                pass
        return list_challenges

    def add_solved(self, challenge1):
        id1 = str(challenge1.id)
        id1 = '0'*(3-len(id1))+id1
        self.solved += id1

    def is_solved(self, chal):
        if chal in self.get_solved():
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