'''
Created on Sep 21, 2016

@author: tomd
'''
import sqlite3

class Connection:
    def __init__(self, dbfile):
        self.dbfile = dbfile
        
    def __enter__(self):
        self.con = sqlite3.connect(self.dbfile)
        self.con.row_factory = sqlite3.Row
        return self.con.cursor()
        
    def __exit__(self,type,value,traceback):
        self.con.commit()
        self.con.close()

def executeSQL(db,sqlfile):
    with Connection(db) as c, open(sqlfile,'r') as fh:
        cmds = fh.read().split(";")
        for cmd in cmds:
            c.execute(cmd)
        
        