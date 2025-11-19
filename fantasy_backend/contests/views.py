import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import CaptainViceCaptainHistory, Contest, Player, Team
from .serializers import ContestSerializer, PlayerSerializer, TeamSerializer
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
# views.py
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .mpesa import initiate_mpesa_stk_push

from django.utils.dateparse import parse_datetime
import json
from .models import Player
import random
import string

import requests
from django.shortcuts import render
from django.core.cache import cache
import pytz
from django.core.paginator import Paginator
from itertools import count, groupby
from operator import itemgetter
from datetime import datetime, timedelta, timezone
from django.utils.timezone import localtime

import matplotlib.pyplot as plt
import seaborn as sns
import io
import urllib, base64
from .models import Contest, Team
from collections import Counter,defaultdict
import pandas as pd
from django.db import models
from django.db.models import Q, Sum
from decimal import Decimal  # Import Decimal




# ------------------------------------------------------------------------------------------------Football API------------
API_KEY = "bdafa7c557334c2a8cf88c509fb414b6"  # Replace with your Football-Data.org API key
BASE_URL = "https://api.football-data.org/v4"

# Predefined goalkeeper shirt images
GOALKEEPER_SHIRTS = [
    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_31_1-110.webp",
    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_17_1-66.webp",
    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_11_1-66.webp",
    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_3_1-66.webp",
    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_31_1-110.webp",
    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_1_1-66.webp",
    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_8_1-66.webp",
    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_7_1-66.webp",
    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_36_1-66.webp",
    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_40_1-66.webp",
    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_4_1-66.webp"
]

TEAM_SHIRTS = {
    "Arsenal": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_3-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_3_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t3.png"
    },
    "Aston Villa": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_7-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_7_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t7.png"
    },
    "Bournemouth": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_91-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_91_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t91.png"
    },
    "Brentford": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_94-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_94_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t94.png"
    },
    "Brighton": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_36-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_36_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t36.png"
    },
    "Chelsea": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_8-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_8_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t8.png"
    },
    "Crystal Palace": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_31-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_31_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t31.png"
    },
    "Everton": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_11-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_11_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t11.png"
    },
    "Fulham": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_54-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_54_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t54.png"
    },
    "Ipswich": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_40-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_40_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t40.png"
    },
    "Leicester": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_13-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_13_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t13.png"
    },
    "Liverpool": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_14-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_14_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t14.png"
    },
    "Man City": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_43-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_43_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t43.png"
    },
    "Man Utd": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_1-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_1_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t1.png"
    },
    "Newcastle": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_4-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_4_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t4.png"
    },
    "Nott'm Forest": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_17-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_17_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t17.png"
    },
    "Southampton": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_20-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_20_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t20.png"
    },
    "Spurs": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_6-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_6_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t6.png"
    },
    "West Ham": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_21-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_21_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t21.png"
    },
    "Wolves": {
        "outfield": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_39-110.webp",
        "goalkeeper": "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_39_1-110.webp",
        "logo": "https://resources.premierleague.com/premierleague/badges/70/t39.png"
    }
}


def get_current_game_week_data():
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
                elif event["is_next"]:  # If "is_current" is False, check "is_next"
                    next_game_week = event

            # If the API still shows an old gameweek as current, return the next gameweek instead
            return next_game_week if next_game_week else current_game_week
        
        else:
            print(f"FPL API error: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error fetching current game week details: {e}")
        return None

def get_specific_game_week_data(game_week):
    """Fetch details for a specific game week from the FPL API.
    
    Args:
        game_week (int): The game week number you want to fetch
        
    Returns:
        dict: The game week details or None if not found/error occurs
    """
    try:
        response = requests.get(f"{FPL_API_BASE_URL}/bootstrap-static/")
        if response.status_code == 200:
            data = response.json()
            
            for event in data.get("events", []):
                if event["id"] == game_week:
                    return event
            
            print(f"Game week {game_week} not found")
            return None
        
        else:
            print(f"FPL API error: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error fetching game week {game_week} details: {e}")
        return None


FPL_API_BASE_URL = "https://fantasy.premierleague.com/api"


def get_team_id_name_map():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    data = response.json()
    team_map = {}
    for team in data["teams"]:
        name = team["name"]
        logo = TEAM_SHIRTS.get(name, {}).get("logo", "")
        team_map[team["id"]] = {"name": name, "logo": logo}
    return team_map

def group_matches_by_day(gameweek):
    url = "https://fantasy.premierleague.com/api/fixtures/"
    response = requests.get(url)
    fixtures = response.json()
    team_map = get_team_id_name_map()
    grouped = defaultdict(list)

    has_started = False
    has_ended = True

    for fixture in fixtures:
        if fixture['event'] == gameweek:
            kickoff = fixture.get("kickoff_time")
            finished = fixture.get("finished_provisional", False)

            if kickoff:
                dt_utc = datetime.strptime(kickoff, '%Y-%m-%dT%H:%M:%SZ')
                dt_eat = dt_utc + timedelta(hours=3)
                date = dt_eat.strftime("%A, %d %B %Y")
                time = dt_eat.strftime("%H:%M")
                if datetime.utcnow() >= dt_utc:
                    has_started = True
            else:
                date, time = "TBD", "TBD"

            if not finished:
                has_ended = False

            grouped[date].append({
                "formatted_time": time,
                "home_team": team_map.get(fixture["team_h"], {"name": "Unknown", "logo": ""}),
                "away_team": team_map.get(fixture["team_a"], {"name": "Unknown", "logo": ""})
            })

    return [{"date": d, "matches": m} for d, m in grouped.items()], has_started, has_ended


def format_time(utc_date, offset_minutes=0):
    """Format UTC date into a human-readable local time with an optional offset."""
    # Convert UTC date string to datetime object
    utc_time = datetime.strptime(utc_date, "%Y-%m-%dT%H:%M:%SZ")

    # Convert to local timezone (e.g., Europe/London)
    local_timezone = pytz.timezone("Europe/London")  # Change to your desired timezone
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)

    # Apply offset for deadline (e.g., subtract minutes)
    if offset_minutes:
        local_time -= timedelta(minutes=offset_minutes)

    # Format into a readable string
    return local_time.strftime("%A, %d %B %Y %H:%M")

FPL_API_BASE_URL = "https://fantasy.premierleague.com/api"

def get_fpl_matches():
    """Fetch match fixtures from the FPL API with team logos, sorted from newest to oldest."""
    # Check if matches are cached
    cached_matches = cache.get("fpl_matches")
    if cached_matches:
        return cached_matches

    # Fetch fixtures and team data
    fixtures_url = f"{FPL_API_BASE_URL}/fixtures/"
    teams_url = f"{FPL_API_BASE_URL}/bootstrap-static/"
    
    try:
        fixtures_response = requests.get(fixtures_url)
        teams_response = requests.get(teams_url)

        if fixtures_response.status_code == 200 and teams_response.status_code == 200:
            fixtures = fixtures_response.json()  # List of matches
            teams_data = teams_response.json().get("teams", [])  # List of teams

            # Map team IDs to names and logos
            team_mapping = {
                team["id"]: {
                    "name": team["name"],
                    "short_name": team["short_name"],
                    "logo": f"https://resources.premierleague.com/premierleague/badges/t{team['id']}.png",
                }
                for team in teams_data
            }

            # Process fixtures
            processed_fixtures = []
            for fixture in fixtures:
                kickoff_time = fixture.get("kickoff_time")  # May be None

                # 🔹 Skip fixtures with missing kickoff_time
                if kickoff_time is None:
                    # print(f"⚠ Skipping fixture with missing kickoff_time (ID {fixture['id']})")
                    continue

                fixture["home_team"] = team_mapping.get(fixture["team_h"], {})
                fixture["away_team"] = team_mapping.get(fixture["team_a"], {})
                fixture["formatted_time"] = kickoff_time  # Optionally format time here
                
                processed_fixtures.append(fixture)

            # 🔹 Sort only valid fixtures by kickoff_time (newest to oldest)
            processed_fixtures = sorted(processed_fixtures, key=lambda x: x["kickoff_time"], reverse=True)

            # Cache the matches for 5 minutes
            cache.set("fpl_matches", processed_fixtures, timeout=300)
            return processed_fixtures
        else:
            print(f"API Error: Fixtures {fixtures_response.status_code}, Teams {teams_response.status_code}")
            return []
    
    except Exception as e:
        print(f"❌ Error fetching matches: {e}")
        return []


