import pymysql


def getConnection():
    conn = pymysql.connect(db='tarea2',
                           user='cc5002',
                           passwd='programacionweb',
                           host='172.17.0.2',
                           port=3306,
                           charset='utf8')
    return conn
