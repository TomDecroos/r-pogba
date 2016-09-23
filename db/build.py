'''
Created on Sep 19, 2016

@author: tomd
'''
import os
import pickle

import config
from tools.functional import logmap, errmap, errfilter
import xml.etree.ElementTree as ET
from pprint import pprint
from db.epl import eventsfile, statisticsfile
from tools.dbhelper import Mapping, add_row, add_rows, create_table, executefile,\
    Connection


# MATCH
matchmappings = [
    Mapping('competition_id', 'CompetitionID', 'int'),
    Mapping('season_id', 'SeasonID', 'int'),
    Mapping('game_date', 'GameData', 'text'),
    Mapping('away_team_id', 'AwayTeamID', 'int'),
    Mapping('home_team_id', 'HomeTeamID', 'int'),
]
matchextra = [("ID", "int primary key")]

def create_matchtable(c):
    create_table(c,'Match', matchmappings, matchextra)

def add_match(c,matchid):
    root = ET.parse(eventsfile(matchid)).getroot()
    extra = [("ID", matchid)]
    add_row(c,"Match", root, matchmappings, extra)

# EVENTS
eventmappings = [
    Mapping('id', 'OptaID', 'int'),
    Mapping('event_type_id', 'TypeID', 'int'),
    Mapping('x', 'X', 'real'),
    Mapping('y', 'Y', 'real'),
    Mapping('player_id', 'PlayerID', 'int'),
    Mapping('team_id', 'TeamID', 'int'),
    Mapping('outcome', 'Outcome', 'int'),
    Mapping('period_id', 'Period', 'int'),
    Mapping('period_minute', 'Minute', 'int'),
    Mapping('period_second', 'Second', 'int')
]
eventextra = [("MatchID", "int")]

def create_eventtable(c):
    create_table(c,'Event', eventmappings, eventextra)
    
def add_events(c,matchid):
    root = ET.parse(eventsfile(matchid)).getroot()
    events = errfilter(lambda x: x.tag != "DeletedEvent", root, 0.10)
    extra = [("MatchID", matchid)]
    add_rows(c,'Event', events, eventmappings, extra)

# EVENTTYPES:
def create_eventtypetable(c):
    executefile(c,config.eventtype_table)
    print "Table Eventtype successfully created"

# TEAMS

def create_teamtable(c):
    c.execute("""create table team
    (id int primary key on conflict replace,name text)""")
    print "Table Team successfully created"

def add_teams(c,matchid):
    root = ET.parse(statisticsfile(matchid)).getroot()
    for team in root[0].findall('Team'):
        teamid = int(team.attrib['uID'].replace("t",""))
        name = team.find('Name').text
        c.execute("insert into team values (?,?)", (teamid, name))
        
# PLAYERS
def create_playertable(c):
    c.execute("""create table player
    (id int primary key on conflict replace, first text, last text)""")
    print "Table Player successfully created"

def add_players(c,matchid):
    root = ET.parse(statisticsfile(matchid)).getroot()
    for team in root[0].findall('Team'):
        for player in team.findall('Player'):
            playerid = int(player.attrib["uID"].replace("p",""))
            name = player.find("PersonName")
            first = name.find("First").text
            last = name.find("Last").text
            c.execute("insert into player values (?,?,?)", 
                      (playerid, first, last))
        

def create_tables(c):
    create_matchtable(c)
    create_eventtable(c)
    create_eventtypetable(c)
    create_teamtable(c)
    create_playertable(c)
    
        
def fill_db(c,matchids):
    def add(matchid):
        add_match(c, matchid)
        add_events(c, matchid)
        add_teams(c,matchid)
        add_players(c, matchid)
    logmap(add, matchids)

def smalldb(dbfile,nb):
    os.remove(dbfile)
    with Connection(dbfile) as c:
        create_tables(c)
        epl = pickle.load(open(config.epl_matches, 'rb'))
        fill_db(c,epl[0:nb])
        
if __name__ == '__main__':
    smalldb(config.db_small,100)
       
        
    