def get_teams(request):
    """Fetch all teams from the Fantasy Premier League API."""
    cached_teams = cache.get("fpl_teams")
    if cached_teams:
        return JsonResponse({"teams": cached_teams}, status=200)

    try:
        response = requests.get(f"{FPL_API_BASE_URL}/bootstrap-static/")
        if response.status_code == 200:
            data = response.json()
            teams = [
                {
                    "id": team["id"],
                    "name": team["name"],
                    "short_name": team["short_name"],
                }
                for team in data.get("teams", [])
            ]
            cache.set("fpl_teams", teams, timeout=3600)
            return JsonResponse({"teams": teams}, status=200)
        else:
            return JsonResponse({"error": f"FPL API error: {response.status_code}"}, status=response.status_code)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_players_by_team_api(request):
    """API to fetch all players with pagination."""
    try:
        # Fetch all players from `get_all_players()` and extract the JSON data
        players_response = get_all_players(request)  # Returns a JsonResponse
        players_data = json.loads(players_response.content.decode("utf-8"))  # Convert to Python dictionary
        players = players_data.get("players", [])  # Extract the players list

        # print(players)

        if not players:
            return JsonResponse({"error": "No players found."}, status=404)

        # Get query parameters for pagination
        page = int(request.GET.get("page", 1))  # Current page
        page_size = int(request.GET.get("page_size", 200))  # Players per page

        # Paginate the players
        paginator = Paginator(players, page_size)
        total_pages = paginator.num_pages

        # Handle invalid page numbers
        if page > total_pages or page < 1:
            return JsonResponse({"error": "Page number out of range."}, status=400)

        # Get the players for the current page
        paginated_players = paginator.get_page(page)

        # Prepare response data
        response_data = {
            "players": list(paginated_players),
            "total_players": paginator.count,
            "current_page": paginated_players.number,
            "total_pages": total_pages,
        }

        return JsonResponse(response_data, status=200)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return JsonResponse({"error": str(e)}, status=500)

