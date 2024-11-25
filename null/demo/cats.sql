drop table if exists boxes;

create table boxes(id number null,
                   live_cats number null);

insert into boxes  (id, live_cats)
            values ( 1,         1),
                   ( 2,         0);

insert into boxes  (  id, live_cats)
            values (   3,      null),
                   (null,      null);

commit;

select * from boxes;

set null [null]

select * from boxes;

select id, live_cats from boxes where (live_cats is not null);

select id, live_cats from boxes where (live_cats is null);

select * from boxes where null;

select id, live_cats from boxes where (live_cats = live_cats);

select id, live_cats, (live_cats = live_cats), (live_cats != live_cats) from boxes;

select id, live_cats, (live_cats = 0), (live_cats != 0) from boxes;

select count(*) from boxes where (live_cats = 0) or (live_cats != 0);

select count(*) from boxes where (live_cats = 0) or (live_cats != 0) or (live_cats is null);

select (null*42), (null/42), (null+42), (null-42);

select (null*0), (null/0), (null/null), (null-null);

select 'cock' || null || 'womble';

select id, live_cats from boxes;

select count(null), count(live_cats), count(*) from boxes;

select live_cats from boxes;

select sum(null), sum(live_cats) from boxes;

select live_cats from boxes;

select avg(null), avg(live_cats) from boxes;

select live_cats from boxes;

select min(null), max(null), min(live_cats), max(live_cats) from boxes;

select live_cats, count(*) from boxes group by live_cats;

select distinct live_cats from boxes;

select live_cats from boxes order by live_cats;

select live_cats from boxes order by live_cats nulls first;

select live_cats from boxes order by live_cats desc;

select live_cats from boxes order by live_cats desc nulls last;

select live_cats, nvl(live_cats, 0), coalesce(live_cats, 0) from boxes;

select live_cats, id, coalesce(live_cats, id, 0) from boxes;
