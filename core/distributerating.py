'''
Created on Sep 27, 2016

@author: tomd
'''
from xg.model import getfeatures

def simpleeventratings(phase, phaserating):
    eventrating = float(phaserating) / len(phase.events)
    def rate(event):
        if event['teamid'] == phase.hometeamid:
            return eventrating
        elif event['teamid'] == phase.awayteamid:
            return -eventrating
        else:
            return 0

    return map(lambda e: (e['rowid'], rate(e)), phase.events)

def xgweightedeventratings(phase, phaserating, xgmodel):
    X = map(getfeatures, phase.events)
    eventweights = list(xgmodel.predict_proba(X)[:,1])
    eventweights = eventweights[1:] + [eventweights[-1]]
    eventweights = map(lambda x: x/sum(eventweights), eventweights)
    
    def rate(event,weight):
        if event['teamid'] == phase.hometeamid:
            t = phaserating
        elif event['teamid'] == phase.awayteamid:
            t = -phaserating
        else:
            t = 0
        return event['rowid'], weight*t
    
    return map(rate, phase.events, eventweights)