from django.core.management.base import BaseCommand, CommandError


from nsextreme.video import models, process

class Command(BaseCommand):
    args = ''
    help = 'Processes the uploaded videos.'

    def handle(self, *args, **options):
        videos = models.Video.objects.all()
        for video in videos:
            process.process_upload(video)

            