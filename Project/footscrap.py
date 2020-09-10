import requests
from Team import Team
from bs4 import BeautifulSoup
from team_codes import team_codes
import string
import re


def get_match_links(team):
    url = 'https://fbref.com/en/squads/{}/2019-2020/matchlogs/s3260/schedule/{}-Scores-and-Fixtures-Serie-A'.format(team_codes[team], team)
    response = requests.get(url)
    url_format = 'https://fbref.com'

    soup = BeautifulSoup(response.text.encode("utf-8"), 'html.parser')
    table = soup.find('div', {'id': 'all_matchlogs_3260'}).find('div', {'class': 'table_outer_container'}).find('div', {'id': 'div_matchlogs_3260'}).find('table', {'id': 'matchlogs_3260'})
    res = table.findAll('tr')
    match_links = []
    for tr in res:
        cols = tr.findAll('td')
        # print(cols)
        if len(cols) > 0:
            match = cols[15].find('a')
            if match:
                match_links.append(match.get('href'))
    match_links = [url_format + x for x in match_links]
    return match_links

def get_match_stats(links):
    teams = {}

    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text.encode("utf-8"), 'html.parser')
        home_team_stats, away_team_stats = {}, {}

        table = soup.find('div', {'id': 'team_stats'}).find('table').findAll('tr')
        i = 0
        facts_list = []
        for row in table:
            stats = row.findAll('td')
            for r in stats:
                x = r.findAll('div')[1]
                y = str(x).strip('</div><strong></strong>')
                y = "".join([ch for ch in y if ch in string.printable])
                facts_list.append(y)
        home_team_stats = {'possession' : int(facts_list[0][:2]),
                           'good_passes': int( (facts_list[2][:facts_list[2].find('<')]).split('of')[0] ),
                           'total_passes' : int( (facts_list[2][:facts_list[2].find('<')]).split('of')[1] ),
                           'shots_target' : int( (facts_list[4][:facts_list[4].find('<')]).split('of')[0] ),
                           'total_shots' : int( (facts_list[4][:facts_list[4].find('<')]).split('of')[1] ),
                           'saves' : int( (facts_list[6][:facts_list[6].find('<')]).split('of')[0] ),
                           'opp_attempts' : int( (facts_list[6][:facts_list[6].find('<')]).split('of')[1] )
                           }
        away_team_stats = {'possession' : int(facts_list[1][:2]),
                           'good_passes': int( (facts_list[3][facts_list[3].find('>') + 1:]).split('of')[0] ),
                           'total_passes' : int( (facts_list[3][facts_list[3].find('>') + 1:]).split('of')[1] ),
                           'shots_target' : int( (facts_list[5][facts_list[5].find('>') + 1:]).split('of')[0] ),
                           'total_shots' : int( (facts_list[5][facts_list[5].find('>') + 1:]).split('of')[1] ),
                           'saves' : int( (facts_list[7][facts_list[7].find('>') + 1 :]).split('of')[0] ),
                           'opp_attempts' : int( (facts_list[7][facts_list[7].find('>')+ 1: ]).split('of')[1] )
                           }

        teams = link[38:]
        home_team = teams.split('-')[0]
        away_team = teams.split('-')[1]


        print(home_team, home_team_stats)
        print(away_team, away_team_stats)
        print()
        # break




links = get_match_links('Parma')
# for l in links:
#     print(l)
#     print()
get_match_stats(links)


