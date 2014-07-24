#!/usr/bin/python
import os


def populate():
    uuser = User.objects.get(username='challenger')
    sender = Challenger.objects.get(user=uuser)
    crypto_cat = add_category('cryptography', 'purple')
    t1 = add_thread(crypto_cat, 'prob 1', 'i have a problem')
    add_message(t1, sender, 'cksjhbc')
    add_message(t1, sender, 'cksjhbcsvcnvjs')

    crypto_cat2 = add_category('network', 'blue')
    t2 = add_thread(crypto_cat2, 'prob 2', 'i still have a problem')
    add_message(t2, sender, 'cksjhbc')
    add_message(t2, sender, 'cksjhbcsvcnvjs')

    crypto_cat3 = add_category('binary', 'red')
    t3 = add_thread(crypto_cat3, 'prob 3', 'no news for my problem :/')
    add_message(t3, sender, 'cksjhbc')
    add_message(t3, sender, 'cksjhbcsvcnvjs')
    # Print out what we have added to the user.
    for c in CategoryChallenge.objects.all():
        for t in Thread.objects.filter(category=c):
            for j in Message.objects.filter(thread=t):
                print "- {0} - {1} - {2}".format(str(c), str(t), str(j))


def add_category(name, color):
    c = CategoryChallenge.objects.get_or_create(name=name, color=color)[0]
    return c


def add_thread(cat, title, question):
    p = Thread.objects.get_or_create(category=cat, title=title, question=question)[0]
    return p


def add_message(thread, sender, content):
    c = Message.objects.get_or_create(thread=thread, sender=sender, content=content)[0]
    return c

# Start execution here!
if __name__ == '__main__':
    print "Starting talk population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ctfbulletin.settings')
    from talk.models import *
    from challenges.models import *
    populate()
