[django-import-export](https://django-import-export.readthedocs.io/en/latest/)は、Django Admin画面でインポート機能・エクスポート機能を行うことのできるライブラリです。

Excel、CSV、JSONなどの複数の形式にも対応しており、要件上、操作画面がDjango Admin画面でも良い場合は有力な選択肢になります。触る機会があるので、理解のためにまとめます。

## サンプルコード

[django-import-export-books](https://github.com/nibuno/django-import-export-books)に全体像を載せています。

以下に要点を抜粋します。

### models.py

まずはmodels.pyです。

* 著者テーブル
* 出版社テーブル
* 本テーブル

の3テーブルを用意します。この辺りは特筆するものはないですが、意図的にunique制約を付与しています。((実際には著者名にuniqueを付与するのは微妙だと思いますが、今回はサンプルコードなので付与しました。))

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

※公式リファレンス上はmodels.pyに書かれているコードを確認しましたが、今回はわかりやすさのため別途resources.pyに分けています。

次に、resources.pyを作成します。ここでは、`Resource`クラスを定義します。

```python
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from .models import Author, Book, Publisher


class AuthorResource(resources.ModelResource):

    class Meta:
        model = Author
        import_id_fields = ['name']
        fields = ('name',)
        skip_unchanged = True
        report_skipped = False


class PublisherResource(resources.ModelResource):

    class Meta:
        model = Publisher
        import_id_fields = ['name']
        fields = ('name',)
        skip_unchanged = True
        report_skipped = False


class BookResource(resources.ModelResource):

    author = fields.Field(
        column_name='author',
        attribute='author',
        widget=ForeignKeyWidget(Author, field='name'),
    )
    publisher = fields.Field(
        column_name='publisher',
        attribute='publisher',
        widget=ForeignKeyWidget(Publisher, field='name'),
    )

    class Meta:
        model = Book
        import_id_fields = ['isbn']
        exclude = ('id',)
        export_order = ('title', 'isbn', 'author', 'publisher', 'published_date', 'price', 'url')
        skip_unchanged = True
        report_skipped = False
```

以下に各フィールドの説明を記載します。

#### model

e.g. `model = Author`

通常のmodelのように、対象のmodelのクラス名を定義します。ここは見たままですね。

#### import_id_fields

e.g. `import_id_fields = ['name']`

インポート時にidとして扱うフィールドを定義します。ここで指定したフィールドをもとに、既存レコードの更新や新規登録が行われます。`AuthorResource`と`BookResource`はuniqueなフィールドでもあることから、`name`フィールドを指定していて、`BookResource`では`isbn`フィールドを指定しています。


#### fields

e.g. `fields = ('name',)`

インポート/エクスポート対象のフィールドです。ここで指定したフィールドのみが対象となります。

#### exclude

e.g. `exclude = ('id',)`
インポート/エクスポート対象から除外するフィールドです。ここではDjangoの自動採番される`id`フィールドを除外しています。`fields`は指定しないと出力されないので、カラムが増えたら自動的に追加したい場合は`exclude`を使うと良いと考えます。

#### skip_unchanged

e.g. `skip_unchanged = True`
インポート時に、変更がないレコードはスキップするかどうかを指定します。`True`に設定すると、変更がない場合はスキップされ、処理が高速化されます。

#### report_skipped

e.g. `report_skipped = False`
スキップしたレコードをレポート（インポート後の画面）に含めるかどうかを指定します。`False`に設定すると、スキップされたレコードはレポートに含まれません。

#### export_order

e.g. `export_order = ('title', 'isbn', 'author', 'publisher', 'published_date', 'price', 'url')`
エクスポート時のカラム順序を指定します。

#### fields.Field

e.g.

```python
author = fields.Field(
    column_name='author',
    attribute='author',
    widget=ForeignKeyWidget(Author, field='name'),
)
```

外部キーに対しては、`fields.Field`を使って定義します。

`column_name`でCSV/JSONのカラム名を指定し、`attribute`でモデルのフィールド名を指定します。

`widget`には`ForeignKeyWidget`を使い、関連するモデルとその識別フィールドを指定します。この例だと、`Author`モデルの`name`フィールドを使って紐付けています。

極論、`ForeignKeyWidget`を使わないことも可能ですが、見た目的にわかりにくい & インポート/エクスポートをする際、例えば別環境に取り込むことを考えると、外部キーのIDに依存しない方が良いことから、`ForeignKeyWidget`を使うことを推奨します。

### admin.py

最後にadmin.pyです。

今回のサンプルコードのadmin.pyでは`django-import-export`の`ImportExportModelAdmin`を継承して基底クラスを用意し、各モデルは基底クラスを継承し、resource_classを指定しています。

今触れた2点は`django-import-export`特有の設定ですが、基本的にはDjango Admin画面のカスタマイズと同じです。

```python
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import CSV, JSON

from .models import Author, Book, Publisher
from .resources import AuthorResource, BookResource, PublisherResource


class ImportExportAdmin(ImportExportModelAdmin):
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

## 削除する場合（これは別記事で良さそう）

ちなみに、CSVに無いレコードを削除する場合は、以下の方法があります。

1. `for_delete`メソッドをオーバーライドして、削除するかどうかを判定する
2. `import_id_fields`で指定したフィールドをもとに、CSVに無いレコードを削除する

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
