-- must include '--local-infile=1' after | lbd when using a csv. This gives permission to use a local file.

drop table if exists type;

create table type (
       type_id   integer unsigned    not null auto_increment primary key,
       type          varchar(150)        not null,
       last_updated      timestamp           not null default current_timestamp on update current_timestamp,
       created           datetime            not null,

       unique key type (type)
) engine InnoDB;

load data local infile 'data/type.csv' into table type
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;

select * from type;