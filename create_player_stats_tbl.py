import sqlite3
from fpl import FPL
import aiohttp
import asyncio
import csv
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import unidecode

gameweek = int(input("Enter the GW No: "))
  
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
player_stats = []

###webscraped XG - matches up stats with ID's
site_url = 'https://understat.com/league/EPL/2021'

res = requests.get(site_url)
soup = BeautifulSoup(res.content, "lxml")

scripts = soup.find_all('script')

string_with_json_obj = ''

for el in scripts:
    if 'playersData' in str(el):
        string_with_json_obj = str(el).strip()

ind_start = string_with_json_obj.index("('")+2
ind_end = string_with_json_obj.index("')")
json_data = string_with_json_obj[ind_start:ind_end]

json_data = json_data.encode('utf8').decode('unicode_escape')
#turn json string into a list of dictionaries
json_players = list(eval(json_data))
#print(json_players[0])

for i in range(len(all_player_list)):
    player = {}
    player["id"] = all_player_list[i]["id"]
    player["name"] = all_player_list[i]["web_name"]
    player["team_id"] = all_player_list[i]["team"]
    player["expected_points"] = float(all_player_list[i]["ep_next"])
    player["total_points"] = int(all_player_list[i]["total_points"])
    player["assists"] = int(all_player_list[i]["assists"])
    player["bps"] = int(all_player_list[i]["bps"])
    player["awarded_bonus"] = int(all_player_list[i]["bonus"])
    player["goals"] = int(all_player_list[i]["goals_scored"])
    player["red_cards"] = int(all_player_list[i]["red_cards"])
    player["yellow_cards"] = int(all_player_list[i]["yellow_cards"])
    player["cost"] = float(all_player_list[i]["now_cost"])/10
    player["xg"] = 0
    player["xa"] = 0
    player["shots"] = 0
    player["key_passes"] = 0
    player["npxg"] = 0
    player["xgchain"] = 0
    player["xgbuildup"] = 0
    player_stats.append(player)

#change names from FPL as names from understat are different
for i in range(len(all_teams)):
    if all_teams[i]["name"] == "Man City":
        all_teams[i]["name"] = "Manchester City"
    elif all_teams[i]["name"] == "Man Utd":
        all_teams[i]["name"] = "Manchester United"
    elif all_teams[i]["name"] == "Newcastle":
        all_teams[i]["name"] = "Newcastle United"
    elif all_teams[i]["name"] == "Spurs":
        all_teams[i]["name"] = "Tottenham"
    elif all_teams[i]["name"] == "Wolves":
        all_teams[i]["name"] = "Wolverhampton Wanderers"

#print(player_stats)

