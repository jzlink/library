
load data local infile 'data/Gbook_author.csv' into table book_author
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;

select * from book_author;