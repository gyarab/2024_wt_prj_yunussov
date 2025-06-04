from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)

    def __str__(self):
        return self.short_name

class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    date = models.DateField()
    location = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"

class MatchStats(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='stats')
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    extra_time = models.BooleanField(default=False)
    home_shots = models.IntegerField(default=0)
    away_shots = models.IntegerField(default=0)
    home_shots_on_target = models.IntegerField(default=0)
    away_shots_on_target = models.IntegerField(default=0)
    home_possession = models.IntegerField(help_text="Possession % for home team")
    away_possession = models.IntegerField(help_text="Possession % for away team")
    home_pass_completion = models.IntegerField(help_text="Pass completion % for home team")
    away_pass_completion = models.IntegerField(help_text="Pass completion % for away team")
    home_yellow_cards = models.IntegerField(default=0)
    away_yellow_cards = models.IntegerField(default=0)
    home_red_cards = models.IntegerField(default=0)
    away_red_cards = models.IntegerField(default=0)
    home_fouls = models.IntegerField(default=0)
    away_fouls = models.IntegerField(default=0)

    def __str__(self):
        return f"Stats for {self.match}"
