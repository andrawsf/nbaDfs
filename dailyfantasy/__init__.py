"""
This file implements a player object to be used to store statistics 
for players accross the dfs application.
"""
thisYear = 1
lastYear = 2

class SeasonStats:
    """
    includes standard stats for players collected during a season
    """
    def __init__(self):
        self.gamesPlayed = 0
        self.assists = 0 #all stats are per game
        self.steals = 0
        self.blocks = 0
        self.rebounds = 0
        self.turnovers = 0
        self.points = 0
        self.minutes = 0
    
    def fromHTML(self, tableRow):
        # follows formatting from basketball-reference.com
        self.gamesPlayed = float(tableRow.find('td', attrs={"data-stat": "g"}).contents[0])
        self.assists = float(tableRow.find('td', attrs={"data-stat": "ast_per_g"}).contents[0])
        self.steals = float(tableRow.find('td', attrs={"data-stat": "stl_per_g"}).contents[0])
        self.blocks = float(tableRow.find('td', attrs={"data-stat": "blk_per_g"}).contents[0])
        self.rebounds = float(tableRow.find('td', attrs={"data-stat": "trb_per_g"}).contents[0])
        self.turnovers = float(tableRow.find('td', attrs={"data-stat": "tov_per_g"}).contents[0])
        self.points = float(tableRow.find('td', attrs={"data-stat": "pts_per_g"}).contents[0])
        self.minutes = float(tableRow.find('td', attrs={"data-stat": "mp_per_g"}).contents[0])

    def calculateFPPG(self):
        self.fantasyPoints =    (self.points * 1)       + \
                                (self.rebounds * 1.2)   + \
                                (self.assists * 1.5)    + \
                                (self.steals * 3)       + \
                                (self.blocks * 3)       + \
                                (self.turnovers * -1)
        # check for div by zero
        if(self.minutes != 0.0):
            self.fantasyPointsPerMinute = self.fantasyPoints / self.minutes

class Player:
    """
    includes the name and position as well as previous stats
    """
    def __init__(self):
        self.name = ""
        self.position = ""
        self.playingTonight = True
        self.injured = False
        self.rookie = False
        self.team = ""
        self.opponent = ""
        self.salary = 0
        self.currentStats = SeasonStats()
        self.prevStats = SeasonStats()

    def fetchCurrentStats(self, tableRow):
        self.name = tableRow.find('td', attrs={"data-stat": "player"}).a.contents[0]
        self.position = tableRow.find('td', attrs={"data-stat": "pos"}).contents[0]
        self.currentStats.fromHTML(tableRow)
        self.currentStats.calculateFPPG()
        self.__dict__.update({'currentStats': self.currentStats.__dict__})

    def fetchPreviousStats(self, tableRow):
        if(self.name == tableRow.find('td', attrs={"data-stat": "player"}).a.contents[0]):
            self.prevStats.fromHTML(tableRow)
            self.prevStats.calculateFPPG()
            self.__dict__.update({'prevStats': self.prevStats.__dict__})
    
    def isSamePlayer(self, name):
        if(self.name == name):
            return True
        else:
            return False