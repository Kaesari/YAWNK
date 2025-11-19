from django.urls import path

from contests import mpesa,payouts
from .views import check_team_status, contest_list, get_all_players,  get_saved_team,player_list, create_team,save_team, update_captain
from . import views

urlpatterns = [
    path('', views.contest_list, name='contest_list'),
    path('<int:contest_id>/', views.contest_detail, name='contest_detail'),
    path('<int:contest_id>/create_team/', views.create_team, name='create_team'),

    path('contests/', contest_list, name='contest_list'),
    path('players/', player_list, name='player_list'),
    path('teams/', create_team, name='create_team'),
    path('swap-coordinates/', views.swap_player_coordinates, name='swap_coordinates'),


    path('register/', views.register, name='register'),

    path('<int:contest_id>/leaderboard/', views.leaderboard, name='leaderboard'),

    path('manageteam/', views.manage_team, name='manage_team'),
    path('manage_team/<int:user_id>/', views.manage_team, name='manage_team_user'), 
    path('prev_gameweek/<int:gameweek>/', views.manage_team, name='manage_team_user_gameweek'),
    path('league/', views.league, name='league'),
    path('statistics/', views.statistics, name='statistics'),
    path('teamselection/', views.team_selection, name='team_selection'),
    path('team_selection/<int:user_id>/', views.team_selection, name='team_selection_user'),  # For specific user
    path('gameweek/<int:gameweek>/', views.team_selection, name='team_selection_gameweek'),  # For specific gameweek
    path('join-league/', views.join_league, name='join-league'),
    path("save-team/", save_team, name="save-team"),
    path("check-team-status/", check_team_status, name="check-team-status"),
    path('create-league/', views.create_league, name='create-league'),
    path("get-saved-team/", get_saved_team, name="get_saved_team"),
    path('get-saved-team/<int:user_id>/', views.get_saved_team, name="get_saved_team_user"),  # For specific user
    path('join-global-league/<int:league_id>/', views.join_global_league, name='join-global-league'),
    path('league/<str:league_code>/teams/', views.league_teams, name='league-teams'),
    path('entry-payment/', views.entry_payment, name='entry-payment'),
    path('entry-payment/<str:league_code>/', views.entry_payment, name='entry-payment'),

    path("get-teams/", views.get_teams, name="get_teams"),
    path("get-all-players/", get_all_players, name="get_all_players"),
    path("get-players-by-team/", views.get_players_by_team_api, name="get_players_by_team_api"),
    # path("api/players/", get_players, name="get_players"),
    # path("captain/", get_captain, name="get_captain"),
    path("update-captain/", update_captain, name="update-captain"),

    #---------------------Admin------------------------
    
    path('manage/', views.admin_view, name='admin_view'),
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard_view'),
    path('private/', views.admin_private_leagues, name='admin_private_leagues'),
    path('global/', views.admin_global_leagues, name='admin_global_leagues'),
    path('reports/', views.admin_reports_leagues, name='admin_reports_leagues'),
    path('profile/', views.admin_user_profile, name='admin_user_profile'),
    path('admin/league/<int:league_id>/edit/', views.edit_league, name='admin_edit_league'),
    path('admin/league/<int:league_id>/view/', views.view_league, name='admin_view_league'),
    path('admin/team/<int:team_id>/view/', views.admin_view_team, name='admin_view_team'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/user/<int:user_id>/edit/', views.admin_edit_user, name='admin_edit_user'),
    path('admin/user/<int:user_id>/view/', views.admin_view_user, name='admin_view_user'),


    #---------------------MPESA API------------------------
    path('mpesa/callback/', mpesa.mpesa_callback, name='mpesa-callback'),
    path('wait-for-payment/', mpesa.wait_for_payment, name='wait-for-payment'),
    path('check-payment-status/', mpesa.check_payment_status, name='check-payment-status'),
    path('payment-success/<int:league_id>/', mpesa.payment_success, name='payment-success'),

    path('mpesa/b2c/result/', payouts.mpesa_b2c_result, name='mpesa-b2c-result'),
    path('mpesa/b2c/timeout/', payouts.mpesa_b2c_timeout, name='mpesa-b2c-timeout'),


    path('mpesa/b2c/payout-league/', payouts.payout_league_winners_70_percent_api, name='payout-league-winners-70-percent'),
    path('mpesa/b2c/test/', payouts.payout_winner, name='payout-winner'),


]
