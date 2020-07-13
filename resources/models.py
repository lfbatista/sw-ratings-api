from django.db import models


class Movie(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    episodeno = models.IntegerField(blank=True)
    director = models.CharField(max_length=50, blank=True, default="")
    release_date = models.CharField(max_length=30, blank=True, default="")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["release_date"]


class Rating(models.Model):
    rating_choices = ((i, i) for i in range(1, 6))
    rating = models.IntegerField(choices=rating_choices, blank=False)
    comment = models.CharField(max_length=255, blank=True)
    owner = models.ForeignKey(
        "auth.User", related_name="ratings", on_delete=models.CASCADE
    )
    movie = models.ForeignKey(Movie, related_name="ratings", on_delete=models.CASCADE)

    class Meta:
        ordering = ["rating"]
