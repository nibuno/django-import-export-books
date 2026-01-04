[django-import-export](https://django-import-export.readthedocs.io/en/latest/)は、Django Admin画面でインポート機能・エクスポート機能を行うことのできるライブラリです。

CSV、JSONなどの複数の形式にも対応しており、要件上、操作画面がDjango Admin画面でも良い場合は有力な選択肢になります。触る機会があるので、理解のためにまとめます。

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

次に、resources.pyを作成します。ここでは、`Resource`クラスを定義します。

※公式リファレンス上にはresources.pyを作成するようなことは説明されておらず、admin.pyにまとめていましたが、今回は理解のしやすさのため別ファイルとして切り出しました。

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

インポート時にidとして扱うフィールドを定義します。

未指定な場合は`id`を用います。ここで指定したフィールドをもとに、既存レコードの更新や新規登録が行われます。`AuthorResource`と`PublisherResource`はuniqueなフィールドでもあることから、`name`フィールドを指定していて、`BookResource`では`isbn`フィールドを指定しています。


#### fields

e.g. `fields = ('name',)`

インポート/エクスポート対象のフィールドを絞り込みたい時に指定します。ここでは`name`フィールドのみを対象としています。`fields`を指定しない場合は、すべてのフィールドが対象となります。

#### exclude

e.g. `exclude = ('id',)`
インポート/エクスポート対象から除外するフィールドです。ここではDjangoの自動採番される`id`フィールドを除外しています。`fields`は指定しないと出力されないので、カラムが増えたら自動的に追加したい場合は`exclude`を使うと良いと考えます。

#### skip_unchanged

e.g. `skip_unchanged = True`
インポート時に、変更がないレコードはスキップするかどうかを指定します。`True`に設定すると、変更がない場合はスキップされます。更新する必要が無ければ`True`で良いと考えています。

#### report_skipped

e.g. `report_skipped = False`
スキップしたレコードをレポート（インポート後の画面）に含めるかどうかを指定します。`False`に設定すると、スキップされたレコードはレポートに含まれません。こちらも必要なければ`False`で良いと考えています。

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

`widget`には`ForeignKeyWidget`を使い、関連するモデルとその識別フィールドを指定します。この例だと、uniqueに設定済である`Author`モデルの`name`フィールドを使って紐付けています。

ちなみに、`ForeignKeyWidget`を使わない場合は、エクスポート時はモデルの`__str__`の内容でエクスポートされるので問題ないですが、インポートしようとした際には、次の画像のようにエラーとなりました。リファレンスを確認したところ、`field`を指定しないと、`pk`として扱われるように記述があり、プレビュー画面のことを考えると`name`など、別の識別子として扱えるカラムがある方が見やすそうです。

[f:id:nibutan:20260104142439p:plain]

### admin.py

続いてadmin.pyです。

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
```

## ダウンロードしたCSVについて

登録した内容については本記事では省略していますが、管理画面からエクスポートしたCSVは以下のようになります。

```csv
title,isbn,author,publisher,published_date,price,url
Pythonプロフェッショナルプログラミング 第4版,978-4-7980-7054-4,株式会社ビープラウド,秀和システム,2024-02-17,3520,https://www.shuwasystem.co.jp/book/9784798070544.html
自走プログラマー,978-4-297-11197-7,株式会社ビープラウド,技術評論社,2020-02-27,2948,https://jisou-programmer.beproud.jp/
```

## import / export の操作について

一度、レコードを削除してみます。

<figure class="figure-image figure-image-fotolife" title="既存レコードの削除">[f:id:nibutan:20260104103748p:plain]<figcaption>既存レコードの削除</figcaption></figure>

右上の「インポート」を押下すると、次のようにインポート画面へ遷移します。

<figure class="figure-image figure-image-fotolife" title="インポート画面">[f:id:nibutan:20260104103814p:plain]<figcaption>インポート画面</figcaption></figure>

そこでファイルを選択して確定を謳歌します。

すると、インポートのプレビュー画面に遷移します。

<figure class="figure-image figure-image-fotolife" title="インポート後のプレビュー画面">[f:id:nibutan:20260104103947p:plain]<figcaption>インポート後のプレビュー画面</figcaption></figure>

インポート実行を押下すると、インポートできました。

<figure class="figure-image figure-image-fotolife" title="インポート完了">[f:id:nibutan:20260104104017p:plain]<figcaption>インポート完了</figcaption></figure>

## 参考リンク

### 公式ドキュメント

* [django-import-export 公式ドキュメント](https://django-import-export.readthedocs.io/en/latest/)
* [Getting started](https://django-import-export.readthedocs.io/en/latest/getting_started.html)
* [Admin integration](https://django-import-export.readthedocs.io/en/latest/admin_integration.html)

### Resource クラス

* [ModelResource](https://django-import-export.readthedocs.io/en/latest/api_resources.html#import_export.resources.ModelResource)

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
