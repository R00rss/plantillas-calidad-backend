from mysql.connector import Error
from functions.DB.connect import connect, closeConnection


def generalQuery(query: str, typeDB=1):
    connection = connect(typeDB)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            closeConnection(connection)
            return result
    except Error as e:
        print("error in general query: ", e)
        closeConnection(connection)
        return None


def updateQuery(query: str):
    connection = connect()
    response = {"message": "", "success": True}
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            rowcount = cursor.rowcount
            if rowcount > 0:
                response["message"] = "rowcount: {}".format(rowcount)
            closeConnection(connection)
            return response
    except Error as e:
        print("error in updateQuery: ", e)
        response["message"] = "error in updateQuery: {}".format(e)
        response["success"] = False
        closeConnection(connection)
        return response


def queryOptions(query: str, options: dict):
    connection = connect()
    response = {"message": "", "success": True, "result": []}
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            if options["fetchOption"] == "all":
                result = cursor.fetchall()
                response["result"] = result
            elif options["fetchOption"] == "one":
                result = cursor.fetchone()
                response["result"] = result
            closeConnection(connection)
            return response
    except Error as e:
        response["message"] = "error in updateQuery: {}".format(e)
        response["success"] = False
        closeConnection(connection)
        return response
