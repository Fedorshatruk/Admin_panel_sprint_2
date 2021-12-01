from rest_framework.routers import SimpleRouter

from movies.api.v1.views import FilmWorkViewsSet

router = SimpleRouter()
router.register('movies', FilmWorkViewsSet)

urlpatterns = router.urls