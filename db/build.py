'''
Created on Sep 19, 2016

@author: tomd
'''
import os
import pickle

import config
from tools.functional import logmap, errmap, errfilter
import xml.etree.ElementTree as ET
from tools.connection import Connection, executefile
from pprint import pprint


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


def add_match(c,matchfile):
    root = ET.parse(matchfile).getroot()
    add_row(c,"Match", root, matchmappings)

    extra = [("MatchID", int(root.attrib['id']))]

    events = errfilter(lambda x: x.tag != "DeletedEvent", root, 0.10)
    add_rows(c,'Event', events, eventmappings, extra)


def create_table(c,name, mappings, extra=[]):
    fields = [m.sqlcolumn + " " + m.sqlcolumntype for m in mappings]
    fields += [x[0] + " " + x[1] for x in extra]
    qry = 'CREATE TABLE %s %s' % (name, "(" + ", ".join(fields) + ")")
    c.execute(qry)
    print "Table %s succesfully created" % name


class mapping:

    def __init__(self, xmlattrib, sqlcolumn, sqlcolumntype):
        self.xmlattrib = xmlattrib
        self.sqlcolumn = sqlcolumn
        self.sqlcolumntype = sqlcolumntype


matchmappings = [
    mapping('id', 'ID', 'int PRIMARY KEY'),
    mapping('competition_id', 'CompetitionID', 'int'),
    mapping('season_id', 'SeasonID', 'int'),
    mapping('game_date', 'GameData', 'text'),
    mapping('away_team_id', 'AwayTeamID', 'int'),
    mapping('home_team_id', 'HomeTeamID', 'int'),
]

eventmappings = [
    mapping('id', 'ID', 'int'),
    mapping('event_type_id', 'TypeID', 'int'),
    mapping('x', 'X', 'real'),
    mapping('y', 'Y', 'real'),
    mapping('player_id', 'PlayerID', 'int'),
    mapping('team_id', 'TeamID', 'int'),
    mapping('outcome', 'Outcome', 'int'),
    mapping('period_id', 'Period', 'int'),
    mapping('period_minute', 'Minute', 'int'),
    mapping('period_second', 'Second', 'int')
]

eventextra = [("MatchID", "int")]

def create_db(dbfile,matchfilter = None):
    os.remove(dbfile)
    with Connection(dbfile) as c:
        create_table(c,'Match', matchmappings)
        create_table(c,'Event', eventmappings, eventextra)
        executefile(c,config.eventtype_table)
        epl = pickle.load(open(config.epl_matches, 'rb'))
        if matchfilter:
            epl = matchfilter(epl)
        logmap(lambda x: add_match(c,x), epl)

if __name__ == '__main__':
    create_db(config.db_small, lambda x: x[0:15])
    