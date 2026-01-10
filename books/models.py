from django.db import models


class AuthorManager(models.Manager):
    def get_by_natural_key(self, last_name, first_name):
        return self.get(last_name=last_name, first_name=first_name)


class Author(models.Model):
    last_name = models.CharField("姓", max_length=100)
    first_name = models.CharField("名", max_length=100)

    objects = AuthorManager()

    class Meta:
        verbose_name = "著者"
        verbose_name_plural = "著者"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def natural_key(self):
        return self.last_name, self.first_name


class PublisherManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Publisher(models.Model):
    name = models.CharField("出版社名", max_length=255, unique=True)

    objects = PublisherManager()

    class Meta:
        verbose_name = "出版社"
        verbose_name_plural = "出版社"

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name,


class BookManager(models.Manager):
    def get_by_natural_key(self, isbn):
        return self.get(isbn=isbn)


class Book(models.Model):
    title = models.CharField("タイトル", max_length=255)
    isbn = models.CharField("ISBN", max_length=17, unique=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        verbose_name="著者",
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.PROTECT,
        verbose_name="出版社",
    )
    published_date = models.DateField("発売日")
    price = models.PositiveIntegerField("価格")
    url = models.URLField("URL", blank=True)

    objects = BookManager()

    class Meta:
        verbose_name = "書籍"
        verbose_name_plural = "書籍"

    def __str__(self):
        return self.title

    def natural_key(self):
        return self.isbn,

    natural_key.dependencies = ["books.Author", "books.Publisher"]
