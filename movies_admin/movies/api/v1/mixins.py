from django.db.models import Prefetch
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from movies.models import Person, RoleType


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'prev': self.page.previous_page_number() if self.page.has_previous() else None,
            'next': self.page.next_page_number() if self.page.has_next() else None,
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })


class FilmWorkViewsSetMixin:
    pagination_class = CustomPagination

    def get_queryset(self):
        qs = super(FilmWorkViewsSetMixin, self).get_queryset()
        return qs.prefetch_related(
            Prefetch('persons', Person.objects.filter(filmworkperson__role=RoleType.ACTOR), 'actors'),
            Prefetch('persons', Person.objects.filter(filmworkperson__role=RoleType.DIRECTOR), 'directors'),
            Prefetch('persons', Person.objects.filter(filmworkperson__role=RoleType.WRITER), 'writers')
        ).prefetch_related('genres')
