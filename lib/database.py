#!/usr/bin/env python
import MySQLdb

_db = MySQLdb.connect('localhost', 'jlink', 'eggplant', 'library')

def getConnection():
    cursor = _db.cursor()
    return cursor

def getDictConnection():    
    cursor = _db.cursor(MySQLdb.cursors.DictCursor)
    return cursor

def execute(cursor, sql):
    #print "Database.execute: sql:",sql
    result = cursor.execute(sql)
    _db.commit()
    return cursor.fetchall()

if __name__ == '__main__':
    # test

    connection = getDictConnection()
    con = getConnection()

    x = execute(connection,
                ''' select auto_increment from information_schema.TABLES
where table_name = "book"''')
    id = x[0]['auto_increment']

    results = execute(connection, 
                      'select book_id, title from book where book_id = %s' %id)

#    for k,v in results.items():
#        print "%s: %s" % (k,v)

    test = execute(connection, 'select max(book_id) from book')
    x = test[0]['max(book_id)'] 
    print x
