https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/constraint.html
https://asktom.oracle.com/ords/f?p=100:11:::::P11_QUESTION_ID:292016138754

---
#WHAT

---
#WHY

* Integrity
* Performance

---




relationship between that foreign key and a specified primary or **unique** key

composite

parent
child

can be same table

To satisfy a composite foreign key constraint, the composite foreign key must refer to a composite unique key or a composite primary key in the parent table or view, or the value of at least one of the columns of the foreign key must be null. 

Table or View???

  EXCEPTIONS INTO wrong_emp;

---
#ON DELETE
 * SET NULL
 * CASCADE
___

drop table p;
drop table c;

create table p(id number not null);
create table c(id number not null, pid number not null);
 
alter table p add constraint p_pk primary key (id);
alter table c add constraint p_c foreign key (id) references p;
alter table p drop constraint p_pk;
alter table c drop constraint  p_c;

alter table p add constraint p_uk unique (id);

alter table p add constraint p_pk primary key (id);
alter table c add constraint p_c foreign key (id) references p(id) exceptions into wrong_c;

alter table c add constraint p_c foreign key (id) references p(id);


alter table p drop constraint p_pk;
alter table c drop constraint  p_c;
alter table p drop constraint p_uk;

create table p(id number not null);
create table c(id number not null, pid number not null);
 
alter table p add constraint p_pk primary key (id);
alter table c add constraint p_c foreign key (id) references p;


create table wrong_c(row_id rowid,
                     owner varchar2(128),
                     table_name varchar2(128),
                     constraint varchar2(128));


• Match None – Partially null composite foreign keys are permitted. If any column of a composite foreign key is null, then the non-null portions of the key do not have to match any corresponding portion of a parent key.

    ON DELETE SET NULL/CASCADE/(No ACTION)   
    ON DELETE 

https://jonathanlewis.wordpress.com/2020/08/28/fk-on-delete/
https://jonathanlewis.wordpress.com/2018/07/10/validate-fk/


DEFERRABLE INITIALLY DEFERRED.

 ENABLE NOVALIDATE 

  DISABLE VALIDATE 


  SELF REFERENCING!!