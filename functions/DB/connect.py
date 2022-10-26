from decouple import config
import mysql.connector
from mysql.connector import Error

DB_HOST_I = config("DB_HOST_I")
DB_NAME_I = config("DB_NAME_I")
DB_USER_I = config("DB_USER_I")
DB_PASS_I = config("DB_PASS_I")
DB_PORT_I = config("DB_PORT_I")

DB_HOST_II = config("DB_HOST_II")
DB_NAME_II = config("DB_NAME_II")
DB_USER_II = config("DB_USER_II")
DB_PASS_II = config("DB_PASS_II")
DB_PORT_II = config("DB_PORT_II")


def connect(typeDB=1):
    if typeDB == 1:        
        try:
            return mysql.connector.connect(
                host=DB_HOST_I,
                user=DB_USER_I,
                password=DB_PASS_I,
                database=DB_NAME_I,
                port=DB_PORT_I,
            )
        except Error as e:
            print(e)
            return None
    elif typeDB == 2:
        try:
            return mysql.connector.connect(
                host=DB_HOST_II,
                user=DB_USER_II,
                password=DB_PASS_II,
                database=DB_NAME_II,
                port=DB_PORT_II,
            )
        except Error as e:
            print(e)
            return None


def closeConnection(connection):
    if connection.is_connected():
        connection.close()
