'''
Created on Sep 19, 2016

@author: tomd
'''
import os
import pickle
import pprint
import sqlite3

import config
from db.tools import logfilter, logmap, errmap, errfilter
import xml.etree.ElementTree as ET


def is_epl_match(matchfile):
    root = ET.parse(matchfile).getroot()
    return int(root.attrib['competition_id']) == config.epl_id


def save_epl_matches():
    matchfiles = [config.optaf21 + m for m in os.listdir(config.optaf21)]
    epl_mfs = logfilter(is_epl_match, matchfiles)
    pickle.dump(epl_mfs, open(config.epl_matches, 'wb'))


def add_row(table, element, mappings, extra=[]):
    add_rows(table, [element], mappings, extra)


def add_rows(table, elements, mappings, extra=[]):
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
    con.executemany(qry, valuess)


def add_match(matchfile):
    root = ET.parse(matchfile).getroot()
    add_row("Match", root, matchmappings)

    extra = [("MatchID", int(root.attrib['id']))]

    events = errfilter(lambda x: x.tag != "DeletedEvent", root, 0.10)
    add_rows('Event', events, eventmappings, extra)


def create_table(name, mappings, extra=[]):
    fields = [m.sqlcolumn + " " + m.sqlcolumntype for m in mappings]
    fields += [x[0] + " " + x[1] for x in extra]
    qry = 'CREATE TABLE %s %s' % (name, "(" + ", ".join(fields) + ")")
    con.execute(qry)
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
]

eventextra = [("MatchID", "int")]

if __name__ == '__main__':
    #os.remove(config.db)
    con = sqlite3.connect(config.db)

#     create_table('Match', matchmappings)
#     create_table('Event', eventmappings, eventextra)
#     con.commit()
#  
# #    import pprint
# # #   save_epl_matches()
#     epl = pickle.load(open(config.epl_matches, 'rb'))
#     logmap(add_match, epl)
    #root = ET.parse(epl[0]).getroot()
    # print root[1].attrib
    # for event in ET.parse(epl[0]).getroot():
    #     print event.attrib['player_id']
# #     # print len(epl)
#     root = ET.parse(epl[5]).getroot()
#     print set([e.tag for e in root])
#     # print root.attrib
#     event = root[6]
#     pprint.pprint(event.attrib)
#     pprint.pprint(matchmappings)
    rows = con.execute("select * from event limit 1000").fetchall()
    pprint.pprint(rows)
    con.commit()
    con.close()
