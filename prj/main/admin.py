from django.contrib import admin
from django.db import models
from .models import Team, Match, MatchStats, Player, PlayerTeam, MatchPlayer

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "total_matches", "total_wins", "total_draws", "total_losses")
    search_fields = ("name", "short_name")
    ordering = ("name",)

    def total_matches(self, obj):
        return obj.home_matches.count() + obj.away_matches.count()
    total_matches.short_description = "Total Matches"

    def total_wins(self, obj):
        home_wins = obj.home_matches.filter(stats__home_score__gt=models.F('stats__away_score')).count()
        away_wins = obj.away_matches.filter(stats__away_score__gt=models.F('stats__home_score')).count()
        return home_wins + away_wins
    total_wins.short_description = "Wins"

    def total_draws(self, obj):
        home_draws = obj.home_matches.filter(stats__home_score=models.F('stats__away_score')).count()
        away_draws = obj.away_matches.filter(stats__away_score=models.F('stats__home_score')).count()
        return home_draws + away_draws
    total_draws.short_description = "Draws"

    def total_losses(self, obj):
        home_losses = obj.home_matches.filter(stats__home_score__lt=models.F('stats__away_score')).count()
        away_losses = obj.away_matches.filter(stats__away_score__lt=models.F('stats__home_score')).count()
        return home_losses + away_losses
    total_losses.short_description = "Losses"

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("__str__", "date", "location", "match_result")
    list_filter = ("date", "home_team", "away_team")
    search_fields = ("home_team__name", "away_team__name", "location")
    date_hierarchy = "date"
    ordering = ("-date",)

    def match_result(self, obj):
        try:
            stats = obj.stats
            return f"{stats.home_score} - {stats.away_score}"
        except MatchStats.DoesNotExist:
            return "No result"
    match_result.short_description = "Result"

@admin.register(MatchStats)
class MatchStatsAdmin(admin.ModelAdmin):
    list_display = (
        "match", "match_result", "extra_time",
        "possession_stats", "shots_stats", "cards_stats"
    )
    list_filter = ("extra_time", "home_score", "away_score")
    search_fields = ("match__home_team__name", "match__away_team__name")
    ordering = ("-match__date",)

    def match_result(self, obj):
        return f"{obj.home_score} - {obj.away_score}"
    match_result.short_description = "Result"

    def possession_stats(self, obj):
        return f"H: {obj.home_possession}% A: {obj.away_possession}%"
    possession_stats.short_description = "Possession"

    def shots_stats(self, obj):
        return f"H: {obj.home_shots_on_target}/{obj.home_shots} A: {obj.away_shots_on_target}/{obj.away_shots}"
    shots_stats.short_description = "Shots (On Target/Total)"

    def cards_stats(self, obj):
        return f"H: {obj.home_yellow_cards}Y {obj.home_red_cards}R A: {obj.away_yellow_cards}Y {obj.away_red_cards}R"
    cards_stats.short_description = "Cards (Y/R)"

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'nationality', 'birth_date', 'current_team', 'current_number')
    list_filter = ('position', 'nationality')
    search_fields = ('name', 'nationality')
    ordering = ('name',)

    def current_team(self, obj):
        current = obj.playerteam_set.filter(left_date__isnull=True).first()
        return current.team.name if current else 'Free Agent'
    current_team.short_description = 'Current Team'

    def current_number(self, obj):
        current = obj.playerteam_set.filter(left_date__isnull=True).first()
        return current.jersey_number if current else '-'
    current_number.short_description = '#'


@admin.register(PlayerTeam)
class PlayerTeamAdmin(admin.ModelAdmin):
    list_display = ('player', 'team', 'jersey_number', 'joined_date', 'left_date')
    list_filter = ('team', 'joined_date')
    search_fields = ('player__name', 'team__name')
    date_hierarchy = 'joined_date'
    ordering = ('-joined_date',)

@admin.register(MatchPlayer)
class MatchPlayerAdmin(admin.ModelAdmin):
    list_display = ('match', 'player', 'team', 'minutes_played', 'performance_stats')
    list_filter = ('team', 'match__date', 'red_card')
    search_fields = ('player__name', 'match__home_team__name', 'match__away_team__name')
    date_hierarchy = 'match__date'
    ordering = ('-match__date',)

    def performance_stats(self, obj):
        stats = []
        if obj.goals_scored: stats.append(f"{obj.goals_scored}G")
        if obj.assists: stats.append(f"{obj.assists}A")
        if obj.yellow_cards: stats.append(f"{obj.yellow_cards}Y")
        if obj.red_card: stats.append("R")
        return " ".join(stats) if stats else "-"
    performance_stats.short_description = 'Performance'
