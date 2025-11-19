from celery import shared_task
from .utils import update_player_scores, get_current_game_week

@shared_task
def update_player_scores_task():
    """Celery task to update player scores for the current game week."""
    try:
        current_game_week = get_current_game_week()
        if current_game_week:
            update_player_scores(current_game_week)
        else:
            print("Failed to fetch the current game week.")
    except Exception as e:
        print(f"Error in update_player_scores_task: {e}")