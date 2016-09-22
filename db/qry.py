'''
Created on Sep 22, 2016

Functions for frequent queries

@author: tomd
'''
from tools.functional import fst

def getmatchids(c):
    qry = "select id from match"
    return map(fst, c.execute(qry).fetchall())

def getteams(c,matchid):
    qry = "select hometeamid,awayteamid from match where id = ?"
    return c.execute(qry,(matchid,)).fetchone()