import logging
import nsextreme.signals

logger = logging.getLogger(__name__)

bad_videos = []

# THIS FUNCTION BELOW IS BAD!!!!!!!!
# This function should be converted to a manage.py command running on crontab that checks all the videos for having valid thunbnails 
def thumbnail_scanner():
    """
    Based on thumbnail status scan all videos and post.

    Keeps track of videos that cause exceptions and doesn't process them
    again until the application is restarted.  This saves precious cycles and
    allows us to have errors reported after upload.
    """
    global bad_videos
    from nsextreme.video.models import Video  # avoid circlular import
    for video in Video.objects.filter(thumbnail=''):
        video_path = video.video.path
        try:
            if video_path not in bad_videos:
                video.post_process()
        except:
            logger.exception(
                "Error occured while processing video #%s: %s",
                str(video.id), video.video.path
            )
            bad_videos.append(video_path)



