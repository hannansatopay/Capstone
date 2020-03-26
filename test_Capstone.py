import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie
import datetime


class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "Capstone_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': 'John Smith',
            'age': 34,
            'gender': 'male',
        }

        self.new_movie = {
            'actor_id': '2',
            'releaseDate': datetime.datetime(2022, 2, 22),
            'title': 'Contagion',
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        selection = Movie.query.filter(Movie.title == 'Contagion').all()
        for movie in selection:
            movie.delete()
        selection = Actor.query.filter(Actor.name == 'John Smith').all()
        for actor in selection:
            actor.delete()
        pass

    def test_get_all_actors(self):
        res = self.client().get('/actors', headers={'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9USXpNakl6UkVZMFJEQXdNRGN3UTBFNVF6TTBNekE0TURNMVF6bERRVGRFUVRNeE1VUXpNdyJ9.eyJpc3MiOiJodHRwczovL29maW5lby5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU3YzY4Y2ExMWRkNDkwYzZiM2VlNTM0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODUyMTE3ODksImV4cCI6MTU4NTI5ODE4OSwiYXpwIjoiMzVNNTJYbEgxM1R6NDl6T3gzQXBkUTdrNmY3Y1Fnb2wiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.s2ZdhS_O7cTCaD92vHdz_nnCI02VG4w4lWy_C5IOi7Ubx5O4HLEJUFKlqSXLOfAGnZrk1bwvhtC2uFcMT6dG8PFvS4zaWeMKVMQM0mFKKnAoEX_y9vXXyBAtj3tl7NqUqyYgK-Mtv-7-vaNnEC6wFNEzchkpAHU6M0KZ__RGcuuAWY9cSBClFiZmcc4CmHeO9GJJCjxau-gzPa9nEG7bvUkEFUGk4evu-ELPG4a9Nmna7JMVQ3eSry3SZnm0Z_uyzV7nUtHcWoD0Bc-xyuF5mt8NFm37PaHyaDLaypiwJ_HfoaWSNCucwuZfXTtZ76w_TvBToqOj9qo40zfOtOeYeQ'})
        data = res.get_json()

        selection = Actor.query.all()

        self.assertEqual(data['status'], True)
        self.assertEqual(data['actors'], [actor.format() for actor in selection])

    def test_post_actor(self):
        table_length = Actor.query.all()

        res = self.client().post('/actors/add', headers={
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9USXpNakl6UkVZMFJEQXdNRGN3UTBFNVF6TTBNekE0TURNMVF6bERRVGRFUVRNeE1VUXpNdyJ9.eyJpc3MiOiJodHRwczovL29maW5lby5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU3YzY4Y2ExMWRkNDkwYzZiM2VlNTM0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODUyMTE3ODksImV4cCI6MTU4NTI5ODE4OSwiYXpwIjoiMzVNNTJYbEgxM1R6NDl6T3gzQXBkUTdrNmY3Y1Fnb2wiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.s2ZdhS_O7cTCaD92vHdz_nnCI02VG4w4lWy_C5IOi7Ubx5O4HLEJUFKlqSXLOfAGnZrk1bwvhtC2uFcMT6dG8PFvS4zaWeMKVMQM0mFKKnAoEX_y9vXXyBAtj3tl7NqUqyYgK-Mtv-7-vaNnEC6wFNEzchkpAHU6M0KZ__RGcuuAWY9cSBClFiZmcc4CmHeO9GJJCjxau-gzPa9nEG7bvUkEFUGk4evu-ELPG4a9Nmna7JMVQ3eSry3SZnm0Z_uyzV7nUtHcWoD0Bc-xyuF5mt8NFm37PaHyaDLaypiwJ_HfoaWSNCucwuZfXTtZ76w_TvBToqOj9qo40zfOtOeYeQ'},
            json=self.new_actor
        )

        data = res.get_json()

        self.assertEqual(data['status'], True)
        self.assertGreater(len(Actor.query.all()), len(table_length))

    def test_patch_actor(self):
        actor = Actor(
            name='Otilio',
            age=22,
            gender='male'
        )
        actor.id = 222
        actor.insert()

        res = self.client().patch('/actors/222', headers={
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9USXpNakl6UkVZMFJEQXdNRGN3UTBFNVF6TTBNekE0TURNMVF6bERRVGRFUVRNeE1VUXpNdyJ9.eyJpc3MiOiJodHRwczovL29maW5lby5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU3YzY4Y2ExMWRkNDkwYzZiM2VlNTM0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODUyMTE3ODksImV4cCI6MTU4NTI5ODE4OSwiYXpwIjoiMzVNNTJYbEgxM1R6NDl6T3gzQXBkUTdrNmY3Y1Fnb2wiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.s2ZdhS_O7cTCaD92vHdz_nnCI02VG4w4lWy_C5IOi7Ubx5O4HLEJUFKlqSXLOfAGnZrk1bwvhtC2uFcMT6dG8PFvS4zaWeMKVMQM0mFKKnAoEX_y9vXXyBAtj3tl7NqUqyYgK-Mtv-7-vaNnEC6wFNEzchkpAHU6M0KZ__RGcuuAWY9cSBClFiZmcc4CmHeO9GJJCjxau-gzPa9nEG7bvUkEFUGk4evu-ELPG4a9Nmna7JMVQ3eSry3SZnm0Z_uyzV7nUtHcWoD0Bc-xyuF5mt8NFm37PaHyaDLaypiwJ_HfoaWSNCucwuZfXTtZ76w_TvBToqOj9qo40zfOtOeYeQ'},
            json={"name": "Otilio", "age": "54"}
        )
        data = res.get_json()

        actor = Actor.query.filter(Actor.id == 222).one_or_none()

        self.assertEqual(data['status'], True)
        self.assertEqual(actor.name, 'Otilio')

        actor.delete()

    def test_delete_actor(self):
        actor = Actor(
            name='Sean Conery',
            age=75,
            gender='male'
        )
        actor.id = 222
        actor.insert()

        res = self.client().delete('/actors/222', headers={
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9USXpNakl6UkVZMFJEQXdNRGN3UTBFNVF6TTBNekE0TURNMVF6bERRVGRFUVRNeE1VUXpNdyJ9.eyJpc3MiOiJodHRwczovL29maW5lby5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU3YzY4Y2ExMWRkNDkwYzZiM2VlNTM0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODUyMTE3ODksImV4cCI6MTU4NTI5ODE4OSwiYXpwIjoiMzVNNTJYbEgxM1R6NDl6T3gzQXBkUTdrNmY3Y1Fnb2wiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.s2ZdhS_O7cTCaD92vHdz_nnCI02VG4w4lWy_C5IOi7Ubx5O4HLEJUFKlqSXLOfAGnZrk1bwvhtC2uFcMT6dG8PFvS4zaWeMKVMQM0mFKKnAoEX_y9vXXyBAtj3tl7NqUqyYgK-Mtv-7-vaNnEC6wFNEzchkpAHU6M0KZ__RGcuuAWY9cSBClFiZmcc4CmHeO9GJJCjxau-gzPa9nEG7bvUkEFUGk4evu-ELPG4a9Nmna7JMVQ3eSry3SZnm0Z_uyzV7nUtHcWoD0Bc-xyuF5mt8NFm37PaHyaDLaypiwJ_HfoaWSNCucwuZfXTtZ76w_TvBToqOj9qo40zfOtOeYeQ'},
        )

        data = res.get_json()
        selection = Actor.query.filter(Actor.id == 222).one_or_none()

        self.assertEqual(data['status'], True)
        self.assertEqual(selection, None)

    def test_get_all_movies(self):
        res = self.client().get('/movies', headers={'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9USXpNakl6UkVZMFJEQXdNRGN3UTBFNVF6TTBNekE0TURNMVF6bERRVGRFUVRNeE1VUXpNdyJ9.eyJpc3MiOiJodHRwczovL29maW5lby5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU3YzY4Y2ExMWRkNDkwYzZiM2VlNTM0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODUyMTE3ODksImV4cCI6MTU4NTI5ODE4OSwiYXpwIjoiMzVNNTJYbEgxM1R6NDl6T3gzQXBkUTdrNmY3Y1Fnb2wiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.s2ZdhS_O7cTCaD92vHdz_nnCI02VG4w4lWy_C5IOi7Ubx5O4HLEJUFKlqSXLOfAGnZrk1bwvhtC2uFcMT6dG8PFvS4zaWeMKVMQM0mFKKnAoEX_y9vXXyBAtj3tl7NqUqyYgK-Mtv-7-vaNnEC6wFNEzchkpAHU6M0KZ__RGcuuAWY9cSBClFiZmcc4CmHeO9GJJCjxau-gzPa9nEG7bvUkEFUGk4evu-ELPG4a9Nmna7JMVQ3eSry3SZnm0Z_uyzV7nUtHcWoD0Bc-xyuF5mt8NFm37PaHyaDLaypiwJ_HfoaWSNCucwuZfXTtZ76w_TvBToqOj9qo40zfOtOeYeQ'})
        data = res.get_json()

        selection = Movie.query.all()

        self.maxDiff = None

        self.assertEqual(data['status'], True)
        self.assertEqual(data['movies'], [movie.format() for movie in selection])

    def test_post_movie(self):
        table_length = Movie.query.all()

        res = self.client().post('/movies/add', headers={
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9USXpNakl6UkVZMFJEQXdNRGN3UTBFNVF6TTBNekE0TURNMVF6bERRVGRFUVRNeE1VUXpNdyJ9.eyJpc3MiOiJodHRwczovL29maW5lby5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU3YzY4Y2ExMWRkNDkwYzZiM2VlNTM0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODUyMTE3ODksImV4cCI6MTU4NTI5ODE4OSwiYXpwIjoiMzVNNTJYbEgxM1R6NDl6T3gzQXBkUTdrNmY3Y1Fnb2wiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.s2ZdhS_O7cTCaD92vHdz_nnCI02VG4w4lWy_C5IOi7Ubx5O4HLEJUFKlqSXLOfAGnZrk1bwvhtC2uFcMT6dG8PFvS4zaWeMKVMQM0mFKKnAoEX_y9vXXyBAtj3tl7NqUqyYgK-Mtv-7-vaNnEC6wFNEzchkpAHU6M0KZ__RGcuuAWY9cSBClFiZmcc4CmHeO9GJJCjxau-gzPa9nEG7bvUkEFUGk4evu-ELPG4a9Nmna7JMVQ3eSry3SZnm0Z_uyzV7nUtHcWoD0Bc-xyuF5mt8NFm37PaHyaDLaypiwJ_HfoaWSNCucwuZfXTtZ76w_TvBToqOj9qo40zfOtOeYeQ'},
            json=self.new_movie
        )

        data = res.get_json()

        self.assertEqual(data['status'], True)
        self.assertGreater(len(Movie.query.all()), len(table_length))

    def test_patch_movie(self):
        movie = Movie(
            title='The cube',
            releaseDate=datetime.datetime(2022, 2, 22),
            actor_id='1'
        )
        movie.id = 222
        movie.insert()

        res = self.client().patch('/movies/222', headers={
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9USXpNakl6UkVZMFJEQXdNRGN3UTBFNVF6TTBNekE0TURNMVF6bERRVGRFUVRNeE1VUXpNdyJ9.eyJpc3MiOiJodHRwczovL29maW5lby5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU3YzY4Y2ExMWRkNDkwYzZiM2VlNTM0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODUyMTE3ODksImV4cCI6MTU4NTI5ODE4OSwiYXpwIjoiMzVNNTJYbEgxM1R6NDl6T3gzQXBkUTdrNmY3Y1Fnb2wiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.s2ZdhS_O7cTCaD92vHdz_nnCI02VG4w4lWy_C5IOi7Ubx5O4HLEJUFKlqSXLOfAGnZrk1bwvhtC2uFcMT6dG8PFvS4zaWeMKVMQM0mFKKnAoEX_y9vXXyBAtj3tl7NqUqyYgK-Mtv-7-vaNnEC6wFNEzchkpAHU6M0KZ__RGcuuAWY9cSBClFiZmcc4CmHeO9GJJCjxau-gzPa9nEG7bvUkEFUGk4evu-ELPG4a9Nmna7JMVQ3eSry3SZnm0Z_uyzV7nUtHcWoD0Bc-xyuF5mt8NFm37PaHyaDLaypiwJ_HfoaWSNCucwuZfXTtZ76w_TvBToqOj9qo40zfOtOeYeQ'},
            json={"title": "avengers vs godzilla", "releaseDate": "2021-03-25 11:55:11.271041"}
        )

        data = res.get_json()
        selection = Movie.query.filter(Movie.id == 222).one_or_none()

        self.assertEqual(data['status'], True)
        self.assertEqual(selection.title, 'avengers vs godzilla')

        selection.delete()

    def test_delete_movie(self):
        movie = Movie(
            title='The cube',
            releaseDate=datetime.datetime(2022, 2, 22),
            actor_id='1'
        )
        movie.id = 222
        movie.insert()

        res = self.client().delete('/movies/222', headers={
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9USXpNakl6UkVZMFJEQXdNRGN3UTBFNVF6TTBNekE0TURNMVF6bERRVGRFUVRNeE1VUXpNdyJ9.eyJpc3MiOiJodHRwczovL29maW5lby5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU3YzY4Y2ExMWRkNDkwYzZiM2VlNTM0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODUyMTE3ODksImV4cCI6MTU4NTI5ODE4OSwiYXpwIjoiMzVNNTJYbEgxM1R6NDl6T3gzQXBkUTdrNmY3Y1Fnb2wiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.s2ZdhS_O7cTCaD92vHdz_nnCI02VG4w4lWy_C5IOi7Ubx5O4HLEJUFKlqSXLOfAGnZrk1bwvhtC2uFcMT6dG8PFvS4zaWeMKVMQM0mFKKnAoEX_y9vXXyBAtj3tl7NqUqyYgK-Mtv-7-vaNnEC6wFNEzchkpAHU6M0KZ__RGcuuAWY9cSBClFiZmcc4CmHeO9GJJCjxau-gzPa9nEG7bvUkEFUGk4evu-ELPG4a9Nmna7JMVQ3eSry3SZnm0Z_uyzV7nUtHcWoD0Bc-xyuF5mt8NFm37PaHyaDLaypiwJ_HfoaWSNCucwuZfXTtZ76w_TvBToqOj9qo40zfOtOeYeQ'},
        )

        data = res.get_json()
        selection = Movie.query.filter(Movie.id == 222).one_or_none()

        self.assertEqual(data['status'], True)
        self.assertEqual(selection, None)

# Make the tests conveniently executable


if __name__ == "__main__":
    unittest.main()
