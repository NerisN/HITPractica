from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List
import os

from database import engine, get_db, Base
from models import Lectura
from schemas import LecturaCreate, LecturaResponse, EstadisticasResponse
from data_generator import generate_co2_data, calculate_alert_level
from clustering import run_clustering_analysis

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Monitoreo CO2 - UES",
    description="Sistema de monitoreo de dióxido de carbono para laboratorios de Ingeniería de Software",
    version="1.0.0"
)

@app.get("/", tags=["Status"])
def root():
    """Endpoint raíz - estado de la API."""
    return {
        "servicio": "API Monitoreo CO2 - UES",
        "estado": "activo",
        "version": "1.0.0",
        "documentacion": "/docs"
    }

@app.post("/lecturas", response_model=LecturaResponse, status_code=201, tags=["Lecturas"])
def crear_lectura(lectura: LecturaCreate, db: Session = Depends(get_db)):
    """Crea una nueva lectura de CO2. ESP32 envía nuevas mediciones aquí."""
    if lectura.co2_ppm < 300 or lectura.co2_ppm > 5000:
        raise HTTPException(status_code=400, detail="Valor CO2 fuera de rango (300-5000 ppm)")

    nivel_alerta = calculate_alert_level(lectura.co2_ppm)

    db_lectura = Lectura(
        co2_ppm=lectura.co2_ppm,
        temperatura=lectura.temperatura,
        laboratorio=lectura.laboratorio,
        nivel_alerta=nivel_alerta
    )
    db.add(db_lectura)
    db.commit()
    db.refresh(db_lectura)

    return db_lectura

@app.get("/lecturas", response_model=List[LecturaResponse], tags=["Lecturas"])
def obtener_lecturas(
    limite: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Obtiene historial de mediciones con paginación."""
    lecturas = db.query(Lectura).order_by(desc(Lectura.timestamp)).offset(offset).limit(limite).all()
    return lecturas

@app.get("/lecturas/ultima", response_model=LecturaResponse, tags=["Lecturas"])
def obtener_ultima_lectura(db: Session = Depends(get_db)):
    """Obtiene la última medición registrada del laboratorio."""
    lectura = db.query(Lectura).order_by(desc(Lectura.timestamp)).first()

    if not lectura:
        raise HTTPException(status_code=404, detail="No hay lecturas registradas")

    return lectura

@app.get("/lecturas/reporte", response_model=List[LecturaResponse], tags=["Lecturas"])
def obtener_reporte(
    fecha_inicio: str = Query("2025-01-01"),
    fecha_fin: str = Query("2026-12-31"),
    db: Session = Depends(get_db)
):
    """Filtra lecturas por rango de fechas (formato: YYYY-MM-DD)."""
    try:
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD")

    lecturas = db.query(Lectura).filter(
        Lectura.timestamp >= inicio,
        Lectura.timestamp <= fin
    ).order_by(Lectura.timestamp).all()

    return lecturas

@app.get("/lecturas/estadisticas", response_model=EstadisticasResponse, tags=["Análisis"])
def obtener_estadisticas(db: Session = Depends(get_db)):
    """Calcula estadísticas generales: promedio, mín, máx por nivel de alerta."""
    total = db.query(func.count(Lectura.id)).scalar()

    if total == 0:
        raise HTTPException(status_code=404, detail="No hay datos para analizar")

    stats = db.query(
        func.avg(Lectura.co2_ppm).label("promedio_co2"),
        func.min(Lectura.co2_ppm).label("min_co2"),
        func.max(Lectura.co2_ppm).label("max_co2"),
        func.avg(Lectura.temperatura).label("promedio_temp")
    ).first()

    registros_por_nivel = db.query(
        Lectura.nivel_alerta,
        func.count(Lectura.id).label("cantidad")
    ).group_by(Lectura.nivel_alerta).all()

    nivel_dict = {nivel: cantidad for nivel, cantidad in registros_por_nivel}

    return EstadisticasResponse(
        promedio_co2=float(stats.promedio_co2 or 0),
        min_co2=float(stats.min_co2 or 0),
        max_co2=float(stats.max_co2 or 0),
        promedio_temp=float(stats.promedio_temp or 0),
        total_registros=int(total),
        registros_normal=int(nivel_dict.get("NORMAL", 0)),
        registros_moderado=int(nivel_dict.get("MODERADO", 0)),
        registros_alto=int(nivel_dict.get("ALTO", 0)),
        registros_critico=int(nivel_dict.get("CRÍTICO", 0))
    )

@app.delete("/lecturas/{lectura_id}", tags=["Lecturas"])
def eliminar_lectura(lectura_id: int, db: Session = Depends(get_db)):
    """Elimina un registro específico por su ID."""
    db_lectura = db.query(Lectura).filter(Lectura.id == lectura_id).first()

    if not db_lectura:
        raise HTTPException(status_code=404, detail="Lectura no encontrada")

    db.delete(db_lectura)
    db.commit()

    return {"mensaje": f"Lectura {lectura_id} eliminada correctamente"}

@app.post("/clustering/analizar", tags=["Análisis"])
def analizar_clustering(db: Session = Depends(get_db)):
    """Ejecuta análisis de clustering cuando hay 500+ registros."""
    total_registros = db.query(func.count(Lectura.id)).scalar()

    if total_registros < 3:
        return {
            "estado": "datos_insuficientes",
            "total_registros": total_registros,
            "requerido": 500,
            "mensaje": "Se necesitan más registros para ejecutar clustering"
        }

    lecturas = db.query(Lectura).all()
    datos = [
        {"co2_ppm": l.co2_ppm, "temperatura": l.temperatura}
        for l in lecturas
    ]

    resultados = run_clustering_analysis(datos)

    return {
        "total_registros": total_registros,
        "analisis": resultados
    }

@app.post("/generar-datos", tags=["Utilidades"])
def generar_datos_demo(cantidad: int = 500, db: Session = Depends(get_db)):
    """Genera dataset simulado de CO2 para pruebas (solo para desarrollo)."""
    datos = generate_co2_data(cantidad)

    insertados = 0
    for dato in datos:
        nivel_alerta = calculate_alert_level(dato["co2_ppm"])
        lectura = Lectura(
            co2_ppm=dato["co2_ppm"],
            temperatura=dato["temperatura"],
            laboratorio=dato["laboratorio"],
            nivel_alerta=nivel_alerta,
            timestamp=dato.get("timestamp")
        )
        db.add(lectura)
        insertados += 1

    db.commit()

    return {
        "mensaje": "Datos generados exitosamente",
        "registros_insertados": insertados,
        "total_en_base": db.query(func.count(Lectura.id)).scalar()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
