from datetime import date
from functions.DB.format import formatSimpleResult
from functions.DB.queries import generalQuery, updateQuery


def semaforizacion(total):
    if 0 <= total and total < 70:
        return "Malo"
    if 70 <= total and total < 85:
        return "Regular"
    if 85 <= total and total < 89:
        return "Bueno"
    if 89 <= total and total <= 100:
        return "Excelente"


def getMetaByIdTrx(idTrx):
    query = "select meta from plantilla where IDTrx = {};".format(idTrx)
    result = generalQuery(query)
    return {"meta": formatSimpleResult(result)[0]}


def saveResults(listResults, listOriginalResults):
    response = {}
    response["changes"] = False
    if listResults != listOriginalResults:
        response["changes"] = True
        queryUpdateAplica = "UPDATE resultados SET Aplica = CASE ID"
        queryUpdateNota = "UPDATE resultados SET Nota = CASE ID"

        totalIdsNotaActual = ""
        totalIdsAplica = ""
        for i in range(len(listResults)):
            idPlantilla = listResults[i]["idPlantilla"]
            if (
                listOriginalResults[i]["idResultado"] == listResults[i]["idResultado"]
            ):  # verifica si es el mismo resultado
                if (
                    listOriginalResults[i]["notaActual"] != listResults[i]["notaActual"]
                ):  # si hay cambios en la nota actual
                    queryUpdateNota += " WHEN {} THEN {} ".format(
                        listResults[i]["idResultado"], listResults[i]["notaActual"]
                    )
                    totalIdsNotaActual += str(listResults[i]["idResultado"]) + ","
                    print(listOriginalResults[i]["notaActual"])
                    print(listResults[i]["notaActual"])
                    print(totalIdsNotaActual)
                    print(queryUpdateNota)
                if (
                    listOriginalResults[i]["aplica"] != listResults[i]["aplica"]
                ):  # si hay cambios en el aplica

                    queryUpdateAplica += " WHEN {} THEN {} ".format(
                        listResults[i]["idResultado"], listResults[i]["aplica"]
                    )
                    totalIdsAplica += str(listResults[i]["idResultado"]) + ","
                    print(listOriginalResults[i]["aplica"])
                    print(listResults[i]["aplica"])
                    print(totalIdsAplica)
                    print(queryUpdateAplica)

        queryUpdateNota += " ELSE 0 END WHERE ID IN (" + totalIdsNotaActual[:-1] + ");"
        queryUpdateAplica += " ELSE 0 END WHERE ID IN (" + totalIdsAplica[:-1] + ");"
        if totalIdsNotaActual != "":
            response["queryUpdateNota"] = updateQuery(queryUpdateNota)
        if totalIdsAplica != "":
            response["queryUpdateAplica"] = updateQuery(queryUpdateAplica)
        response["queries"] = {
            "updateNota": queryUpdateNota,
            "updateAplica": queryUpdateAplica,
        }
    return response
