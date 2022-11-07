from functions.DB.format import formatError
from functions.DB.queries import generalQuery, updateQuery


def getErrorsFromGroup(GrupoErrorId):
    query = "SELECT Nombre,MaximaNota,NotaActual,Aplica FROM Errores WHERE GrupoErrorId = {};".format(
        GrupoErrorId
    )
    result = generalQuery(query)
    return result


def getErrors(PlantillaId):
    query = "SELECT * FROM GrupoErrores WHERE PlantillaId = {};".format(PlantillaId)
    result = generalQuery(query)
    errors = []
    for row in result:
        itemsErrors = getErrorsFromGroup(row[0])
        auxItems = []
        for item in itemsErrors:
            auxItems.append(formatError(item))
        auxDict = {
            "nombre": row[1],
            "tipo": row[2],
            "notaMaxima": row[3],
            "notaActual": row[4],
            "aplica": row[5],
            "items": auxItems,
        }
        errors.append(auxDict)
    return {"errors": errors}


def insertGroupsError(nombre, tipoError, notaMaxima, notaActual, PlantillaId):
    query = "INSERT INTO grupoErrores (Nombre,TipoError,MaximaNota,NotaActual,PlantillaId) VALUES ('{}','{}',{},{},{})".format(
        nombre, tipoError, notaMaxima, notaActual, PlantillaId
    )
    return updateQuery(query)


def insertError(nombre, notaMaxima, notaActual, aplica, grupoErrorId):
    query = "INSERT INTO errores (Nombre,MaximaNota,NotaActual,Aplica,GrupoErrorId) VALUES ('{}','{}',{},{},{})".format(
        nombre, notaMaxima, notaActual, aplica, grupoErrorId
    )
    return updateQuery(query)


def insertPlantilla(nombre, trxId):
    query = "INSERT INTO calidadPlantillas (nombre,TrxId) VALUES ('{}', {})".format(
        nombre, trxId
    )
    return updateQuery(query)


