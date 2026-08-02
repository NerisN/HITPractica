from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LecturaCreate(BaseModel):
    co2_ppm: float
    temperatura: float
    laboratorio: Optional[str] = "Lab-Sw-01"

class LecturaResponse(BaseModel):
    id: int
    co2_ppm: float
    temperatura: float
    laboratorio: str
    nivel_alerta: str
    timestamp: datetime

    class Config:
        from_attributes = True

class EstadisticasResponse(BaseModel):
    promedio_co2: float
    min_co2: float
    max_co2: float
    promedio_temp: float
    total_registros: int
    registros_normal: int
    registros_moderado: int
    registros_alto: int
    registros_critico: int
