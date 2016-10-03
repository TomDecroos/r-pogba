'''
Created on Sep 28, 2016

@author: tomd
'''
import config
from tools.dbhelper import Connection, latexify

qry= """
WITH
    goals (teamid, playerid, nbgoals) AS
        (select teamid, playerid, count(*)
        from event
        join eventtype on (event.typeid = eventtype.typeid)
        join match on (event.matchid = match.id)
        where eventtype.name = 'goal' and matchday <= 40
        group by teamid, playerid
        )
        
select (player.first || " " || player.last) as "Player", team.name as "Club"
    ,printf("%.2f",sum(gr.rating)) as 'Rating'
    ,nbgoals as "Goals"
from event as e
left outer join isgoalrating as gr on (e.rowid = gr.eventrowid)
join player on (e.playerid = player.id)
join team on (e.teamid = team.id)
left outer join goals on (e.playerid = goals.playerid and e.teamid = goals.teamid)
join match on (e.matchid = match.id)
group by e.teamid, e.playerid
order by sum(gr.rating) desc
limit 15
;"""

if __name__ == '__main__':
    with Connection(config.epl2012db) as c:
        latexify(c,qry)