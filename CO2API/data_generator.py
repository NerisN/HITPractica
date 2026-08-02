import numpy as np
from datetime import datetime, timedelta
import random

def generate_co2_data(n_records: int = 500) -> list:
    """Genera dataset simulado de 500 registros de CO2 con comportamiento realista."""

    data = []
    base_time = datetime.now() - timedelta(days=30)

    for i in range(n_records):
        hour_of_day = (i % 24)

        if hour_of_day < 8 or hour_of_day > 18:
            base_co2 = np.random.normal(550, 50)
            base_temp = np.random.normal(20, 2)
        elif hour_of_day < 10:
            base_co2 = np.random.normal(700, 100)
            base_temp = np.random.normal(21, 2)
        elif hour_of_day < 12:
            base_co2 = np.random.normal(950, 150)
            base_temp = np.random.normal(23, 2)
        elif hour_of_day < 14:
            base_co2 = np.random.normal(1100, 200)
            base_temp = np.random.normal(24, 2)
        elif hour_of_day < 16:
            base_co2 = np.random.normal(1200, 200)
            base_temp = np.random.normal(25, 2)
        else:
            base_co2 = np.random.normal(850, 150)
            base_temp = np.random.normal(23, 2)

        co2_ppm = max(300, min(5000, base_co2 + np.random.normal(0, 30)))
        temperatura = max(15, min(35, base_temp + np.random.normal(0, 1)))

        data.append({
            "co2_ppm": float(co2_ppm),
            "temperatura": float(temperatura),
            "laboratorio": "Lab-Sw-01",
            "timestamp": base_time + timedelta(minutes=i*2.88)
        })

    return data

def calculate_alert_level(co2_ppm: float) -> str:
    """Calcula nivel de alerta según estándar ASHRAE 62.1-2022."""
    if co2_ppm < 800:
        return "NORMAL"
    elif co2_ppm < 1000:
        return "MODERADO"
    elif co2_ppm < 1500:
        return "ALTO"
    else:
        return "CRÍTICO"
