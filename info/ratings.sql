.mode "column"
.headers on
WITH
    goals (teamid, playerid, nbgoals) AS
        (select teamid, playerid, count(*)
        from event
        join eventtype on (event.typeid = eventtype.typeid)
        join match on (event.matchid = match.id)
        where eventtype.name = 'goal' and matchday <= 40
        group by teamid, playerid
        ),
    multiteam (playerid) AS
        (select playerid
        from event
        group by playerid
        having count(distinct teamid) > 1
        )
        
select team.name as "full team name", player.first, player.last
    ,nbgoals
    --printf("%.2f", nbgoals * 100.0 / count(*)) as goalavg,
    ,printf("%.2f",sum(gr.rating)) as 'r-pogba'
    ,printf("%.2f", sum(xgr.rating)) as expgoal
    --,printf("%.2f", 1000*avg(gr.rating)) as isgoalavg
    --printf("%.2f", 1000*avg(xgr.rating)) as expgoalavg,
    --count(distinct e.matchid),
    --count(*)
from event as e
left outer join isgoal as gr on (e.rowid = gr.eventrowid)
left outer join expgoal as xgr on (e.rowid = xgr.eventrowid)
join player on (e.playerid = player.id)
join team on (e.teamid = team.id)
left outer join goals on (e.playerid = goals.playerid and e.teamid = goals.teamid)
join match on (e.matchid = match.id)
--join multiteam on (e.playerid = multiteam.playerid)
where matchday <= 40
group by e.teamid, e.playerid
having count(*)> 60 -- and 1000*avg(xgr.rating) > 1
order by sum(xgr.rating) desc
limit 15
;