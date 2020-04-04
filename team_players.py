import pandas as pd
from requests import get
from bs4 import BeautifulSoup
import requests

try:
    from constants import TEAM_TO_TEAM_ABBR
except:
    from basketball_reference_scraper.constants import TEAM_TO_TEAM_ABBR

try:
    from utils import get_player_suffix
except:
    from basketball_reference_scraper.utils import get_player_suffix



# get static information ("franchise", "div" and "conf") for all team
def get_team_misc():
    r = get("https://www.basketball-reference.com/teams")
    df = None
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        # print(table)
        df = pd.read_html(str(table))[0]
        df1 = df[['Franchise', 'Lg', 'Div', 'Conf']]
        return df1


def get_team_stats(season_end_year):
    r = get(
        f'https://www.basketball-reference.com/leagues/NBA_{season_end_year}.html'
    )
    df = None
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        tables = soup.findAll('table')
        df = pd.read_html(str(tables))[0]
        df1 = df[['Eastern Conference', 'W', 'L']]
        # df = pd.read_html(str(tables))[1]
        # df1 = df[['Western Conference', 'W', 'L']]
        return df1


def get_team_players(team, season_end_year):
    r = get(
        f'https://www.basketball-reference.com/teams/{team}/{season_end_year}.html'
    )
    df = None
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        tables = soup.findAll('table')
        df = pd.read_html(str(tables))[0]
        return df


def get_player_stats(name, stat_type='PER_GAME', playoffs=False, career=False):
    suffix = get_player_suffix(name).replace('/', '%2F')
    selector = stat_type.lower()
    if playoffs:
        selector = 'playoffs_' + selector
    r = get(
        f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url={suffix}&div=div_{selector}'
    )
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        df.rename(columns={
            'Season': 'SEASON',
            'Age': 'AGE',
            'Tm': 'TEAM',
            'Lg': 'LEAGUE',
            'Pos': 'POS'
        },
                  inplace=True)
        career_index = df[df['SEASON'] == 'Career'].index[0]
        print(career_index)
        if career:
            df = df.iloc[career_index + 2:, :]
        else:
            df = df.iloc[:career_index, :]

        df = df.reset_index().dropna(axis=1).drop('index', axis=1)
        return df


# print(get_team_misc())
# print(get_team_stats(2020))
print(get_team_players('TOR', 2020))
# print(get_player_stats('Kyle Lowry'))
