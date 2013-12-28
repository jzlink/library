create table when_read (

       when_id integer unsigned not null auto_increment primary key,
       when_read date,
       book_id integer unsigned,
       last_updated timestamp not null default current_timestamp on update current_timestamp,
       created datetime default null,

       foreign key (book_id) references book (book_id) 
 
        )engine InnoDB;