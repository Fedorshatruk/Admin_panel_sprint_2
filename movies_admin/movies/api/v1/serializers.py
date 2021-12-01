from rest_framework import serializers

from movies.models import FilmWork


class FilmWorkSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()
    directors = serializers.SerializerMethodField()
    writers = serializers.SerializerMethodField()

    class Meta:
        model = FilmWork
        fields = ('id', 'title', 'description', 'creation_date',
                  'rating', 'type', 'genres', 'actors', 'directors',
                  'writers',
                  )

    def get_genres(self, obj):
        return [genre.name for genre in obj.genres.all()]

    def get_actors(self, obj):
        return [author.full_name for author in obj.actors]

    def get_directors(self, obj):
        return [director.full_name for director in obj.directors]

    def get_writers(self, obj):
        return [writer.full_name for writer in obj.writers]
