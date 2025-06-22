from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    short_name = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50)
    birth_date = models.DateField()
    position = models.CharField(max_length=3, choices=[
        ('GK', 'Goalkeeper'),
        ('CB', 'Center-Back'),
        ('LB', 'Left-Back'),
        ('RB', 'Right-Back'),
        ('CM', 'Central-Midfielder'),
        ('CAM', 'Central-Attacking-Midfielder'),
        ('CDM', 'Central-Defending-Midfielder'),
        ('LW', 'Left-Winger'),
        ('RW', 'Right-Winger'),
        ('ST', 'Striker'),
    ])
    teams = models.ManyToManyField(Team, through='PlayerTeam', related_name='players')

    def __str__(self):
        return f"{self.name} ({self.get_position_display()})"

class PlayerTeam(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    joined_date = models.DateField()
    left_date = models.DateField(null=True, blank=True)
    jersey_number = models.PositiveIntegerField()

    class Meta:
        unique_together = [('team', 'jersey_number', 'joined_date')]

    def __str__(self):
        return f"{self.player.name} at {self.team.name}"

class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    date = models.DateField()
    location = models.CharField(max_length=100, blank=True, null=True)
    players = models.ManyToManyField(Player, through='MatchPlayer', related_name='matches')

    class Meta:
        # A match is uniquely identified by teams and date
        unique_together = [('home_team', 'away_team', 'date')]

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name}"

class MatchPlayer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    minutes_played = models.PositiveIntegerField()
    goals_scored = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    yellow_cards = models.PositiveIntegerField(default=0)
    red_card = models.BooleanField(default=False)

    class Meta:
        unique_together = [('match', 'player')]

    def __str__(self):
        return f"{self.player.name} in {self.match}"

class MatchStats(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='stats')
    home_score = models.PositiveIntegerField(default=0)
    away_score = models.PositiveIntegerField(default=0)
    extra_time = models.BooleanField(default=False)
    home_shots = models.PositiveIntegerField(default=0)
    away_shots = models.PositiveIntegerField(default=0)
    home_shots_on_target = models.PositiveIntegerField(default=0)
    away_shots_on_target = models.PositiveIntegerField(default=0)
    home_possession = models.PositiveIntegerField(help_text="Possession % for home team")
    away_possession = models.PositiveIntegerField(help_text="Possession % for away team")
    home_pass_completion = models.PositiveIntegerField(help_text="Pass completion % for home team")
    away_pass_completion = models.PositiveIntegerField(help_text="Pass completion % for away team")
    home_yellow_cards = models.PositiveIntegerField(default=0)
    away_yellow_cards = models.PositiveIntegerField(default=0)
    home_red_cards = models.PositiveIntegerField(default=0)
    away_red_cards = models.PositiveIntegerField(default=0)
    home_fouls = models.PositiveIntegerField(default=0)
    away_fouls = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Match stats"

    def __str__(self):
        return f"Stats for {self.match}"
