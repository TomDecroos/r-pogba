.mode "column"
.headers on
WITH
    goals (teamid, playerid, goals) AS
        (select teamid, playerid, count(*)
        from event
        join eventtype on (event.typeid = eventtype.typeid)
        where eventtype.name = 'goal'
        group by teamid, playerid
        ),
    isgoalsum (teamid, playerid, rating) AS
        (select teamid, playerid, printf("%.2f", sum(rating))
        from event
        join isgoalrating on (event.rowid = isgoalrating.eventrowid)
        group by teamid, playerid
        ),
    isgoalavg (teamid, playerid, rating) AS
        (select teamid, playerid, printf("%.3f", 1000*avg(rating))
        from event
        join isgoalrating on (event.rowid = isgoalrating.eventrowid)
        group by teamid, playerid
        ),
    expgoalsum (teamid, playerid, rating) AS
        (select teamid, playerid, printf("%.2f", sum(rating))
        from event
        join expgoalrating on (event.rowid = expgoalrating.eventrowid)
        group by teamid, playerid
        ),
    expgoalavg (teamid, playerid, rating) AS
        (select teamid, playerid, printf("%.3f", 1000*avg(rating))
        from event
        join expgoalrating on (event.rowid = expgoalrating.eventrowid)
        group by teamid, playerid
        ),
    frequentplayer (teamid,playerid,nbmatches) AS
        (select teamid, playerid, matches
        from (select teamid, playerid, count(distinct matchid) as matches
             from event
             group by teamid, playerid)
        where matches > 10),
    a as (select * from goals),
    b as (select * from isgoalsum),
    c as (select * from expgoalsum)
      
select team.name, player.first, player.last, a.goals/frequentplayer.nbmatches,
b.rating, c.rating
from a
join b on (a.teamid = b.teamid and a.playerid = b.playerid)
join c on (a.teamid = c.teamid and a.playerid = c.playerid)
join team on (a.teamid = team.id)
join player on (a.playerid = player.id)
join frequentplayer on (a.teamid = frequentplayer.teamid 
    and a.playerid = frequentplayer.playerid)
order by b.rating desc
limit 30;