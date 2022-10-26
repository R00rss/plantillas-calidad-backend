def formatSimpleResult(result):
    auxResult = []
    for row in result:
        if row[0] != "" and row[0] != None:
            auxResult.append(row[0])
    return auxResult


def formatError(error):
    return {
        "nombre": error[0],
        "notaMaxima": error[1],
        "notaActual": error[2],
        "aplica": error[3],
    }


def formatPlantilla(plantilla):
    auxPlantilla = plantilla[0]
    return {
        "id": auxPlantilla[0],
        "nombre": auxPlantilla[1],
        "trxId": auxPlantilla[2],
    }


def formatResult(result):
    auxResult = result[0]
    return {
        "notaTotal": auxResult[0],
        "notaENC": auxResult[1],
        "notaECUF": auxResult[2],
        "notaECN": auxResult[3],
        "meta": auxResult[4],
        "semaforizacion": auxResult[5],
    }
