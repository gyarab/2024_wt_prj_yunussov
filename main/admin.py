from django.contrib import admin
from .models import Team, Match, MatchStats

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name")
    search_fields = ("name", "short_name")

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("home_team", "away_team", "date", "location")
    list_filter = ("date", "home_team", "away_team")
    search_fields = ("home_team__name", "away_team__name")
    date_hierarchy = "date"

@admin.register(MatchStats)
class MatchStatsAdmin(admin.ModelAdmin):
    list_display = (
        "match", "home_score", "away_score", "home_shots", "away_shots", "home_shots_on_target", "away_shots_on_target",
        "home_yellow_cards", "away_yellow_cards", "home_red_cards", "away_red_cards",
        "home_fouls", "away_fouls",
        "home_possession", "away_possession", "home_pass_completion", "away_pass_completion", "extra_time"
    )
    search_fields = ("match__home_team__name", "match__away_team__name")
