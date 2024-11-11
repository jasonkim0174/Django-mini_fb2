from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import Q
from django.core.paginator import Paginator
import plotly.express as px
import pandas as pd

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset()
        
        party = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        
        elections = {
            'v20state': self.request.GET.get('v20state'),
            'v21town': self.request.GET.get('v21town'),
            'v21primary': self.request.GET.get('v21primary'),
            'v22general': self.request.GET.get('v22general'),
            'v23town': self.request.GET.get('v23town'),
        }

        if party:
            queryset = queryset.filter(party_affiliation=party)
        if min_dob:
            queryset = queryset.filter(date_of_birth__gte=min_dob)
        if max_dob:
            queryset = queryset.filter(date_of_birth__lte=max_dob)
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
        
        for election, value in elections.items():
            if value == 'on':  
                queryset = queryset.filter(**{election: True})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['voter_scores'] = list(range(0, 6))  
        return context
    
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'


class GraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        party = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        
        elections = {
            'v20state': self.request.GET.get('v20state'),
            'v21town': self.request.GET.get('v21town'),
            'v21primary': self.request.GET.get('v21primary'),
            'v22general': self.request.GET.get('v22general'),
            'v23town': self.request.GET.get('v23town'),
        }

        if party:
            queryset = queryset.filter(party_affiliation=party)
        if min_dob:
            queryset = queryset.filter(date_of_birth__gte=min_dob)
        if max_dob:
            queryset = queryset.filter(date_of_birth__lte=max_dob)
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
        
        for election, value in elections.items():
            if value == 'on':  
                queryset = queryset.filter(**{election: True})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['voter_scores'] = list(range(0, 6)) 
        filtered_voters = self.get_queryset().values()
        df = pd.DataFrame(filtered_voters)

        if not df.empty:
            birth_year_hist = px.histogram(
                df,
                x='date_of_birth',
                title='Voter distribution by Year of Birth',
                nbins=30
            )
            context['birth_year_graph'] = birth_year_hist.to_html(full_html=False)

            party_pie_chart = px.pie(
                df,
                names='party_affiliation',
                title='Voter distribution by Party Affiliation',
                hole=0.4
            )
            context['party_affiliation_graph'] = party_pie_chart.to_html(full_html=False)

            election_columns = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
            election_counts = df[election_columns].sum().reset_index(name='count')
            election_counts.columns = ['election', 'count']
            vote_count_chart = px.bar(
                election_counts,
                x='election',
                y='count',
                title='Vote Count by Election'
            )
            context['vote_count_graph'] = vote_count_chart.to_html(full_html=False)
        else:
            context['birth_year_graph'] = "No data available for the selected filters."
            context['party_affiliation_graph'] = "No data available for the selected filters."
            context['vote_count_graph'] = "No data available for the selected filters."

        return context