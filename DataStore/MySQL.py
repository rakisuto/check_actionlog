import pymysql
import pymysql.cursors
import sys

sys.path.append('../../')
import ini

conn = pymysql.connect(host=ini.ini_host,
                    user=ini.ini_user,
                    password=ini.ini_pass,
                    db=ini.ini_db,
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


