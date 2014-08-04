from django.test.client import Client
from django.test import TestCase
from django.contrib.auth.models import User
from nsextreme.tests.util import movie_path, json_data_path
from nsextreme.video.models import Video


class TestApi(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='!')
        self.user1.set_password('password')
        self.user1.save()

    def tearDown(self):
        self.user1.delete()

    def test_get(self):
        c = Client()
        response = c.get('/api/v1/upload_video')
        # 400 == BAD REQUEST
        assert response.status_code == 400

    def test_upload_no_arguments(self):
        c = Client()
        response = c.post('/api/v1/upload_video')
        # 400 == BAD REQUEST
        assert response.status_code == 400

    def test_upload_success(self):
        assert len(Video.objects.filter(user=self.user1)) == 0
        c = Client()
        response = c.post('/api/v1/upload_video',
                          {"username": "user1", "password": "password",
                          "title": "Dummy",
                          "video": file(movie_path('testdata'), 'rb'),
                          "data": file(json_data_path)})
        assert response.status_code == 200  # Success
        assert len(Video.objects.filter(user=self.user1)) == 1

    # TODO: find a better place to put the test files -- maybe under tests/data
    def test_upload_user_invalid(self):
        c = Client()
        response = c.post('/api/v1/upload_video',
                          {"username": "user1", "password": "BAD",
                          "title": "Dummy",
                          "video": file(movie_path('testdata'), 'rb'),
                          "data": file(json_data_path)})
        assert response.status_code == 403  # Unauthorized
