---
name: django-import-export
description: django-import-exportを使用する際に参照
---

# Django-Import-Export スキル

公式ドキュメントから生成された、django-import-export用のスキルファイルです。

## このスキルを使うタイミング

以下の場合にこのスキルを参照してください：
- django-import-exportを使った開発時
- django-import-exportの機能やAPIについて質問があるとき
- django-import-exportのソリューションを実装するとき
- django-import-exportのコードをデバッグするとき
- django-import-exportのベストプラクティスを学ぶとき

## クイックリファレンス

### よくある問題と解決策（FAQ）

#### import_id_fields エラー

インポート時に以下のエラーが表示される場合：

```
The following fields are declared in 'import_id_fields' but are not present in the resource
```

これはResourceが正しく設定されていないことを示しています。`import_id_fields`で定義されたフィールドがリソースのフィールドに存在しません。

#### Signalによる二重保存の問題

Admin画面でインポートを使用し、post_saveシグナルを実装している場合、シグナルが各インスタンスに対して2回呼ばれます。

**理由**: モデルの`save()`メソッドが2回呼ばれるため（「確認」ステップと「インポート」ステップ）

**回避策**: インスタンスに一時フラグを設定

```python
class BookResource(resources.ModelResource):
    def before_save_instance(self, instance, row, **kwargs):
        # 「確認」ステップ中は dry_run が True
        instance.dry_run = kwargs.get("dry_run", False)

    class Meta:
        model = Book
        fields = ('id', 'name')
```

シグナルレシーバーでフラグを確認：

```python
@receiver(post_save, sender=Book)
def my_callback(sender, **kwargs):
    instance = kwargs["instance"]
    if getattr(instance, "dry_run", False):
        # 「確認」ステップでは何もしない
        return
    else:
        # カスタムロジックをここに
        # 「インポート」ステップでのみ実行される
        pass
```

#### インポート時のIDが2回インクリメントされる

Admin画面でインポートすると、プレビューで表示されたIDと実際のIDが異なることがあります。これは「確認」時にインポートされた後、トランザクションがロールバックされるためです。

**回避策**: `IMPORT_EXPORT_SKIP_ADMIN_CONFIRM`を有効にする

#### 空のCharFieldでNot Null制約エラー

v3で発生していた問題で、v4で解決済み。Excelからインポートする際、空セルがNoneに変換されることで発生。

v4では、DjangoのCharFieldに`blank=True`が設定されている場合、null値や空文字列は空文字列として保存されます。

Noneを保存したい場合：

```python
class BookResource(resources.ModelResource):
    name = Field(widget=CharWidget(allow_blank=False))

    class Meta:
        model = Book
```

#### インポート時に外部キーがnullになる

モデルのリレーションは、ダブルアンダースコア構文でフィールドを定義できます：

```python
class BookResource(ModelResource):
    class Meta:
        model = Book
        fields = ("author__name",)
```

これはエクスポート時には機能しますが、**インポート時には機能しません**。インポート時は`ForeignKeyWidget`を使用してください。

#### エクスポートカラム名の変更

`get_export_headers()`をオーバーライドします：

```python
class BookResource(ModelResource):
    def get_export_headers(self, fields=None):
        headers = super().get_export_headers(fields=fields)
        for i, h in enumerate(headers):
            if h == 'name':
                headers[i] = "新しいカラム名"
        return headers

    class Meta:
        model = Book
```

#### 大量ファイルのインポート

タイムアウトが発生する場合は、Celeryやバルクインポートを参照してください。

#### Admin インポート確認時の FileNotFoundError

マルチサーバー/コンテナ環境で発生することがあります。一時ファイルストレージがサーバープロセス間で共有されていないためです。

**解決策**: マルチサーバー環境では一時ファイルシステムストレージを避ける

---

## リリースノート

### v5.0 破壊的変更

- フォームフィールド名のクラッシュを修正。`resource`、`format`、`export_items`フィールド名に`django-import-export-`プレフィックスが追加
- 非推奨の`get_valid_export_item_pks()`メソッドを削除。代わりに`get_queryset()`を使用
- エクスポートフォームがインポートフィールドを表示していた問題を修正

**非推奨**:
- `get_user_visible_fields()`は非推奨。v6.0で削除予定
- 代わりに`get_user_visible_import_fields()`（インポート用）と`get_user_visible_export_fields()`（エクスポート用）を使用

### v4.2 破壊的変更