def get_upcoming_fixtures():
    """Fetch upcoming fixtures for the next 7 days."""
    try:
        response = requests.get(f"{FPL_API_BASE_URL}/fixtures/")
        if response.status_code != 200:
            print(f"FPL API error: {response.status_code}")
            return []

        fixtures = response.json()
        now = datetime.now(timezone.utc)
        next_week = now + timedelta(days=7)

        upcoming_fixtures = []

        for fixture in fixtures:
            kickoff_time = fixture.get("kickoff_time")

            # 🔹 Skip fixtures with missing kickoff_time
            if not kickoff_time:
                # print(f"⚠ Skipping fixture with missing kickoff_time (ID {fixture['id']})")
                continue

            try:
                # Convert kickoff_time to a datetime object
                kickoff_datetime = datetime.strptime(kickoff_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

                # Ensure kickoff_datetime is valid before adding
                if now < kickoff_datetime <= next_week:
                    upcoming_fixtures.append(fixture)

            except (ValueError, TypeError) as e:
                print(f"❌ Error parsing kickoff_time '{kickoff_time}' for fixture ID {fixture['id']}: {e}")
                continue  # Skip invalid date entries

        return upcoming_fixtures

    except Exception as e:
        print(f"❌ Error fetching fixtures: {e}")
        return []

def get_teams_playing_in_upcoming_fixtures():
    """Get the teams that are playing in the upcoming fixtures."""
    upcoming_fixtures = get_upcoming_fixtures()
    teams_playing = set()
    for fixture in upcoming_fixtures:
        teams_playing.add(fixture["team_h"])
        teams_playing.add(fixture["team_a"])
    return teams_playing

def get_all_players(request):
    """Fetch all players and enrich them with fixtures, team names, and correct team shirts."""
    try:
        # Check if players are cached
        cached_all_players = cache.get("fpl_all_players")
        if cached_all_players:
            return JsonResponse({"players": cached_all_players}, status=200)

        # Fetch general player data
        players_response = requests.get(f"{FPL_API_BASE_URL}/bootstrap-static/")
        if players_response.status_code != 200:
            return JsonResponse({"error": "Failed to fetch players from FPL API."}, status=players_response.status_code)

        data = players_response.json()
        all_players = data.get("elements", [])
        teams = {team["id"]: {"name": team["name"], "short_name": team["short_name"]} for team in data["teams"]}

        # Fetch upcoming fixtures
        fixtures_data = get_upcoming_fixtures()

        # Create a fixture map for each team
        team_fixtures = {team_id: [] for team_id in teams.keys()}
        for fixture in fixtures_data:
            home_team_id = fixture["team_h"]
            away_team_id = fixture["team_a"]
            home_short = teams[home_team_id]["short_name"]
            away_short = teams[away_team_id]["short_name"]
            team_fixtures[home_team_id].append(f"{away_short} (H)")
            team_fixtures[away_team_id].append(f"{home_short} (A)")

        # Get teams playing in upcoming fixtures
        # teams_playing = get_teams_playing_in_upcoming_fixtures()

        
        # Process players into a simple format
        players = []
        for player in all_players:
            team_id = player["team"]

            team_name = teams[team_id]["name"]
            team_short_name = teams[team_id]["short_name"]
            fixture_list = team_fixtures.get(team_id, [])

            # Fetch correct shirts
            team_info = TEAM_SHIRTS.get(team_name, {})

            home_team_logo = team_info.get("logo", "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_54-110.webp") 

            # Assign correct team shirt
            if player["element_type"] == 1:  # Goalkeepers (Random selection)
                 team_shirt_url = team_info.get("goalkeeper", "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_14_1-66.webp")
            else:  # Outfield Players (Standard team shirt)
                team_shirt_url = team_info.get("outfield", "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_54-110.webp")

            # Find the next fixture
            next_opponent = "None"
            next_opponent_logo = team_info.get("logo", "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_54-110.webp")  # Default logo
            fixture_time = "TBD"

            # Shorten fixture list to max 3 fixtures
            formatted_fixtures = ", ".join(fixture_list[:1]) if fixture_list else "No upcoming fixture"


            for fixture in fixtures_data:
                if fixture["team_h"] == team_id:
                    opponent_team_id = fixture["team_a"]
                    fixture_time = fixture.get("kickoff_time", "TBD")
                elif fixture["team_a"] == team_id:
                    opponent_team_id = fixture["team_h"]
                    fixture_time = fixture.get("kickoff_time", "TBD")
                else:
                    continue  # Skip non-matching fixtures

                if opponent_team_id in teams:
                    next_opponent = teams[opponent_team_id]["short_name"]
                    # Fetch correct shirts
                    team_info = TEAM_SHIRTS.get(teams[opponent_team_id]["name"], {})
                    next_opponent_logo = team_info.get("logo", "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_54-110.webp") 
                break  # Stop after finding the first valid fixture

            # Append player data
            players.append({
                "id": player["id"],
                "name": player["web_name"],
                "position": ["Goalkeepers", "Defenders", "Midfielders", "Forwards"][player["element_type"] - 1]
                if 1 <= player["element_type"] <= 4 else "Unknown",
                "price": f"{player['now_cost'] / 10}",
                "form": player.get("form", "N/A"),
                "total_points": player["total_points"],
                "tsb": f"{player.get('selected_by_percent', '0')}%",
                "team": team_name,
                "team_short": team_short_name,
                "teamLogo": home_team_logo,
                "fixture":formatted_fixtures,
                # Fixture Details with Correct Opponent
                "fixture_data": {
                    "team1": team_short_name,  # Player's Team
                    "team1Logo": home_team_logo,
                    "team2": next_opponent,  # Correct Opponent Name
                    "team2Logo": next_opponent_logo,  # Correct Opponent Badge
                    "time": fixture_time if fixture_time != "TBD" else "TBD"
                },

                "image": f"https://resources.premierleague.com/premierleague/photos/players/110x140/p{player['code']}.png",
                "team_shirt": team_shirt_url
            })

        # Cache players for 1 hour
        cache.set("fpl_all_players", players, timeout=3600)

        return JsonResponse({"players": players}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_teams_api(request):
    """API to fetch all teams."""
    teams = get_teams()
    if teams:
        return JsonResponse({"teams": teams}, status=200)
    else:
        return JsonResponse({"error": "Failed to fetch teams."}, status=500)

def teams_view(request):
    """Render the teams page."""
    return render(request, "contests/teams.html")


#------------------------------------------------------------------------------------AUTH

def home(request):
    """Render the homepage with the top 10 real-time matches."""
    # matches = get_fpl_matches()
    # Get leagues based on their type
    public_leagues = Contest.objects.filter(league_type="Public")
    # private_leagues = Contest.objects.filter(league_type="Private", users=request.user)

    context = {
        "public_leagues": public_leagues,
        # "private_leagues": private_leagues,
        # "matches": matches
    }

    return render(request, 'contests/home.html', context)

@api_view(['GET'])
def contest_list(request):
    contests = Contest.objects.all()
    serializer = ContestSerializer(contests, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def player_list(request):
    players = Player.objects.all()
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_team(request):
    serializer = TeamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        gender = request.POST.get('gender')
        day = request.POST.get('day')
        month = request.POST.get('month')
        year = request.POST.get('year')
        country = request.POST.get('country')
        mobile = request.POST.get('mobile')

        if password1 != password2:
            messages.warning(request, "Passwords do not match!")
            return render(request, 'registration/register.html')

        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password1
            )
            user.save()
            profile = user.profile
            profile.gender = gender
            profile.day = day
            profile.month = month
            profile.year = year
            profile.country = country
            profile.phone_number = mobile
            profile.save()

            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
        except Exception as e:
            messages.warning(request, f"An error occurred: {str(e)}")
            return render(request, 'registration/register.html')

    return render(request, 'registration/register.html')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True  # Redirect already authenticated users

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirect authenticated users without adding the "Login Successful!" message
            messages.info(request, "You are already logged in.")
            return redirect(self.get_success_url())
        # Proceed for unauthenticated users
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Add "Login Successful!" message only after successful login
        messages.success(self.request, "Login Successful!")
        return super().form_valid(form)

    def get_success_url(self):
        # Define where to redirect the user after successful login
        return reverse_lazy('home')

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, "You have successfully logged out.")
        else:
            messages.warning(request, "You are already logged out.")
        return super().dispatch(request, *args, **kwargs)

#------------------------------------------------------------------------------------CONTEST
def contest_list(request):
    contests = Contest.objects.all()
    return render(request, 'contests/contest_list.html', {'contests': contests})

def contest_detail(request, contest_id):
    contest = Contest.objects.get(id=contest_id)
    return render(request, 'contests/contest_detail.html', {'contest': contest})

@login_required
def create_team(request, contest_id):
    contest = Contest.objects.get(id=contest_id)
    players = Player.objects.all()
    return render(request, 'contests/create_team.html', {'contest': contest, 'players': players})

def leaderboard(request, contest_id):
    contest = Contest.objects.get(id=contest_id)
    teams = Team.objects.filter(contest=contest).order_by('-score')
    return render(request, 'contests/leaderboard.html', {'contest': contest, 'teams': teams})

#------------------------------------------------------------------------------------Manage teams

@login_required
def league(request):
    
    # Fetch current game week data
    current_game_week = get_current_game_week_data()
    current_gameweek_id = current_game_week['id']

    # Get public leagues for the current gameweek
    public_leagues = Contest.objects.filter(
        league_type="Public",
        gameweek=current_gameweek_id
    )

    # Get private leagues for the current gameweek where the user is joined
    private_leagues = Contest.objects.filter(
        league_type="Private",
        users=request.user,
        gameweek=current_gameweek_id
    )


    # Get the user's team (assuming only one team per user for now)
    user_team = Team.objects.filter(user=request.user).first()

    # Check if the team has a captain and vice-captain
    show_captain_toast = False
    show_vicecaptain_toast = False

    if user_team:
        if not user_team.captain:
            show_captain_toast = True
        if not user_team.vice_captain:
            show_vicecaptain_toast = True

    # If either Captain or Vice-Captain is missing, redirect to manage_team page
    if show_captain_toast or show_vicecaptain_toast:
        if show_captain_toast:
            messages.warning(request, "Please select a Captain.")
        if show_vicecaptain_toast:
            messages.warning(request, "Please select a Vice Captain.")
        return redirect('manage_team')  # Redirect to the manage_team page

    context = {
        "public_leagues": public_leagues,
        "private_leagues": private_leagues,
        "current_game_week": current_game_week,
        "show_captain_toast": show_captain_toast,
        "show_vicecaptain_toast": show_vicecaptain_toast,
    }

    return render(request, "contests/league.html", context)

@login_required
def admin_view(request):
    # user = request.user  # Get the logged-in user

    # context = {
    #     "email": user.email,  # User's email
    #     "date_joined": user.date_joined.strftime("%d %B, %Y"),  # Format join date
    # }

    return render(request, "contests/admin/base.html")

def admin_dashboard_view(request):
    # Fetch Data
    total_leagues = Contest.objects.count()
    private_leagues = Contest.objects.filter(league_type="Private").count()
    public_leagues = Contest.objects.filter(league_type="Public").count()

    # Compute Revenue & Cost
    total_revenue = Contest.objects.aggregate(Sum('prize_pool'))['prize_pool__sum'] or 0
    total_cost = total_revenue * Decimal("0.1")  # Convert 0.1 to Decimal


    # Get Data for Revenue vs. Cost Graph
    contests = Contest.objects.all()
    contest_names = [contest.name for contest in contests]
    revenue = [contest.prize_pool for contest in contests]
    cost = [contest.prize_pool * Decimal("0.1") for contest in contests] 

    # Create a Bar Chart for Revenue vs Cost
    fig, ax = plt.subplots(figsize=(8, 5))
    bar_width = 0.4
    index = range(len(contest_names))

    ax.bar(index, revenue, bar_width, label="Revenue (Prize Pool)", color="blue")
    ax.bar([i + bar_width for i in index], cost, bar_width, label="Cost (10%)", color="red")

    ax.set_xlabel("Contests")
    ax.set_ylabel("Amount ($)")
    ax.set_title("Revenue vs. Cost Per Contest")
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(contest_names, rotation=30, ha="right")
    ax.legend()

    # Convert plot to a base64 string
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    chart_url = "data:image/png;base64," + string

    # Get the count of private and public leagues
    private_leagues_count = Contest.objects.filter(league_type="Private").count()
    public_leagues_count = Contest.objects.filter(league_type="Public").count()

    # Generate Pie Chart
    labels = ['Private Leagues', 'Public Leagues']
    sizes = [private_leagues_count, public_leagues_count]
    colors = ['#FF6384', '#36A2EB']

    fig, ax = plt.subplots()
    if sum(sizes) == 0:
        # Avoid plotting an empty pie chart
        ax.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center', fontsize=14)
        ax.axis('off')
    else:
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Convert plot to image in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the image to Base64 for embedding in the template
    chart1 = base64.b64encode(image_png).decode('utf-8')
    chart1_uri = f"data:image/png;base64,{chart1}"

    user = request.user  # Get the logged-in user

    # Send Data to Template
    context = {
        "total_leagues": total_leagues,
        "private_leagues": private_leagues,
        "public_leagues": public_leagues,
        "total_revenue": total_revenue,
        "total_cost": total_cost,
        "revenue_vs_cost_chart": chart_url,
        "chart1": chart1_uri,
        "username": user.first_name if user.first_name else user.username,
    }

    return render(request, "contests/admin/dashboard.html", context)

def admin_private_leagues(request):
    # Get leagues based on their type
    private_leagues = Contest.objects.filter(league_type="Private")

    # Fetch current game week data
    # current_game_week = get_current_game_week_data()

    context = {
        "private_leagues": private_leagues,
        # 'current_game_week': current_game_week,
    }
    return render(request, "contests/admin/privateleagues.html",context)

def admin_global_leagues(request):
    # Get leagues based on their type
    public_leagues = Contest.objects.filter(league_type="Public")
    
    # Fetch current game week data
    # current_game_week = get_current_game_week_data()

    context = {
        "public_leagues": public_leagues,
        # 'current_game_week': current_game_week,
    }
    return render(request, "contests/admin/globalleagues.html",context)

def generate_chart(fig):
    """Convert Matplotlib figure to a base64 image for embedding in HTML."""
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    string = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return f"data:image/png;base64,{string}"

def admin_reports_leagues(request):
    # Query contest data
    contests = Contest.objects.all()
    teams = Team.objects.all()

    # 1️⃣ **Doughnut Chart: Public vs Private Leagues**
    league_counts = contests.values("league_type").annotate(count(models.Count("id")))
    labels = [item["league_type"] for item in league_counts]
    values = [item["count"] for item in league_counts]
    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, wedgeprops={"edgecolor": "white"})
    ax1.set_title("Public vs Private Leagues")
    chart1 = generate_chart(fig1)

    # 2️⃣ **Bar Chart: Number of contests per sport**
    sport_counts = contests.values("sport").annotate(count(models.Count("id")))
    sports = [item["sport"] for item in sport_counts]
    sport_values = [item["count"] for item in sport_counts]
    fig2, ax2 = plt.subplots()
    sns.barplot(x=sports, y=sport_values, ax=ax2)
    ax2.set_title("Contests by Sport")
    chart2 = generate_chart(fig2)

    # 3️⃣ **Line Chart: Growth of Leagues Over Time**
    contests_df = pd.DataFrame(contests.values("created_at"))
    contests_df["created_at"] = pd.to_datetime(contests_df["created_at"])
    contests_df["month"] = contests_df["created_at"].dt.to_period("M")
    contests_per_month = contests_df.groupby("month").size()
    fig3, ax3 = plt.subplots()
    contests_per_month.plot(kind="line", marker="o", ax=ax3)
    ax3.set_title("Growth of Leagues Over Time")
    ax3.set_xlabel("Month")
    ax3.set_ylabel("Number of Contests")
    chart3 = generate_chart(fig3)

    # 4️⃣ **Bar Chart: Prize Pool Distribution**
    prize_pools = contests.values_list("prize_pool", flat=True)
    fig4, ax4 = plt.subplots()
    sns.histplot(prize_pools, bins=10, kde=True, ax=ax4)
    ax4.set_title("Prize Pool Distribution")
    ax4.set_xlabel("Prize Pool Amount")
    chart4 = generate_chart(fig4)

    # 5️⃣ **Pie Chart: Favorite Clubs in Teams**
    favorite_club_counts = teams.values("favorite_club").annotate(count=models.Count("id"))
    clubs = [item["favorite_club"] for item in favorite_club_counts]
    club_values = [item["count"] for item in favorite_club_counts]
    fig5, ax5 = plt.subplots()
    ax5.pie(club_values, labels=clubs, autopct="%1.1f%%", startangle=140)
    ax5.set_title("Distribution of Favorite Clubs")
    chart5 = generate_chart(fig5)

    # 6️⃣ **Histogram: Entry Fee Distribution**
    entry_fees = contests.values_list("entry_fee", flat=True)
    fig6, ax6 = plt.subplots()
    sns.histplot(entry_fees, bins=10, kde=True, ax=ax6)
    ax6.set_title("Entry Fee Distribution")
    ax6.set_xlabel("Entry Fee Amount")
    chart6 = generate_chart(fig6)

    # Send charts to the template
    context = {
        "chart1": chart1,
        "chart2": chart2,
        "chart3": chart3,
        "chart4": chart4,
        "chart5": chart5,
        "chart6": chart6,
    }
    return render(request, "contests/admin/reports.html", context)

