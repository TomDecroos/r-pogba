'''
Created on Sep 23, 2016

@author: tomd
'''
from tools.dbhelper import Connection
from core.phase import getmatchphases
from db.qry import getmatchids, storeeventratings, createeventratingstable
from core.rating import isgoal, geteventratings
from tools.functional import logmap
import config


def ratematch(c,matchid,ratefn,table):
    phases = getmatchphases(c, matchid)
    ratings = []
    for phase in phases:
        rating = ratefn(phase)
        eventratings = geteventratings(phase, rating)
        ratings += eventratings
    storeeventratings(c, ratings, table)

def rateevents(dbfile, ratefn, table):
    with Connection(dbfile) as c:
        createeventratingstable(c,table)
        
        matchids = getmatchids(c)
        def rate(x):
            ratematch(c, x, ratefn, table)
        logmap(rate, matchids)

if __name__ == '__main__':
    rateevents(config.db_small, isgoal, 'isgoalrating')