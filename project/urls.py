"""Description: Defines the URL patterns for the application, mapping views to specific routes. Includes paths 
             for team and match CRUD operations, user authentication (login and logout), and user registration.
             File: admin.py
            Author: Jason Kim
            Email: jasonkim@bu.edu
            Date: December 10, 2024
             
             """

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    TeamListView, TeamDetailView, TeamCreateView,
    TeamUpdateView, TeamDeleteView, MatchListView,
    MatchDetailView, SignUpView, MatchUpdateView, MatchCreateView,
    MatchDeleteView
)

urlpatterns = [
    path('', TeamListView.as_view(), name='team-list'), 
    path('teams/', TeamListView.as_view(), name='team-list'),
    path('<int:pk>/', TeamDetailView.as_view(), name='team-detail'),
    path('add/', TeamCreateView.as_view(), name='team-add'),
    path('<int:pk>/edit/', TeamUpdateView.as_view(), name='team-edit'),
    path('<int:pk>/delete/', TeamDeleteView.as_view(), name='team-delete'),
    path('matches/', MatchListView.as_view(), name='match-list'),
    path('matches/add/', MatchCreateView.as_view(), name='match-add'),
    path('matches/<int:pk>/edit/', MatchUpdateView.as_view(), name='match-edit'),
    path('matches/<int:pk>/delete/', MatchDeleteView.as_view(), name='match-delete'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='team-list'), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    
]
