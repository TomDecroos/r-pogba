'''
Created on Sep 22, 2016

@author: tomd
'''
import matplotlib.pyplot as plt
import config
from tools.connection import Connection
from db.qry import getmatchids
from core.phase import getmatchphases
from numpy import mean, std
from pprint import pprint
from explore.event import plotevents

def nbhist(phases):
    x = map(lambda x: x.nbevents(), phases)
    plt.hist(x)
    plt.show()

def durhist(phases):
    x = map(lambda x: x.duration(), phases)
    plt.hist(x)
    plt.show()

def longestphase(phases):
    return max(phases, key = lambda x: x.duration())

def stats(phases):
    print "n: %s" % len(phases)
    nbs = map(lambda x: x.nbevents(), phases)
    durs = map(lambda x: x.duration(), phases)
    print "nbevents avg: %2.2f std: %2.2f" % (mean(nbs), std(nbs))
    print "duration avg: %2.2f std: %2.2f" % (mean(durs), std(durs))
    
def plotphases(phases):
    for phase in phases:
        plotevents(phase.events,phase.hometeamid,phase.awayteamid)

def plotphasesconsecutive(phases):
    events = []
    for phase in phases:
        events += phase.events
    plotevents(events, phases[0].hometeamid, phases[0].awayteamid)

if __name__ == '__main__':
    
    with Connection(config.db_small) as c:
        ids = getmatchids(c)
        phases = getmatchphases(c,ids[0])
        plotphasesconsecutive(phases[2:5])
        #print(tuple(phases[0].events[0]))
#         stats(phases)
#         durhist(phases)
#         nbhist(phases)