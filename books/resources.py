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


class AuthorWidget(ForeignKeyWidget):
    """
    著者を「姓 名」形式でインポート/エクスポートするカスタムウィジェット
    """

    def __init__(self):
        super().__init__(Author)

    def clean(self, value, row=None, **kwargs):
        """インポート時: 「姓 名」からAuthorインスタンスを取得"""
        if not value:
            return None
        parts = value.split(' ', 1)
        if len(parts) == 2:
            last_name, first_name = parts
        else:
            last_name, first_name = parts[0], ''
        return Author.objects.get(last_name=last_name, first_name=first_name)

    def render(self, value, obj=None):
        """エクスポート時: Authorインスタンスを「姓 名」形式で出力"""
        if value:
            return str(value)
        return ''


class AuthorResource(resources.ModelResource):
    """
    Authorモデル用のリソースクラス

    ModelResourceを継承することで、モデルのフィールドを自動的に
    インポート/エクスポート対象として認識します。
    """

    class Meta:
        model = Author

        # インポート時にレコードを識別するフィールド（複合キー）
        import_id_fields = ['last_name', 'first_name']

        # インポート/エクスポート対象のフィールド
        fields = ('last_name', 'first_name')

        skip_unchanged = True
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
    # AuthorWidgetで「姓 名」形式での入出力に対応
    author = fields.Field(
        column_name='author',
        attribute='author',
        widget=AuthorWidget(),
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
