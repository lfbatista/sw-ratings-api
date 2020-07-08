import requests
from django.shortcuts import redirect, render, reverse
from django.views import View
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

from ratings.permissions import IsOwnerOrReadOnly
from ratings.serializers import *


# API entrypoint
@api_view(["GET"])
def api_root(request, format=None):
    """Response object with API resources and its endpoints."""

    return {
        "users": reverse("user-list", request=request, format=format),
        "movies": reverse("movies-list", request=request, format=format),
        "ratings": reverse("ratings-list", request=request, format=format),
    }


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get movies list and movie detail.
    Search parameterers are "title" and "episode_n".
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    search_fields = (
        "title",
        "episode_n",
    )


#    def perform_create(self, serializer):
#        """Associate rating with created movie."""

#        serializer.save(owner=self.request.user)


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

    queryset = User.objects.all()
    serializer_class = UserSerializer


class Home(View):
    template = "home.html"
    context = {
        "page_title": "Home",
    }

    def get_movies(self):
        """
        Get movies from swapi.dev.
        :returns list dictionaries with movies.
        """
        api_url = "https://swapi.dev/api/films"
        page_length = 10

        response = requests.get(api_url)
        data = response.json()

        return [
            {
                "title": movie["title"],
                "episode_n": movie["episode_id"],
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
                episode_n=movie["episode_n"],
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

        new_movies = self.import_movies()

        return render(request, self.template, self.context)


#        return redirect(reverse("home"))


class ImportMovies(View):
    """Get movies from swapi.dev and save them into the database"""

    template = "import_movies.html"
    context = {"page_title": "Import Movies"}

    @staticmethod
    def get_movies():
        api_url = "https://swapi.dev/api/films"
        page_length = 10

        response = requests.get(api_url)
        data = response.json()

        return [
            {
                "title": movie["title"],
                "episode_n": movie["episode_id"],
                "director": movie["director"],
                "release_date": movie["release_date"],
            }
            for movie in data["results"]
        ]

    @staticmethod
    def import_movies():
        new_movies = 0
        for movie in Home.get_movies():

            _, created = Movie.objects.get_or_create(
                title=movie["title"],
                episode_n=movie["episode_n"],
                director=movie["director"],
                release_date=movie["release_date"],
            )

            if created:
                new_movies += 1

        return new_movies

    def get(self, request):
        movies_num = Movie.objects.all().count()
        self.context["movies_num"] = movies_num  # or number_of_movies

        return render(request, self.template, self.context)

    def post(self, request):
        # movies_num = Movie.objects.all().count()
        # self.context["movies_num"] = movies_num  # or number_of_movies

        erase_all_before_import = request.POST.get("erase_all_movies_before")
        # previous_number_of_movies = Movie.objects.all().count()

        if erase_all_before_import:
            Movie.objects.all().delete()

        new_movies = self.import_movies()
        # new_movies_total = Movie.objects.all().count()

        #        return render(request, self.template, self.context)
        return redirect(reverse("home"))
