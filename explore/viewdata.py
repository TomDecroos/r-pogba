'''
Created on Sep 21, 2016

@author: tomd
'''
from tools.connection import Connection
import config
from pprint import pprint
from tools.functional import fst
import matplotlib.pyplot as plt

def view_eventtype_hist(c):
    qry = "select typeid from event"
    typeids = map(fst, c.execute(qry).fetchall())
    typeids = set(typeids)
    pprint(typeids)
    #plt.hist(typeids,bins=max(typeids))
    #plt.show()

if __name__ == '__main__':
    with Connection(config.db) as c:
        view_eventtype_hist(c)
    #rows = c.exeute()