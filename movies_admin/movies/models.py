import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('дата последнего изменения'))


class BaseModelMixin(TimeStampedMixin):
    class Meta:
        abstract = True

    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)


class Person(BaseModelMixin):
    full_name = models.TextField(verbose_name=_('Полное имя'), max_length=40)
    birth_date = models.DateField(verbose_name=_('Дата рождения'), null=True)

    class Meta:
        verbose_name = _('Персона')
        verbose_name_plural = _('Персоны')
        db_table = '"content"."person"'

    def __str__(self):
        return f'{self.full_name}'


class Genre(BaseModelMixin):
    name = models.TextField(verbose_name=_('Название'), max_length=30)
    description = models.TextField(verbose_name=_('Описание'), blank=True)

    class Meta:
        verbose_name = _('Жанр')
        verbose_name_plural = _('Жанры')
        db_table = '"content"."genre"'

    def __str__(self):
        return f'{self.name}'


class RoleType(models.TextChoices):
    ACTOR = 'actor', _('актер')
    WRITER = 'writer', _('сценарист')
    DIRECTOR = 'director', _('режиссер')


class FilmWork(BaseModelMixin):
    title = models.TextField(verbose_name=_('Название'), max_length=255)
    description = models.TextField(verbose_name=_('Описание'), blank=True)
    creation_date = models.DateField(verbose_name=_('Дата выпуска'), blank=True, null=True)
    certificate = models.TextField(verbose_name=_('Сертификат'), blank=True, null=True)
    rating = models.FloatField(
        verbose_name=_('Рейтинг'), validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True, blank=True
    )
    type = models.CharField(verbose_name=_('Тип'), max_length=30, blank=True)
    file_path = models.FileField(verbose_name=_('Файл'), upload_to='films', blank=True, null=True)
    genres = models.ManyToManyField('Genre', through='GenreFilmWork')
    persons = models.ManyToManyField('Person', through='FilmWorkPerson')

    class Meta:
        verbose_name = _('Фильм')
        verbose_name_plural = _('Фильмы')
        db_table = '"content"."film_work"'

    def __str__(self):
        return f'{self.title}'


class FilmWorkPerson(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(verbose_name=_('Роль'), choices=RoleType.choices)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('дата создания'))

    class Meta:
        verbose_name = _('Учасник фильма')
        verbose_name_plural = _('Учасники фильма')
        db_table = '"content"."person_film_work"'
        unique_together = ('film_work', 'person', 'role')

    def __str__(self):
        return f'{self.person} -- {self.film_work}'


class GenreFilmWork(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('дата создания'))

    class Meta:
        verbose_name = _('Жанр фильма')
        verbose_name_plural = _('Жанры фильмов')
        db_table = '"content"."genre_film_work"'
        unique_together = ('film_work', 'genre')

    def __str__(self):
        return f'{self.film_work} -- {self.genre}'
