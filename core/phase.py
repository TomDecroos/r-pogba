'''
Created on Sep 22, 2016

@author: tomd
'''
from tools.time import mintosec
from core.split import split
from db.qry import getteams

class Phase:
    
    def __init__(self, events, hometeamid, awayteamid):
        self.events = events
        self.hometeamid = hometeamid
        self.awayteamid = awayteamid
    
    def nbevents(self):
        return len(self.events)
    
    def duration(self):
        f = self.events[0]
        l = self.events[-1]
        timef = mintosec(f['minute'], f['second'])
        timel = mintosec(l['minute'], l['second'])
        return timel - timef
    
    def __str__(self):
        return "\n".join(map(str,map(tuple,self.events)))
        

def getallphases():
    pass

def getmatchphases(c,matchid):
    qry = """
        select *
        from event natural join eventtype
        where matchid = ?
        order by period, minute, second
        """
    events = c.execute(qry,(matchid,)).fetchall()
    eventss = split(events)
    home,away = getteams(c,matchid)
    return map(lambda x: Phase(x,home,away), eventss)

    
    