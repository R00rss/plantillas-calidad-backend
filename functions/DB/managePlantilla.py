from functions.DB.queries import generalQuery, updateQuery


def createPlantilla(idTrx, tipoPlantilla, idUsuario=121):
    query = "INSERT INTO plantilla (IDTrx,IDTPlantilla,IDUsuario) VALUES ({}, {},{})".format(
        idTrx, tipoPlantilla, idUsuario
    )
    result = updateQuery(query)
    if result["success"]:
        return True
    return False


def verifyExistPlantilla(idTrx):
    query = "select * from plantilla where IDTrx = {};".format(idTrx)
    result = generalQuery(query)
    if len(result) == 0 and isinstance(result, list):
        return False
    return True


def generateItemsPlantilla(idTipoPlantilla):
    return idTipoPlantilla


def finishPlantillaById(id):

    query = "UPDATE plantilla SET estadoGestion = 'Finalizada' WHERE ID = {};".format(
        id
    )
    return updateQuery(query)


def updateStatusPlantilla(id, newStatus):
    query = "UPDATE plantilla SET estadoGestion = '{}' WHERE ID = {};".format(
        newStatus,id
    )
    return updateQuery(query)
