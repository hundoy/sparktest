drop table relation_score;
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

drop table links;
create table links as
select node1, node2, score from(
	select *, row_number() over (partition by twoid order by node1) as rn from(
		select
			node1, node2, abs(s1-s2)/20+least(s1,s2) as score, concat(least(node1, node2), greatest(node1, node2)) as twoid
		from (
			select 
				--*
				coalesce(s1.master, s2.guest) as node1, coalesce(s1.guest, s2.master) as node2, coalesce(s1.score,0) as s1, coalesce(s2.score,0) as s2
			from relation_score s1
			full outer join relation_score s2 on s1.master = s2.guest and s1.guest=s2.master
			where (s1.master is not null and s1.master<>s1.guest) or (s2.master is not null and s2.master<>s2.guest)
		)sco
		where abs(s1-s2)/20+least(s1,s2)>=10
	) tmp
) tmp2
where rn=1
order by score desc
;

select DISTINCT uid from 
(
select node1 as uid from links
UNION ALL
select node2 as uid from links
) tmp
;

-- BASE get nodes and links. 222 data.
select 
node1, node2, u1.nick_name as name1, u2.nick_name as name2, score 
from links l
left join kuser u1 on l.node1=u1.uid
left join kuser u2 on l.node2=u2.uid
where score>=15
order by score desc;

select 
node1, node2, u1.nick_name as name1, u2.nick_name as name2, score, 0.01385*score-0.1077 as strengthd
from links l
join kuser u1 on l.node1=u1.uid
join kuser u2 on l.node2=u2.uid
where score>=15
order by score desc;

-- analyze 
-- avg = 17
select avg(score)
from links;

select
sum(case score between 0 and 4 when true then 1 else 0 end) as cnt_0_4,
sum(case score between 5 and 9 when true then 1 else 0 end) as cnt_5_9,
sum(case score between 10 and 10 when true then 1 else 0 end) as cnt_10,
sum(case score between 11 and 14 when true then 1 else 0 end) as cnt_11_14,
sum(case score between 15 and 19 when true then 1 else 0 end) as cnt_15_19,
sum(case score between 20 and 39 when true then 1 else 0 end) as cnt_20_39,
sum(case score between 40 and 59 when true then 1 else 0 end) as cnt_40_59,
sum(case score between 60 and 79 when true then 1 else 0 end) as cnt_60_79
from links



-- missing persons
select 
node1, node2, u1.nick_name as name1, u2.nick_name as name2, score 
from links l
left join kuser u1 on l.node1=u1.uid
left join kuser u2 on l.node2=u2.uid
where score>=15
and u1.nick_name is null or u2.nick_name is null
order by score desc;

