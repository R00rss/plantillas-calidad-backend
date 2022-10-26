from pydantic import BaseModel


class plantillaModel(BaseModel):
    nombre: str
    trxId: int


class createPlantillaModel(BaseModel):
    idTrx: int
    tipoPlantilla: int
    idUser: int


class errorModel(BaseModel):
    nombre: str
    maximaNota: float
    notaActual: float
    aplica: bool
    grupoErrorId: int
