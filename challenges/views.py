from django.shortcuts import render, HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from challenges.forms import *
import Image
import os
from django.conf import settings


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
    # solved = challenger.did_solved(challenge)
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
                challenger.score += challenge.score
                # challenger.add_solved(challenge)
                return HttpResponse('success')
    return HttpResponse('fail')


@login_required()
def get_writeup(request, chid):
    try:
        challenge = Challenge.objects.get(id=chid)
    except Challenge.DoesNotExist:
        raise Http404
