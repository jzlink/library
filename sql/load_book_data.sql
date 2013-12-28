load data local infile 'data/Gbook.csv' into table book
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;

select count(*) from book;