def admin_user_profile(request):
    return render(request, "contests/admin/profile.html")

from django.utils.html import escape

# Your GOALKEEPER_SHIRTS and TEAM_SHIRTS dictionaries are already defined

def statistics(request):
    fpl_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(fpl_url)
    
    if response.status_code == 200:
        data = response.json()
        players = data['elements']  # Player data
        teams = {team['id']: team for team in data['teams']}  # Full team dict

        player_stats = []
        for player in players:
            team_id = player['team']
            team_name = teams[team_id]['name']  # Full team name, e.g., "Arsenal"

            # Get team shirt info
            shirt_info = TEAM_SHIRTS.get(team_name)

            if not shirt_info:
                # Fallback if team is not found (e.g., promoted teams without a mapping yet)
                team_jersey = "https://via.placeholder.com/80"  # Default jersey image
                team_logo = "https://via.placeholder.com/80"  # Default logo
            else:
                # Choose jersey based on position
                if player['element_type'] == 1:  # 1 = Goalkeeper
                    team_jersey = shirt_info['goalkeeper']
                else:
                    team_jersey = shirt_info['outfield']
                team_logo = shirt_info['logo']

            player_stats.append({
                'name': escape(player['web_name']),
                'team': escape(team_name),
                'team_short_name': escape(teams[team_id]['short_name']),
                'team_logo': team_logo,
                'team_jersey': team_jersey,
                'position': player['element_type'],  # 1: GK, 2: DEF, 3: MID, 4: FWD
                'price': f"Ksh {player['now_cost'] / 10:.1f}m",
                'selection_percentage': f"{player['selected_by_percent']}%",
                'form': player['form'],
                'total_points': player['total_points'],
            })

        # Sort players by total points (default)
        player_stats = sorted(player_stats, key=lambda x: x['total_points'], reverse=True)
    else:
        player_stats = []  # Fallback if API fails

    context = {
        'player_stats': player_stats,
    }
    return render(request, 'contests/statistics.html', context)


def manage_team(request, user_id=None, gameweek=None):
    # If user_id is provided in the URL, get that user; otherwise, use the logged-in user
    if user_id:
        user = get_object_or_404(User, id=user_id)
    else:
        user = request.user  # Default to logged-in user

    # Check if the user already has a team
    user_team = Team.objects.filter(user=user).first()
    # Check if the user already has a team

    # user_team = Team.objects.filter(user=request.user).first()
    matches = get_fpl_matches()
    # Fetch current game week data
    current_game_week = get_current_game_week_data()

    # If the user already has a team, redirect to the team selection page
    if user_team:
        if user_id:
            return redirect('team_selection_user', user_id=user.id)
        else:
            if gameweek:
                if gameweek==current_game_week['id']:
                    # If there's no user_id, redirect to the general team_selection page
                    return redirect('team_selection') 
                else:
                    return redirect('team_selection_gameweek', gameweek=gameweek)
            else:
                # If there's no user_id and gameweek, redirect to the general team_selection page
                return redirect('team_selection') 

    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        favorite_club = request.POST.get('favorite_club')  # Club name
        favorite_club_id = request.POST.get('favorite_club_id')  # Club ID from the hidden field
        terms_accepted = request.POST.get('terms')


        # Captain and Vice Captain IDs (as integers)
        captain_id = request.POST.get('captain')  # Captain ID
        vice_captain_id = request.POST.get('vice_captain')  # Vice Captain ID


        # Check if all fields are filled
        if not team_name or not favorite_club or not favorite_club_id or not terms_accepted:
            messages.warning(request, "All fields are required.")
            return render(request, 'contests/manageteam.html', {"matches": matches})

        # Save the team to the database
        team = Team.objects.create(
            user=request.user,
            name=team_name,
            favorite_club=f"{favorite_club} ({favorite_club_id})",  # Save the favorite club name and id together
            score=0
        )
        # Save the team object
        team.save()

        # Success message and redirect
        messages.success(request, "Team created successfully!")
        # return redirect('team_selection')  # Replace with your success URL
        return redirect('team_selection')

    return render(request, 'contests/manageteam.html', {"matches": matches})

def filter_fixtures_matches(matches):
    today = datetime.utcnow()
    next_week = today + timedelta(days=7)
    
    return [match for match in matches if today <= datetime.strptime(match["kickoff_time"], "%Y-%m-%dT%H:%M:%SZ") <= next_week]

