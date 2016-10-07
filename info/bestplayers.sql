select team.name, player.first, player.last, sum(isgoal.rating) as score
from event
join team on (event.teamid = team.id)
join player on (event.playerid = player.id)
join expgoal on (event.rowid = expgoal.eventrowid)
group by team.name, player.id
order by score desc
limit 15;