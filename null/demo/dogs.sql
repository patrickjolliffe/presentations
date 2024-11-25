set serveroutput off

alter session set statistics_level=all;

drop table if exists pedigree_pooches;

create table pedigree_pooches(name  varchar2(16),
                              breed varchar2(16) not null);


select constraint_name, search_condition from user_constraints where table_name = 'PEDIGREE_POOCHES';

select column_name, nullable from user_tab_cols where table_name = 'PEDIGREE_POOCHES';

insert into pedigree_pooches (name, breed) values ('Franck', null);

insert into pedigree_pooches (name, breed) values ('Brian', 'Spaniel'),
                                                  ('Brian', 'Spaniel'),
                                                  ('Brian', 'Spaniel'),
                                                  ('Brian', 'Spaniel'),
                                                  ('Brian', 'Spaniel'),
                                                  ('Brian', 'Spaniel');

insert into pedigree_pooches (name, breed) values ('Bruce', 'Dalmation'),
                                                  ('Bruce', 'Dalmation'),
                                                  ('Bruce', 'Dalmation'),
                                                  ('Bruce', 'Dalmation'),
                                                  ('Bruce', 'Dalmation'),
                                                  ('Bruce', 'Dalmation'),
                                                  ('Bruce', 'Dalmation'),
                                                  ('Bruce', 'Dalmation'),
                                                  ('Bruce', 'Dalmation'),
                                                  ('Bruce', 'Dalmation'),
                                                  ('Bruce', 'Dalmation');

commit;

create index pooch_breeds on pedigree_pooches (breed);

exec dbms_stats.gather_table_stats(null, 'pedigree_pooches');

select count(name) from pedigree_pooches where breed = 'Spaniel';

select * from dbms_xplan.display_cursor(format=>'allstats last');

select count(*) from pedigree_pooches where name is null;

alter table pedigree_pooches modify name not null;

select count(name) from pedigree_pooches where breed = 'Spaniel';

select * from dbms_xplan.display_cursor(format=>'allstats last');

drop table if exists bad_dogs;

create table bad_dogs(name  varchar2(16) constraint name_nn    not null,
                      owner varchar2(16) check     (owner   is not null)   );


create table people(name varchar(16) constraint name_nn not null);

insert into bad_dogs(name, owner) values ('Gnasher', null);

select nullable from user_tab_cols where table_name = 'BAD_DOGS' and column_name = 'OWNER';

drop table if exists good_dogs;

create table good_dogs(name varchar2(16) not null);

drop table if exists dogs;

create table dogs(name  varchar2(15) primary key,
                  owner varchar2(15) null        );

select nullable from user_tab_cols where table_name = 'DOGS' and column_name = 'NAME';

select constraint_name, constraint_type from user_constraints where table_name = 'DOGS';

alter table dogs disable primary key;

select nullable from user_tab_cols where table_name = 'DOGS' and column_name = 'NAME';

alter table dogs modify name not null enable enable primary key;

drop table if exists people;

create table people(name varchar2(16) not null primary key);

insert into people (name) values ('Martin'),
                                 ('Martin');

alter table dogs add constraint fk_dog_owners foreign key (owner) references people(name);  

insert into dogs   (name,   owner    )
            values ('Nala', 'Manuela');

insert into people (name) values ('Manuela');

insert into dogs   (name,   owner    )
            values ('Nala', 'Manuela');

insert into dogs   (name,     owner)
            values ('Franck', null ),
                   ('Bailey', null );

commit;

select name from people;

select name, owner from dogs;

alter table dogs modify owner not null;

select name, owner from dogs;

alter table dogs add handle varchar2(16);

alter table dogs add constraint unique_handle unique(handle);

insert into dogs (name,     handle          ) 
          values ('Doug',   '@itsdougthepug'),
                 ('Marnie', '@marniethedog' );

commit;

update dogs set handle = '@itsdougthepug' where name = 'Franck';

select name, handle from dogs order by handle;

select * from dogs;

drop table if exists gods;

create table gods as select handle, owner, name from dogs;

select * from gods;

