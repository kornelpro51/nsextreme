from django.contrib import admin
from nsextreme.video.models import Video, VideoCategory, VideoComment

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date_created')
    readonly_fields = ("date_created",)

"""
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "title",)
    readonly_fields = ("user",)
"""

admin.site.register(Video, VideoAdmin)
#admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(VideoCategory)
admin.site.register(VideoComment)

