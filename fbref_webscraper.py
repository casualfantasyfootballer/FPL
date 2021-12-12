import requests
import pandas as pd
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from fpl import FPL
from operator import itemgetter
import unidecode

#Players ID's, Names & Teams from FPL
async def main():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        player = await fpl.get_players(return_json=True)
    return player

async def all_teams_info():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        teams = await fpl.get_teams(return_json=True)
    return teams

all_teams = asyncio.run(all_teams_info())
all_players = asyncio.run(main())
all_player_list = list(all_players)
fpl_players = []

for i in range(len(all_player_list)):
        player = []
        player.append(all_player_list[i]['id'])
        player.append(unidecode.unidecode(all_player_list[i]["web_name"]))
        player.append(all_player_list[i]["first_name"])
        player.append(all_player_list[i]["second_name"])
        player.append(all_teams[int(all_player_list[i]["team"])-1]['name'])
        player.append(int(all_player_list[i]["team"]))
        fpl_players.append(player)

#sort by web name
fpl_players = sorted(fpl_players, key=itemgetter(1))

#players & URL's from FBRef
url = "https://fbref.com/en/comps/9/Premier-League-Stats"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

team_urls = []

for row in soup.findAll('table')[0].tbody.findAll('tr'):
        team = []
        team_name = row.findAll('td')[0].find('a').text
        team_url = row.findAll('td')[0].find('a').get('href')
        team.append(team_name)
        team.append(team_url)
        team_urls.append(team)

#change team names to match fantasy premier league
for i, team in enumerate(team_urls):
        if team[0] == 'Leicester City':
                team[0] = 'Leicester'
        elif team[0] == 'Leeds United':
                team[0] = 'Leeds'
        elif team[0] == 'Manchester City':
                team[0] = 'Man City'
        elif team[0] == 'Manchester United':
                team[0] = 'Man Utd'
        elif team[0] == 'Newcastle United':
                team[0] = 'Newcastle'
        elif team[0] == 'Norwich City':
                team[0] = 'Norwich'
        elif team[0] == 'Tottenham':
                team[0] = 'Spurs'

team_base_url = "https://fbref.com"

for i in range(len(team_urls)):
        players = []
        url = team_base_url + team_urls[i][1]
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')   
        for row in soup.findAll('table')[0].tbody.findAll('tr'):
                player = []
                player_name = row.findAll('th')[0].find('a').text.split()
                player_url = row.findAll('th')[0].find('a').get('href')
                for name in player_name:
                        player.append(unidecode.unidecode(name))
                player.append(team_urls[i][0])
                player.append(player_url)
                players.append(player)
        team_urls[i].append(players)

fbref_players = sorted(team_urls, key=itemgetter(0))

#Match FPL to FBRef
for i in range(len(fpl_players)):
        team_to_check = fpl_players[i][5]-1
        #leeds & leicester have incorrect ID's when in alphabetical order, accountning for above line of code
        if team_to_check == 8:
                team_to_check = 9
        elif team_to_check == 9:
                team_to_check = 8
        fpl_surname_to_check = unidecode.unidecode(fpl_players[i][1]).lower().split()
        #matched = 0
        for j in range(len(fbref_players[team_to_check][2])): 
                fbref_surname_to_check = unidecode.unidecode(fbref_players[team_to_check][2][j][-3]).lower().split()
                #check display name, most occurance
                if fbref_surname_to_check[-1] == fpl_surname_to_check[-1]:
                        fpl_players[i].append(fbref_players[team_to_check][2][j][-1])
                #check first name e.g Son
                elif fbref_players[team_to_check][2][j][0].lower() == fpl_surname_to_check[0]:
                        fpl_players[i].append(fbref_players[team_to_check][2][j][-1])
                #check first name and last name for FPL players A.Armstrong
                elif fbref_players[team_to_check][2][j][0].lower() == fpl_players[i][2].lower() and fbref_surname_to_check[-1] == fpl_players[i][3].lower() :
                        fpl_players[i].append(fbref_players[team_to_check][2][j][-1])
                #check for surnames without '-' e.g Smith-Rowe
                elif fbref_surname_to_check[-1] == "smith-rowe" and fpl_surname_to_check[-1] == "rowe":
                        fpl_players[i].append(fbref_players[team_to_check][2][j][-1])
        #print(fpl_players[i][1] + " Matched: " + str(matched))

print(fpl_players)





