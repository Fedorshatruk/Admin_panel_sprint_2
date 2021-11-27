import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from tqdm import tqdm

from movies.factories import FilmWorkFactory, GenreFactory, PersonFactory
from movies.models import GenreFilmWork, FilmWorkPerson, RoleType, Person, Genre, FilmWork

PERSONS = 100000
FILMS = 1000000
GENRES = 10

BATCH_SIZE = 50000
TEST = 10


def generate_films():
    films = []
    for _ in tqdm(range(FILMS)):
        film = FilmWorkFactory.build(type=type)
        films.append(film)
    return films


def generate_genres():
    genres = []
    for _ in tqdm(range(GENRES)):
        genre = GenreFactory.build()
        genres.append(genre)
    return genres


def generate_persons():
    persons = []
    for _ in tqdm(range(PERSONS)):
        person = PersonFactory.build()
        persons.append(person)
    return persons


class Command(BaseCommand):
    help = 'Генерирует тестовые данные'

    def handle(self, *args, **kwargs):
        self.stdout.write('Создаем данные\n')

        self.stdout.write('Генерируем фильмы\n')
        films = generate_films()
        print(films[0])
        self.stdout.write('Генерируем жанры\n')
        genres = generate_genres()

        self.stdout.write('Генерируем персоны\n')
        persons = generate_persons()

        self.stdout.write('Создаем связи\n')

        self.stdout.write('Генерируем жанры фильма и актеров\n')
        genres_films_work = []
        films_work_persons = []

        for film in tqdm(films):
            genre_film_work = GenreFilmWork()
            genre_film_work.film_work = film
            genre_film_work.genre = random.choice(genres)
            genres_films_work.append(genre_film_work)

            for _ in range(random.randint(1, 20)):
                film_work_person = FilmWorkPerson()
                film_work_person.film_work = film
                film_work_person.person = random.choice(persons)
                film_work_person.role = random.choices(RoleType.choices)[0][0]
                films_work_persons.append(film_work_person)

        self.stdout.write('Все данные сгенерированы\n')

        self.stdout.write('Сохраняем данные в БД\n')

        self.stdout.write('Сохраняем персон\n')
        Person.objects.bulk_create(tqdm(persons))

        self.stdout.write('Сохраняем жанры\n')
        Genre.objects.bulk_create(tqdm(genres))

        self.stdout.write('Сохраняем фильмы\n')
        FilmWork.objects.bulk_create(tqdm(films), batch_size=BATCH_SIZE)

        self.stdout.write('Сохраняем жанры конкретных фильмов в БД\n')
        GenreFilmWork.objects.bulk_create(tqdm(genres_films_work), batch_size=BATCH_SIZE)

        self.stdout.write('Сохраняем персон фильмов в БД\n')
        try:
            FilmWorkPerson.objects.bulk_create(tqdm(films_work_persons), batch_size=BATCH_SIZE)
        except IntegrityError:
            pass

        self.stdout.write('Создание данных завершено!\n')
