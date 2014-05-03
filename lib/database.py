import MySQLdb

db = MySQLdb.connect('localhost', 'jlink', 'eggplant', 'library')
def getConnection():
    db = MySQLdb.connect('localhost', 'jlink', 'eggplant', 'library')
    cursor = db.cursor()
    return cursor

def getDictConnection():    
    #    db = MySQLdb.connect('localhost', 'jlink', 'eggplant', 'library')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    return cursor

def execute(cursor, sql):
    print "Database.execute: sql:",sql
    result = cursor.execute(sql)
    print "result:", result
    db.commit()
    return cursor.fetchall()

if __name__ == '__main__':
    # test

    connection = getDictConnection()
    results = execute(connection, 
                      'select book_id, title from book where book_id = 1')
    for k,v in results[0].items():
        print "%s: %s" % (k,v)


