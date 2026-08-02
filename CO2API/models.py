from sqlalchemy import Column, Integer, Float, String, DateTime, func
from datetime import datetime
from database import Base

class Lectura(Base):
    __tablename__ = "lecturas"

    id = Column(Integer, primary_key=True, index=True)
    co2_ppm = Column(Float, nullable=False)
    temperatura = Column(Float, nullable=False)
    laboratorio = Column(String(100), default="Lab-Sw-01")
    nivel_alerta = Column(String(20), default="NORMAL")
    timestamp = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Lectura(id={self.id}, co2_ppm={self.co2_ppm}, nivel={self.nivel_alerta})>"
