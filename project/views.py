"""Description: Contains class-based views for handling various functionalities of the application, including:
             - Team and match CRUD operations
             - User authentication (signup)
             - Filtering and displaying teams and matches
             - Updating team and match stats
             File: admin.py
            Author: Jason Kim
            Email: jasonkim@bu.edu
            Date: December 10, 2024
             
             """


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from project.forms import MatchForm
from .models import Team, Match, League, Player
from django.contrib.auth.forms import UserCreationForm

class TeamListView(ListView):
    """
    Displays a list of teams, with search functionality and additional context data.
    
    Context:
    - `leagues`: All leagues ordered by season.
    - `teams_by_league`: Teams grouped by league, ordered by points.
    - `top_teams`: Top 3 teams based on points.
    - `top_scorers`: Top 3 players based on goals.
    - `matches`: Matches involving teams matching the search query, if provided.
    """
    model = Team
    template_name = 'project/team_list.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        """
        Adds additional context data, such as leagues, top teams, and matches,
        based on a search query.
        """
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        
        context['leagues'] = League.objects.all().order_by('season')
        teams_by_league = {league: league.teams.order_by('-points') for league in context['leagues']}
        context['teams_by_league'] = teams_by_league
        context['top_teams'] = Team.objects.all().order_by('-points')[:3]
        context['top_scorers'] = Player.objects.order_by('-goals')[:3]
        
        if query:
            context['matches'] = Match.objects.filter(
                home_team__name__icontains=query
            ) | Match.objects.filter(
                away_team__name__icontains=query
            )
            context['matches'] = context['matches'].order_by('-date')
        else:
            context['matches'] = None

        return context

    def get_queryset(self):
        """
        Returns a queryset of teams filtered by a search query if provided,
        otherwise all teams ordered by points.
        """
        query = self.request.GET.get('q')
        if query:
            
            return Team.objects.filter(name__icontains=query).order_by('-points')
        return Team.objects.all().order_by('-points')



class TeamDetailView(DetailView):
    """
    Displays details for a single team, including a list of matches they have played.
    """
    model = Team
    template_name = 'project/team_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        context['matches'] = Match.objects.filter(
            home_team=team
        ) | Match.objects.filter(
            away_team=team
        )
        context['matches'] = context['matches'].order_by('date')
        return context


class SignUpView(CreateView):
    """
    Handles user registration using the built-in UserCreationForm.
    """
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'project/signup.html'


class TeamCreateView(LoginRequiredMixin, CreateView):
    """
    Allows logged-in users to add a new team to the database.
    """
    model = Team
    fields = ['name', 'points', 'matches_played', 'wins', 'losses', 'ties', 'league']
    template_name = 'project/team_form.html'
    success_url = reverse_lazy('team-list')

    def get_context_data(self, **kwargs):
        """
        Adds an 'action' variable to the context to indicate 'Create'.
        """
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        return context

    def form_valid(self, form):
        """
        Ensures a default league is assigned if not provided.
        """
       
        if not form.instance.league:
            form.instance.league = League.objects.first()  
        return super().form_valid(form)

class TeamUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allows logged-in users to update an existing team's information.
    """
    model = Team
    fields = ['name', 'points', 'matches_played', 'wins', 'losses', 'ties']
    template_name = 'project/team_form.html'
    success_url = reverse_lazy('team-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Edit'
        return context


class TeamDeleteView(LoginRequiredMixin, DeleteView):
    """
    Allows logged-in users to delete a team.
    """
    model = Team
    template_name = 'project/team_confirm_delete.html'
    success_url = reverse_lazy('team-list')


from django.db.models import Q

class MatchListView(ListView):
    """
    Displays a list of matches with optional filtering by team name, date range,
    score range, and match status.
    """
    model = Match
    template_name = 'project/match_list.html'
    context_object_name = 'matches'

    def get_queryset(self):
        """
        Filters the match queryset based on the GET parameters provided in the request.
        Supports filtering by:
        - Team name (either home or away)
        - Date range
        - Score range (home and away scores)
        - Match status
        """
        queryset = Match.objects.all()
        team_query = self.request.GET.get('team')  
        start_date = self.request.GET.get('start_date')  
        end_date = self.request.GET.get('end_date') 
        min_home_score = self.request.GET.get('min_home_score')  
        max_home_score = self.request.GET.get('max_home_score')  
        min_away_score = self.request.GET.get('min_away_score')  
        max_away_score = self.request.GET.get('max_away_score')  
        status_query = self.request.GET.get('status')  

        # Filter by team name (either home or away)
        if team_query:
            queryset = queryset.filter(
                Q(home_team__name__icontains=team_query) | Q(away_team__name__icontains=team_query)
            )

        # Filter by date range
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        if min_home_score:
            queryset = queryset.filter(home_score__gte=min_home_score)
        if max_home_score:
            queryset = queryset.filter(home_score__lte=max_home_score)
        if min_away_score:
            queryset = queryset.filter(away_score__gte=min_away_score)
        if max_away_score:
            queryset = queryset.filter(away_score__lte=max_away_score)

        if status_query:
            queryset = queryset.filter(status__iexact=status_query)

        return queryset.order_by('-date')

    def get_context_data(self, **kwargs):
        """
        Adds filtering parameters back into the context to prepopulate the form.
        """
        context = super().get_context_data(**kwargs)
        context['team_query'] = self.request.GET.get('team', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        context['min_home_score'] = self.request.GET.get('min_home_score', '')
        context['max_home_score'] = self.request.GET.get('max_home_score', '')
        context['min_away_score'] = self.request.GET.get('min_away_score', '')
        context['max_away_score'] = self.request.GET.get('max_away_score', '')
        context['status_query'] = self.request.GET.get('status', '')
        return context

    
    


class MatchDetailView(DetailView):
    """
    Displays details for a single match.
    """
    model = Match
    template_name = 'project/match_detail.html'


class MatchDeleteView(DeleteView):
    """
    Allows users to delete a match.
    """
    model = Match
    template_name = 'project/match_confirm_delete.html'
    success_url = reverse_lazy('match-list')


class MatchUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allows logged-in users to update match results.
    """
    model = Match
    fields = ['home_score', 'away_score', 'status']
    template_name = 'project/match_update_form.html'
    success_url = reverse_lazy('match-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.update_team_stats(self.object)
        return response

    def get_context_data(self, **kwargs):
        """
        Adds the current match to the context data.
        """
        context = super().get_context_data(**kwargs)
        context['match'] = self.object  
        return context

    @staticmethod
    def update_team_stats(match):
        """
        Updates the stats of the home and away teams based on match results.
        """
        if match.home_score > match.away_score:
            match.home_team.wins += 1
            match.away_team.losses += 1
            match.home_team.points += 3
        elif match.home_score < match.away_score:
            match.away_team.wins += 1
            match.home_team.losses += 1
            match.away_team.points += 3
        else:
            match.home_team.ties += 1
            match.away_team.ties += 1
            match.home_team.points += 1
            match.away_team.points += 1
        match.home_team.matches_played += 1
        match.away_team.matches_played += 1
        match.home_team.save()
        match.away_team.save()


class MatchCreateView(LoginRequiredMixin, CreateView):
    """
    Allows logged-in users to create a new match.
    """
    model = Match
    form_class = MatchForm
    template_name = 'project/match_form.html'
    success_url = reverse_lazy('match-list')