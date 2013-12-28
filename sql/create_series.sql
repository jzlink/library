-- must include '--local-infile=1' after | lbd when using a csv. This gives permission to use a local file.

drop table if exists series;

create table series (
       series_id   integer unsigned    not null auto_increment primary key,
       series      varchar(150)        not null,
       number	   int unsigned,
       last_updated      timestamp           not null default current_timestamp on update current_timestamp,
       created           datetime            not null


) engine InnoDB;

load data local infile 'data/series.csv' into table series
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;

select * from series;