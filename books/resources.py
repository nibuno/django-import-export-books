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

    # 削除フラグ用のフィールド
    # インポート時に delete=1 の行は削除対象となる
    delete = fields.Field(column_name='delete', default='')

    def for_delete(self, row, instance):
        """
        行を削除するかどうかを判定する

        CSVの'delete'列が'1'の場合、該当レコードを削除する。
        削除対象の行は、既存レコードが存在する場合のみ削除される。
        （新規レコードに delete=1 が指定されている場合はスキップされる）
        """
        return row.get('delete') == '1'

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
