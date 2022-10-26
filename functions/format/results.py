def formatResultIntoObj(result):
    return {
        "IDResultado": result[0],
        "IDItem": result[1],
        "NotaActual": result[2],
        "Aplica": result[3],
        "IDPlantilla": result[4],
    }