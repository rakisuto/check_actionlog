import pymysql.cursors

conn = pymysql.connect(host='localhost',
                    user='enix',
                    password='enix',
                    db='test',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)
'''
def __init__(self, **dns):
    self.dns = dns
    self.dbh = None

def _open(self):
    self.dbh = mysql.connector.MySQLConnection(**self.dns)

def _close(self):
    self.dbh.close()
'''


def query(stmt, *args): #ユーザ, クエリ,
    try:
        conn.ping()
        with conn.cursor() as cursor:
            cursor.execute(stmt, (args))
            data = cursor.fetchall()
            print(data)
    finally:
        conn.close()
        cursor.close()

def ins_query(stmt, *args): #ユーザ, クエリ,
    try:
        conn.ping()
        with conn.cursor() as cursor:
            cursor.execute(stmt, (args))
            data = cursor.fetchall()
            print(data)
    finally:
        conn.commit()
        conn.close()
        cursor.close()


# select test
name = "test"
stmt = 'SELECT * FROM users\
            WHERE name = %s'
execute = query(stmt, name)
if execute:
    print(execute)


# insert test
name = 'Jon Doe 3'
age = '90'
gender = "男"
password = '135791'
stmt = 'INSERT INTO users (name, age, gender, password) VALUES\
            (%s, %s, %s, %s)'
execute = ins_query(stmt, name, age, gender, password)
if execute:
    print(execute)

'''
try:
    with conn.cursor() as cursor:
        sql = "SELECT * FROM users WHERE age = %s"
        cursor.execute(sql, ('12',))
        result = cursor.fetchall()
        print(result)
finally:
    conn.close()
'''

'''
try:
    with conn.cursor() as cursor:
        sql = "INSERT INTO users (name, age, gender, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, ('Jon Doe', '11', "男", '123456'))

    # オートコミットじゃないので、明示的にコミットを書く必要がある
    conn.commit()
finally:
    conn.close()
'''
