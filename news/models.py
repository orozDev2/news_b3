from django.db import models


class News(models.Model):

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'

    name = models.CharField(verbose_name='заголовок', max_length=100)
    image = models.ImageField(verbose_name='изображение', upload_to='news_images/', blank=True, null=True)
    description = models.CharField(verbose_name='краткое описание', max_length=200)
    content = models.TextField(verbose_name='контент')
    date = models.DateTimeField(verbose_name='дата добавленения')
    category = models.ForeignKey('news.Category', on_delete=models.PROTECT, related_name='news', verbose_name='категория')
    tags = models.ManyToManyField('news.Tag', related_name='news', verbose_name='теги', blank=True)

    def __str__(self):
        return f'{self.id}: {self.name} - {self.date}'


# class NewsTags(models.Model):
#
#     news = models.ForeignKey('news.News', on_delete=models.CASCADE, related_name='tags')
#     tag = models.ForeignKey('news.Tag', on_delete=models.CASCADE, related_name='news')
#
#     def __str__(self):
#         return f'{self.news} - {self.tag}'


class Category(models.Model):

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    name = models.CharField(verbose_name='название категории', max_length=50, unique=True)

    def __str__(self):
        return f'{self.id}: {self.name}'


class Tag(models.Model):

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    name = models.CharField(verbose_name='название тега', max_length=50, unique=True)

    def __str__(self):
        return f'{self.id}: {self.name}'


# Create your models here.
