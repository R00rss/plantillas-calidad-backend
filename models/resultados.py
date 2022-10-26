from pydantic import BaseModel


class resultadosModel(BaseModel):
    resultados: list
    idUser:int | None = None
