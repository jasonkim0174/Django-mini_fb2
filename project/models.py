"""Description: Defines the database models for the application, including League, Team, Match, and Player. 
             These models represent the structure and relationships of the data, such as teams belonging 
             to leagues, matches involving teams, and players associated with teams. Includes methods for 
             updating match results and calculating team stats."""


from django.db import models


class League(models.Model):
    """
    Represents a football league.
    Attributes:
    - logo: Optional logo for the league.
    - season: The season of the league (e.g., "2023-2024").
    - league_type: The type of the league, selected from predefined options (e.g., Premier League, La Liga).
    """
    LEAGUE_TYPES = [
        ('Premier League', 'Premier League'),
        ('La Liga', 'La Liga'),
        ('Serie A', 'Serie A'),
    ]

    logo = models.ImageField(upload_to='league_logos/', null=True, blank=True)  
    season = models.CharField(max_length=20)
    league_type = models.CharField(
        max_length=50,
        choices=LEAGUE_TYPES,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.season} - {self.get_league_type_display()}"


class Team(models.Model):
    """
    Represents a team participating in a league.
    Attributes:
    - name: The name of the team.
    - points: The team's current points in the league.
    - matches_played: The number of matches the team has played.
    - wins, losses, ties: Records of wins, losses, and ties for the team.
    - league: Foreign key to the League the team belongs to.
    - player_of_the_season: Optional reference to the team's Player of the Season.
    """
    name = models.CharField(max_length=100)
    points = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    ties = models.IntegerField(default=0)
    
    # ForeignKey to League (a team belongs to one league)
    league = models.ForeignKey(
        "League", on_delete=models.CASCADE, related_name="teams"
    )
    
    # ForeignKey to Player (Player of the Season)
    player_of_the_season = models.ForeignKey(
        "Player", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="highlighted_teams"
    )

    def __str__(self):
        return self.name


class Match(models.Model):
    """
    A model representing a match.

    Fields:
    - `home_team`, `away_team`: Foreign keys linking to the participating teams.
    - `home_score`, `away_score`: Scores for the home and away teams.
    - `time`, `date`: Time and date of the match.
    - `status`: Indicates whether the match is scheduled or completed.
    """
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    time = models.TimeField(null=True, blank=True)
    date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed')],
        default='Scheduled'
    )

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.date}"

    def record_result(self):
        """
        Updates the teams' stats based on the match result.
        - Updates wins, losses, and ties.
        - Calculates points based on wins and ties.
        - Saves the updated team records.
        """
        if self.status == 'Completed':
            if self.home_score > self.away_score:
                self.home_team.wins += 1
                self.away_team.losses += 1
            elif self.home_score < self.away_score:
                self.away_team.wins += 1
                self.home_team.losses += 1
            else:
                self.home_team.ties += 1
                self.away_team.ties += 1

            self.home_team.points = self.home_team.wins * 3 + self.home_team.ties
            self.away_team.points = self.away_team.wins * 3 + self.away_team.ties

            self.home_team.matches_played += 1
            self.away_team.matches_played += 1

            self.home_team.save()
            self.away_team.save()


class Player(models.Model):
    """
    A model representing a player.

    Fields:
    - `name`: Name of the player.
    - `age`: Age of the player.
    - `position`: Position the player plays (e.g., forward, midfielder).
    - `team`: Foreign key linking the player to their team.
    - `goals`, `assists`, `matches_played`: Stats for the player.
    """
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    position = models.CharField(max_length=50)
    team = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.position} - {self.team.name})"

