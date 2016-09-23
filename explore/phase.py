'''
Created on Sep 22, 2016

@author: tomd
'''
import matplotlib.pyplot as plt
import config
from tools.dbhelper import Connection
from db.qry import getmatchids
from core.phase import getmatchphases, getallphases
from numpy import mean, std
from pprint import pprint
from explore.event import plotevents
from tools.time import sectomin

def nbhist(phases):
    x = map(lambda x: x.nbevents(), phases)
    plt.hist(x)
    plt.title("Nb of events in phase")
    plt.show()

def durhist(phases):
    x = map(lambda x: x.duration(), phases)
    plt.hist(x)
    plt.title("Duration of phase")
    plt.show()

def longestphase(phases):
    return max(phases, key = lambda x: x.duration())

def stats(phases):
    print "n: %s" % len(phases)
    nbs = map(lambda x: x.nbevents(), phases)
    durs = map(lambda x: x.duration(), phases)
    print "nbevents avg: %2.2f std: %2.2f" % (mean(nbs), std(nbs))
    print "duration avg: %2.2f std: %2.2f" % (mean(durs), std(durs))
    print "playtime: %dm%ds" % sectomin(sum(durs))
    
def plotphases(phases):
    for phase in phases:
        plotevents(phase.events,phase.hometeamid,phase.awayteamid)

def plotphasesconsecutive(phases):
    events = []
    for phase in phases:
        events += phase.events
    plotevents(events, phases[0].hometeamid, phases[0].awayteamid)

def console():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-matchnb", nargs="?", type=int, default=0)
    parser.add_argument("-maxdistfirst", nargs="?", type=int, default=20)
    parser.add_argument("-maxdistlast", nargs="?", type=int, default=10)
    parser.add_argument("-minnbevents", nargs="?", type=int, default=3)
    parser.add_argument('-plot', action = 'store_const', const=True,
                        default= False)
    parser.add_argument('-hist', action = 'store_const', const=True,
                        default= False)
    parser.add_argument('-stats', action = 'store_const', const=True,
                        default= False)
    parser.add_argument('-all', action = 'store_const', const=True,
                        default= False)
    parser.add_argument('-event', nargs ="?")
    args = parser.parse_args()
    
    with Connection(config.db_small) as c:
        ids = getmatchids(c)
        if args.all:
            phases = getallphases(c,ids, args.maxdistfirst,
                                  args.maxdistlast, args.minnbevents)
        else:
            phases = getmatchphases(c,ids[args.matchnb], args.maxdistfirst,
                                args.maxdistlast, args.minnbevents)
        if args.event:
            phases = filter(lambda x: x.hasevent(args.event), phases)
            
        if args.stats:
            stats(phases)
        if args.hist:
            nbhist(phases)
            durhist(phases)
        if args.plot:
            plotphases(phases)

if __name__ == '__main__':
    console()
#     with Connection(config.db_small) as c:
#         ids = getmatchids(c)
#         phases = getmatchphases(c,ids[0])
#         plotphasesconsecutive(phases[2:5])