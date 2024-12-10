"""
File: admin.py
Author: Jason Kim
Email: jasonkim@bu.edu
Date: December 10, 2024
Description: This file configures the Django admin interface for the Elite Squads application. It defines 
             custom admin classes for the Team, Player, Match, and League models, specifying the fields 
             to display, filters, and search functionalities. These customizations enhance the usability 
             and organization of the admin panel for managing application data.
"""



from django.contrib import admin
from .models import Team, Match, League, Player


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        'name', 
        'points', 
        'matches_played', 
        'wins', 
        'losses', 
        'ties', 
        'league', 
        'player_of_the_season',
    )
    
    # Fields to display in the form view
    fields = (
        'name', 
        'points', 
        'matches_played', 
        'wins', 
        'losses', 
        'ties', 
        'league', 
        'player_of_the_season',
    )
    
    # Add a filter for leagues and search functionality
    list_filter = ('league',)  # Allows filtering teams by league
    search_fields = ('name',)  # Enables search by team name


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        'name', 
        'team', 
        'position', 
        'goals', 
        'assists', 
        'matches_played',
    )
    
    # Add filters for better usability
    list_filter = ('team', 'position')  # Allows filtering by team and position
    
    # Add search functionality for players
    search_fields = ('name', 'team__name')  # Enables search by player name or team name


# Register remaining models
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'home_score', 'away_score', 'date')
    list_filter = ('date',)
    search_fields = ('home_team__name', 'away_team__name')


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('league_type', 'season')
    search_fields = ('league_type', 'season')
