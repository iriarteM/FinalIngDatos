import cx_Oracle


def conectar_bd():
    try:
        conexion = cx_Oracle.connect(
            user="user1",
            password="123",
            dsn="localhost:1521/XE",
            encoding="UTF-8",
        )
        return conexion

    except Exception as ex:
        print("Error al conectar a la base de datos Oracle:", ex)
        return None
