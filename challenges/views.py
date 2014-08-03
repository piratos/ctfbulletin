from django.shortcuts import render, HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from challenges.forms import *
from ctf.models import Team
import Image
import os
from django.conf import settings


def get_challenger(request):
    try:
        user = request.user
        try:
            challenger = Challenger.objects.get(user=user)
        except Challenger.DoesNotExist:
            challenger = None
            return {'challenger': challenger, 'testing': 'success', 'ctf': True}
    except Exception:
        user = None
        return {'testing': 'fail', 'ctf': True}
    try:
        challenger = Challenger.objects.get(user=user)
    except Challenger.DoesNotExist:
        challenger = None
    return {'challenger': challenger, 'testing': 'success', 'ctf': True}


def register(request):                                              # TODO if profile non validated delete user
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        challenger_form = ChallengerProfile(data=request.POST)
        if user_form.is_valid and challenger_form.is_valid:
            theuser = user_form.save()
            theuser.set_password(theuser.password)
            theuser.save()
            challenger_profile = challenger_form.save(commit=False)
            challenger_profile.user = theuser
            challenger_profile.badge = 'A'
            challenger_profile.score = 0
            challenger_profile.member = ""
            if 'picture' in request.FILES:
                challenger_profile.picture = request.FILES['picture']
            if 'cv' in request.FILES:
                challenger_profile.cv = request.FILES['cv']
            challenger_profile.save()
            media_dir = settings.MEDIA_ROOT
            profile_pic_dir = os.path.join(media_dir, 'profile_pics')
            pic_name = os.path.basename(challenger_profile.picture.url)
            absolute_url = os.path.join(profile_pic_dir, pic_name)
            im = Image.open(absolute_url)                                # TODO make avatar more precise in term of size
            im.thumbnail((80, 80), Image.ANTIALIAS)
            im.save(absolute_url)
            registered = True  # everything is good ? then save to db
        else:
            print user_form.errors, challenger_form.errors
    else:
        #  first time loading the page
        user_form = UserForm()
        challenger_form = ChallengerProfile()
    return render(request, 'challenges/register.html', {
        'user_form': user_form,
        'challenger_form': challenger_form,
        'regitered': registered
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/challenges/')
            else:
                return render(request, 'challenges/account_problem.html', {'inactive': True, 'username': username})
        else:
            return render(request, 'challenges/account_problem.html', {'inactive': False, 'username': username})
    else:  # do nothing just render the page with an empty dict
        return render(request, 'challenges/login.html', {})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/challenges/')


def index(request):
    context_list = []
    categories = CategoryChallenge.objects.all()
    for category in categories:
        try:
            challenges = Challenge.objects.filter(category=category).order_by('-score')
        except Challenge.DoesNotExist:
            challenges = ()
        context_list.append({'category': category, 'challenges': challenges})  # TODO grid presentation for challenges
    return render(request, 'challenges/index.html', {'list': context_list})


@login_required()
def get_challenge(request, ch_id):
    solved = False
    try:
        challenge = Challenge.objects.get(id=ch_id)
    except Challenge.DoesNotExist:
        raise Http404
    challenger = Challenger.objects.get(user=request.user)
    solved = challenger.did_solved(challenge)
    return render(request, 'challenges/challenge.html', {'challenge': challenge,
                                                         'solved': solved})


def check_flag(request):
    if request.method == 'GET':
        if 'flag' and 'chid' in request.GET:
            flag = request.GET['flag']
            chid = request.GET['chid']
            try:
                challenge = Challenge.objects.get(id=chid)
            except Challenge.DoesNotExist:
                return HttpResponse('fail')
            if challenge.flag == flag:
                challenger = Challenger.objects.get(user=request.user)
                if challenger.did_solved(challenge):     # even he finds somewhere to send flag again
                    return HttpResponse('0')             # send 0 as score
                else:
                    challenger.score += challenge.score
                    challenger.solved.append(challenge.id)
                    challenger.save()
                    return HttpResponse(str(challenger.score))
    return HttpResponse('fail')


@login_required()
def get_writeup(request, chid):
    try:
        challenge = Challenge.objects.get(id=chid)
    except Challenge.DoesNotExist:
        raise Http404
    writeups = WriteUp.objects.all().filter(challenge=challenge)
    return render(request, 'challenges/writeups.html', {'challenge': challenge,
                                                        'writeups': writeups})

@login_required()
def full_writeup(request, wid):
    try:
        writeup = WriteUp.objects.get(id=wid)
    except WriteUp.DoesNotExist:
        raise Http404
    return render(request, 'challenges/fullwriteup.html', {'writeup': writeup})


@login_required()
def profile(request):
    pics = {
        'A': '/static/challenges/img/app.png',
        'Me': '/static/challenges/img/men.png',
        'Ma': '/static/challenges/img/mas.png',
        'G': '/static/challenges/img/gur.png',
    }
    challenger = Challenger.objects.get(user=request.user)
    bagde = str(challenger.badge)
    pic = pics[bagde]
    keys = []
    try:
        team = Team.objects.get(user_admin=challenger)
        keys = team.get_keys()
    except Team.DoesNotExist:
        team = False
    return render(request, 'challenges/profile.html', {'pic_url': pic,
                                                       'keys': keys,
                                                       'team': team})