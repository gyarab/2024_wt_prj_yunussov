from django.shortcuts import render, get_object_or_404
from .models import Match, Team
from datetime import date
try:
    from django.db.models import Q
except ImportError:
    Q = None
import unicodedata

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

def get_homepage(request):
    today = date.today()
    q = request.GET.get('q', '').strip()
    match_filter = None
    teams = None
    if q:
        q_norm = strip_accents(q).lower()
        # Filter teams (in Python, for accent-insensitive)
        all_teams = Team.objects.all()
        teams = [t for t in all_teams if q_norm in strip_accents(t.name).lower() or q_norm in strip_accents(t.short_name).lower()]
        # Filter matches by team or location (accent-insensitive for location, but DB for team names)
        if Q:
            match_filter = (
                Q(home_team__name__icontains=q) | Q(home_team__short_name__icontains=q) |
                Q(away_team__name__icontains=q) | Q(away_team__short_name__icontains=q) |
                Q(location__icontains=q)
            )
            todays_matches = Match.objects.filter(date=today).filter(match_filter).order_by('-date')
            past_matches = Match.objects.filter(date__lt=today).filter(match_filter).order_by('-date')
            future_matches = Match.objects.filter(date__gt=today).filter(match_filter).order_by('date')
        else:
            todays_matches = Match.objects.filter(date=today).order_by('-date')
            past_matches = Match.objects.filter(date__lt=today).order_by('-date')
            future_matches = Match.objects.filter(date__gt=today).order_by('date')
    else:
        todays_matches = Match.objects.filter(date=today).order_by('-date')
        past_matches = Match.objects.filter(date__lt=today).order_by('-date')
        future_matches = Match.objects.filter(date__gt=today).order_by('date')
    context = {
        "h1_title": "All Matches",
        "todays_matches": todays_matches,
        "past_matches": past_matches,
        "future_matches": future_matches,
        "search_teams": teams,
        "search_query": q,
    }
    return render(request, "main/home.html", context)

# Detail view for a match

def match_detail(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    stats = getattr(match, 'stats', None)
    today = date.today()
    context = {
        "match": match,
        "stats": stats,
        "today": today,
    }
    return render(request, "main/match_detail.html", context)

def teams_list(request):
    teams = Team.objects.all().order_by('name')
    return render(request, "main/teams_list.html", {"teams": teams})

def team_stats(request):
    from django.db.models import Q
    teams = Team.objects.all()
    stats = []
    for team in teams:
        matches = Match.objects.filter(Q(home_team=team) | Q(away_team=team)).select_related('stats')
        played = 0
        wins = 0
        draws = 0
        losses = 0
        goals_for = 0
        goals_against = 0
        for match in matches:
            match_stats = getattr(match, 'stats', None)
            if not match_stats:
                continue
            played += 1
            if match.home_team == team:
                gf = match_stats.home_score
                ga = match_stats.away_score
            else:
                gf = match_stats.away_score
                ga = match_stats.home_score
            goals_for += gf
            goals_against += ga
            if gf > ga:
                wins += 1
            elif gf == ga:
                draws += 1
            else:
                losses += 1
        points = wins * 3 + draws
        stats.append({
            'team': team,
            'played': played,
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'goal_diff': goals_for - goals_against,
            'points': points,
        })
    stats.sort(key=lambda x: (x['points'], x['goal_diff'], x['goals_for']), reverse=True)
    return render(request, 'main/team_stats.html', {'stats': stats})
