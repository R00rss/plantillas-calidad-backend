from pydantic import BaseModel


class resultadosModel(BaseModel):
    data: list
    originalData: list
    idUser:int | None = None
