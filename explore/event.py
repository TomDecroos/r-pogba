'''
Created on Sep 22, 2016

@author: tomd
'''

import scipy.ndimage

import config
import matplotlib.pyplot as plt
from tools.connection import Connection
from tools.time import mintosec
from tools.sql import getfields
from db.qry import getteams


def getevents(c,matchid,period=1,startmin=0,endmin=1,relevant=True):
    qry = """
        select x, y, minute, second, name, teamid, outcome
        from event natural join eventtype
        where matchid = ? and period = ?
        and minute*60 + second >= ?
        and minute*60 + second < ?
        """
    if relevant: qry += " and relevant = 1"
    values = (matchid, period, mintosec(startmin), mintosec(endmin))
    return c.execute(qry, values).fetchall()

def printevents(events, hometeamid, awayteamid):
    fieldnames = "name,teamid,outcome"
    name, teamid, outcome = getfields(events, fieldnames)
    
    for t, n, o in zip(teamid, name, outcome):
        msg = "+" if hometeamid == t else "-"
        msg += n
        msg += "*" if o == 0 else ""
        print msg
    
def plotevents(events,hometeamid,awayteamid):
    fieldnames = "x,y,minute,second,name,teamid,outcome"
    x,y,minute,second,name,teamid,outcome = getfields(events,fieldnames)
    time = map(lambda x:mintosec(x[0],x[1]), zip(minute,second))
    
    def correction(x,teamid):
        return x if teamid == hometeamid else 1-x
    x = map(lambda x: correction(*x), zip(x, teamid))
    y = map(lambda x: correction(*x), zip(y, teamid))
    
    teamcolours = {hometeamid : 'lightblue',
                   awayteamid : 'yellow'}
    
    def choosecolors(teamid,outcome,name):
        box = teamcolours.get(teamid, 'white')
        edge = 'black' if (outcome==1 and name != 'turnover') else 'red'
        return box,edge
    
    colors = map(lambda x: choosecolors(*x), zip(teamid,outcome,name))
        
    fig = plt.figure()
    size = 11
    fig.set_size_inches(1.61*size,size, forward=True)
    
    axtx = plt.subplot2grid((2,2), (0,0))
    _plottimeseries(axtx, time, x, colors, name)
    
    axty = plt.subplot2grid((2,2), (1,0))
    _plottimeseries(axty, time, y, colors, name)
   
    axxy = plt.subplot2grid((2,2), (0,1), rowspan = 2)
    _plotxy(axxy, x, y, colors, name)
    
    plt.tight_layout()
    plt.show() 

def _plottimeseries(ax, times, xs, colors = None, labels = None):
    ax.set_ylim(0,1)
    ax.plot(times, xs, c= 'black')
    if labels and colors:
        for label, time, x, color in zip(labels, times, xs, colors):
            bbox = dict(boxstyle = 'round', fc = color[0],
                        ec = color[1], lw = 3 if color[1] == 'red' else 1,
                        alpha = 0.8)
            ax.annotate(label, xy=(time, x), bbox = bbox,
                        horizontalalignment = 'left',
                        verticalalignment = 'center')


def _plotxy(ax, xs, ys, colors = None, labels = None, rotate=True):    
    ax.set_xlim(-0.05,1.05)
    ax.set_ylim(-0.05,1.05)
    img = plt.imread(config.soccerfield)
    if rotate:
        img = scipy.ndimage.rotate(img,90)
        ys, xs = xs, ys
        
    ax.imshow(img, extent=(-0.05, 1.05, -0.05, 1.05), aspect = 'auto',)
    ax.plot(xs, ys, color="black")
    if labels and colors:
        for label, x, y, color in zip(labels, xs, ys, colors):
            bbox = dict(boxstyle = 'round', fc = color[0],
                        ec= color[1], lw = 3 if color[1] == 'red' else 1,
                        alpha = 1)
            ax.annotate(label, xy=(x, y), bbox = bbox,
                        horizontalalignment = 'center',
                        verticalalignment = 'center')

def console(dbfile):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-matchnb",nargs="?", type=int, default=0)
    parser.add_argument("-period", nargs="?", type=int)
    parser.add_argument('-startmin',nargs="?", type=float, default=0)
    parser.add_argument('-endmin',nargs="?",type=float)
    parser.add_argument('-relevant', action = 'store_const', const=True,
                        default= False)
    parser.add_argument('-print', action = 'store_const', const=True,
                        default= False)
    parser.add_argument('-plot', action = 'store_const', const=True,
                        default= False)
    args = parser.parse_args()
    if not args.period:
        args.period = 1 if args.startmin < 45 else 2
    if not args.endmin:
        args.endmin = args.startmin + 1
    
    with Connection(dbfile) as c:
        qry = "select id from match"
        (matchid,) = c.execute(qry).fetchall()[args.matchnb]
        events = getevents(c,matchid, args.period, args.startmin,
                           args.endmin, relevant=args.relevant)
        home,away = getteams(c, matchid)
        if args.plot:
            plotevents(events, home, away)
        else:
            printevents(events, home, away)
        
if __name__ == '__main__':
    console(config.db_small)