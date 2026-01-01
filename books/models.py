from django.db import models


class Author(models.Model):
    name = models.CharField('著者名', max_length=255, unique=True)

    class Meta:
        verbose_name = '著者'
        verbose_name_plural = '著者'

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField('出版社名', max_length=255, unique=True)

    class Meta:
        verbose_name = '出版社'
        verbose_name_plural = '出版社'

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField('タイトル', max_length=255)
    isbn = models.CharField('ISBN', max_length=17, unique=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        verbose_name='著者',
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.PROTECT,
        verbose_name='出版社',
    )
    published_date = models.DateField('発売日')
    price = models.PositiveIntegerField('価格')
    url = models.URLField('URL', blank=True)

    class Meta:
        verbose_name = '書籍'
        verbose_name_plural = '書籍'

    def __str__(self):
        return self.title
