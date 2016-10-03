'''
Created on Sep 23, 2016

@author: tomd
'''

import pickle
import config

from core.distributerating import simpleeventratings, xgweightedeventratings
from core.phase import getmatchphases
from core.rating import isgoal, expgoal
from db.qry import getmatchids, storeeventratings, createeventratingstable
from tools.dbhelper import Connection
from tools.functional import logmap


def ratematch(c,matchid,ratefn,distributefn,table):
    print matchid
    phases = getmatchphases(c, matchid)
    ratings = []
    for phase in phases:
        rating = ratefn(phase)
        eventratings = distributefn(phase, rating)
        ratings += eventratings
    storeeventratings(c, ratings, table)

def rateevents(c, ratefn, distributefn, table):
        createeventratingstable(c,table)
        
        matchids = getmatchids(c)
        def rate(x):
            ratematch(c, x, ratefn, distributefn, table)
        logmap(rate, matchids)
        
def console(c):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-isgoal', action = 'store_const', const=True,
                        default= False)
    parser.add_argument('-expgoal', action = 'store_const', const=True,
                        default= False)
    parser.add_argument('-pogba', action = 'store_const', const=True,
                        default= False)
    parser.add_argument('-xgweighted', action = 'store_const', const=True,
                        default= False)
    
    args = parser.parse_args()
    if args.xgweighted:
        with open(config.xgmodel,'rb') as fh:
            xgmodel = pickle.load(fh)
        def distributefn(phase,rating):
            return xgweightedeventratings(phase, rating, xgmodel)
    else:
        distributefn = simpleeventratings
        
    if args.isgoal:
        print "building table isgoalrating..."
        rateevents(c, isgoal, distributefn, 'isgoalrating')
        
    if args.expgoal:
        print "building table expgoalrating..."
        with open(config.xgmodel, 'rb') as fh:
            xgmodel = pickle.load(fh)
        rateevents(c, lambda x: expgoal(x, xgmodel),
                   distributefn, 'expgoalrating')

if __name__ == '__main__':
    with Connection(config.epl2012db) as c:
        console(c)
        