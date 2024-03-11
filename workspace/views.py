from pprint import pprint
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from news.models import Category, Tag, News
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from workspace.filters import NewsFilter
from workspace.forms import NewsForm, LoginForm


def login_profile(request):
    print('The view was called')
    print(request.user)

    if request.user.is_authenticated:
        return redirect('/')

    form = LoginForm()
    message = None

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        username = form.data.get('username')
        password = form.data.get('password')

        user = authenticate(username=username, password=password)
        print('User:', user)
        if user:
            login(request, user)
            print(request.user, 'is logged in successfully!')
            messages.success(request, f'The user has been logged in successfully!')
            return redirect('/workspace/')

        message = 'The password is not incorrect or user does not exist.'

    return render(request, 'auth/login.html', {'form': form, 'message': message})


def logout_profile(request):

    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def workspace(request):
    if request.user.is_authenticated:
        news = News.objects.all().order_by('-date')

        search_query = request.GET.get('search')
        if search_query:
            news = news.filter(
                Q(description__icontains=search_query) |
                Q(name__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        filter_set = NewsFilter(queryset=news, data=request.GET)
        news = filter_set.qs
        form = filter_set.form

        paginator = Paginator(news, 6)
        page = int(request.GET.get('page', 1))
        news = paginator.get_page(page)

        return render(request, 'workspace/index.html', {'news': news, 'form': form})
    return redirect('/')


# def create_news(request):
#     tags = Tag.objects.all()
#
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         description = request.POST.get('description')
#         content = request.POST.get('content')
#         date = request.POST.get('date')
#         category_id = request.POST.get('category')
#         tags = request.POST.getlist('tags')
#
#         if category_id:
#             news = News.objects.create(
#                 name=name,
#                 description=description,
#                 content=content,
#                 date=date,
#                 category_id=category_id
#             )
#
#         if tags:
#             news.tags.add(*tags)
#
#         image = request.FILES.get('image')
#
#         if image:
#             news.image = image
#             news.save()
#
#         messages.success(request, f'The news "{news.name}" has been created successfully.')
#
#         return redirect('/workspace/')
#
#     return render(request, 'workspace/create_news.html', {
#         'tags': tags
#     })


def create_news(request):
    form = NewsForm()
    if request.method == 'POST':

        form = NewsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            news = form.save()
            messages.success(request, f'The news "{news.name}" has been created successfully.')
            return redirect('/workspace/')

    return render(request, 'workspace/create_news.html', {
        'form': form
    })


# def update_news(request, id):
#     news_object = get_object_or_404(News, id=id)
#     categories = Category.objects.all()
#     tags = Tag.objects.all()
#
#     if request.method == "POST":
#         name = request.POST.get('name')
#         description = request.POST.get('description')
#         content = request.POST.get('content')
#         date = request.POST.get('date')
#         category_id = request.POST.get('category')
#         tags = request.POST.getlist('tags')
#         image = request.FILES.get('image')
#
#         news_object.name = name
#         news_object.description = description
#         news_object.content = content
#         news_object.date = date
#         news_object.category_id = category_id
#         if image:
#             news_object.image = image
#         news_object.save()
#
#         news_object.tags.clear()
#         news_object.tags.add(*tags)
#
#         messages.success(request, f'The news "{news_object.name}" has been updated successfully.')
#
#         return redirect('/workspace/')
#
#     return render(request, 'workspace/update_news.html', {
#         'news': news_object,
#         'categories': categories,
#         'tags': tags
#     })


def update_news(request, id):
    news = get_object_or_404(News, id=id)
    form = NewsForm(instance=news)
    if request.method == "POST":
        form = NewsForm(instance=news, data=request.POST, files=request.FILES)
        if form.is_valid():
            news = form.save()
            messages.success(request, f'The news "{news.name}" has been updated successfully.')
            return redirect('/workspace/')

    return render(request, 'workspace/update_news.html', {
        'news': news,
        'form': form
    })


def delete_news(request, id):
    news_object = get_object_or_404(News, id=id)
    news_object.delete()
    messages.warning(request, f'The news "{news_object.name}" has been deleted successfully.')
    return redirect('/workspace/')

# Create your views here.
