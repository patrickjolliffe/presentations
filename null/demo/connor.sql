variable id number

exec :id := 1

create index box_id on boxes (id) ;

explain plan for select  * from boxes where id = nvl(:id, id);

select * from dbms_xplan.display_cursor(format=>'allstats last');

explain plan for select * from t where object_id = coalesce(:search_criteria,object_id)

select * from dbms_xplan.display();