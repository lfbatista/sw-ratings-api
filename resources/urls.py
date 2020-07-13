from django.conf.urls import include, url
from resources.views import *
from rest_framework.routers import DefaultRouter

# Register viewsets
router = DefaultRouter()
router.register(r"movies", MovieViewSet)
router.register(r"ratings", RatingViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    url(r"api/", include(router.urls)),
    url(r"^$", Home.as_view(), name="home"),
    url(r"", include("rest_framework.urls")),  # login view
]
