from datetime import date

from django.core.management.base import BaseCommand

from books.models import Author, Book, Publisher


class Command(BaseCommand):
    help = 'サンプルの書籍データを読み込みます'

    def handle(self, *args, **options):
        # 著者を作成
        author_beproud, _ = Author.objects.get_or_create(name='株式会社ビープラウド')

        # 出版社を作成
        publisher_gihyo, _ = Publisher.objects.get_or_create(name='技術評論社')
        publisher_shuwa, _ = Publisher.objects.get_or_create(name='秀和システム')

        # 書籍を作成
        books_data = [
            {
                'title': '自走プログラマー',
                'isbn': '978-4-297-11197-7',
                'author': author_beproud,
                'publisher': publisher_gihyo,
                'published_date': date(2020, 2, 27),
                'price': 2948,
                'url': 'https://jisou-programmer.beproud.jp/',
            },
            {
                'title': 'Pythonプロフェッショナルプログラミング 第4版',
                'isbn': '978-4-7980-7054-4',
                'author': author_beproud,
                'publisher': publisher_shuwa,
                'published_date': date(2024, 2, 17),
                'price': 3520,
                'url': 'https://www.shuwasystem.co.jp/book/9784798070544.html',
            },
        ]

        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data,
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'作成: {book.title}'))
            else:
                self.stdout.write(f'既存: {book.title}')

        self.stdout.write(self.style.SUCCESS('サンプルデータの読み込みが完了しました'))
