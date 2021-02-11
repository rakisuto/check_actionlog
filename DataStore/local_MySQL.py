# import mysql.connector
import pymysql.cursors
# from mysql.connector.constants import ClientFlag

conn = pymysql.connect(host='localhost',
                    user='enix',
                    password='enix',
                    db='test',
                    charset='utf8mb4'
                    #cursorclass=pymysql.cursors.DictCursor
                    )


class MySQL:

    # select
    def query(stmt, *args):
        try:
            conn.ping()
            with conn.cursor() as cursor:
                cursor.execute(stmt, (args))
                data = cursor.fetchall()
        finally:
            conn.close()
            cursor.close()
            return data

    # insert
    def ins_query(stmt, *args):
        try:
            conn.ping()
            with conn.cursor() as cursor:
                cursor.execute(stmt, (args))
                data = cursor.fetchall()
        finally:
            conn.commit()
            conn.close()
            cursor.close()
            return True


