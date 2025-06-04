# prj/main/management/commands/add_sample_data.py
from django.core.management.base import BaseCommand
from main.models import Team, Match, MatchStats
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Add sample teams, matches, and stats'

    def handle(self, *args, **kwargs):
        arsenal, _ = Team.objects.get_or_create(name="Arsenal", short_name="ARS")
        chelsea, _ = Team.objects.get_or_create(name="Chelsea", short_name="CHE")
        liverpool, _ = Team.objects.get_or_create(name="Liverpool", short_name="LIV")
        manutd, _ = Team.objects.get_or_create(name="Manchester United", short_name="MUN")
        teams = [arsenal, chelsea, liverpool, manutd]

        def create_match_and_stats(home, away, match_date, location):
            if home == away:
                return
            match = Match.objects.create(
                home_team=home,
                away_team=away,
                date=match_date,
                location=location
            )
            possession = random.randint(40, 60)
            home_shots = random.randint(5, 20)
            away_shots = random.randint(5, 20)
            MatchStats.objects.create(
                match=match,
                home_score=random.randint(0, 5),
                away_score=random.randint(0, 5),
                extra_time=random.choice([True, False]),
                home_shots=home_shots,
                away_shots=away_shots,
                home_shots_on_target=random.randint(0, home_shots),
                away_shots_on_target=random.randint(0, away_shots),
                home_possession=possession,
                away_possession=100-possession,
                home_pass_completion=random.randint(70, 95),
                away_pass_completion=random.randint(70, 95),
                home_yellow_cards=random.randint(0, 3),
                away_yellow_cards=random.randint(0, 3),
                home_red_cards=random.randint(0, 1),
                away_red_cards=random.randint(0, 1),
                home_fouls=random.randint(3, 15),
                away_fouls=random.randint(3, 15),
            )

        today = date.today()
        for i in range(3):
            create_match_and_stats(
                random.choice(teams), random.choice(teams),
                today - timedelta(days=i+1), "Stadium " + str(i+1)
            )
            create_match_and_stats(
                random.choice(teams), random.choice(teams),
                today + timedelta(days=i+1), "Arena " + str(i+1)
            )
        create_match_and_stats(arsenal, liverpool, today, "Emirates Stadium")
        self.stdout.write(self.style.SUCCESS('Sample data added!'))