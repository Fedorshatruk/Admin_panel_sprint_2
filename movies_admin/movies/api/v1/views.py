from django.db.models import Count
from rest_framework.viewsets import ReadOnlyModelViewSet

from movies.api.v1.mixins import FilmWorkViewsSetMixin
from movies.api.v1.serializers import FilmWorkSerializer
from movies.models import FilmWork


class FilmWorkViewsSet(FilmWorkViewsSetMixin, ReadOnlyModelViewSet):
    queryset = FilmWork.objects.all()
    serializer_class = FilmWorkSerializer
