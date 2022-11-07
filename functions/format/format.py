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
    # "SELECT IdUser,Id,Password,Name1,Email,UserGroup FROM user WHERE STATE = 1"
    return {
        "id": user[0],
        # "username": user[1],
        # "password": user[2],
        "name": user[3],
        "email": user[4],
        "rol": user[5]
    }
