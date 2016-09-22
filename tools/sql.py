'''
Created on Sep 22, 2016

@author: tomd
'''

def getfields(rows,fieldnames):
    return tuple(map(lambda f: map(lambda r: r[f], rows),
                     fieldnames.split(',')))