from django.shortcuts import render, Http404, HttpResponseRedirect
from blog.models import *


def user_or_challenger(request):
    user = request.user
    chexist = False
    try:
        challenger = Challenger.objects.get(user=user)
        chexist = True
        user = challenger
    except Challenger.DoesNotExist:
        pass
    return user, chexist


def index(request):
    articles = Article.objects.all()
    return render(request, 'blog/index.html', {'articles': articles})


def read(request, blog_url):
    blog_url_name = blog_url.replace('_', ' ')
    try:
        blog = Article.objects.get(title=blog_url_name)
    except Article.DoesNotExist:
        raise Http404
    try:
        messages = BlogComment.objects.filter(article=blog).order_by('date_comment')
    except BlogComment.DoesNotExist:
        pass
        messages = None
    user, chexist = user_or_challenger(request)
    return render(request, 'blog/read.html', {'blog': blog,
                                              'exist': chexist,
                                              'messages': messages,
                                              'user': user})


def add_message(request):
    user, chexist = user_or_challenger(request)
    if 'content' and 'article' in request.POST and chexist:
        comment = request.POST['content']
        article_name = request.POST['article']
        try:
            article = Article.objects.get(title=article_name)
        except Article.DoesNotExist:
            raise Http404
        comment_blog = BlogComment.objects.get_or_create(comment=comment, commenter=user, article=article)
        return read(request, article.title.replace(' ', '_'))
    else:
        return index(request)