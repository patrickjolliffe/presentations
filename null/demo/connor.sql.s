create table t as select * From dba_objects;

variable search_criteria number
exec :search_criteria := 123

create index ix1 on t ( object_id ) ;

select * from t where object_id = nvl(:search_criteria, object_id);

