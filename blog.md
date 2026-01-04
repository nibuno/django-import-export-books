[django-import-export](https://django-import-export.readthedocs.io/en/latest/)は、Django Admin画面でインポート機能・エクスポート機能を行うことのできるライブラリです。

Excel、CSV、JSONなどの複数の形式にも対応しており、要件上Django Admin画面でも良い場合は有力な選択肢になります。

## サンプルコード

[django-import-export-books](https://github.com/nibuno/django-import-export-books)に全体像を載せています。

以下に要点を抜粋します。

### models.py

まずはmodels.pyです。

* 著者テーブル
* 出版社テーブル
* 本テーブル

の3テーブルを用意します。

```python
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

```

ER図にすると、次のようになります。

<figure class="figure-image figure-image-fotolife" title="ER図">[f:id:nibutan:20260104084919p:plain]<figcaption>ER図</figcaption></figure>

### resources.py

※公式リファレンス上は特に言及は無いのですが、分けることにします。公式リファレンス上はmodels.pyに書かれているコードを確認しました。

次に、resources.pyを作成します。

```python
"""
django-import-export用のリソース定義モジュール

Resourceクラスは、DjangoモデルとCSV/JSON等のファイル形式との間の
インポート・エクスポート処理を定義します。
各モデルに対応するResourceクラスを作成することで、
管理画面からのインポート/エクスポート機能が利用可能になります。
"""

from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from .models import Author, Book, Publisher


class AuthorResource(resources.ModelResource):
    """
    Authorモデル用のリソースクラス

    ModelResourceを継承することで、モデルのフィールドを自動的に
    インポート/エクスポート対象として認識します。
    """

    class Meta:
        # 対象となるDjangoモデル
        model = Author

        # インポート時にレコードを識別するフィールド
        # 通常はpk(id)が使われるが、ここでは'name'で識別する
        # これにより、別環境でもIDに依存せずデータを同期できる
        import_id_fields = ['name']

        # インポート/エクスポート対象のフィールド
        fields = ('name',)

        # インポート時、データに変更がなければスキップする
        # パフォーマンス向上と不要な更新を防ぐ
        skip_unchanged = True

        # スキップしたレコードをレポートに含めない
        # Trueにするとスキップ理由が表示されるが、件数が多いと見づらくなる
        report_skipped = False


class PublisherResource(resources.ModelResource):
    """
    Publisherモデル用のリソースクラス

    AuthorResourceと同様の設定。名前で識別する。
    """

    class Meta:
        model = Publisher
        import_id_fields = ['name']
        fields = ('name',)
        skip_unchanged = True
        report_skipped = False


class BookResource(resources.ModelResource):
    """
    Bookモデル用のリソースクラス

    ForeignKey（author, publisher）を持つため、
    関連モデルとの紐付け方法をFieldとWidgetで明示的に定義する。
    """

    # ForeignKeyフィールドの定義
    # エクスポート時はForeignKeyWidgetがなくても__str__の値が出力される
    # 指定した場合は、widgetの挙動に従う（ここでは'name'フィールドの値をエクスポート・インポートで使う）

    # ForeignKeyWidgetはインポート時に名前から関連モデルを検索して紐付けるために必要
    # 仮に指定していない場合、以下のようなエラーが出る
    # Cannot assign "'株式会社ビープラウド'": "Book.author" must be a "Author" instance.
    author = fields.Field(
        # CSV/JSONでのカラム名
        column_name='author',
        # Bookモデルのフィールド名
        attribute='author',
        # Authorモデルの'name'フィールドで紐付け
        # エクスポート: author.nameの値を出力
        # インポート: name=<値>でAuthorを検索して紐付け
        widget=ForeignKeyWidget(Author, field='name'),
    )
    publisher = fields.Field(
        column_name='publisher',
        attribute='publisher',
        widget=ForeignKeyWidget(Publisher, field='name'),
    )

    class Meta:
        model = Book

        # ISBNで書籍を識別（一意なのでIDの代わりに使える）
        import_id_fields = ['isbn']

        # 除外フィールド（これ以外は自動的にインポート/エクスポート対象になる）
        exclude = ('id',)

        # エクスポート時のカラム順序
        export_order = ('title', 'isbn', 'author', 'publisher', 'published_date', 'price', 'url')

        skip_unchanged = True
        report_skipped = False

```

#### model

* 通常のmodelのように、対象のmodelのクラス名を定義します。

#### import_id_fields

* インポート時にレコードを識別するフィールドです。


#### fields

* インポート/エクスポート対象のフィールドです

### admin.py

続いてadmin.pyです。admin.pyでは`django-import-export`の`ImportExportModelAdmin`を継承して

#### fields.Field

外部キーに対しては、必要に応じてForeignKeyWidgetを定義します。

```python
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
    list_display = ('name',)
    search_fields = ('name',)


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
    date_hierarchy = 'published_date'
```

## ダウンロードしたCSV

登録した内容については本記事では省略していますが、既にサンプルデータを用意しており、管理画面からエクスポートしたCSVは以下のようになります。

```csv
title,isbn,author,publisher,published_date,price,url
Pythonプロフェッショナルプログラミング 第4版,978-4-7980-7054-4,株式会社ビープラウド,秀和システム,2024-02-17,3520,https://www.shuwasystem.co.jp/book/9784798070544.html
自走プログラマー,978-4-297-11197-7,株式会社ビープラウド,技術評論社,2020-02-27,2948,https://jisou-programmer.beproud.jp/
```

一度、レコードを削除してみます。

次のようにインポートが可能になります。

インポートできました。

ちなみに、変更点があった場合は次のようになります。

## 参考リンク

### 公式ドキュメント

* [django-import-export 公式ドキュメント](https://django-import-export.readthedocs.io/en/latest/)
* [Getting started](https://django-import-export.readthedocs.io/en/latest/getting_started.html)
* [Admin integration](https://django-import-export.readthedocs.io/en/latest/admin_integration.html)

### Resource クラス

* [ModelResource](https://django-import-export.readthedocs.io/en/latest/api_resources.html#import_export.resources.ModelResource)
* [for_delete](https://django-import-export.readthedocs.io/en/latest/api_resources.html#import_export.resources.Resource.for_delete) - インポート時に行を削除するかどうかを判定するメソッド

### Meta オプション (ResourceOptions)

* [model](https://django-import-export.readthedocs.io/en/latest/api_resources.html#import_export.options.ResourceOptions.model) - 対象となるDjangoモデル
* [import_id_fields](https://django-import-export.readthedocs.io/en/latest/api_resources.html#import_export.options.ResourceOptions.import_id_fields) - インポート時にレコードを識別するフィールド
* [fields](https://django-import-export.readthedocs.io/en/latest/api_resources.html#import_export.options.ResourceOptions.fields) - インポート/エクスポート対象のフィールド
* [exclude](https://django-import-export.readthedocs.io/en/latest/api_resources.html#import_export.options.ResourceOptions.exclude) - 除外フィールド
* [export_order](https://django-import-export.readthedocs.io/en/latest/api_resources.html#import_export.options.ResourceOptions.export_order) - エクスポート時のカラム順序
* [skip_unchanged](https://django-import-export.readthedocs.io/en/latest/api_resources.html#import_export.options.ResourceOptions.skip_unchanged) - 変更がなければスキップ
* [report_skipped](https://django-import-export.readthedocs.io/en/latest/api_resources.html#import_export.options.ResourceOptions.report_skipped) - スキップしたレコードをレポートに含めるか

### Field / Widget

* [fields.Field](https://django-import-export.readthedocs.io/en/latest/api_fields.html#import_export.fields.Field) - フィールド定義
* [ForeignKeyWidget](https://django-import-export.readthedocs.io/en/latest/api_widgets.html#import_export.widgets.ForeignKeyWidget) - 外部キーの紐付け用ウィジェット
