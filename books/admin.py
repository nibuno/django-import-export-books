from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import CSV, JSON

from .models import Author, Book, Publisher
from .resources import AuthorResource, BookResource, PublisherResource


class ImportExportAdmin(ImportExportModelAdmin):
    """CSV/JSONのインポート・エクスポートに対応した管理画面の基底クラス"""

    def get_export_formats(self):
        return [CSV, JSON]

    def get_import_formats(self):
        return [CSV, JSON]


@admin.register(Author)
class AuthorAdmin(ImportExportAdmin):
    resource_class = AuthorResource
    list_display = ('last_name', 'first_name')
    search_fields = ('last_name', 'first_name')


@admin.register(Publisher)
class PublisherAdmin(ImportExportAdmin):
    resource_class = PublisherResource
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(ImportExportAdmin):
    resource_class = BookResource
    list_display = ('title', 'isbn', 'author', 'publisher', 'published_date', 'price')
    list_filter = ('publisher', 'author')
    search_fields = ('title', 'isbn')
