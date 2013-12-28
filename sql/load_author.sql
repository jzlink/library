
load data local infile 'data/Gauthor.csv' into table author
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;

select * from author;