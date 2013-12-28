create table book_author (

       ba_id integer unsigned not null auto_increment primary key,
       book_id integer unsigned,
       author_id integer unsigned,
       last_updated timestamp not null default current_timestamp on update current_timestamp,
       created datetime default null,

       foreign key (book_id) references book (book_id), 
       foreign key (author_id) references author (author_id)

        )engine InnoDB;