def get_team_score_for_gameweek(user, gameweek):
    """
    Get the total score of all players in a user's team for a specific gameweek.
    """
    # Filter the players that belong to the user's team and the specified gameweek
    total_score = Player.objects.filter(user=user, gameweek=gameweek).aggregate(total_score=Sum('score'))['total_score']

    return total_score if total_score else 0

def get_user_team_position(user, gameweek):
    """
    Get the position of the user's team compared to other teams for a specific gameweek
    along with the leading team's score. Handles cases where multiple teams have the same score.
    """
    # First, calculate the total score for all teams in the given gameweek
    team_scores = Team.objects.annotate(
        total_score=Sum('players__score', filter=Q(players__gameweek=gameweek))
    ).order_by('-total_score')

    # Now find the total score of the user's team
    user_team_score = Team.objects.filter(user=user).annotate(
        total_score=Sum('players__score', filter=Q(players__gameweek=gameweek))
    ).first()

    # Check if the user has a team
    if user_team_score:
        # If no players exist for this user in the given gameweek (total_score is None), handle that case
        if user_team_score.total_score is None:
            return "-", "-"  # Return "-" if no players found for the user's team in this gameweek

        # Handle ties: Find all teams with the same score as the user's team
        tied_teams = [team for team in team_scores if team.total_score == user_team_score.total_score]

        # Assign positions with ties handling
        position = None
        current_position = 1
        for index, team in enumerate(team_scores):
            # If it's the first team with this score, assign position
            if team.total_score == user_team_score.total_score:
                position = current_position
                break
            # If the score is the same as the previous team, assign the same position
            if index > 0 and team.total_score == team_scores[index - 1].total_score:
                continue
            current_position += 1

        # Get the leading team score (the first team in the list)
        leading_team_score = team_scores.first().total_score if team_scores else None

        return position, leading_team_score
    else:
        # If no user team score found, return "-"
        return "-", "-"
    
def user_has_joined_league_in_gameweek(user, gameweek):
    return Contest.objects.filter(users=user, gameweek=gameweek).exists()

def get_gameweek_saved_team(user, gameweek=None):
    # Fetch saved players for the user
    saved_players = Player.objects.filter(user=user)

    # Fetch all players from `get_all_players()` and extract the JSON data
    players_response = get_all_players(None)  # Pass None if `request` is not needed
    players_data = json.loads(players_response.content.decode("utf-8"))  # Convert to Python dictionary
    players = players_data.get("players", [])  # Extract the players list

    # Additional logic...
    return players

from datetime import datetime, timedelta, timezone

def check_match_status(players):
    """
    Check if any player's match has started and if the last player's match has been played.

    Args:
        players (list): A list of player dictionaries. Each dictionary should contain a 'kickoff' key
                        with the kickoff time as a string in ISO 8601 format (e.g., "2025-05-04T15:00:00Z").

    Returns:
        dict: A dictionary with two keys:
              - 'any_match_started': True if any player's match has started, False otherwise.
              - 'last_match_played': True if the last player's match has been played (kickoff + 95 minutes), False otherwise.
    """
    now = datetime.now(timezone.utc)  # Get the current UTC time as an offset-aware datetime
    any_match_started = False
    last_match_played = False

    # Sort players by kickoff time to determine the last match
    players_sorted_by_kickoff = sorted(
        players,
        key=lambda player: datetime.fromisoformat(player.get("kickoff", "").replace("Z", "+00:00"))
        if player.get("kickoff") else datetime.max
    )

    for player in players:
        kickoff_times = player.get("kickoff", [])
        if not isinstance(kickoff_times, list):
            kickoff_times = [kickoff_times]  # Ensure it's a list

        for kickoff in kickoff_times:
            try:
                kickoff_time = datetime.fromisoformat(kickoff.replace("Z", "+00:00"))  # Parse ISO 8601 time
                if kickoff_time < now:  # Check if the match has started
                    any_match_started = True
                if kickoff_time + timedelta(minutes=95) > now:  # Check if the match is still ongoing
                    last_match_played = False
                    break
            except ValueError:
                # Skip invalid kickoff times
                continue

    # Check if the last player's match has been played
    if players_sorted_by_kickoff and players_sorted_by_kickoff[-1].get("kickoff"):
        last_kickoff = datetime.fromisoformat(players_sorted_by_kickoff[-1]["kickoff"].replace("Z", "+00:00"))
        last_match_played = (last_kickoff + timedelta(minutes=95)) < now

    return {
        "any_match_started": any_match_started,
        "last_match_played": last_match_played,
    }

def team_selection(request, user_id=None, gameweek=None):
    """Team Selection View with Grouped Matches and AJAX Pagination"""
    
    # Fetch current game week data
    current_game_week = get_current_game_week_data()

    # Get leagues based on their type
    public_leagues = Contest.objects.filter(league_type="Public",gameweek=gameweek or current_game_week['id'])
    
    # If user_id is provided in the URL, use that user; otherwise, use the logged-in user
    if user_id:
        user = get_object_or_404(User, id=user_id)
    else:
        user = request.user  # Default to logged-in user

    # Get the team of the user (either logged-in or specific user)
    user_team = Team.objects.filter(user=user).first()
    matches = get_fpl_matches()

    upcoming_matches = filter_fixtures_matches(matches)  # Get only matches in the next 7 days

    # Format matches for grouping and display
    for match in upcoming_matches:
        kickoff_time = match["kickoff_time"]
        match["formatted_date"] = format_time(kickoff_time, date_only=True)
        match["formatted_time"] = format_time(kickoff_time, time_only=True)

    # Group matches by formatted_date
    grouped_matches = []
    for date, group in groupby(sorted(upcoming_matches, key=itemgetter("formatted_date")), key=itemgetter("formatted_date")):
        grouped_matches.append({
            "date": date,
            "matches": list(group)
        })

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(grouped_matches, 1)  # 2 days of fixtures per page
    paginated_matches = paginator.get_page(page)

    # Handle AJAX request for pagination
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        match_data = [
            {
                "date": day["date"],
                "matches": [
                    {
                        "formatted_time": match["formatted_time"],
                        "formatted_date": match["formatted_date"],
                        "home_team": {
                            "name": match["home_team"]["name"],
                            "logo": match["home_team"]["logo"],
                        },
                        "away_team": {
                            "name": match["away_team"]["name"],
                            "logo": match["away_team"]["logo"],
                        },
                    }
                    for match in day["matches"]
                ],
            }
            for day in paginated_matches
        ]
        return JsonResponse({
            "matches": match_data,
            "has_next": paginated_matches.has_next(),
            "has_previous": paginated_matches.has_previous(),
            "current_page": paginated_matches.number,
            "total_pages": paginator.num_pages,
        })

    # Fetch all teams and their scores (assuming 'score' or 'points' is a field in your Team model)
    all_teams = Team.objects.all()  # This may vary based on your model structure
    teams_scores = [(team, team.score) for team in all_teams]  # Assuming 'score' holds the team points

    # Sort the teams by score (in descending order)
    sorted_teams = sorted(teams_scores, key=lambda x: x[1], reverse=True)

    # Get points for the leading team
    leading_team_points = sorted_teams[0][1] if sorted_teams else 0

    # For non-AJAX requests
    favorite_club_id = None
    if user_team and user_team.favorite_club:
        match = re.search(r"\((\d+)\)", user_team.favorite_club)
        if match:
            favorite_club_id = match.group(1)



    # Fetch players for the user's team
    # players = get_saved_team(user, gameweek or current_game_week['id'])  # Replace with your logic to fetch players

    # response_player = get_saved_team(request)
    # response_data_player = json.loads(response_player.content.decode("utf-8"))  # Extract the JSON data
    # players = response_data_player.get("team", [])  # Get the list of players

    # print(players)

        # Check if the user has players saved for the current gameweek
    user_has_players_for_gameweek = has_saved_players_for_gameweek(request.user, gameweek or current_game_week['id'])

    # if user_has_players_for_gameweek:
    #     print("has players saved.")
    # else:
    #     print("does not have players.")

    fixtures_by_day, has_started, has_ended = group_matches_by_day(current_game_week['id']-1)

    if gameweek or (has_started and not has_ended):
        # print("Gameweek provided")
        # print(user_id)
        team_score = get_team_score_for_gameweek(user, gameweek or current_game_week['id']-1)
        user_position, leading_team_points = get_user_team_position(user, gameweek or current_game_week['id']-1)
        fixtures_by_day, has_started, has_ended = group_matches_by_day( gameweek or current_game_week['id']-1)
        # Check if the user has joined a league
        has_joined_league = user_has_joined_league_in_gameweek(user, gameweek or current_game_week['id']-1)
        # Get leagues based on their type
        public_leagues = Contest.objects.filter(league_type="Public",gameweek=gameweek or current_game_week['id']-1)

        # print(user_id)

        return render(request, 'contests/prev_teamselection.html', {
            'user_team': user_team,
            'team_score': team_score,
            'matches': fixtures_by_day,
            'favorite_club_id': favorite_club_id,
            'current_game_week': current_game_week,
            'user_id': user_id,
            'gameweek': gameweek or current_game_week['id']-1,
            'public_leagues': public_leagues,
            'user_position': user_position,
            'leading_team_points': leading_team_points,
            'has_joined_league': has_joined_league,
            'has_started': has_started,
            'has_ended': has_ended,
        })

    team_score = get_team_score_for_gameweek(user, current_game_week['id'])
    user_position, leading_team_points = get_user_team_position(user, current_game_week['id'])
    fixtures_by_day, has_started, has_ended = group_matches_by_day(current_game_week['id'])

    # print(user_has_players_for_gameweek)

    return render(request, 'contests/teamselection.html', {
        'user_team': user_team,
        'team_score': team_score,
        'matches': fixtures_by_day,
        'favorite_club_id': favorite_club_id,
        'current_game_week': current_game_week,
        'user_id': user_id,
        'public_leagues': public_leagues,
        'user_position': user_position,
        'leading_team_points': leading_team_points,
        'has_started': has_started,
        'has_ended': has_ended,
        'user_has_team': user_has_players_for_gameweek,
    })

