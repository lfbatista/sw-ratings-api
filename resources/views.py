import requests
from django.shortcuts import render
from django.views import View
from rest_framework import permissions, viewsets
from resources.permissions import IsOwnerOrReadOnly
from resources.serializers import *


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get movies list and movie detail.
    Search parameterers are "title" and "episodeno".
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    search_fields = (
        "title",
        "episodeno",
    )


class RatingViewSet(viewsets.ModelViewSet):
    """
    List all ratings or get, create, update or delete a rating.
    Search parameter is "rating".
    """

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    search_fields = ("rating",)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """Associate user with created rating."""

        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Get users list and user details."""

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer


class Home(View):
    template = "home.html"
    context = {
        "page_title": "Home",
    }

    @staticmethod
    def get_movies():
        """
        Get movies from swapi.dev.
        :returns list dictionaries with movies.
        """
        api_url = "https://swapi.dev/api/films"

        response = requests.get(api_url)
        data = response.json()

        return [
            {
                "title": movie["title"],
                "episodeno": movie["episode_id"],
                "director": movie["director"],
                "release_date": movie["release_date"],
            }
            for movie in data["results"]
        ]

    def import_movies(self):
        """
        Save movies in database.
        :returns number of new movies stored.
        """

        new_movies = 0
        for movie in self.get_movies():

            _, created = Movie.objects.get_or_create(
                title=movie["title"],
                episodeno=movie["episodeno"],
                director=movie["director"],
                release_date=movie["release_date"],
            )

            if created:
                new_movies += 1

        return new_movies

    def get(self, request):
        return render(request, self.template, self.context)

    def post(self, request):
        """Post request to delete all movies."""

        erase_all_before_import = request.POST.get("erase_all_movies_before")
        if erase_all_before_import:
            Movie.objects.all().delete()

        self.import_movies()

        return render(request, self.template, self.context)