- 数値、boolean、日時ウィジェットがスプレッドシート形式（ODS, XLS, XLSX）にネイティブ値として書き込まれるように変更
- `coerce_to_string`の値は、Admin画面からスプレッドシート形式にエクスポートする場合は無視される

サブクラスしている場合、`**kwargs`パラメータを追加する必要があります：

| 変更前 | 変更後 |
|--------|--------|
| `Widget.render(self, value, obj=None)` | `Widget.render(self, value, obj=None, **kwargs)` |
| `Field.export(self, instance)` | `Field.export(self, instance, **kwargs)` |
| `Resource.export_field(self, field, instance)` | `Resource.export_field(self, field, instance, **kwargs)` |

### v4.1

- `Resource.get_fields()`メソッドは非推奨。オーバーライドしている場合は削除してください

### v4.0 主要な変更

#### インストール

オプション依存関係を許可するためインストール方法が変更されました：

```bash
pip install django-import-export[all]
```

#### Admin UIの変更

`resource_class`は`resource_classes`に置き換え：

```python
class BookAdmin(ImportExportModelAdmin):
    # これを削除
    # resource_class = BookResource

    # これに置き換え
    resource_classes = [BookResource]
```

#### エクスポートフォーマット

v4では、デフォルトで文字列としてレンダリングされます。v3の動作（Excelでネイティブ型）を維持するには：

```python
coerce_to_string = False
```

#### インポートエラーメッセージ

デフォルトでエラーメッセージのみ表示。元のフォーマット（行とトレースバック含む）を復元：

```python
class BookAdmin(ImportExportModelAdmin):
    import_error_display = ("message", "row", "traceback")
```

#### API変更（主要なもの）

| 変更前 | 変更後 | 概要 |
|--------|--------|------|
| `import_obj(self, obj, data, dry_run, **kwargs)` | `import_instance(self, instance, row, **kwargs)` | obj→instance, data→row, dry_runはkwargsへ |
| `before_import(self, dataset, using_transactions, dry_run, **kwargs)` | `before_import(self, dataset, **kwargs)` | using_transactions, dry_runはkwargsへ |
| `save_instance(self, instance, is_create, using_transactions=True, dry_run=False)` | `save_instance(self, instance, is_create, row, **kwargs)` | rowが必須引数に追加 |

---

## 管理コマンド

### エクスポートコマンド

```bash
python manage.py export <format> <resource> [--encoding ENCODING]
```

**例**:
```bash
# UserモデルをCSVでエクスポート
python manage.py export CSV auth.User

# カスタムResourceをXLSXでエクスポート
python manage.py export XLSX mymodule.resources.MyResource
```

### インポートコマンド

```bash
python manage.py import <resource> <import_file_name> [--format FORMAT] [--encoding ENCODING] [--dry-run] [--raise-errors]
```

**例**:
```bash
# デフォルトリソースでインポート
python manage.py import auth.User users.csv

# カスタムResourceでインポート（エラー発生時に例外を投げる）
python manage.py import --raise-errors helper.MyUserResource users.csv
```

---

## リファレンスファイル

このスキルには`references/`に詳細なドキュメントが含まれています：

- **_images.md** - 画像関連ドキュメント
- **_sources.md** - ソースドキュメント
- **api.md** - APIドキュメント
- **other.md** - その他のドキュメント

詳細情報が必要な場合は、`view`コマンドで特定のリファレンスファイルを読み込んでください。

## このスキルの使い方

### 初心者向け
getting_startedやtutorialsのリファレンスファイルから基本概念を学んでください。

### 特定機能について
適切なカテゴリのリファレンスファイル（api、guidesなど）を参照してください。

### コード例
上記のクイックリファレンスセクションには、公式ドキュメントから抽出されたよくあるパターンが含まれています。

## リソース

### references/
公式ソースから抽出された整理されたドキュメント：
- 詳細な説明
- 言語アノテーション付きコード例
- 元のドキュメントへのリンク
- クイックナビゲーション用の目次

### scripts/
一般的な自動化タスク用のヘルパースクリプトを追加してください。

### assets/
テンプレート、ボイラープレート、サンプルプロジェクトを追加してください。

## 注意事項

- このスキルは公式ドキュメントから自動生成されました
- リファレンスファイルはソースドキュメントの構造と例を保持しています
- コード例には適切なシンタックスハイライトのための言語検出が含まれています
- クイックリファレンスパターンはドキュメントの一般的な使用例から抽出されています

## 更新方法

最新のドキュメントでこのスキルを更新するには：
1. 同じ設定でスクレイパーを再実行
2. スキルが最新情報で再構築されます
