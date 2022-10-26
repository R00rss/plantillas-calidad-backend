from functions.cypher.auth import verifyUserPassword
from fastapi import FastAPI
import uvicorn
import requests

# funciones
from functions.DB.queries import generalQuery
from functions.DB.format import formatSimpleResult
from functions.DB.manageResultadosTotales import getMetaByIdTrx, saveResults
from functions.DB.manageErrors import generateResults, verifyExistResults, test
from functions.DB.managePlantilla import (
    createPlantilla,
    verifyExistPlantilla,
)

# modelos para la base de datos
from models.users import userAuthModel
from models.plantillas import createPlantillaModel
from models.llamadas import infoLlamadaModel
from models.resultados import resultadosModel

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.post("/api/auth")
async def auth(userAuth: userAuthModel):
    return verifyUserPassword(userAuth.username, userAuth.password)


# create methods
@app.post("/api/plantilla")
async def postPlantilla(plantilla: createPlantillaModel):
    idTrx = plantilla.idTrx
    idTipoPlantilla = plantilla.tipoPlantilla
    idUsuario = plantilla.idUser

    existPlantilla = verifyExistPlantilla(idTrx)
    existResult = verifyExistResults(idTrx)

    createdPlantilla = False
    createdResult = False

    if not existPlantilla:
        createdPlantilla = createPlantilla(idTrx, idTipoPlantilla, idUsuario)
    if not existResult:
        createdResult = generateResults(idTrx)
    existPlantilla = verifyExistPlantilla(idTrx)
    existResult = verifyExistResults(idTrx)
    if existPlantilla and existResult:
        return {
            "result": test(idTipoPlantilla, idTrx),
            "success": True,
            "existPlantilla": existPlantilla,
            "existResult": existResult,
            "createdPlantilla": createdPlantilla,
            "createdResult": createdResult,
        }
    return {
        "message": "No se puedo crear",
        "success": False,
        "existPlantilla": existPlantilla,
        "existResult": existResult,
        "createdPlantilla": createdPlantilla,
        "createdResult": createdResult,
    }


@app.post("/api/resultados")
async def resultados(payload: resultadosModel):
    return saveResults(payload.resultados)


# find methods


@app.get("/api/subMotivos")
async def getSubMotivos(motivo: str):
    query = (
        "SELECT distinct(SubmotivoLlamada) FROM trx where MotivoLlamada = '{}'".format(
            motivo
        )
    )
    data = generalQuery(query)
    return {"result": formatSimpleResult(data)}


@app.get("/api/inicialData")
async def getInicialData():
    cooperativas = generalQuery("SELECT distinct(Cooperativa) FROM trx")
    motivos = generalQuery("SELECT distinct(MotivoLlamada) FROM trx")
    return {
        "cooperativas": formatSimpleResult(cooperativas),
        "motivos": formatSimpleResult(motivos),
    }


@app.get("/api/meta/{idTrx}")
async def getMeta(idTrx: int):
    return getMetaByIdTrx(idTrx)


# route del filtro de llamadas
@app.post("/api/getLlamadas")
async def getLlamadas(infoCall: infoLlamadaModel):
    query = "SELECT NombreCliente, Identificacion, Cooperativa, Agent, substr(StartedManagement,1,19), TipoLlamada, Celular, MotivoLlamada, SubmotivoLlamada,Observaciones,ID FROM trx WHERE NombreCliente like '%{nombres}%' and Cooperativa like '%{cooperativa}%' and Identificacion like '{cedula}%' and MotivoLlamada like '%{motivo}%' and SubmotivoLlamada like '%{subMotivo}%' {rangeDate};".format(
        nombres=infoCall.nombres if infoCall.nombres else "",
        cooperativa=infoCall.cooperativa if infoCall.cooperativa else "",
        cedula=infoCall.cedula if infoCall.cedula else "",
        motivo=infoCall.motivo if infoCall.motivo else "",
        subMotivo=infoCall.subMotivo if infoCall.subMotivo else "",
        fechaI=infoCall.fechaI if infoCall.fechaI else "",
        fechaF=infoCall.fechaF if infoCall.fechaF else "",
        rangeDate="AND StartedManagement BETWEEN '"
        + infoCall.fechaI
        + " 00:00:00' AND '"
        + infoCall.fechaF
        + " 23:59:59'"
        if (infoCall.fechaI and infoCall.fechaF)
        else "",
    )
    data = generalQuery(query)
    return {"data": data}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=2001, reload=True)
