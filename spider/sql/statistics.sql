-- 发博数统计
select cnt, nick_name
from kuser u
join(
SELECT count(1) as cnt,uid from wb group by uid
) w
on u.uid=w.uid;

-- 评、转、赞统计
select nick_name,comment_cnt,repost_cnt,like_cnt
from kuser u
join(
SELECT 
  sum(case wbtype when 'comment' then 1 else 0 end) as comment_cnt,
  sum(case wbtype when 'repost' then 1 else 0 end) as repost_cnt,
  sum(case wbtype when 'like' then 1 else 0 end) as like_cnt,
  sum(case wbtype when 'reply' then 1 else 0 end) as reply_cnt,
  w.uid
from wb w
join wb_detail d
on w.wbid=d.wbid
group by w.uid
) w
on u.uid=w.uid
;

-- 互动用户打分总排名
-- 赞1分 转、评5分
select * from (
select
  sum(case wbtype when 'comment' then 5 when 'repost' then 5 when 'reply' then 10 else 1 end) as score,
  d.uid
from wb_detail d
join wb w
on d.wbid=w.wbid
where d.uid<>w.uid
group by d.uid
) tmp
where score>=50
order by score desc;

-- 分人的互动用户打分排名
select nick_name, duid, rn, score
from (
select *,row_number() over(partition by wuid order by score desc) as rn
from (
select 
sum(case wbtype when 'comment' then 5 when 'repost' then 5 when 'reply' then 10 else 1 end) as score,
d.uid as duid,
w.uid as wuid
from wb_detail d
join wb w
on d.wbid=w.wbid
where d.uid<>w.uid
group by d.uid,w.uid
) wd
join kuser u
on wd.wuid=u.uid
) tmp
where rn<=15

-- 选人，各选15人，然后去重
select distinct duid from (
select nick_name, duid, rn, score
from (
select *,row_number() over(partition by wuid order by score desc) as rn
from (
select 
sum(case wbtype when 'comment' then 5 when 'repost' then 5 when 'reply' then 10 else 1 end) as score,
d.uid as duid,
w.uid as wuid
from wb_detail d
join wb w
on d.wbid=w.wbid
where d.uid<>w.uid
group by d.uid,w.uid
) wd
join kuser u
on wd.wuid=u.uid
) tmp
where rn<=50
) tmp2


