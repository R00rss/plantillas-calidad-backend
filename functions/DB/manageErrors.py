from functions.format.results import formatResultIntoObj
from functions.DB.format import formatSimpleResult
from functions.format.format import formatError, formatItem
from functions.DB.queries import generalQuery, updateQuery


def getErrorsByType(idTipoPlantilla):
    query = "select * from items where IDTipoPlantilla = {};".format(idTipoPlantilla)
    result = generalQuery(query)
    formatResult = []
    if len(result) == 0:
        return False
    for row in result:
        auxErrorFormatted = formatError(row)
        formatResult.append(auxErrorFormatted)
    return formatResult


def test(idTipoPlantilla, idTrx):
    def getResultByIdItem(idItem, results):
        for result in results:
            if result["IDItem"] == idItem:
                return result
        return None

    query = "SELECT items.Descripción,items.NotaMax,gruposerror.Descripción,tiposerrores.Descripción,items.ID FROM campaniasinbound.items as items INNER JOIN campaniasinbound.gruposerror as gruposerror ON campaniasinbound.items.IDGrupo = campaniasinbound.gruposerror.ID INNER JOIN	campaniasinbound.tiposerrores as tiposerrores ON tiposerrores.ID = IDTipo where items.IDTipoPlantilla = {};".format(
        idTipoPlantilla
    )
    items = generalQuery(query)
    if len(items) == 0:
        return False

    query2 = "select distinct(Descripción) from campaniasinbound.gruposerror;"
    gruposerror = generalQuery(query2)
    if len(gruposerror) == 0:
        return False

    gruposerror = formatSimpleResult(gruposerror)

    finalResult = {}

    for grupo in gruposerror:
        finalResult[grupo] = {"items": [], "tipo": "", "aplica": 1, "nombre": grupo}

    resultados = getResults(idTrx)
    if resultados["success"]:
        auxResultados = resultados["data"]
        for i in range(len(items)):
            grupoAux = items[i][2]
            idItem = items[i][4]
            findedResult = getResultByIdItem(idItem, auxResultados)
            if findedResult != None and grupoAux in gruposerror:
                auxObj = {
                    "nombre": items[i][0],
                    "notaMaxima": items[i][1],
                    "notaActual": findedResult["NotaActual"],
                    "aplica": findedResult["Aplica"],
                    "idItem": findedResult["IDItem"],
                    "idPlantilla": findedResult["IDPlantilla"],
                    "idResultado": findedResult["IDResultado"],
                }
                finalResult[grupoAux]["items"].append(auxObj)
            finalResult[grupoAux]["tipo"] = items[i][3]
    return finalResult


def verifyExistResults(idTrx):
    query = "SELECT ID from campaniasinbound.plantilla where IDTrx = {};".format(idTrx)
    resultPlantilla = generalQuery(query)
    if len(resultPlantilla) == 0 and isinstance(resultPlantilla, list):
        return False

    IDPlantilla = resultPlantilla[0][0]

    query = "SELECT ID from campaniasinbound.resultados where IDPlantilla = {};".format(
        IDPlantilla
    )
    result = generalQuery(query)
    if len(result) == 0:
        return False
    return True


def getResults(idTrx):
    query = "SELECT ID from campaniasinbound.plantilla where IDTrx = {};".format(idTrx)
    resultPlantilla = generalQuery(query)
    if len(resultPlantilla) == 0:
        return {"message": "no plantilla", "success": False}

    IDPlantilla = resultPlantilla[0][0]

    query = "SELECT * from campaniasinbound.resultados where IDPlantilla = {};".format(
        IDPlantilla
    )
    result = generalQuery(query)
    if len(result) == 0:
        return {"message": "no resultados", "success": False}
    # return {"message": "", "success": True, "result": result}
    finalResult = []
    for row in result:
        finalResult.append(formatResultIntoObj(row))
    return {
        "message": "existen resultados",
        "success": True,
        "data": finalResult,
        "idPlantilla": IDPlantilla,
    }


def generateResults(idTrx):
    # one per plantilla
    query = "SELECT ID,IDTPlantilla from campaniasinbound.plantilla where IDTrx = {};".format(
        idTrx
    )
    resultPlantilla = generalQuery(query)
    if len(resultPlantilla) == 0:
        return {"message": "no plantilla", "success": False}

    IDPlantilla = resultPlantilla[0][0]
    IDTipoPlantilla = resultPlantilla[0][1]

    # return {"IDPlantilla": IDPlantilla, "IDTipoPlantilla": IDTipoPlantilla}

    query = "SELECT ID,NotaMax from campaniasinbound.items where IDTipoPlantilla = {};".format(
        IDTipoPlantilla
    )
    items = generalQuery(query)
    if len(items) == 0:
        return {"message": "no items", "success": False}

    queryToCreateResults = (
        "INSERT INTO resultados (IDPlantilla,IDItem,Nota,Aplica) VALUES "
    )
    for i in range(len(items)):
        if i == len(items) - 1:
            queryToCreateResults += "({},{},{},{});".format(
                IDPlantilla, items[i][0], items[i][1], 1
            )
        else:
            queryToCreateResults += "({},{},{},{}),".format(
                IDPlantilla, items[i][0], items[i][1], 1
            )
    statusQuery = updateQuery(queryToCreateResults)
    return {"query": statusQuery}
