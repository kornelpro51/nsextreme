import os
import json
from PIL import Image
from django.contrib.auth.models import User
from django.core import mail
from django.core.files import File
from django.test import TestCase
from mock_django import http
from qtfaststart.exceptions import FastStartException
import qtfaststart.processor

from nsextreme.effects import split_video, Vtime
from nsextreme.tests.util import movie_path, json_data_path
from nsextreme.video.models import Video
import unittest2


class TestThumbs(TestCase, unittest2.TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='!')
        self.user1.set_password('password')
        self.user1.save()

    def tearDown(self):
        self.user1.delete()

    def test_thumbnail_generate(self):
        # create a video object manually
        video_file = File(file(movie_path('testdata')))
        json_data = file(json_data_path).read()
        video = Video.objects.create(title="Test", user=self.user1,
                                     video=video_file,
                                     data=json_data)
        video.save()

        assert not video.thumbnail

        # trigger thumbnail generation
        video.generate_thumbnail()

        # check the resulting thumbnail
        assert video.thumbnail

        image = Image.open(video.thumbnail)

        self.failUnlessEqual(image.size, (192, 108,))

    def test_thumbnail_scanner(self):
        # add a video with no thumbnail
        video_file = File(file(movie_path('testdata')))
        json_data = file(json_data_path).read()
        video = Video.objects.create(
            title="Test", user=self.user1, video=video_file,
            data=json_data)
        video.save()

        # run scanner
        from nsextreme import thumbnail_scanner
        thumbnail_scanner()

        # check to see if thumbnail was generated
        video = Video.objects.get(pk=video.pk)
        assert video.thumbnail

        # check qtfaststart was applied
        with self.assertRaises(FastStartException):
            qtfaststart.processor.process(video.video.path, '/dev/null')

    def test_small_videos(self):
        """
        Test that small videos (4 seconds and less) are processed properly
        """
        # create 4 second video
        new_filename = split_video(movie_path('testdata'), "00:00:04", "00:00:03.5")
        json_data = '{}'
        try:
            video = Video.objects.create(
                title="test", user=self.user1,
                video=File(file(new_filename)), data=json_data)
            video.save()
            video.post_process()
        finally:
            os.remove(new_filename)


class TestVtime(TestCase):
        def test_vtime_add(self):
            a = Vtime("01:01:01.25")
            b = Vtime("01:01:01.75")
            result = a + b
            self.failUnlessEqual(str(result), "02:02:3.000000")

        def test_vtime_float(self):
            t1 = Vtime(100)
            self.failUnlessEqual(str(t1), "00:01:40.000000")


class TestModel(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='!')
        self.user1.set_password('password')
        self.user1.email = "test@foo.com"
        self.user1.save()

    def tearDown(self):
        self.user1.delete()

    def test_email_on_notify(self):
        # request is implictly used by the notification method
        request = http.MockHttpRequest()
        request  # get PEP8 to ignore the unused variable
        video_file = File(file(movie_path('testdata')))
        json_data = file(json_data_path).read()
        assert self.user1.email
        video = Video.objects.create(title="Test", user=self.user1, video=video_file, data=json_data)
        video.notify_processing()
        self.failUnlessEqual(len(mail.outbox), 1)

    def test_apply_slomo_effect(self):
        video_file = File(file(movie_path('testdata')))
        json_data = file(json_data_path).read()
        video = Video.objects.create(title="Test", user=self.user1, video=video_file, data=json_data)
        video.apply_slomo_effect()

        # test that timestamps got stretched too
        video = Video.objects.get(pk=video.pk)
        data = json.loads(video.data)
        timestamps = [round(f['time'], 1) for f in data['frames']][38:54]
        expected_timestamps = [5.9,
            6.7,
            7.1,
            7.5,
            7.9,
            8.3,
            8.7,
            9.5,
            10.3,
            11.1,
            11.1,
            11.9,
            12.3,
            12.7,
            13.1,
            13.4]
        self.failUnlessEqual(expected_timestamps, timestamps)

    def test_data_stretching(self):
        from nsextreme import stretch_timestamps
        # make some other data
        times = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        frames = []
        for time in times:
            frames.append({"time": time})
        data = {"frames": frames}
        data = stretch_timestamps(data, factor=3, start=4, end=7)
        timestamps = [round(f['time'], 1) for f in data['frames']]
        self.failUnlessEqual(timestamps, [1.0, 2.0, 3.0, 6.0, 9.0, 12.0, 13.0, 14.0, 15.0, 16.0])

    def test_delete_video_file(self):
        """
        Test that the underlying video file is removed with the models
        """
        video_file = File(file(movie_path('testdata')))
        json_data = file(json_data_path).read()
        video = Video.objects.create(title="Test", user=self.user1, video=video_file, data=json_data)
        video.generate_thumbnail()

        video_path = video.video.path
        thumbnail_path = video.thumbnail.path

        assert os.path.exists(video_path)
        assert os.path.exists(thumbnail_path)

        video.delete()

        assert not os.path.exists(video_path)
        assert not os.path.exists(thumbnail_path)
