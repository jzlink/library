import MySQLdb

def getConnection():

    db = MySQLdb.connect('localhost', 'jlink', 'eggplant', 'library')

    cursor = db.cursor()

    return cursor

def execute(cursor, sql):
    cursor.execute(sql)
    return cursor.fetchall()


if __name__ == '__main__':
    # test

    connection = getConnection()
    results = execute(connection, 'select book_id, title from book where book_id = 1')
    book_id, title =  results[0]
    #print type(results)
    
    print 'book_id:', book_id
    print 'title:', title

