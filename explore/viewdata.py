'''
Created on Sep 21, 2016

@author: tomd
'''
from tools.connection import Connection
import config
from pprint import pprint
from tools.functional import fst, snd
import matplotlib.pyplot as plt
from collections import Counter

def eventtype_freq(c,matchid=None):
    qry = "select name from event natural join eventtype"
    if matchid != None:
        qry += " where matchid = ?"
        rows = c.execute(qry, (matchid,))
    else:
        rows = c.execute(qry)
    typeids = map(fst, rows.fetchall())
    eventtypes = sorted(Counter(typeids).items(), key=snd)
    pprint(eventtypes)
    

def window(c,matchid,period=1,startmin=0,endmin=1):
    qry = """
        select x, y, minute, second, name, teamid, outcome
        from event natural join eventtype
        where matchid = ? and period = ? and minute >= ? and minute < ?
        """
    events = c.execute(qry, (matchid, period, startmin, endmin)).fetchall()
    x,y,minute,second,name,teamid,outcome = zip(*events)
    time = map(lambda x:mintosec(x[0],x[1]), zip(minute,second))
    
    qry = "select hometeamid from match where id = ?"
    (hometeamid,) = c.execute(qry,(matchid,)).fetchone()
    def correction(x,teamid):
        return x if teamid == hometeamid else 1-x
    x = map(lambda x: correction(*x), zip(x, teamid))
    y = map(lambda x: correction(*x), zip(y, teamid))
    
    def choosecolor(teamid,outcome,name):
        if outcome==1 or name == 'turnover':
            return 'lightblue' if teamid == hometeamid else 'lightgreen'
        else:
            return 'red'
    colors = map(lambda x: choosecolor(*x), zip(teamid,outcome,name))
    
    fig = plt.figure()
    size = 10
    fig.set_size_inches(1.61 * 2 * size, 1 * size, forward=True)
    
    axtx = plt.subplot2grid((2,2), (0,0))
    plottimeseries(axtx, time, x, colors, name)
    
    axty = plt.subplot2grid((2,2), (1,0))
    plottimeseries(axty, time, y, colors, name)
   
    axxy = plt.subplot2grid((2,2), (0,1), rowspan = 2)
    plotxy(axxy, x, y, colors, name)
    
    plt.tight_layout()
    plt.show() 

def plottimeseries(ax, times, xs, colors = None, labels = None):
    ax.set_ylim(0,1)
    ax.plot(times, xs, c= 'black')
    if labels and colors:
        for label, time, x, color in zip(labels, times, xs, colors):
            bbox = dict(boxstyle = 'round', fc = color, alpha = 0.8)
            ax.annotate(label, xy=(time, x), bbox = bbox,
                        horizontalalignment = 'left',
                        verticalalignment = 'center')


def plotxy(ax, xs, ys, colors = None, labels = None):    
    ax.set_xlim(-0.05,1.05)
    ax.set_ylim(-0.05,1.05)
    img = plt.imread(config.soccerfield)
    ax.imshow(img, extent=(-0.05, 1.05, -0.05, 1.05), aspect = 'auto')
    
    ax.plot(xs, ys, color="black")
    if labels and colors:
        for label, x, y, color in zip(labels, xs, ys, colors):
            bbox = dict(boxstyle = 'round', fc = color, alpha = 0.8)
            ax.annotate(label, xy=(x, y), bbox = bbox,
                        horizontalalignment = 'center',
                        verticalalignment = 'center')

def mintosec(minute, second):
    return 60 * minute + second


if __name__ == '__main__':
    with Connection(config.db_small) as c:
        qry = "select id from match"
        (matchid,) = c.execute(qry).fetchall()[0]
        window(c,matchid,1,4,6)
        #eventtype_freq(c)
    #rows = c.exeute()