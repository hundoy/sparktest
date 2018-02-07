create table relation_score as
select
w.uid as master, 
d.uid as guest,
sum(case d.wbtype when 'comment' then 5 when'repost' then 5 when 'reply' then 10 else 1 end) as score
from wb_detail d
join wb w on d.wbid=w.wbid
group by w.uid, d.uid
;

select abs(-1), least(12,22,23)
;

create table links as
select node1, node2, score from(
	select *, row_number() over (partition by twoid order by node1) as rn from(
		select
			node1, node2, abs(s1-s2)/50+least(s1,s2) as score, concat(least(node1, node2), greatest(node1, node2)) as twoid
		from (
			select 
				coalesce(s1.master, s2.guest) as node1, coalesce(s2.master, s1.guest) as node2, coalesce(s1.score,0) as s1, coalesce(s2.score,0) as s2
			from relation_score s1
			full outer join relation_score s2 on s1.master = s2.guest and s1.guest=s2.master and s1.master<>s2.master
		)sco
		where abs(s1-s2)/50+least(s1,s2)>=12
	) tmp
) tmp2
where rn=1
order by score desc
;

