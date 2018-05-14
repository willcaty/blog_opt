from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from blog.forms import UserForm
from .models import Article, Comment, Category


# Create your views here.
#@cache_page(60 * 15)
def index(request):
    article_list = Article.objects.all().order_by('-create_at')
    category = Category.objects.all()
    paginator = Paginator(article_list, 4, 1)  # 每页4条少于1条合并上一个页
    page = request.GET.get('page')
    try:
        article_list = paginator.page(page)
    except PageNotAnInteger:
        article_list = paginator.page(1)
    except EmptyPage:
        article_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html', context={'article': article_list, 'category': category})

#@cache_page(60 * 15)
def search_view(request):
    q = request.GET.get('q')
    category = Category.objects.all()
    article_list = Article.objects.filter(title__icontains=q)
    return render(request, 'blog/search.html', context={'article': article_list, 'category': category})

#@cache_page(60 * 15)
def detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    comment = Comment.objects.filter(article=article_id).order_by('-create_at')
    min_comment = comment[0:5]
    #comment.count()  #速度最快
    #comment_count = len(comment)    #速度其次
    #{{ comment|length }} 速度最慢
    return render(request, 'blog/single.html',
                  context={'article': article,  'comment': comment,'min_comment':min_comment})


@login_required
def add_comment(request, article_id):
    name = request.POST['name']
    email = request.POST['email']
    message = request.POST['message']
    article = article_id
    comment = Comment(name=name, email=email, message=message, article=article)
    comment.save()
    return HttpResponseRedirect('/detail/' + str(article_id) + '/')


def register_view(request):
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user:
                context['userExit'] = True
                return render(request, 'register.html', context)
            user = User.objects.create_user(username=username, password=password)
            user.save()
            request.session['username'] = username
            auth.login(request, user)
            return HttpResponseRedirect('/index')
    else:
        context = {'isLogin': False}

    return render(request, 'blog/register.html', context)


def login_view(request):
    context = {}
    print('login')
    if request.method == "POST":
        form = UserForm(request.POST)
        print(form)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                request.session['username'] = username
                return HttpResponseRedirect('/index/')
            else:
                context = {'isLogin': False, 'pawd': False}
                return render(request, 'blog/login.html', context)
    else:
        context = {'isLogin': False, 'pawd': True}

    return render(request, 'blog/login.html', context)


def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


@login_required
def add_page(request):
    category = Category.objects.all()
    return render(request, 'blog/add.html', context={'category': category})


@login_required
def add_article(request):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        abstract = request.POST['abstract']
        category = request.POST['category']
        category = Category.objects.get(id=category)
        article = Article(title=title, body=body, abstract=abstract, category=category)
        article.save()

    return HttpResponseRedirect('/index/')
