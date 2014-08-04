from django import template

register = template.Library()

@register.filter
def chk_favorite_video(video, user):
    return video.profile_set.filter(user=user).exists()

@register.simple_tag
def is_favorite_video(user, video):
    return video.profile_set.filter(user=user).exists()

@register.simple_tag
def video_vote_status(user, video):
    return video.profile_set.filter(user=user).exists()