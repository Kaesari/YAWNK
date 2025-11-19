
import json
import requests
from django.db.models import Sum
from contests.models import Player, Team

FPL_API_BASE_URL = "https://fantasy.premierleague.com/api"

def get_current_game_week():
    """Fetch the current or next game week details from the FPL API."""
    try:
        response = requests.get(f"{FPL_API_BASE_URL}/bootstrap-static/")
        if response.status_code == 200:
            data = response.json()
            current_game_week = None
            next_game_week = None

            for event in data.get("events", []):
                if event["is_current"]:
                    current_game_week = event
                elif event["is_next"]:
                    next_game_week = event

            return next_game_week if next_game_week else current_game_week
        
        else:
            print(f"FPL API error: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error fetching current game week details: {e}")
        return None

def get_player_points(player_id, game_week):
    """Fetch a player's points for a specific game week."""
    try:
        response = requests.get(f"{FPL_API_BASE_URL}/element-summary/{player_id}/")
        if response.status_code == 200:
            data = response.json()
            for event in data.get("history", []):
                if event["round"] == game_week:
                    return event.get("total_points", 0)
            return 0
        else:
            print(f"FPL API error: {response.status_code}")
            return 0
    except Exception as e:
        print(f"Error fetching player points: {e}")
        return 0

def player_played_in_gameweek(player_id, game_week):
    """Check if a player participated in a specific gameweek (played at least 1 minute)."""
    try:
        response = requests.get(f"{FPL_API_BASE_URL}/element-summary/{player_id}/")
        if response.status_code == 200:
            data = response.json()
            for event in data.get("history", []):
                if event["round"] == game_week and event.get("minutes", 0) > 0:
                    return True
        return False
    except Exception as e:
        print(f"Error checking if player played: {e}")
        return False

def update_player_scores(game_week=None):
    """Update all player scores for the given game week. Defaults to the current game week."""
    if game_week is None:
        game_week = get_current_game_week()

    gameweek_id = game_week.get("id") if isinstance(game_week, dict) else game_week
    # print(f"Updating player scores for game week: {gameweek_id}")
    players = Player.objects.filter(gameweek=gameweek_id - 1)
    # players = Player.objects.filter(gameweek=gameweek_id)

    for player in players:
        try:
            coordinates = json.loads(player.position_coordinates) if player.position_coordinates else {}
        except json.JSONDecodeError:
            coordinates = {}

        # # Skip player if position_coordinates are empty
        # if coordinates.get("top") == "" or coordinates.get("left") == "":
        #     continue

        # Skip bench players (those with top == "100%")
        if coordinates.get("top") == "100%":
            continue

        points = get_player_points(player.player_id, gameweek_id - 1)
        # points = get_player_points(player.player_id, gameweek_id)

        for team in player.teams.all():
            player_score = points  # Default score

            if team.captain == player:
                if player_played_in_gameweek(player.player_id, gameweek_id - 1):
                # if player_played_in_gameweek(player.player_id, gameweek_id):
                    player_score = points * 2
                else:
                    player_score = 0

            elif team.vice_captain == player:
                # Vice-captain gets double points if captain didn't play, else 1.5x points
                if not player_played_in_gameweek(team.captain.player_id, gameweek_id - 1):
                # if not player_played_in_gameweek(team.captain.player_id, gameweek_id):
                    player_score = points * 2
                elif player_played_in_gameweek(player.player_id, gameweek_id - 1):
                # elif player_played_in_gameweek(player.player_id, gameweek_id):
                    player_score = points * 1.5
                else:
                    player_score = 0

            # Update the player's score
            player.score = player_score
            player.save()

    update_team_scores()

def update_team_scores():
    """Update the total score for all teams."""
    teams = Team.objects.all()

    for team in teams:
        total_score = team.players.aggregate(total_score=Sum('score'))['total_score']
        team.score = total_score if total_score is not None else 0
        team.save()
