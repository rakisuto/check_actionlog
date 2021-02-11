import pymysql
import pymysql.cursors

conn = pymysql.connect(host='us-cdbr-east-03.cleardb.com',
                    user='b43c007fae4cbb',
                    password='641f32al',
                    db='heroku_5c65651484c4266',
                    charset='utf8mb4'
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


