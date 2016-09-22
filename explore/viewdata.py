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
import scipy.ndimage
from tools.time import mintosec

def eventtype_freq(dbfile,matchid=None):
    with Connection(dbfile) as c:
        qry = "select name from event natural join eventtype"
        if matchid != None:
            qry += " where matchid = ?"
            rows = c.execute(qry, (matchid,))
        else:
            rows = c.execute(qry)
        typeids = map(fst, rows.fetchall())
        eventtypes = sorted(Counter(typeids).items(), key=snd)
        pprint(eventtypes)
    
if __name__ == '__main__':
    eventtype_freq(config.db_small)
    