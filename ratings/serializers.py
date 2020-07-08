from django.contrib.auth.models import User
from rest_framework import serializers
from ratings.models import *


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    #    ratings = serializers.HyperlinkedRelatedField(
    #        many=True, view_name="rating-detail", read_only=True
    #    )

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "created",
            "episode_n",
            "director",
            #            "ratings",
            "release_date",
            "url",
            # "owner"
        ]


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    #    movie = serializers.HyperlinkedRelatedField(
    #        #many=True,
    #        view_name="movie-detail", read_only=True
    #    )

    class Meta:
        model = Rating
        fields = ["id", "comment", "owner", "rating", "url", "movies"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    ratings = serializers.HyperlinkedRelatedField(
        many=True, view_name="rating-detail", read_only=True
    )
    # movies = serializers.HyperlinkedRelatedField(
    #     many=True, view_name="movie-detail", read_only=True
    # )

    class Meta:
        model = User
        fields = ["id", "username", "url", "ratings"]
