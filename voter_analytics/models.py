from django.db import models
import csv
from datetime import datetime

class Voter(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.CharField(max_length=20)
    
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    voter_score = models.IntegerField()

    def __str__(self):
        return f'{self.first_name} {self.last_name} - Precinct {self.precinct_number}'


def load_data(filepath='voter_analytics/newton_voters.csv'):
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Voter.objects.create(
                last_name=row['Last Name'],
                first_name=row['First Name'],
                street_number=row['Residential Address - Street Number'],
                street_name=row['Residential Address - Street Name'],
                apartment_number=row['Residential Address - Apartment Number'] or None,
                zip_code=row['Residential Address - Zip Code'],
                date_of_birth=datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date(),
                date_of_registration=datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date(),
                party_affiliation=row['Party Affiliation'],
                precinct_number=row['Precinct Number'],
                v20state=row['v20state'].strip().lower() == 'true',
                v21town=row['v21town'].strip().lower() == 'true',
                v21primary=row['v21primary'].strip().lower() == 'true',
                v22general=row['v22general'].strip().lower() == 'true',
                v23town=row['v23town'].strip().lower() == 'true',
                voter_score=int(row['voter_score']),
            )