def has_saved_players_for_gameweek(user, gameweek):
    """Check if the user has players saved for the specified gameweek"""
    
    # Get the user's team
    user_team = Team.objects.filter(user=user).first()
    
    if not user_team:
        return False  # User has no team
    
    # Check if the team has players for the specific gameweek
    players_for_gameweek = user_team.players.filter(gameweek=gameweek)
    
    # If there are any players for this gameweek, return True, else False
    return players_for_gameweek.exists()

def format_time(utc_time, date_only=False, time_only=False):
    """Format UTC time to readable date or time."""
    from datetime import datetime
    try:
        match_time = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")
        if date_only:
            return match_time.strftime("%A %d %B %Y")
        if time_only:
            return match_time.strftime("%H:%M")
        return match_time.strftime("%A %d %B %Y %H:%M")
    except Exception as e:
        print(f"Error formatting time: {e}")
        return utc_time

def join_league(request):
    if request.method == 'POST':
        league_code = request.POST.get('leagueCode', '').strip()

        if not league_code:
            messages.warning(request, 'League code is required.')
            return render(request, 'contests/join_league.html')

        try:
            # Find the league with the given code
            league = Contest.objects.get(league_code=league_code)

            # Check if the user is already part of the league
            if request.user in league.users.all():
                messages.warning(request, 'You are already a member of this league.')
                return render(request, 'contests/join_league.html')

            # Deduct the entry fee if necessary
            entry_fee = league.entry_fee
            # Implement wallet deduction or balance checks here (if applicable)

            # Add the user to the league
            league.users.add(request.user)
            league.update_prize_pool()  # Update the prize pool

            messages.success(request, f'You have successfully joined the league "{league.name}".')
            return redirect('league')  # Redirect to the leagues page

        except Contest.DoesNotExist:
            messages.warning(request, 'Invalid league code. Please try again.')

    return render(request, 'contests/join_league.html')

def join_global_league(request, league_id):
    if request.method == 'POST':
        league = get_object_or_404(Contest, id=league_id, is_private=False)

        # Check if the user is already in the league
        if request.user in league.users.all():
            messages.warning(request, 'You are already a member of this league.')
            return redirect('leagues')

        # Add the user to the league
        league.users.add(request.user)
        league.update_prize_pool()  # Update the prize pool dynamically

        messages.success(request, f'You have successfully joined the league "{league.name}".')
        return redirect('leagues')

    return redirect('leagues')

# def entry_payment(request, league_code=None):
#     if league_code:
#         league = get_object_or_404(Contest, league_code=league_code)
#         # Handle payment for existing leagues
#         return handle_existing_league_payment(request, league)
    
#     # Handle payment for new leagues
#     pending_league = request.session.get('pending_league')
#     if not pending_league:
#         messages.warning(request, 'No pending league found. Please try creating the league again.')
#         return redirect('create-league')

#     if request.method == 'POST':
#         phone_number = request.POST.get('phoneNumber')

#         if not phone_number:
#             messages.warning(request, 'Phone number is required.')
#             return render(request, 'contests/entry_payment.html', {'pending_league': pending_league})

#         # Simulate successful payment and create the league
#         league = create_league_from_pending(request.user, pending_league)
#         del request.session['pending_league']  # Clear session
#         messages.success(request, f'Payment for league "{league.name}" was successful!')
#         return render(request, 'contests/payment_success.html', {'league': league})

#     return render(request, 'contests/entry_payment.html', {'pending_league': pending_league})

def entry_payment(request, league_code=None):
    if league_code:
        league = get_object_or_404(Contest, league_code=league_code)
        return handle_existing_league_payment(request, league)

    # print("pending_league in session:", request.session.get('pending_league'))
    pending_league = request.session.get('pending_league')
    
    if not pending_league:
        messages.warning(request, 'No pending league found. Please try creating the league again.')
        return redirect('create-league')

    if request.method == 'POST':
        phone_number = request.POST.get('phoneNumber')
        if not phone_number:
            messages.warning(request, 'Phone number is required.')
            return render(request, 'contests/entry_payment.html', {'pending_league': pending_league})

        amount = pending_league['entry_fee']
        account_reference = pending_league['name']
        transaction_desc = f"League Entry: {pending_league['name']}"
        # callback_url = request.build_absolute_uri(reverse('mpesa-callback'))
        # mpesa_response = initiate_mpesa_stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        mpesa_response = initiate_mpesa_stk_push(phone_number, amount, account_reference, transaction_desc)

        if mpesa_response.get('ResponseCode') == '0':
            request.session['mpesa_checkout_request_id'] = mpesa_response.get('CheckoutRequestID')
            request.session['pending_league_phone'] = phone_number
            messages.info(request, "A payment prompt has been sent to your phone. Please complete the payment.")
            return redirect('wait-for-payment')
        else:
            messages.warning(request, f"M-Pesa payment failed: {mpesa_response.get('errorMessage', 'Unknown error')}")
            return render(request, 'contests/entry_payment.html', {'pending_league': pending_league})

    return render(request, 'contests/entry_payment.html', {'pending_league': pending_league})

# def handle_existing_league_payment(request, league):
#     if request.method == 'POST':
#         phone_number = request.POST.get('phoneNumber')

#         if not phone_number:
#             messages.warning(request, 'Phone number is required.')
#             return render(request, 'contests/entry_payment.html', {'league': league})

#         if request.user in league.users.all():
#             messages.warning(request, 'You are already a member of this league.')
#             return redirect('league')

#         # Simulate payment success
#         league.users.add(request.user)
#         league.update_prize_pool()
#         messages.success(request, f'Payment for league "{league.name}" was successful!')
#         return render(request, 'contests/payment_success.html', {'league': league})

#     return render(request, 'contests/entry_payment.html', {'league': league})


