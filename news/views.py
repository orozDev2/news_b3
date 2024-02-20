from django.shortcuts import render, redirect, get_object_or_404

from news.models import News, Category


def list_news(request):
    news = News.objects.all()
    categories = Category.objects.all()
    search_query = request.GET.get('search')

    if search_query:
        news = news.filter(name__icontains=search_query)

    return render(request, 'list_news.html', {'news': news, 'categories': categories})


def main(request):
    return render(request, 'index.html')


def list_news_by_category(request, id):
    # try:
    #     category = Category.objects.get(id=id)
    # except Category.DoesNotExist:
    #     return redirect('/news/')
    category = get_object_or_404(Category, id=id)
    news = News.objects.filter(category=category)

    search_query = request.GET.get('search')
    if search_query:
        news = news.filter(name__icontains=search_query)

    categories = Category.objects.all()
    return render(request, 'list_news.html', {
        'news': news,
        'categories': categories,
        'category': category
    })


def detail_news(request, id):
    news = News.objects.get(id=id)
    return render(request, 'detail_news.html', {'news': news})

# Create your views here.
