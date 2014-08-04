from nsextreme.video import effects
from nsextreme.tests.util import movie_path, snapshot
from unittest2 import TestCase


class TestVideoFiles(TestCase):
    @snapshot
    def test_split_video(self):
        """
        Test that a video file can be split and that length of the split file
        is correct.
        """
        new_filename = effects.split_video(
            movie_path('testdata'), "00:00:04", "00:00:04")
        self.failUnless(
            effects.video_length(new_filename).startswith("00:00:04"))
        return new_filename

    @snapshot
    def test_split_video_no_duration(self):
        new_filename = effects.split_video(
            movie_path('testdata'), "00:00:04")
        self.failUnlessEqual(effects.video_length(new_filename), "00:00:11.14")
        return new_filename

    @snapshot
    def test_apply_effect(self):
        # basically a NOP, slight timing change due to ffmpeg
        new_filename = effects.apply_effect(
            movie_path('testdata'), "00:00:00", "00:00:05")
        return new_filename

    @snapshot
    def test_slow_motion(self):
        new_filename = effects.slow_motion(movie_path('testdata'))
        return new_filename

    @snapshot
    def test_apply_slomo_effect(self):
        new_filename = effects.apply_effect(
            effects.flip_180(movie_path('flipped')),
            "00:00:05", "00:00:04", effect=effects.slow_motion)
        return new_filename

    @snapshot
    def test_flip_180(self):
        filename = movie_path('flipped')
        new_filename = effects.flip_180(filename)
        # after being flipped the rotation data should be reset!
        self.failIfEqual(effects.get_rotation(new_filename), '180')
        return new_filename

    def test_video_length(self):
        self.failUnlessEqual(effects.video_length(movie_path('testdata')),
                             "00:00:14.78")

    def test_get_rotation(self):
        filename = movie_path('flipped')
        self.failUnlessEqual(effects.get_rotation(filename), '180')
