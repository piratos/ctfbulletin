from django.shortcuts import render, Http404, HttpResponse
from talk.models import Thread, Message
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from talk.forms import *


def index(request):
    categories = CategoryChallenge.objects.all()
    for category1 in categories:
        category1.name = category1.name.replace(' ', '_')
    return render(request, 'talk/index.html', {'categories': categories})


def category(request, cat_name):
    cat_name_url = cat_name
    cat_name = cat_name.replace('_', ' ')
    try:
        category1 = CategoryChallenge.objects.get(name=cat_name)
    except CategoryChallenge.DoesNotExist:
        raise Http404
    threads = Thread.objects.filter(category=category1)
    return render(request, 'talk/category.html', {'threads': threads,
                                                  'category': cat_name,
                                                  'cat_name_url': cat_name_url})


@login_required()
def thread(request, thread_id):
    user = request.user
    chexist = False
    try:
        ch = Challenger.objects.get(user=user)
        user = ch
        chexist = True
    except Challenger.DoesNotExist:
        pass
    try:
        thread1 = Thread.objects.get(id=thread_id)
    except Thread.DoesNotExist:
        raise Http404
    messages = Message.objects.filter(thread=thread1).order_by('start_date')
    if request.method == 'POST':
        message_form = MessageForm(data=request.POST)
        reply = message_form.save(commit=False)
        reply.thread = thread1
        reply.sender = user
        reply.save()
    else:
        message_form = MessageForm()
    return render(request, 'talk/thread.html', {'messages': messages,
                                                'the_user': user,
                                                'exist': chexist,
                                                'thread': thread1,
                                                'message_form': message_form})


@login_required()
def add_message(request):
    if request.method == 'GET':
        if 'message_content' and 'user_name' and 'thread_id' in request.GET:
            mesage_content = request.GET['message_content']
            user_name = request.GET['user_name']
            thread_id = request.GET['thread_id']
            try:
                user = User.objects.get(username=user_name)
                challenger = Challenger.objects.get(user=user)
                thread1 = Thread.objects.get(id=thread_id)
                message = Message.objects.get_or_create(sender=challenger, content=mesage_content, thread=thread1)
            except Thread.DoesNotExist:
                pass
            except User.DoesNotExist:
                pass
            except Challenger.DoesNotExist:
                pass
        return HttpResponse(True)
    else:
        return HttpResponse(False)