from json import load

import pymysql

with open('db/querys.json', 'r') as querys:
    QUERY_DICT = load(querys)


def getConnection():
    conn = pymysql.connect(db='tarea2',
                           user='cc5002',
                           passwd='programacionweb',
                           host='172.17.0.2',
                           port=3306,
                           charset='utf8')
    return conn


def insertContact(nombre, email, celular, comuna_id, fecha_creacion):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(QUERY_DICT["insertContact"],
                   (nombre, email, celular, comuna_id, fecha_creacion))
    conn.commit()


# fix this
def insertDispositivo(contacto_id, nombre, descripcion, tipo, anos_uso,
                      estado):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(QUERY_DICT["insertDispositivo"],
                   (contacto_id, nombre, descripcion, tipo, anos_uso, estado))
    conn.commit()


def insertArchivo(ruta_archivo, nombre_archivo, dispositivo_id):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(QUERY_DICT["insertArchivo"],
                   (ruta_archivo, nombre_archivo, dispositivo_id))
    conn.commit()


def getContactId(nombre, email, celular, comuna_id, fecha_creacion):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(QUERY_DICT["getContactId"],
                   (nombre, email, celular, comuna_id, fecha_creacion))
    id, = cursor.fetchone()
    return id


def getDispositivoId(contacto_id, nombre, descripcion, tipo, anos_uso, estado):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(QUERY_DICT["getDispositivoId"],
                   (contacto_id, nombre, descripcion, tipo, anos_uso, estado))
    id, = cursor.fetchone()
    return id


def ver5Dispositivos(offset):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(QUERY_DICT["ver5Dispositivos"], (offset))
    data = cursor.fetchmany(5)
    # La query retorna un max de 6 elementos para
    # ver si agregar el botón para la siguiente página
    # en ver-dispositivos
    r = 1 if cursor.fetchone() else 0
    return (data, r)


def getArchivoById(id):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(QUERY_DICT["getArchivoById"], (id))
    return cursor.fetchall()


def getContactInfo(id):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(QUERY_DICT["getContactInfo"], (id))
    return cursor.fetchone()


def getDispositivoInfo(id):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(QUERY_DICT["getDispositivoInfo"], (id))
    return cursor.fetchone()


def getComunaInfo(id):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(QUERY_DICT["getComunaInfo"], (id))
    return cursor.fetchone()


def getRegionName(id):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(QUERY_DICT["getRegionName"], (id))
    return cursor.fetchone()[0]
