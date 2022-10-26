from typing import Dict
from pydantic import BaseModel


class infoLlamadaModel(BaseModel):
    fechaI: str = None
    fechaF: str = None
    cooperativa: str = None
    cedula: str = None
    nombres: str = None
    motivo: str = None
    subMotivo: str = None
