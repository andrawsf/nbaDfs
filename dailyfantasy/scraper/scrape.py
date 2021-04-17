# standard library imports
import requests
import json
import os.path

# Third party imports
from bs4 import BeautifulSoup

# local application imports
from dailyfantasy import Player

def FixNbaPlayerNamesWithAccents(playerName):
    if ('Jonas V' in playerName):
        playerName = "Jonas Valanciunas"
    if ('Luka D' in playerName):
        playerName = "Luka Doncic"
    if ('Nikola J' in playerName):
        playerName = "Nikola Jokic"
    if ('Nikola V' in playerName):
        playerName = "Nikola Vucevic"
    if ('Goran D' in playerName):
        playerName = "Goran Dragic"
    return playerName

def GetCurrentSeasonPlayerStats():
    playerStatArray = []
    currentSeasonurl = 'https://www.basketball-reference.com/leagues/NBA_2021_per_game.html'
    lastSeasonurl = 'https://www.basketball-reference.com/leagues/NBA_2020_per_game.html'
    
    response = requests.get(currentSeasonurl, timeout = 5)
    siteContentCurrent = BeautifulSoup(response.content, "html.parser")
    response = requests.get(lastSeasonurl, timeout = 5)
    siteContentLast = BeautifulSoup(response.content, "html.parser")

    statTableCurrent = siteContentCurrent.find('table')
    statRowsCurrent = statTableCurrent.findAll('tr', attrs={"class":"full_table"})
    statTableLast = siteContentLast.find('table')
    statRowsLast = statTableLast.findAll('tr', attrs={"class":"full_table"})

    for currentStats in statRowsCurrent:
        currentStats.find('td', attrs={"data-stat": "player"}).a.contents[0] = FixNbaPlayerNamesWithAccents(currentStats.find('td', attrs={"data-stat": "player"}).a.contents[0])
        player = Player()
        player.fetchCurrentStats(currentStats)

        for PreviousStats in statRowsLast:
            PreviousStats.find('td', attrs={"data-stat": "player"}).a.contents[0] = FixNbaPlayerNamesWithAccents(PreviousStats.find('td', attrs={"data-stat": "player"}).a.contents[0])
            if(player.isSamePlayer(PreviousStats.find('td', attrs={"data-stat": "player"}).a.contents[0])):
                player.fetchPreviousStats(PreviousStats)
                playerStatArray.append(player.__dict__) # TODO - deal with rookies
        
    with open(r"..\data\playerData.json", 'w') as outfile:
       json.dump(playerStatArray, outfile)  
    