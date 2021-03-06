'''
Created on Sep 23, 2016

@author: tomd
'''

import pickle
import config

from core.distributerating import simpleeventratings, xgweightedeventratings
from core.phase import getmatchphases, getallphases
from core.rating import isgoal, expgoal, pogba
from db.qry import getmatchids, storeeventratings, createeventratingstable
from tools.dbhelper import Connection
from tools.functional import logmap
from tools.timefn import Timer
from pogba.vptree import VPTree
import os
import time


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

def gettable(args):
    if args.pogba:
        if args.expgoal:
            table = "pogbaexppgoalrating"
        elif args.isgoal:
            table = "pogbaisgoalrating"
        else:
            raise Exception("No valid rating function given")
    elif args.isgoal:
        table = "isgoal"
    elif args.expgoal:
        table = "expgoal"
    else:
        print "Exception: No valid rating function given"
        raise Exception("No valid rating function given")
    return table

def getdistributefn(args):
    if args.xgweighted:
        with open(config.xgmodel,'rb') as fh:
            xgmodel = pickle.load(fh)
        def distributefn(phase,rating):
            return xgweightedeventratings(phase, rating, xgmodel)
    else:
        distributefn = simpleeventratings
    return distributefn

def getratefn(args):

    if args.pogba:
        with open(config.phasetree,'rb') as fh, Timer('loading phasetree'):
            phasetree = pickle.load(fh)
    if args.expgoal:
        with open(config.xgmodel,'rb') as fh, Timer('loading xgmodel'):
            xgmodel = pickle.load(fh)
            
    if args.pogba:
        if args.expgoal:
            def ratefn(x):
                return pogba(x,phasetree,args.k,lambda x: expgoal(x,xgmodel))
        else:
            def ratefn(x):
                return pogba(x,phasetree,args.k,isgoal)
    elif args.isgoal:
        ratefn = isgoal
    elif args.expgoal:
        def ratefn(x):
            return expgoal(x,xgmodel)
    return ratefn

def execute(c, args, table, folder):
        matchids = getmatchids(c)
        nb = len(matchids)
        step = float(nb)/args.n
        start  = int((args.i)*step)
        end = int((args.i+1)*step) if args.i < args.n - 1 else nb
        with Timer("loading matches %d to %d from %d matches" % (start,end,nb)):
            phases = getallphases(c,matchids[start:end],relevant=True)
        
        ratefn = getratefn(args)
        distributefn = getdistributefn(args)
        def getactionratings(phase):
            rating = ratefn(phase)
            return distributefn(phase, rating)
        
        ratingss = logmap(getactionratings, phases)
        ratings = [r for ratings in ratingss for r in ratings]
        with Timer("Dumping action ratings"):
            fh = open("%s%s-%d.pkl" % (folder,table, args.i),'wb')
            pickle.dump(ratings,fh)

def storeindatabase(c, args, folder):
    cnt = 0
    while True:
        dumps = filter(lambda x: ".pkl" in x, os.listdir(folder))
        if dumps:
            for dump in dumps:
                table = dump.split("-")[0]
                with Timer("storing %s in database" % dump):
                    ratings = pickle.load(open(folder + dump,'rb'))
                    storeeventratings(c, ratings, table)
                    os.remove(folder + dump)
                cnt+=1
            if cnt >= args.n - 1:
                print "%d dumps stored, shutting down." % args.n
                break
        else:
            time.sleep(2)
    
def console():
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
    parser.add_argument("-k", nargs="?", type=int, default=50)
    parser.add_argument("-n", nargs="?", type=int, default=1)
    parser.add_argument("-i", nargs="?", type=int, default=0)
    parser.add_argument('-create', action = 'store_const', const=True,
                        default= False)
    parser.add_argument('-store', action = 'store_const', const=True,
                        default= False)
    
    return parser.parse_args()

if __name__ == '__main__':
    args = console()
    with Connection(config.epl2012db) as c:
        if args.store:
            storeindatabase(c, args, config.tmpratingsfolder)
        else:
            table = gettable(args)
            if args.create:
                print "creating table %s" % table
                createeventratingstable(c, table)
            else:
                execute(c, args, table, config.tmpratingsfolder)
        
        