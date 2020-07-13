from django.contrib.auth.models import User
from django.test import TestCase
from .models import *
from rest_framework import status


class TestEndpoints(TestCase):
    fixtures = ["movies.json", "ratings.json", "users.json"]

    def get(self, url):
        return self.client.get(url)

    def authenticate(self):
        return self.client.login(username="admin", password="admin")

    def test_api_root(self):
        self.assertEqual(self.get("/api/").status_code, status.HTTP_200_OK)

    def test_movies(self):
        self.assertEqual(self.get("/api/movies/").status_code, status.HTTP_200_OK)

    def test_movies_detail(self):
        response = self.get("/api/movies/1/")
        json_data = response.json()
        movie = Movie.objects.get(pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(movie.title, json_data["title"])

    def test_movies_search(self):
        response = self.get("/api/movies/?search=mena")
        json_data = response.json()
        movie = Movie.objects.get(title="The Phantom Menace")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(movie.title, json_data["results"][0]["title"])

        list_response = self.get("/api/movies/")
        list_data = list_response.json()
        self.assertLess(json_data["count"], list_data["count"])

    def test_ratings(self):
        self.assertEqual(self.get("/api/ratings/").status_code, status.HTTP_200_OK)

    def test_ratings_detail(self):
        response = self.get("/api/ratings/1/")
        json_data = response.json()
        rating = Rating.objects.get(pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rating.rating, json_data["rating"])

    def test_ratings_search(self):
        response = self.get("/api/ratings/?search=5")
        json_data = response.json()
        rating = Rating.objects.get(id=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rating.comment, json_data["results"][0]["comment"])

        list_response = self.get("/api/ratings/")
        list_data = list_response.json()
        self.assertLess(json_data["count"], list_data["count"])

    def test_ratings_post(self):
        self.authenticate()

        response = self.client.post(
            "/api/ratings/",
            {"rating": 4, "movie": "http://127.0.0.1:8000/api/movies/3/"},
        )
        json_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        instance_response = self.get(f"/api/ratings/{json_data['id']}/")
        instance_data = instance_response.json()
        self.assertEqual(json_data["comment"], instance_data["comment"])

    def test_ratings_post_unauthenticated(self):
        response = self.client.post(
            "/api/ratings/",
            {"rating": 4, "movie": "http://127.0.0.1:8000/api/movies/3/"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ratings_post_without_req_params(self):
        self.authenticate()

        response = self.client.post(
            "/api/ratings/", {"movie": "http://127.0.0.1:8000/api/movies/3/"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ratings_put(self):
        self.authenticate()

        instance_response = self.get("/api/ratings/2/")
        instance_json_data = instance_response.json()

        payload = {
            "rating": 4,
            "movie": "http://127.0.0.1:8000/api/movies/2/",
            "comment": "neat",
        }
        response = self.client.put(
            "/api/ratings/2/", payload, content_type="application/json"
        )
        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(instance_json_data["comment"], json_data["comment"])

    def test_ratings_delete(self):
        self.authenticate()

        response = self.client.delete("/api/ratings/2/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_users(self):
        self.assertEqual(self.get("/api/users/").status_code, status.HTTP_200_OK)

    def test_users_detail(self):
        response = self.get("/api/users/1/")
        json_data = response.json()
        user = User.objects.get(pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.username, json_data["username"])
