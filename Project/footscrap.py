import requests
from bs4 import BeautifulSoup

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

links = get_match_links('Juventus')

for link in links:
    response = requests.get(link)
    soup = BeautifulSoup(response.text.encode("utf-8"), 'html.parser')

    table = soup.find('div', {'id': 'team_stats'}).find('table').findAll('tr')
    for row in table:
        # print(row)
        if row.find("Possession") != -1:
            print(row, [...])

    break

    # res = table.findAll('tr')
    # for row in res:
    #     print(res, [...])
