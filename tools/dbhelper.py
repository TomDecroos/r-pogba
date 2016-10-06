'''
Created on Sep 22, 2016

@author: tomd
'''
from tools.functional import errmap
import sqlite3

#Connection

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

def executefile(c,sqlfile):
    with open(sqlfile,'r') as fh:
        cmds = fh.read().split(";")
        for cmd in cmds:
            c.execute(cmd)

def latexify(c, qry):
    rows = c.execute(qry).fetchall()
    print "\\toprule"
    keys = rows[0].keys()
    print "&".join(["\\textbf{%s}" % key for key in keys]) + "\\\\"
    print "\\midrule"
    for row in rows:
        print "&".join([str(row[key]) for key in keys]) + "\\\\"
    print "\\bottomrule"

# easy field retrieval

def getfields(rows,fieldnames):
    fields = fieldnames.split(',')
    def fieldvalues(field):
        return [row[field] for row in rows]
    return tuple([fieldvalues(field) for field in fields])
    
# mapping xml to sql

class Mapping:

    def __init__(self, xmlattrib, sqlcolumn, sqlcolumntype):
        self.xmlattrib = xmlattrib
        self.sqlcolumn = sqlcolumn
        self.sqlcolumntype = sqlcolumntype


def create_table(c,name, mappings, extra=[]):
    fields = [m.sqlcolumn + " " + m.sqlcolumntype for m in mappings]
    fields += [x[0] + " " + x[1] for x in extra]
    qry = 'CREATE TABLE %s %s' % (name, "(" + ", ".join(fields) + ")")
    c.execute(qry)
    print "Table %s successfully created" % name


def add_row(c,table, element, mappings, extra=[]):
    add_rows(c,table, [element], mappings, extra)


def add_rows(c,table, elements, mappings, extra=[]):
    columns = [m.sqlcolumn for m in mappings]
    columns += ([x[0] for x in extra])
    questionmarks = map(lambda x: "?", columns)
    strcolumns = "(%s)" % ", ".join(columns)
    strmarks = "(%s)" % ", ".join(questionmarks)
    qry = "INSERT INTO %s %s VALUES %s" % (table, strcolumns, strmarks)

    def getvalues(element):
        values = [element.attrib[m.xmlattrib] for m in mappings]
        values += ([x[1] for x in extra])
        return tuple(values)

    valuess = errmap(getvalues, elements, threshold=0.05)
    c.executemany(qry, valuess)
