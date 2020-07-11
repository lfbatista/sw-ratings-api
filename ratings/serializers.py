from django.contrib.auth.models import User
from rest_framework import serializers
from ratings.models import *


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "created",
            "episodeno",
            "director",
            "ratings",
            "release_date",
            "url",
        ]


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Rating
        fields = ["id", "comment", "owner", "rating", "url", "movie"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    ratings = serializers.HyperlinkedRelatedField(
        many=True, view_name="rating-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["id", "username", "url", "ratings"]
