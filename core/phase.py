'''
Created on Sep 22, 2016

@author: tomd
'''
from tools.timefn import mintosec
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
    
    def hasevent(self,name):
        return name in map(lambda x: x['name'], self.events)
    
    def _correctedxy(self,e):
        if e['teamid'] == self.hometeamid:
            return e['x'], e['y']
        else:
            return 1- e['x'], 1 - e['y']
    
    def correctedcoords(self):
        return zip(*[self._correctedxy(e) for e in self.events])
    
    def __str__(self):
        return "\n".join(map(str,map(tuple,self.events)))
        

def getallphases(c, matchids, maxdistfirst = 20, maxdistlast = 10,
                 minnbevents = 3, relevant = False, ratingtable = None,
                 players = False):
    phases = []
    for mid in matchids:
        # weird hackerisch stuff
        qry = "insert into eventtype values (?,?,?)"
        c.executemany(qry,[])
        # actual useful code
        phases += getmatchphases(c, mid, maxdistfirst, maxdistlast,
                                 minnbevents, relevant, ratingtable, players)
    return phases

def getmatchphases(c, matchid, maxdistfirst = 20, maxdistlast = 10,
                   minnbevents = 3, relevant = False, ratingtable = None,
                   players=False):
    selectstr = "select event.rowid as rowid, *"
    fromstr = "from event natural join eventtype"
    if ratingtable:
        fromstr += " join %s as r on (event.rowid = r.eventrowid)" % ratingtable
    if players:
        fromstr += " join player on (event.playerid = player.id)"
    wherestr = "where matchid = ? "
    if relevant:
        wherestr += " and relevant = %d " % relevant
    orderbystr = "order by period, minute, second"
    qry = " ".join([selectstr,fromstr,wherestr,orderbystr])
    
    events = c.execute(qry,(matchid,)).fetchall()
    eventss = split(events, maxdistfirst, maxdistlast, minnbevents)
    home,away = getteams(c,matchid)
    return map(lambda x: Phase(x,home,away), eventss)
