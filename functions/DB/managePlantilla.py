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
    # query = "SELECT items.Descripción,items.NotaMax,gruposerror.Descripción,tiposerrores.Descripción FROM campaniasinbound.items as items INNER JOIN campaniasinbound.gruposerror as gruposerror ON campaniasinbound.items.IDGrupo = campaniasinbound.gruposerror.ID INNER JOIN	campaniasinbound.tiposerrores as tiposerrores ON tiposerrores.ID = IDTipo where items.IDTipoPlantilla = {};".format(
    #     idTipoPlantilla
    # )
    # return query
    # items = generalQuery(query)
    # if len(items) == 0:
    #     return {"message": "No se encontraron items", "success": False}

    # query2 = "select distinct(Descripción) from campaniasinbound.gruposerror;"
    # gruposerror = generalQuery(query2)
    # if len(gruposerror) == 0:
    #     return {"message": "No se encontraron grupos error", "success": False}

    # gruposerror = formatSimpleResult(gruposerror)

    # finalResult = {}

    # for grupo in gruposerror:
    #     finalResult[grupo] = {"items": [], "tipo": "", "aplica": 0, "nombre": grupo}

    # for item in items:
    #     grupoAux = item[2]
    #     if grupoAux in gruposerror:
    #         finalResult[grupoAux]["items"].append(formatItem(item))
    #     finalResult[grupoAux]["tipo"] = item[3]

    # return {
    #     "message": "Datos obtenidos con éxito",
    #     "success": True,
    #     "result": finalResult,
    # }
