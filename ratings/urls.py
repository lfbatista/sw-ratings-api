from django.conf.urls import include, url

# from django.urls import include, path
from rest_framework.routers import DefaultRouter
from ratings.views import *


# Register viewsets
router = DefaultRouter()
router.register(r"movies", MovieViewSet)
router.register(r"ratings", RatingViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    url(r"api/", include(router.urls)),
    url(r"^$", Home.as_view(), name="home"),
    url(r"", include("rest_framework.urls")),  # login view
    #    url(r"import/", ImportMovies.as_view(), name = "importmovies"),
]
