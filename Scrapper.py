# Work in progress ( has some reduntant code) 

import requests
from bs4 import BeautifulSoup
import re


class Team:
    def __init__(self, location, name, conference, division,
                 seasonStartingYear, regularSeasonWins, regularSeasonLosses,
                 players):
        self.location = location
        self.name = name
        self.conference = conference
        self.division = division
        self.seasonStartingYear = seasonStartingYear
        self.regularSeasonWins = regularSeasonWins
        self.regularSeasonLosses = regularSeasonLosses
        self.players = players

    def __repr__(self):
        return str("location:" + self.location + ", name: " + self.name +
                   ", conference: " + self.conference + ", division: " +
                   self.division + ", seasonStartingYearL " +
                   self.seasonStartingYear + ", regularSeasonWins: " +
                   self.regularSeasonWins + ", regularSeasonLoses: " +
                   self.regularSeasonLosses)


#   def __str__(self):
#      return (str(self.location) + " " + str(self.name))

Teams = []
URL = 'https://www.basketball-reference.com/teams/'
page = requests.get(
    URL,
    headers={
        'user-agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    })

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find("div", {"id": "all_teams_active"})

teamsFullTable = results.find_all("tr", {"class": "full_table"})

for team in teamsFullTable:
    location = ""
    seasonStartingYear = ""
    regularSeasonWins = ""
    regularSeasonLosses = ""
    players = []
    
    name = team.find("th", {"data-stat": "franch_name"}).get_text()
    division = team.find("td", {
        "data-stat": "years_division_champion"
    }).get_text()
    conference = team.find("td", {
        "data-stat": "years_conference_champion"
    }).get_text()
    
    Teams.append(
        Team(location, name, conference, division, seasonStartingYear,
             regularSeasonWins, regularSeasonLosses, players))

teamsPartialTable = results.find_all("tr", {"class": "partial_table"})
for team in teamsPartialTable:
    location = ""
    seasonStartingYear = ""
    regularSeasonWins = ""
    regularSeasonLosses = ""
    players = []
    
    name = team.find("th", {"data-stat": "team_name"}).get_text()
    division = team.find("td", {
        "data-stat": "years_division_champion"
    }).get_text()
    conference = team.find("td", {
        "data-stat": "years_conference_champion"
    }).get_text()
    
    Teams.append(
        Team(location, name, conference, division, seasonStartingYear,
             regularSeasonWins, regularSeasonLosses, players))

for team in Teams:
    print(team)
