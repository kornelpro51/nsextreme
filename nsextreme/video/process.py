import json
import logging
import os
import subprocess


from django.conf import settings
from django.core.files import File
from django.core.mail import send_mail


from nsextreme.utils import get_request, generate_tempfilename
from nsextreme.video import effects


logger = logging.getLogger(__name__)

def process_upload(video):
    """Process a video after upload"""

    # Rotate video if needed
    check_rotation(video)

    # Process video
    # TODO: catch errors/cron script check for correctly processed video
    generate_thumbnail(video)
    apply_slomo_effect(video)
    generate_faststart(video)
    notify_processing(video)

    # ensure correct file permissions, appears required for Apache mod_wsgi
    os.chmod(video.video.path, 0644)


def stretch_timestamps(data, factor, start, end):
    """
    Apply a stretch transformation to data by factor
    eg. 1 second becomes 3 if factor is 3
    NOTE: mutates data!

    We modify the time of each frame and store the original time.
    """
    previous_frame = dict(time=0, original_time=0)
    for frame in data['frames']:
        frame['original_time'] = frame['time']
        elapsed = frame['time'] - previous_frame['original_time']
        if frame['time'] >= start and frame['time'] < end:
            elapsed = elapsed * factor
        frame['time'] = elapsed + previous_frame['time']
        previous_frame = frame
    return data


def check_rotation(video):
    rotation = effects.get_rotation(video.video.path)
    if rotation == "180":
        apply_effect(video, effect=effects.flip_180)



def generate_faststart(video):
    script = os.path.join(settings.SITE_ROOT, 'bin/qtfaststart')
    command = '%(script)s %(video)s'
    cmdargs = {'script': script, 'video': os.path.join(settings.MEDIA_ROOT,
                                     video.video.name)}
    try:
        response = subprocess.call(command % cmdargs, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    except:
        response = -1

    if response != 0:
        logger.error("couldn't faststart video: %s", command % cmdargs)
        return False

    return True


def apply_slomo_effect(video):
    # parse slomo data looking for start and end
    # convert start and end to start and duration
    data = json.loads(video.data)
    slomo_info = data.get('slow-motion-bracket')
    if slomo_info:
        start = float(slomo_info['startTime'])
        length = float(slomo_info['endTime'] - start)
        apply_effect(video, effects.Vtime(start), effects.Vtime(length),
                          effects.slow_motion)
        data = json.loads(video.data)
        data = stretch_timestamps(
            data, effects.SLOMO_FACTOR, slomo_info['startTime'],
            slomo_info['endTime'])
        video.data = json.dumps(data)
        video.save()


def generate_thumbnail(video):
    if video.thumbnail:
        return
    video_filename = os.path.join(settings.MEDIA_ROOT, video.video.name)
    # adjust start time to generate thumbnails for smaller videos
    video_length = effects.video_length(video_filename)
    if effects.Vtime(video_length).total_seconds < 5:
        start_at = 0
    else:
        start_at = 4
    command = 'ffmpeg -itsoffset -%(start_at)d -i %(video)s' + \
              ' -vframes 1 -s 192x108 %(dest)s'
    thumbnail_filename = generate_tempfilename(suffix='.jpg')
    try:
        cmdargs = {'video': video_filename,
                   'dest': thumbnail_filename,
                   'start_at': start_at}
        response = subprocess.call(
            command % cmdargs, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Fail silently if ffmpeg is not installed.
        # the ffmpeg commandline tool that is.
        if response != 0:
            logger.error(
                "couldn't generate thumbnail - ffmpeg failed: %s",
                command % cmdargs)
            return

        if not os.path.exists(thumbnail_filename):
            logger.error(
                "couldn't generate thumbnail - no file " +
                "generated: %s", command % cmdargs)
            return

        video.thumbnail.save(
            os.path.basename(thumbnail_filename),
            File(file(thumbnail_filename)))
    finally:
        os.remove(thumbnail_filename)
    return True

def apply_effect(self, start=None, length=None, effect=None):
    if effect is None:
        raise
    original_filename = os.path.join(settings.MEDIA_ROOT, self.video.name)
    if start is None and length is None:
        new_filename = effect(original_filename)
    else:
        new_filename = effects.apply_effect(
            original_filename, start, length, effect)

    self.video.save(os.path.basename(new_filename),
                    File(file(new_filename)))
    os.unlink(new_filename)

def notify_processing(video):
    request = get_request()
    if request:
        if video.user.email:
            # send email
            url = video.get_absolute_url()
            video_url = request.build_absolute_uri(url)
            send_mail(
                'Your video is ready!',
                "Please see your video at: %s\n\n"
                "Thank you for using the NSExtreme App and website. "
                "We are very interested in what you think of your App "
                "and website experience. Please send feedback to: "
                "info@nsextreme.com\n\nThank you,\n\n"
                "The NSExtreme Team" % video_url,
                'noreply@nsextreme.com', (video.user.email,)
            )
        else:
            logging.info("no email for user %s", video.user.username)
    else:
        logging.error("notify_processing: no request")