create table fat_dogs (
    snack001 varchar2(16), snack002 varchar2(16), snack003 varchar2(16),
    snack004 varchar2(16), snack005 varchar2(16), snack006 varchar2(16),
    snack007 varchar2(16), snack008 varchar2(16), snack009 varchar2(16),
    snack010 varchar2(16), snack011 varchar2(16), snack012 varchar2(16),
    snack013 varchar2(16), snack014 varchar2(16), snack015 varchar2(16),
    snack016 varchar2(16), snack017 varchar2(16), snack018 varchar2(16),
    snack019 varchar2(16), snack020 varchar2(16), snack021 varchar2(16),
    snack022 varchar2(16), snack023 varchar2(16), snack024 varchar2(16),
    snack025 varchar2(16), snack026 varchar2(16), snack027 varchar2(16),
    snack028 varchar2(16), snack029 varchar2(16), snack030 varchar2(16),
    snack031 varchar2(16), snack032 varchar2(16), snack033 varchar2(16),
    snack034 varchar2(16), snack035 varchar2(16), snack036 varchar2(16),
    snack037 varchar2(16), snack038 varchar2(16), snack039 varchar2(16),
    snack040 varchar2(16), snack041 varchar2(16), snack042 varchar2(16),
    snack043 varchar2(16), snack044 varchar2(16), snack045 varchar2(16),
    snack046 varchar2(16), snack047 varchar2(16), snack048 varchar2(16),
    snack049 varchar2(16), snack050 varchar2(16), snack051 varchar2(16),
    snack052 varchar2(16), snack053 varchar2(16), snack054 varchar2(16),
    snack055 varchar2(16), snack056 varchar2(16), snack057 varchar2(16),
    snack058 varchar2(16), snack059 varchar2(16), snack060 varchar2(16),
    snack061 varchar2(16), snack062 varchar2(16), snack063 varchar2(16),
    snack064 varchar2(16), snack065 varchar2(16), snack066 varchar2(16),
    snack067 varchar2(16), snack068 varchar2(16), snack069 varchar2(16),
    snack070 varchar2(16), snack071 varchar2(16), snack072 varchar2(16),
    snack073 varchar2(16), snack074 varchar2(16), snack075 varchar2(16),
    snack076 varchar2(16), snack077 varchar2(16), snack078 varchar2(16),
    snack079 varchar2(16), snack080 varchar2(16), snack081 varchar2(16),
    snack082 varchar2(16), snack083 varchar2(16), snack084 varchar2(16),
    snack085 varchar2(16), snack086 varchar2(16), snack087 varchar2(16),
    snack088 varchar2(16), snack089 varchar2(16), snack090 varchar2(16),
    snack091 varchar2(16), snack092 varchar2(16), snack093 varchar2(16),
    snack094 varchar2(16), snack095 varchar2(16), snack096 varchar2(16),
    snack097 varchar2(16), snack098 varchar2(16), snack099 varchar2(16),
    snack100 varchar2(16), snack101 varchar2(16), snack102 varchar2(16),
    snack103 varchar2(16), snack104 varchar2(16), snack105 varchar2(16),
    snack106 varchar2(16), snack107 varchar2(16), snack108 varchar2(16),
    snack109 varchar2(16), snack110 varchar2(16), snack111 varchar2(16),
    snack112 varchar2(16), snack113 varchar2(16), snack114 varchar2(16),
    snack115 varchar2(16), snack116 varchar2(16), snack117 varchar2(16),
    snack118 varchar2(16), snack119 varchar2(16), snack120 varchar2(16),
    snack121 varchar2(16), snack122 varchar2(16), snack123 varchar2(16),
    snack124 varchar2(16), snack125 varchar2(16), snack126 varchar2(16),
    snack127 varchar2(16), snack128 varchar2(16), snack129 varchar2(16),
    snack130 varchar2(16), snack131 varchar2(16), snack132 varchar2(16),
    snack133 varchar2(16), snack134 varchar2(16), snack135 varchar2(16),
    snack136 varchar2(16), snack137 varchar2(16), snack138 varchar2(16),
    snack139 varchar2(16), snack140 varchar2(16), snack141 varchar2(16),
    snack142 varchar2(16), snack143 varchar2(16), snack144 varchar2(16),
    snack145 varchar2(16), snack146 varchar2(16), snack147 varchar2(16),
    snack148 varchar2(16), snack149 varchar2(16), snack150 varchar2(16),
    snack151 varchar2(16), snack152 varchar2(16), snack153 varchar2(16),
    snack154 varchar2(16), snack155 varchar2(16), snack156 varchar2(16),
    snack157 varchar2(16), snack158 varchar2(16), snack159 varchar2(16),
    snack160 varchar2(16), snack161 varchar2(16), snack162 varchar2(16),
    snack163 varchar2(16), snack164 varchar2(16), snack165 varchar2(16),
    snack166 varchar2(16), snack167 varchar2(16), snack168 varchar2(16),
    snack169 varchar2(16), snack170 varchar2(16), snack171 varchar2(16),
    snack172 varchar2(16), snack173 varchar2(16), snack174 varchar2(16),
    snack175 varchar2(16), snack176 varchar2(16), snack177 varchar2(16),
    snack178 varchar2(16), snack179 varchar2(16), snack180 varchar2(16),
    snack181 varchar2(16), snack182 varchar2(16), snack183 varchar2(16),
    snack184 varchar2(16), snack185 varchar2(16), snack186 varchar2(16),
    snack187 varchar2(16), snack188 varchar2(16), snack189 varchar2(16),
    snack190 varchar2(16), snack191 varchar2(16), snack192 varchar2(16),
    snack193 varchar2(16), snack194 varchar2(16), snack195 varchar2(16),
    snack196 varchar2(16), snack197 varchar2(16), snack198 varchar2(16),
    snack199 varchar2(16), snack200 varchar2(16), snack201 varchar2(16),
    snack202 varchar2(16), snack203 varchar2(16), snack204 varchar2(16),
    snack205 varchar2(16), snack206 varchar2(16), snack207 varchar2(16),
    snack208 varchar2(16), snack209 varchar2(16), snack210 varchar2(16),
    snack211 varchar2(16), snack212 varchar2(16), snack213 varchar2(16),
    snack214 varchar2(16), snack215 varchar2(16), snack216 varchar2(16),
    snack217 varchar2(16), snack218 varchar2(16), snack219 varchar2(16),
    snack220 varchar2(16), snack221 varchar2(16), snack222 varchar2(16),
    snack223 varchar2(16), snack224 varchar2(16), snack225 varchar2(16),
    snack226 varchar2(16), snack227 varchar2(16), snack228 varchar2(16),
    snack229 varchar2(16), snack230 varchar2(16), snack231 varchar2(16),
    snack232 varchar2(16), snack233 varchar2(16), snack234 varchar2(16),
    snack235 varchar2(16), snack236 varchar2(16), snack237 varchar2(16),
    snack238 varchar2(16), snack239 varchar2(16), snack240 varchar2(16),
    snack241 varchar2(16), snack242 varchar2(16), snack243 varchar2(16),
    snack244 varchar2(16), snack245 varchar2(16), snack246 varchar2(16),
    snack247 varchar2(16), snack248 varchar2(16), snack249 varchar2(16),
    snack250 varchar2(16), snack251 varchar2(16), snack252 varchar2(16),
    snack253 varchar2(16), snack254 varchar2(16), snack255 varchar2(16),
    snack256 varchar2(16)
);

