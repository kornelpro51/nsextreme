import subprocess
import re
import math
import os
import logging
import json
logger = logging.getLogger(__name__)


from django.conf import settings


from nsextreme.utils import generate_tempfilename

FFMPEG_PATH = settings.FFMPEG_PATH

class Vtime(object):
    """
    Time class used to represent seconds in a way ffmpeg understands
    """
    def __init__(self, timespec):
        if (type(timespec) in (type(1), type(1.1))):
            self.total_seconds = timespec
        elif (type(timespec) is Vtime):
            self.total_seconds = timespec.total_seconds
        else:
            hours, minutes, seconds = timespec.split(":")
            self.total_seconds = float(seconds) + (int(minutes) * 60) + (int(hours) * 3600)

    def __add__(self, other):
        total_seconds = self.total_seconds + other.total_seconds
        return Vtime(total_seconds)

    def __sub__(self, other):
        total_seconds = self.total_seconds - other.total_seconds
        return Vtime(total_seconds)

    def __eq__(self, other):
        return self.total_seconds == other.total_seconds

    def __str__(self):
        total_seconds = self.total_seconds
        hours = math.floor(total_seconds / 3600)
        total_seconds -= (hours * 3600)
        minutes = math.floor(total_seconds / 60)
        seconds = total_seconds - (minutes * 60)
        return "%02d:%02d:%02.06f" % (hours, minutes, seconds)

    def __repr__(self):
        return "< Vtime(\"%s\")" % str(self)


def apply_effect(original_filename, start_time, length, effect=None):
    start_time = Vtime(start_time)
    after_time = start_time + Vtime(length)
    actual_duration = after_time - start_time
    logger.debug("apply_effect(%s, %s, %s, %s)" % (original_filename, start_time, actual_duration, repr(effect)))
    before_filename = slo_raw_filename = after_filename = slo_output = None
    try:
        before_filename = split_video(original_filename, "00:00:00", start_time.total_seconds)
        slo_raw_filename = split_video(original_filename, start_time, actual_duration.total_seconds)
        # assert int(Vtime(video_length(slo_raw_filename)).total_seconds) == int(actual_duration.total_seconds)
        after_filename = split_video(original_filename, after_time)
        # apply slomo effect to slo_filename
        if effect is None:
            effect = lambda filename: filename
        slo_output = effect(slo_raw_filename)
        if start_time.total_seconds >= 1:
            new_filename = join_video_files(before_filename, slo_output, after_filename)
        else:
            new_filename = join_video_files(slo_output, after_filename)

        assert os.path.exists(new_filename)

        return new_filename
    finally:
        for filename in (before_filename, slo_raw_filename, after_filename, slo_output):
            if filename and os.path.exists(filename):
                logger.debug("removing %s" % filename)
                os.remove(filename)


def split_video(input_filename, start, duration=None):
    logger.debug("split_video(%s, %s, %s)" % (input_filename, start, duration))
    output_filename = generate_tempfilename('.mov')
    if duration is None:
        cmdline = FFMPEG_PATH + " >/dev/null 2>&1  -i %(input_filename)s -ss %(start)s -sameq %(output_filename)s" % locals()
    else:
        cmdline = FFMPEG_PATH + " >/dev/null 2>&1  -i %(input_filename)s -ss %(start)s -t %(duration)s -sameq %(output_filename)s" % locals()
    logger.debug(cmdline)
    try:
        subprocess.check_output(cmdline, shell=True, stderr=subprocess.PIPE)
    except:
        return False
    return output_filename


def join_video_files(*files):
    logger.debug("join_video_files(%s)" % repr(files))
    output_filename = generate_tempfilename('.mov')
    swallow_output = ['>/dev/null 2>&1']
    cmdline = ['umask 022 &&', os.path.join(os.path.dirname(__file__), 'bin', 'mmcat')] + swallow_output + list(files)
    cmdline.append(output_filename)
    try:
        subprocess.check_output(' '.join(cmdline), shell=True)
    except:
        return False
    return output_filename


def slow_motion(input_filename):
    output_filename = generate_tempfilename('.mov')
    length = Vtime(Vtime(video_length(input_filename)).total_seconds * SLOMO_FACTOR)
    video_index = video_stream_index(input_filename)
    # note, we specify output length with -t since /dev/zero is infinite in length
    cmdline = FFMPEG_PATH + " >/dev/null 2>&1 -i %(input_filename)s -ar 44100 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -acodec aac -ab 128k -strict -2 -vcodec libx264 -vf 'setpts=%(slomo_factor)i*PTS' -map 0:%(video_index)s -map 1:0 -t %(length)s %(output_filename)s"
    cmdline = cmdline % {
        'input_filename': input_filename, 'slomo_factor': SLOMO_FACTOR,
        'output_filename': output_filename, 'video_index': video_index,
        'length': length
    }
    try:
        subprocess.check_output(cmdline, shell=True)
    except:
        return False
    return output_filename
SLOMO_FACTOR = 4


def video_length(filename):
    cmdline = FFMPEG_PATH + " -i %(filename)s" % locals()
    output = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[1]
    match = duration_re.search(output)
    if not match:
        raise Exception("couldn't parse video length: " + output)
    return match.group(1)
duration_re = re.compile("Duration: (.*?),", )


def video_metadata(filename):
    cmdline = FFMPEG_PATH + " -i %(filename)s" % locals()
    try:
        output = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[1]
    except:
        return False
    matches = metadata_re.findall(output)
    if not matches:
        raise Exception("couldn't parse metadata")
    metadata = {}
    for k, v in matches:
        metadata[k] = v
    return metadata
metadata_re = re.compile(' {6}(\w+)\s*:\s*(\w+)')


def video_stream_index(filename):
    cmdline = "ffprobe -print_format json -show_streams -v quiet -i %(filename)s" % locals()
    try:
        output = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0]
    except:
        return False
    data = json.loads(output)
    for stream in data['streams']:
        if stream['codec_type'] == 'video':
            return stream['index']


def _ffmpeg(input_filename, args):
    output_filename = generate_tempfilename('.mov')
    cmdline = FFMPEG_PATH + " >/dev/null 2>&1 -i %(input_filename)s -map_metadata -1 %(args)s -vcodec libx264 %(output_filename)s" % locals()
    try: 
        subprocess.check_output(cmdline, shell=True)
    except:
        return False
    return output_filename


def flip_180(filename):
    logger.debug("flip_180(%s)" % filename)
    new_filename = _ffmpeg(filename, "-vf vflip,hflip -sameq")
    # set_rotation(new_filename, "0")
    return new_filename


def get_rotation(filename):
    metadata = video_metadata(filename)
    return metadata.get('rotate')