def handle_existing_league_payment(request, league):
    if request.method == 'POST':
        phone_number = request.POST.get('phoneNumber')

        if not phone_number:
            messages.warning(request, 'Phone number is required.')
            return render(request, 'contests/entry_payment.html', {'league': league})

        if request.user in league.users.all():
            messages.warning(request, 'You are already a member of this league.')
            return redirect('league')

        amount = league.entry_fee
        account_reference = league.name
        transaction_desc = f"League Entry: {league.name}"
        # Optionally: callback_url = request.build_absolute_uri(reverse('mpesa-callback'))
        mpesa_response = initiate_mpesa_stk_push(phone_number, amount, account_reference, transaction_desc)

        if mpesa_response.get('ResponseCode') == '0':
            request.session['mpesa_checkout_request_id'] = mpesa_response.get('CheckoutRequestID')
            request.session['pending_league_phone'] = phone_number
            # Store pending_league in session for payment status check
            request.session['pending_league'] = {
                'id': league.id,
                'name': league.name,
                'entry_fee': float(league.entry_fee),
                'start_date': league.start_date.isoformat() if hasattr(league.start_date, 'isoformat') else str(league.start_date),
                'league_type': league.league_type,
                'gameweek': league.gameweek,
                'league_code': league.league_code,
            }
            messages.info(request, "A payment prompt has been sent to your phone. Please complete the payment.")
            return redirect('wait-for-payment')
        else:
            messages.warning(request, f"M-Pesa payment failed: {mpesa_response.get('errorMessage', 'Unknown error')}")
            return render(request, 'contests/entry_payment.html', {'league': league})

    return render(request, 'contests/entry_payment.html', {'league': league})

def create_league_from_pending(user, pending_league):
    # Create league and add the user
    league_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    league = Contest.objects.create(
        name=pending_league['name'],
        sport='Football',
        entry_fee=pending_league['entry_fee'],
        start_date=pending_league['start_date'],
        league_code=league_code,
        prize_pool=pending_league['entry_fee'],
        league_type=pending_league['league_type'],
        gameweek=pending_league['gameweek'],
    )
    league.users.add(user)
    league.update_prize_pool()
    return league

def league_teams(request, league_code):
    # Get the league/contest by league_code
    contest = get_object_or_404(Contest, league_code=league_code)

    # Get all users in the league
    league_users = contest.users.all()

    # Fetch current game week data (returns a dictionary)
    real_current_game_week = get_current_game_week_data()
    # print(current_game_week)


    current_game_week = get_specific_game_week_data(contest.gameweek)

    # print(current_game_week1)

    # Ensure deadline_time exists in the dictionary
    if "deadline_time" in current_game_week and current_game_week["deadline_time"]:
        deadline_time = current_game_week["deadline_time"]

        if isinstance(deadline_time, str):
            # Convert string to datetime
            deadline_time = parse_datetime(deadline_time)

        if isinstance(deadline_time, datetime):
            # Convert to local time
            deadline_time = localtime(deadline_time)

            # Format deadline time
            current_game_week["formatted_deadline"] = deadline_time.strftime("%a %d %b %H:%M")

    # Get the current gameweek
    gameweek = current_game_week.get("id")

    # Fetch teams for the league and calculate their scores dynamically
    teams = Team.objects.filter(user__in=league_users).annotate(
        total_score=Sum('players__score', filter=Q(players__gameweek=gameweek))
    ).order_by('-total_score')

    # Manually assign positions to handle ties
    position = 1
    last_score = None
    for idx, team in enumerate(teams):
        # If the score is different from the previous team's score, assign a new position
        if team.total_score != last_score:
            position = idx + 1  # Position starts from 1 and is incremented by index + 1
        team.position = position
        last_score = team.total_score

    # Render the template with dynamic team scores and positions
    return render(request, 'contests/league_teams.html', {
        'contest': contest,
        'teams': teams,
        'current_game_week': current_game_week,
        'real_current_game_week': real_current_game_week,
    })

@login_required
def get_saved_team(request, user_id=None):
    # If a user_id is provided, fetch the specific user; otherwise, use the logged-in user
    if user_id:
        user = get_object_or_404(User, id=user_id)
    else:
        user = request.user  # Default to logged-in user

    # Fetch saved players for the user
    saved_players = Player.objects.filter(user=user)

    # Fetch all players from `get_all_players()` and extract the JSON data
    players_response = get_all_players(request)  # Returns a JsonResponse
    players_data = json.loads(players_response.content.decode("utf-8"))  # Convert to Python dictionary
    players = players_data.get("players", [])  # Extract the players list

    # print(players)

    team = get_object_or_404(Team, user=user)
    # Get the captain's player ID
    captain_id = team.captain.player_id if team.captain else None
    # Get the vicecaptain's player ID
    vicecaptain_id = team.vice_captain.player_id if team.vice_captain else None

    team_data = []

    for player in saved_players:
        # 🔥 Find the corresponding player from `players` based on `player_id`
        matched_player = next((p for p in players if p["id"] == player.player_id), None)

        # Merge data: If matched, update missing fields; otherwise, use default values
        team_data.append({
            "name": player.name,
            "position": player.position,
            "player_id": player.player_id,
            "score": player.score,
            "image": player.image_url,
            "formation_name": player.formation_name,
            "position_coordinates": player.position_coordinates,
            "kickoff": player.kickoff,
            "gameweek": player.gameweek,

            #From Team
            "is_captain": player.player_id == captain_id,
            "is_vicecaptain": player.player_id == vicecaptain_id,

            # Fields from `players`
            "team": matched_player["team"] if matched_player else "N/A",
            "price": matched_player["price"] if matched_player else "0.0",
            "form": matched_player["form"] if matched_player else "N/A",
            "total_points": matched_player["total_points"] if matched_player else 0,
            "tsb": matched_player["tsb"] if matched_player else "0%",
            "team_short": matched_player["team_short"] if matched_player else "UNK",
            "teamLogo": matched_player["teamLogo"] if matched_player else "https://via.placeholder.com/20",
            "fixture": matched_player["fixture"] if matched_player else "No upcoming match",
            "fixture_data": matched_player["fixture_data"] if matched_player else {
                "team1": "UNK",
                "team1Logo": "https://via.placeholder.com/20",
                "team2": "UNK",
                "team2Logo": "https://via.placeholder.com/20",
                "time": "TBD"
            },
            "team_shirt": matched_player["team_shirt"] if matched_player else "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_8-110.webp"
        })

    # print(len(team_data))

    return JsonResponse({"team": team_data}, status=200)

