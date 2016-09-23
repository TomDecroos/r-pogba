'''
Created on Sep 22, 2016

@author: tomd
'''

def isgoal(phase):
    goals = filter(lambda x: x['name'] == 'goal', phase.events)
    home = 1 if filter(lambda x: x['teamid'] == phase.hometeamid, goals) else 0
    away = 1 if filter(lambda x: x['teamid'] == phase.awayteamid, goals) else 0
    return home - away

def xG(phase):
    return 0

def pogba(phase):
    return 0


def geteventratings(phase, phaserating):
    eventrating = float(phaserating) / len(phase.events)
    def rate(event):
        if event['teamid'] == phase.hometeamid:
            return eventrating
        elif event['teamid'] == phase.awayteamid:
            return -eventrating
        else:
            return 0

    return map(lambda e: (e['rowid'], rate(e)), phase.events)