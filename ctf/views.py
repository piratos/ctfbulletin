from django.shortcuts import render, Http404, redirect
from ctf.models import Team
from challenges.models import Challenger
from django.contrib.auth.decorators import login_required


def clean(s):
    s = s.replace(' ', '')
    return s

@login_required()
def index(request):
    return render(request, 'ctf/index.html', {})


@login_required()
def add_team(request):
    if request.method == 'POST':
        name = request.POST["group"]
        exist = False
        have = False
        unique_keys = []
        user = request.user
        admin = Challenger.objects.get(user=user)
    #try:
    #    admin_team = Challenger.objects.get(user_admin=admin)
    # except Challenger.DoesNotExist:
    #    raise Http404
        try:
            team = Team.objects.get(name=name)
            name = team.name
            exist = True
        except Team.DoesNotExist:
            try:
                team = Team.objects.get(user_admin=admin)
                have = True
                name = team.name
            except Team.DoesNotExist:
                team = Team.create(name=name, user_admin=admin)
                team.save()
                unique_keys = team.get_keys()
        return render(request, 'ctf/team.html', {'exist': exist,
                                                 'keys': unique_keys,
                                                 'name': name,
                                                 'have': have,
                                                 'add': True})
    else:
        return redirect('/ctf/')


@login_required()
def join_team(request):
    user = request.user
    have = False
    try:
        challenger = Challenger.objects.get(user=user)
    except Challenger.DoesNotExist:
        raise Http404  # really ?! (-_-)
    exist = False
    if request.method == 'POST':
        if clean(challenger.member) != "":  # ta7lilou mish ndhif xD
            have = True
            return render(request, 'ctf/team.html', {'have': have})
        name = request.POST['name']
        key = request.POST['key']
        order = int(key[10])
        empty = True
        try:
            team = Team.objects.get(name=name)
            exist = True
            keys = team.get_keys()
            key_athentic = True
            if key in keys:  # key is authentic !
                if order == 2:                  # TODO dirty hack , any other solution ?
                    if team.user2 is None:
                        team.user2 = challenger
                        team.save()
                    else:
                        empty = False
                elif order == 3:
                    if team.user3 is None:
                        team.user3 = challenger
                        team.save()
                    else:
                        empty = False
                elif order == 4:
                    if team.user4 is None:
                        team.user4 = challenger
                        team.save()
                    else:
                        empty = False
            else:
                key_athentic = False
            return render(request, 'ctf/team.html', {'exist': exist,
                                                     'empty': empty,
                                                     'key_athentic': key_athentic,
                                                     'name': name})
        except Team.DoesNotExist:
            return render(request, 'ctf/team.html', {'exist': exist, 'name': name})  # team does not exist
