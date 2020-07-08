from django.db import models


class Movie(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    episode_n = models.IntegerField(blank=True)
    director = models.CharField(max_length=50, blank=True, default="")
    release_date = models.CharField(max_length=30, blank=True, default="")

    # owner = models.ForeignKey(
    #     "auth.User", related_name="movies", on_delete=models.CASCADE
    # )

    class Meta:
        ordering = ["release_date"]


class Rating(models.Model):
    # TODO: validate if table Movie exists before getting it
    movie_choices = [
        (getattr(movie, "title"), getattr(movie, "title"))
        for movie in Movie.objects.all()
    ]
    movies = models.CharField(
        choices=movie_choices, default="", blank=False, max_length=100
    )
    rating_choices = ((i, i) for i in range(1, 6))
    rating = models.IntegerField(
        choices=rating_choices, blank=False
    )  # ratings are integers between 0 and 5
    comment = models.CharField(max_length=255, blank=True, default="")
    owner = models.ForeignKey(
        "auth.User", related_name="ratings", on_delete=models.CASCADE
    )
    #    movie = models.ForeignKey(Movie, related_name="movies", on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ["rating"]
