from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import Count
import pandas as pd  
import plotly.express as px
from datetime import datetime
from plotly.io import to_html




class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = Voter.objects.all()

        party = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']

        if party:
            queryset = queryset.filter(party_affiliation=party.strip())
        if min_dob:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_dob))
        if max_dob:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_dob))
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))
        for election in elections:
            if self.request.GET.get(election):
                queryset = queryset.filter(**{election: True})

        unique_voters = {}
        unique_queryset = []
        for voter in queryset:
            unique_key = (voter.first_name, voter.last_name, voter.date_of_birth, voter.party_affiliation)
            if unique_key not in unique_voters:
                unique_voters[unique_key] = True
                unique_queryset.append(voter)

        return unique_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        context['years'] = range(1900, datetime.now().year + 1)
        context['voter_scores'] = Voter.objects.values_list('voter_score', flat=True).distinct()
        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'


class GraphListView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'
    
    def get_queryset(self):
        queryset = Voter.objects.all()

        party = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']

        if party:
            queryset = queryset.filter(party_affiliation=party.strip())
        if min_dob:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_dob))
        if max_dob:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_dob))
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))
        for election in elections:
            if self.request.GET.get(election):
                queryset = queryset.filter(**{election: True})

        unique_voters = {}
        unique_queryset = []
        for voter in queryset:
            unique_key = (voter.first_name, voter.last_name, voter.date_of_birth, voter.party_affiliation)
            if unique_key not in unique_voters:
                unique_voters[unique_key] = True
                unique_queryset.append(voter)

        return unique_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        voters = self.get_queryset()

        birth_years = [voter.date_of_birth.year for voter in voters]
        birth_year_fig = px.histogram(birth_years, nbins=100, title="Voter Distribution by Year of Birth")
        context['birth_year_chart'] = to_html(birth_year_fig, full_html=False)

        party_counts = {}
        for voter in voters:
            party = voter.party_affiliation
            party_counts[party] = party_counts.get(party, 0) + 1
        party_fig = px.pie(
            names=list(party_counts.keys()),
            values=list(party_counts.values()),
            title="Voter Distribution by Party Affiliation"
        )

        context['party_affiliation_chart'] = to_html(party_fig, full_html=False)

        participation_data = {
            '2020 State': sum(voter.v20state for voter in voters),
            '2021 Town': sum(voter.v21town for voter in voters),
            '2021 Primary': sum(voter.v21primary for voter in voters),
            '2022 General': sum(voter.v22general for voter in voters),
            '2023 Town': sum(voter.v23town for voter in voters),
        }
        election_fig = px.bar(
            x=list(participation_data.keys()),
            y=list(participation_data.values()),
            title="Voter Participation in Elections"
        )
        context['election_participation_chart'] = to_html(election_fig, full_html=False)

        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        context['years'] = range(1900, datetime.now().year + 1)
        context['voter_scores'] = Voter.objects.values_list('voter_score', flat=True).distinct()
        
        return context