@csrf_exempt
def save_team(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            team_name = data.get("team_name", "Default Team")
            team_id = data.get("team_id", 0)
            current_gameweek = int(data.get("current_gameweek", 0))
            favorite_club = data.get("favorite_club", "Unknown")
            players_data = data.get("team", [])

            if not isinstance(players_data, list):
                return JsonResponse({"error": "Invalid team data."}, status=400)

            user = request.user

            # ✅ Get or create the team
            team, _ = Team.objects.get_or_create(user=user, name=team_name, defaults={"favorite_club": favorite_club})

            # ✅ Remove only current gameweek player associations
            existing_players = Player.objects.filter(gameweek=current_gameweek, teams=team)
            for player in existing_players:
                team.players.remove(player)

            # ✅ Save new players for current gameweek
            for pdata in players_data:
                player, _ = Player.objects.update_or_create(
                    user=user,
                    player_id=pdata.get("playerid", 0),
                    gameweek=current_gameweek,
                    defaults={
                        "name": pdata["name"],
                        "position": pdata["position"],
                        "position_coordinates": pdata["position_coordinates"],
                        "formation_name": pdata["formation_name"],
                        "score": pdata.get("score", 0),
                        "team": f"{team_name} ({team_id})",
                        "kickoff": pdata["kickoff"],
                        "image_url": pdata.get("image_url", ""),
                    }
                )
                team.players.add(player)

            team.save()
            return JsonResponse({"message": "Team saved successfully."}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)

def check_team_status(request):
    if request.user.is_authenticated:
        user_has_team = Player.objects.filter(user=request.user).exists()
        return JsonResponse({"team_exists": user_has_team})
    return JsonResponse({"error": "User not authenticated"}, status=401)

def create_league(request):
    if request.method == 'POST':
        league_name = request.POST.get('leagueName', '').strip()
        entry_fee = request.POST.get('entryFee', '0').strip()
        start_date = request.POST.get('startDate', '').strip()
        league_type = request.POST.get('leagueType', 'Public').strip()  # Default to Public
        current_gameweek = get_current_game_week_data()['id']

        # Validate league name
        if len(league_name) == 0 or len(league_name) > 30:
            messages.warning(request, 'League name must be between 1 and 30 characters.')
            return render(request, 'contests/create_league.html')

        # Validate start date
        if not start_date:
            messages.warning(request, 'Start date is required.')
            return render(request, 'contests/create_league.html')

        try:
            start_date = parse_datetime(start_date)
            if not start_date:
                raise ValueError("Invalid date format.")
        except ValueError:
            messages.warning(request, 'Invalid start date format.')
            return render(request, 'contests/create_league.html')

        # Validate entry fee
        try:
            entry_fee = float(entry_fee)
            if entry_fee < 0:
                raise ValueError("Entry fee cannot be negative.")
        except ValueError:
            messages.warning(request, 'Invalid entry fee amount.')
            return render(request, 'contests/create_league.html')

        # Save league details to session
        request.session['pending_league'] = {
            'name': league_name,
            'entry_fee': entry_fee,
            'start_date': start_date.isoformat(),
            'league_type': league_type,
            'gameweek': current_gameweek,
        }

        # Redirect to the payment page
        return redirect(reverse('entry-payment'))

    return render(request, 'contests/create_league.html')

@login_required
def update_captain(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            player_id = data.get("player_id")
            role = data.get("role")  # "captain" or "vice_captain"

            # Fetch the current gameweek
            current_gameweek_id = get_current_game_week_data()['id']

            # Ensure player_id is provided and valid
            if not player_id or role not in ["captain", "vice_captain"]:
                return JsonResponse({"error": "Invalid request data."}, status=400)

            # Get the logged-in user's team
            team = get_object_or_404(Team, user=request.user)

            # Ensure the player exists in the team before assigning
            # player = get_object_or_404(Player, player_id=player_id, teams=team)
            player = get_object_or_404(Player, player_id=player_id, teams=team, gameweek=current_gameweek_id)

            # Check if there's already a history record for this team and gameweek
            history_record = CaptainViceCaptainHistory.objects.filter(
                team=team,
                gameweek=current_gameweek_id
            ).first()

            if history_record:
                # If a history record exists, update it instead of creating a new one
                if role == "captain":
                    history_record.captain = player
                    history_record.vice_captain = team.vice_captain
                elif role == "vice_captain":
                    history_record.captain = team.captain
                    history_record.vice_captain = player
                
                history_record.save()  # Save the updated record
            else:
                # If no history record exists, create a new one
                if role == "captain":
                    history_record = CaptainViceCaptainHistory(
                        team=team,
                        captain=player,
                        vice_captain=team.vice_captain,
                        gameweek=current_gameweek_id
                    )
                elif role == "vice_captain":
                    history_record = CaptainViceCaptainHistory(
                        team=team,
                        captain=team.captain,
                        vice_captain=player,
                        gameweek=current_gameweek_id
                    )
                history_record.save()  # Save the new record

            # Assign the player as captain or vice-captain in the team
            if role == "captain":
                team.captain = player
            elif role == "vice_captain":
                team.vice_captain = player

            team.save()  # Save team after assigning the captain or vice-captain

            return JsonResponse({"message": f"{player.name} is now the {role}!", "captain": player_id}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)

def get_previous_gameweek_captain_and_vice_captain(team, gameweek):
    try:
        # Get the captain and vice-captain for the previous gameweek
        previous_gameweek_history = CaptainViceCaptainHistory.objects.filter(
            team=team,
            gameweek=gameweek - 1  # Get the history for the previous gameweek
        ).first()

        if previous_gameweek_history:
            return previous_gameweek_history.captain, previous_gameweek_history.vice_captain
        else:
            return None, None  # No history found for the previous gameweek
    except CaptainViceCaptainHistory.DoesNotExist:
        return None, None

@login_required
def swap_player_coordinates(request):
    try:
        data = json.loads(request.body)

        first_id = data.get('first_player_id')
        second_id = data.get('second_player_id')
        first_coords = data.get('first_coordinates')
        second_coords = data.get('second_coordinates')
        current_game_week = get_current_game_week_data()['id']

        if not all([first_id, second_id, first_coords, second_coords, current_game_week]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        user = request.user

        # Filter players by ID, user, and gameweek
        try:
            first_player = Player.objects.get(player_id=first_id, user=user, gameweek=current_game_week)
            second_player = Player.objects.get(player_id=second_id, user=user, gameweek=current_game_week)
        except Player.DoesNotExist:
            return JsonResponse({'error': 'One or both players not found for the user and gameweek.'}, status=404)

        # Swap coordinates
        first_player.position_coordinates = second_coords
        second_player.position_coordinates = first_coords

        first_player.save()
        second_player.save()

        return JsonResponse({'success': True, 'message': 'Coordinates swapped successfully.'})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# team = get_object_or_404(Team, user=request.user)
# gameweek = get_current_game_week_data()['id']

# captain, vice_captain = get_previous_gameweek_captain_and_vice_captain(team, gameweek)

# if captain and vice_captain:
#     print(f"Previous Gameweek Captain: {captain.name}, Vice-Captain: {vice_captain.name}")
# else:
#     print("No previous captain or vice-captain found.")


@login_required
def edit_league(request, league_id):
    league = get_object_or_404(Contest, id=league_id)
    if request.method == "POST":
        league.name = request.POST.get("name")
        league.sport = request.POST.get("sport")
        league.entry_fee = request.POST.get("entry_fee")
        league.prize_pool = request.POST.get("prize_pool")
        league.start_date = request.POST.get("start_date")
        league.save()
        return redirect('admin_global_leagues')
    return render(request, "contests/admin/edit_league.html", {"league": league})


@login_required
def view_league(request, league_id):
    league = get_object_or_404(Contest, id=league_id)
    # Get all teams whose user is in this league
    teams = Team.objects.filter(user__in=league.users.all()).order_by('-score')
    return render(request, "contests/admin/view_league.html", {
        "league": league,
        "teams": teams,
    })

@login_required
def admin_view_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    # Get the current gameweek ID
    current_gameweek = get_current_game_week_data()
    current_gameweek_id = current_gameweek['id'] if current_gameweek else None

    # Get only players for the current gameweek
    if current_gameweek_id:
        players = team.players.filter(gameweek=current_gameweek_id).order_by('position')
    else:
        players = team.players.all().order_by('position')

    # Find a league this team/user is in (if possible)
    league = None
    user_leagues = Contest.objects.filter(users=team.user)
    if user_leagues.exists():
        league = user_leagues.first()

    return render(request, "contests/admin/admin_view_team.html", {
        "team": team,
        "players": players,
        "league": league,
    })

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

@login_required
def admin_users(request):
    User = get_user_model()
    users = User.objects.all().order_by('-date_joined')
    return render(request, "contests/admin/admin_users.html", {"users": users})

@login_required
def admin_edit_user(request, user_id):
    User = get_user_model()
    user_obj = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user_obj.username = request.POST.get("username")
        user_obj.email = request.POST.get("email")
        user_obj.first_name = request.POST.get("first_name")
        user_obj.last_name = request.POST.get("last_name")
        user_obj.is_active = request.POST.get("is_active") == "True"
        user_obj.save()
        return redirect('admin_users')
    return render(request, "contests/admin/admin_edit_user.html", {"user_obj": user_obj})

@login_required
def admin_view_user(request, user_id):
    User = get_user_model()
    user_obj = get_object_or_404(User, id=user_id)

    # Get current gameweek
    current_gameweek = get_current_game_week_data()
    current_gameweek_id = current_gameweek['id'] if current_gameweek else None

    # Filter leagues and players for current gameweek
    if current_gameweek_id:
        leagues = Contest.objects.filter(users=user_obj, gameweek=current_gameweek_id)
        players = Player.objects.filter(user=user_obj, gameweek=current_gameweek_id)
    else:
        leagues = Contest.objects.none()
        players = Player.objects.none()

    teams = Team.objects.filter(user=user_obj)
    return render(request, "contests/admin/admin_view_user.html", {
        "user_obj": user_obj,
        "leagues": leagues,
        "players": players,
        "teams": teams,
    })