insert into fat_dogs(snack256) values ('Pupcorn');

insert into fat_dogs(snack255) values ('Pawperoni');

commit;

insert into people (name) values ('Patrick'),
                                 ('Connor' );

update dogs set owner = 'Patrick' where name = 'Franck';

update dogs set owner = 'Connor' where name = 'Bailey';

exec dbms_stats.gather_table_stats(null, 'dogs');

select num_nulls, num_distinct from user_tab_cols where table_name  = 'DOGS'
                                                    and column_name = 'OWNER';

select name from dogs where owner is null;

select * from dbms_xplan.display_cursor(format=>'allstats last');

select owner, count(*) from dogs group by owner order by owner;

create index dogs_owner on dogs(owner);

select num_rows, distinct_keys from user_indexes where index_name = 'DOGS_OWNER';

select /*+ index_rs_asc(dogs) */ name from dogs where owner is null;

select * from dbms_xplan.display_cursor(format=>'allstats last');

select owner, name from dogs order by owner, name;

create index dogs_owner_name on dogs(owner, name);

select num_rows, distinct_keys from user_indexes where index_name = 'DOGS_OWNER_NAME';

select name from dogs where owner is null;

select * from dbms_xplan.display_cursor(format=>'allstats last');

alter table dogs add status varchar2(16) default 'Full';

update dogs set status = 'Hungry' where name = 'Franck';

commit;

select name, status from dogs;

create or replace function is_hungry (status varchar2) 
return integer
deterministic
is
begin
  if status = 'Hungry' then
    return 1;
  else
    return null;
  end if;
end;
/

select name, status, is_hungry(status) from dogs;

create index hungry_dogs on dogs(is_hungry(status));

select index_type, num_rows, distinct_keys from user_indexes where index_name = 'HUNGRY_DOGS';

exec dbms_stats.gather_table_stats(null, 'dogs');

select name from dogs where is_hungry(status) = 1;

select * from dbms_xplan.display_cursor();
