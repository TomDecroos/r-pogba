'''
Created on Sep 22, 2016

@author: tomd
'''
import matplotlib.pyplot as plt
import config
from tools.dbhelper import Connection, getfields
from db.qry import getmatchids
from core.phase import getmatchphases, getallphases
from numpy import mean, std
from explore.event import plotevents, plotxy
from tools.timefn import sectomin

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

def plotphase(ax, phase):
    fieldnames = "X,Y,Name,TeamID,Outcome"
    x,y,name,teamid,outcome = getfields(phase.events,fieldnames)
    
    rating=None
    if 'rating' in phase.events[0].keys():
        rating, = getfields(phase.events,'rating')
    
    def correction(x,teamid):
        return x if teamid == phase.hometeamid else 1-x
    x = map(lambda x: correction(*x), zip(x, teamid))
    y = map(lambda x: correction(*x), zip(y, teamid))
    
    teamcolours = {phase.hometeamid : 'lightblue',
                   phase.awayteamid : 'yellow'}
    
    def choosecolors(teamid,outcome,name):
        box = teamcolours.get(teamid, 'white')
        edge = 'black' if (outcome==1 and name != 'turnover') else 'red'
        return box,edge
    
    colors = map(lambda x: choosecolors(*x), zip(teamid,outcome,name))
   
    if 'last' in phase.events[0].keys():
        last, = getfields(phase.events, 'last')
        labels = map(lambda a,b: a + " | " + b, last, name)
    else:
        labels = name
        
    plotxy(ax, x, y, colors, labels, rating)
    
def comparephases(phase1,phase2):
    fig = plt.figure()
    size = 11
    fig.set_size_inches(1.61*size,size, forward=True)
    ax1 = plt.subplot2grid((1,2), (0,0))
    plotphase(ax1, phase1)
    ax2 = plt.subplot2grid((1,2), (0,1))
    plotphase(ax2, phase2)
    plt.show()

def plotphasesconsecutive(phases):
    events = []
    for phase in phases:
        events += phase.events
    plotevents(events, phases[0].hometeamid, phases[0].awayteamid)

def console(c):
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
    parser.add_argument('-relevant', action = 'store_const', const=True,
                        default= False)
    parser.add_argument('-ratingtable', nargs ="?", type = str, default= None)
    parser.add_argument('-players', action = 'store_const', const=True,
                        default= False)
    args = parser.parse_args()
    
    ids = getmatchids(c)
    if args.all:
        phases = getallphases(c,ids, args.maxdistfirst, args.maxdistlast,
                              args.minnbevents, args.relevant, args.ratingtable,
                              args.players)
    else:
        phases = getmatchphases(c,ids[args.matchnb], args.maxdistfirst,
                            args.maxdistlast, args.minnbevents,
                            args.relevant, args.ratingtable,
                            args.players)
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
    with Connection(config.epl2012db) as c:
        console(c)
#     with Connection(config.db_small) as c:
#         ids = getmatchids(c)
#         phases = getmatchphases(c,ids[0])
#         plotphasesconsecutive(phases[2:5])