import requests
from Team import Team
from bs4 import BeautifulSoup
import string

def get_match_links(team):
    url = 'https://fbref.com/en/squads/e0652b02/{}'.format(team)
    response = requests.get(url)
    url_format = 'https://fbref.com'

    soup = BeautifulSoup(response.text.encode("utf-8"), 'html.parser')
    table = soup.find('table', {'id': 'ks_sched_all'})
    res = table.findAll('tr')
    match_links = []
    for tr in res:
        cols = tr.findAll('td')
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
                # print(str(x).strip('</div><strong></strong>').replace('<strong>', ''))
                y = str(x).strip('</div><strong></strong>')
                y = "".join([ch for ch in y if ch in string.printable])
                # print(y)
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

        extra = soup.find('div', {'id': 'team_stats_extra'})
        print(extra, [...])


        print(home_team_stats)
        print(away_team_stats)
        break




links = get_match_links('Juventus')
get_match_stats(links)



    # res = table.findAll('tr')
    # for row in res:
    #     print(res, [...])
