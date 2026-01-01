# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

django-import-exportライブラリを使用した書籍データのエクスポート機能を試すプロジェクト。プラウド出版の書籍（自走プログラマー、Pythonプロフェッショナルプログラミング等）を管理する。

## 技術スタック

- Django 5.2
- django-import-export

## セットアップ

```bash
# 仮想環境の有効化
source venv/bin/activate

# 依存パッケージのインストール
pip install -r requirements.txt

# マイグレーション
python manage.py migrate

# サンプルデータの読み込み
python manage.py load_sample_data
```

## コマンド

```bash
# 開発サーバー起動
python manage.py runserver

# マイグレーション
python manage.py makemigrations
python manage.py migrate

# テスト実行
python manage.py test

# 単一テスト実行
python manage.py test <app_name>.tests.<TestClass>.<test_method>

# サンプルデータ読み込み
python manage.py load_sample_data
```

## 管理画面

- URL: http://localhost:8000/admin/
- 開発用アカウント: admin / admin
- エクスポート: 各モデルの一覧画面から「エクスポート」ボタンでCSV/JSONをダウンロード
- インポート: 各モデルの一覧画面から「インポート」ボタンでCSV/JSONをアップロード

## アーキテクチャ

### アプリ構成

- 単一アプリ（`books`）にすべてのモデルをまとめる

### モデル設計

| モデル | 説明 |
|--------|------|
| Book | 書籍情報を管理 |
| Author | 著者情報を管理（Bookから1対多） |
| Publisher | 出版社情報を管理（Bookから1対多） |

### Bookモデルのフィールド

| フィールド | 型 | 備考 |
|-----------|-----|------|
| title | CharField | タイトル |
| isbn | CharField | ISBN（一意、エクスポート時の識別キー） |
| publisher | ForeignKey | 出版社 |
| published_date | DateField | 発売日 |
| price | IntegerField | 価格 |
| author | ForeignKey | 著者（1冊につき1著者） |
| url | URLField | 書籍紹介ページ |

### Author/Publisherモデル

- 名前（name）を一意キーとして扱う
- エクスポート/インポート時は名前で識別

### インポート/エクスポート設計

- **対応形式**: CSV, JSON
- **識別方法**: BookはISBN、Author/Publisherは名前で識別（IDに依存しない）
- **目的**: 別環境へのデータ移行
- **インポート時の動作**: 変更がないデータはスキップ（`skip_unchanged=True`）

### データベース

- SQLite（開発・検証用途）

## 今後の課題

- Bookモデルに自然キーカラムを追加する（別課題）
