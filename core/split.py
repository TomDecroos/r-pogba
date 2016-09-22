'''
Created on Sep 22, 2016

@author: tomd
'''
from tools.time import mintosec, eventsec

def split(events, disttofirst = 20, disttolast = 10):
    phases = []
    phase = []
    for event in events:
        if samephase(phase,event,disttofirst,disttolast):
            phase.append(event)
        else:
            if validphase(phase):
                phases.append(phase)
            elif (#specialevent(phase[-1]) and 
                  phases and phases[0] and 
            eventsec(phase[-1]) - eventsec(phases[-1][-1]) < disttolast):
                phases[-1] += phase
            phase = [event]
    return phases
    
def samephase(phase, event, disttofirst=20,disttolast=10):
    if not phase:
        return True
    
    first = phase[0]
    if first['period'] != event['period']:
        return False
    
    last = phase[-1]
    if specialevent(last):
        return False
    
    time1 = eventsec(first)
    time2 = eventsec(event)
    time3 = eventsec(last)
    return time2 - time1 < disttofirst and time2 - time3 < disttolast

def validphase(phase):
    return len(phase) >= 4

def specialevent(event):
    return event['name'] in ['goal', 'corner awarded']