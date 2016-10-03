'''
Created on Sep 22, 2016

@author: tomd
'''
from tools.timefn import eventsec

def split(events, maxdistfirst = 20, maxdistlast = 10, minnbevents = 3):
    phases = []
    phase = []
    for event in events:
        if samephase(phase,event,maxdistfirst,maxdistlast):
            phase.append(event)
        else:
            if len(phase) >= minnbevents:
                phases.append(phase)
            elif (phases and phases[0] and not specialevent(phases[-1][-1])
            and eventsec(phase[-1]) - eventsec(phases[-1][-1]) < maxdistlast):
                phases[-1] += phase
            phase = [event]
    return phases
    
def samephase(phase, event, maxdistfirst=20, maxdistlast=10):
    if not phase:
        return True
    
    first = phase[0]
    if first['matchid'] != event['matchid']:
        return False
    if first['period'] != event['period']:
        return False
    
    last = phase[-1]
    if specialevent(last):
        return False
    
    time1 = eventsec(first)
    time2 = eventsec(event)
    time3 = eventsec(last)
    return abs(time2 - time1) <= maxdistfirst and abs(time2 - time3) <= maxdistlast

def specialevent(event):
    return event['name'] in ['goal', 'corner awarded']