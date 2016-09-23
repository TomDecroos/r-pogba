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

def storeeventratings(c, eventratings, table):
    qry = "insert into %s values (?,?)" % table
    c.executemany(qry, eventratings)
    
def createeventratingstable(c,table):
    qry = "drop table if exists %s" % table
    c.execute(qry)
    
    qry = "create table %s (eventrowid int primary key, rating float)" % table
    c.execute(qry)