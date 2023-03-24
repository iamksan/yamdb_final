import logging
from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import (Category, Comment, Genre, Review, Title,
                            TitleGenre, User)


class Command(BaseCommand):
    """
    Скрипт загружает данные из csv файлов в БД.
    Для использования воспользуйтесь командой:
    python manage.py load_csv
    """

    def handle(self, *args, **options):

        for row in DictReader(open('static/data/users.csv', encoding='utf8')):

            user = User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name']
            )
            user.save()

        logging.debug('Данные из users.csv импортированы.')

        for row in DictReader(open('static/data/category.csv',
                                   encoding='utf8')):

            category = Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            category.save()

        logging.debug('Данные из category.csv импортированы.')

        for row in DictReader(open('static/data/genre.csv',
                                   encoding='utf8')):

            genre = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            genre.save()

        logging.debug('Данные из genre.csv импортированы.')

        for row in DictReader(open('static/data/titles.csv', encoding="utf8")):

            title = Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(id=row['category'])
            )
            title.save()

        logging.debug('Данные из titles.csv импортированы.')

        for row in DictReader(open('static/data/genre_title.csv',
                                   encoding='utf8')):

            category = TitleGenre(
                id=row['id'],
                title=Title.objects.get(id=row['title_id']),
                genre=Genre.objects.get(id=row['genre_id']),
            )
            category.save()

        logging.debug('Данные из genre_title.csv импортированы.')

        for row in DictReader(open('static/data/review.csv', encoding="utf8")):

            review = Review(
                id=row['id'],
                title=Title.objects.get(id=row['title_id']),
                text=row['text'],
                author=User.objects.get(id=row['author']),
                score=row['score'],
                pub_date=row['pub_date']
            )
            review.save()

        logging.debug('Данные из review.csv импортированы.')

        for row in DictReader(open('static/data/comments.csv',
                                   encoding="utf8")):

            comment = Comment(
                id=row['id'],
                review=Review.objects.get(id=row['review_id']),
                text=row['text'],
                author=User.objects.get(id=row['author']),
                pub_date=row['pub_date'],
            )
            comment.save()

        logging.debug('Данные из comments.csv импортированы.')

        logging.debug('Все данные импортированы!')