for i in range(len(player_stats)):
    matched = 0
    for j in range(len(json_players)):
        name_to_check = json_players[j]["player_name"].split()
        fpl_name = player_stats[i]["name"].split()
        fpl_surname = fpl_name[-1].split(".")
        fpl_first_name = fpl_name[0]
        #last name = last name check, most
        if unidecode.unidecode(fpl_surname[-1].lower()) == unidecode.unidecode(name_to_check[-1].lower()):
            team_to_check = json_players[j]["team_title"].split(",")
            if all_teams[int(player_stats[i]["team_id"]-1)]["name"].lower() == team_to_check[0].lower():
                player_stats[i]["xg"] = round(float(json_players[j]["xG"]),2)
                player_stats[i]["xa"] = round(float(json_players[j]["xA"]),2)
                player_stats[i]["shots"] = int(json_players[j]["shots"])
                player_stats[i]["key_passes"] = int(json_players[j]["key_passes"])
                player_stats[i]["npxg"] = round(float(json_players[j]["npxG"]),2)
                player_stats[i]["xgchain"] = round(float(json_players[j]["xGChain"]),2)
                player_stats[i]["xgbuildup"] = round(float(json_players[j]["xGBuildup"]),2)
        #first name = last name check
        elif unidecode.unidecode(fpl_first_name.lower()) == unidecode.unidecode(name_to_check[-1].lower()):
            team_to_check = json_players[j]["team_title"].split(",")
            if all_teams[int(player_stats[i]["team_id"]-1)]["name"].lower() == team_to_check[0].lower():
                player_stats[i]["xg"] = round(float(json_players[j]["xG"]),2)
                player_stats[i]["xa"] = round(float(json_players[j]["xA"]),2)
                player_stats[i]["shots"] = int(json_players[j]["shots"])
                player_stats[i]["key_passes"] = int(json_players[j]["key_passes"])
                player_stats[i]["npxg"] = round(float(json_players[j]["npxG"]),2)
                player_stats[i]["xgchain"] = round(float(json_players[j]["xGChain"]),2)
                player_stats[i]["xgbuildup"] = round(float(json_players[j]["xGBuildup"]),2)
        #first name = first name check
        elif unidecode.unidecode(fpl_first_name.lower()) == unidecode.unidecode(name_to_check[0].lower()):
            team_to_check = json_players[j]["team_title"].split(",")
            if all_teams[int(player_stats[i]["team_id"]-1)]["name"].lower() == team_to_check[0].lower():
                player_stats[i]["xg"] = round(float(json_players[j]["xG"]),2)
                player_stats[i]["xa"] = round(float(json_players[j]["xA"]),2)
                player_stats[i]["shots"] = int(json_players[j]["shots"])
                player_stats[i]["key_passes"] = int(json_players[j]["key_passes"])
                player_stats[i]["npxg"] = round(float(json_players[j]["npxG"]),2)
                player_stats[i]["xgchain"] = round(float(json_players[j]["xGChain"]),2)
                player_stats[i]["xgbuildup"] = round(float(json_players[j]["xGBuildup"]),2)
        #first name = middle name check e.g tanguy ndombele alvaro
        elif len(name_to_check) > 1:
            if unidecode.unidecode(fpl_first_name.lower()) == unidecode.unidecode(name_to_check[1].lower()):
                team_to_check = json_players[j]["team_title"].split(",")
                if all_teams[int(player_stats[i]["team_id"]-1)]["name"].lower() == team_to_check[0].lower():
                    player_stats[i]["xg"] = round(float(json_players[j]["xG"]),2)
                    player_stats[i]["xa"] = round(float(json_players[j]["xA"]),2)
                    player_stats[i]["shots"] = int(json_players[j]["shots"])
                    player_stats[i]["key_passes"] = int(json_players[j]["key_passes"])
                    player_stats[i]["npxg"] = round(float(json_players[j]["npxG"]),2)
                    player_stats[i]["xgchain"] = round(float(json_players[j]["xGChain"]),2)
                    player_stats[i]["xgbuildup"] = round(float(json_players[j]["xGBuildup"]),2)
        #unique exception as fpl does not include a hyphen between name whereas understat does
        if player_stats[i]["name"].lower() == "smith rowe" and json_players[j]["player_name"].lower() == "emile smith-rowe": 
            player_stats[i]["xg"] = round(float(json_players[j]["xG"]),2)
            player_stats[i]["xa"] = round(float(json_players[j]["xA"]),2)
            player_stats[i]["shots"] = int(json_players[j]["shots"])
            player_stats[i]["key_passes"] = int(json_players[j]["key_passes"])
            player_stats[i]["npxg"] = round(float(json_players[j]["npxG"]),2)
            player_stats[i]["xgchain"] = round(float(json_players[j]["xGChain"]),2)
            player_stats[i]["xgbuildup"] = round(float(json_players[j]["xGBuildup"]),2)
    output = "Player: " + player_stats[i]["name"] + ", Matched: " + str(matched)
    #print(output)


#print(player_stats[3])
conn = sqlite3.connect("fpl.db")
c = conn.cursor()

#sqlite autoincrements ID if no value is given
for i in range(len(player_stats)):
    c.execute("INSERT INTO Player_Stats_tbl ( player_id, gw_id, next_gw_pred_points, total_points, gw_assists, gw_bps, awarded_bonus_points, gw_goals, gw_red, gw_yellow, cost, xg, xa, shots, key_passes, npxg, xg_chain, xg_buildup) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",\
                      (player_stats[i]["id"],gameweek,player_stats[i]["expected_points"],player_stats[i]["total_points"],player_stats[i]["assists"],player_stats[i]["bps"],player_stats[i]["awarded_bonus"],player_stats[i]["goals"],player_stats[i]["red_cards"],player_stats[i]["yellow_cards"],player_stats[i]["cost"],player_stats[i]["xg"],player_stats[i]["xa"],player_stats[i]["shots"],player_stats[i]["key_passes"],player_stats[i]["npxg"],player_stats[i]["xgchain"],player_stats[i]["xgbuildup"]))
conn.commit()

c.close()
