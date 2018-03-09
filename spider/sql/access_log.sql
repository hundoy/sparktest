-- ÿ�������
select count(1),to_char(access_time,'YYYY-MM-DD') as ad from access_log_uni group by ad order by count(1) desc;

-- ʡPV
select count(1),province  from access_log_uni where country='�й�' and province is not null group by province order by count(1) desc;
-- ʡUV
select count(distinct ip),province from access_log_uni where country='�й�' and province is not null group by province order by count(distinct ip) desc;


-- ʡ��PV
select count(1),province,city from access_log_uni where country='�й�' and city is not null group by province,city order by count(1) desc;
-- ʡ��UV
select count(distinct ip),province,city from access_log_uni where country='�й�' and city is not null group by province,city order by count(distinct ip) desc;

-- ʡ��PV  ����
select count(1),country from access_log_uni 
where country<>'�й�'
group by country
order by count(1) desc;
-- ʡ��UV ����
select count(distinct ip),country from access_log_uni 
where country<>'�й�'
group by country order by count(distinct ip) desc;


-- �û���Ϣ������
select count(1), al.uid,u.nick_name
from access_log_uni al
left join kuser u on al.uid=u.uid
where page='display_detail'
group by al.uid,u.nick_name
order by count(1) desc;
-- UV
select count(distinct al.ip), al.uid,u.nick_name
from access_log_uni al
left join kuser u on al.uid=u.uid
where page='display_detail'
group by al.uid,u.nick_name
order by count(distinct al.ip) desc;

-- nodata 
select count(1), al.uid,u.nick_name
from access_log_uni al
left join kuser u on al.uid=u.uid
where page='nodata'
group by al.uid,u.nick_name
order by count(1) desc;
-- UV
select count(distinct al.ip), al.uid,u.nick_name
from access_log_uni al
left join kuser u on al.uid=u.uid
where page='nodata'
group by al.uid,u.nick_name
order by count(distinct al.ip) desc;
