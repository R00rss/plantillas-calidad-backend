def formatError(error):
    return {
        "nombre": error[1],
        "notaMaxima": error[2],
        "notaActual": error[2],
        "aplica": 1,
    }


def formatItem(item):
    return {
        "nombre": item[0],
        "notaMaxima": item[1],
        "notaActual": item[1],
        "aplica": 1,
    }


def formatDataUserDB2(user):
    return {
        "id": user[0],
        "username": user[4],
    }
