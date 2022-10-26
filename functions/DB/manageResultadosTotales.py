from functions.DB.format import formatSimpleResult
from functions.DB.queries import generalQuery, updateQuery


def getMetaByIdTrx(idTrx):
    query = "select meta from plantilla where IDTrx = {};".format(idTrx)
    result = generalQuery(query)
    return {"meta": formatSimpleResult(result)[0]}


def saveResults(listResults):
    def semaforizacion(total):
        if 0 <= total and total < 70:
            return "Malo"
        if 70 <= total and total < 85:
            return "Regular"
        if 85 <= total and total < 89:
            return "Bueno"
        if 89 <= total and total <= 100:
            return "Excelente"
    queryUpdateAplica = "UPDATE resultados SET Aplica = CASE ID"
    queryUpdateNota = "UPDATE resultados SET Nota = CASE ID"
    totalIds = ""
    response = {}
    subTotalCal = 0
    subTotalMax = 0
    for result in listResults:
        idPlantilla = result["idPlantilla"]
        if result["aplica"] == 1:
            subTotalCal += result["notaActual"]
            subTotalMax += result["notaMaxima"]

        queryUpdateNota += " WHEN {} THEN {} ".format(
            result["idResultado"], result["notaActual"]
        )
        queryUpdateAplica += " WHEN {} THEN {} ".format(
            result["idResultado"], result["aplica"]
        )
        totalIds += str(result["idResultado"]) + ","

    notaFinal = round((subTotalCal / subTotalMax) * 100, 2)
    semaforizacionCalidad = semaforizacion(notaFinal)
    results = {
        "notaFinal": notaFinal,
        "semaforizacion": semaforizacionCalidad,
        "idPlantilla": idPlantilla,
    }

    queryUpdateNota += " ELSE 0 END WHERE ID IN (" + totalIds[:-1] + ");"
    queryUpdateAplica += " ELSE 0 END WHERE ID IN (" + totalIds[:-1] + ");"

    response["queryUpdateNota"] = updateQuery(queryUpdateNota)
    response["queryUpdateAplica"] = updateQuery(queryUpdateAplica)
    return response
