from django.core.management.base import BaseCommand, CommandError
from cocktail.tasks import process_youtube_videos

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        process_youtube_videos()
        self.stdout.write(self.style.SUCCESS('Updated Videos'))