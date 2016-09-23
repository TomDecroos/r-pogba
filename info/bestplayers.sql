select team.name, player.first, player.last, sum(rating) as score
from event
join team on (event.teamid = team.id)
join player on (event.playerid = player.id)
join isgoalrating on (event.rowid = isgoalrating.eventrowid)
group by team.name, player.id
order by score;