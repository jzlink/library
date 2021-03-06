
create table author(
        author_id integer unsigned not null auto_increment primary key,
        last_name varchar(150),
	first_name varchar(150),
	last_updated timestamp not null default current_timestamp on update current_timestamp,
	created datetime default null
        ) engine InnoDB;