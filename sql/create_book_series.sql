--DO NOT CREATE! TABLE WAS DROPPED FROM DB--

create table book_series (

       bs_id integer unsigned not null auto_increment primary key,
       book_id integer unsigned,
       series_id integer unsigned,
       series_num integer unsigned,
       last_updated timestamp not null default current_timestamp on update current_timestamp,
       created datetime default null,

       foreign key (book_id) references book (book_id), 
       foreign key (series_id) references series (series_id)

        )engine InnoDB;


