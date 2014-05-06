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
    results = execute(connection, 
                      'select book_id, title from book where book_id = 1')
    for k,v in results[0].items():
        print "%s: %s" % (k,v)


