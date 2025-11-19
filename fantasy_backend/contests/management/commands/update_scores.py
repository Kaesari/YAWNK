
from django.core.management.base import BaseCommand
from contests.utils import update_player_scores, get_current_game_week

class Command(BaseCommand):
    help = "Update player and team scores from FPL API"

    def handle(self, *args, **options):
        game_week = get_current_game_week()  # ✅ Fetch the current game week
        update_player_scores(game_week)  # ✅ Pass the game week as an argument

        self.stdout.write(self.style.SUCCESS("Successfully updated player scores"))


        