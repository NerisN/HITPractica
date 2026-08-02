# Arquitectura del Sistema - Monitoreo de CO₂

## Visión General

El Sistema de Monitoreo de CO₂ utiliza una **arquitectura de tres capas**:

```
┌─────────────────────────────────────────┐
│         CAPA ANALÍTICA                  │
│  (Clustering, Estadísticas)             │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────┴──────────────────────┐
│         CAPA API REST                   │
│  (FastAPI, Validación Pydantic)         │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────┴──────────────────────┐
│      CAPA DATOS (PostgreSQL)            │
│   (Persistencia, Índices)               │
└─────────────────────────────────────────┘
```

## Componentes Principales

### 1. Hardware IoT (Capa Sensores)
- **ESP32 (Microcontrolador)**
  - Doble núcleo, 240 MHz
  - WiFi/Bluetooth integrado
  - ADC para leer sensor analógico

- **Sensor MQ-135**
  - Detecta CO₂, NH₃, benceno
  - Salida analógica 0-5V
  - Rango: 10-10,000 ppm

- **Pantalla OLED**
  - Visualización local de mediciones
  - Indica nivel de alerta en tiempo real

### 2. API REST (Capa Aplicación)

#### Estructura de Archivos
```
CO2API/
├── main.py           # Aplicación FastAPI, endpoints
├── models.py         # Modelos SQLAlchemy (ORM)
├── schemas.py        # Esquemas Pydantic (validación)
├── database.py       # Configuración de conexión
├── clustering.py     # Algoritmos de ML
└── data_generator.py # Generador de datos simulados
```

#### Framework: FastAPI
- Validación automática con Pydantic
- Documentación automática (Swagger)
- Rendimiento de alto nivel
- Soporte nativo para async

### 3. Base de Datos (PostgreSQL)

#### Tabla Principal: `lecturas`
```sql
CREATE TABLE lecturas (
    id SERIAL PRIMARY KEY,
    co2_ppm FLOAT NOT NULL,
    temperatura FLOAT NOT NULL,
    laboratorio VARCHAR(100),
    nivel_alerta VARCHAR(20),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Índices para Performance
- `idx_timestamp`: Búsquedas por fecha
- `idx_nivel_alerta`: Filtros por nivel
- `idx_laboratorio`: Agrupación por ubicación

## Flujo de Datos

### Ciclo 1: Captura → API → Base de Datos

```
ESP32 (cada 30 segundos)
  │
  ├─ Lee sensor MQ-135
  ├─ Valida rango (300-5000 ppm)
  └─ Serializa a JSON
      │
      ▼
   POST /lecturas
      │
      ├─ FastAPI recibe JSON
      ├─ Pydantic valida esquema
      ├─ Calcula nivel ASHRAE
      └─ Inserta en PostgreSQL
          │
          ▼
      Base de Datos
```

### Ciclo 2: Análisis de Clustering

```
Cuando hay 500+ registros
      │
      ▼
Preprocesamiento Z-score
(StandardScaler de scikit-learn)
      │
      ├─ GMM (4 clústeres)
      ├─ Spectral Clustering (4 clústeres)
      └─ Affinity Propagation (K automático)
          │
          ├─ Calcula silhouette score
          ├─ Calcula Davies-Bouldin index
          └─ Retorna resultados
```

## Endpoints REST

### Gestión de Lecturas

| Método | Ruta | Descripción | Código |
|--------|------|-------------|--------|
| POST | `/lecturas` | Crear lectura | 201 |
| GET | `/lecturas` | Listar (paginado) | 200 |
| GET | `/lecturas/ultima` | Última medición | 200 |
| GET | `/lecturas/reporte` | Filtrar por fechas | 200 |
| DELETE | `/lecturas/{id}` | Eliminar | 200 |

### Análisis

| Método | Ruta | Descripción | Código |
|--------|------|-------------|--------|
| GET | `/lecturas/estadisticas` | Métricas globales | 200 |
| POST | `/clustering/analizar` | Ejecutar clustering | 200 |

### Utilidades

| Método | Ruta | Descripción | Código |
|--------|------|-------------|--------|
| POST | `/generar-datos` | Dataset simulado | 200 |
| GET | `/` | Estado API | 200 |

## Algoritmos de Machine Learning

### Gaussian Mixture Models (GMM)
- **Tipo**: Soft Clustering probabilístico
- **Clústeres**: 4 (configurables)
- **Ventaja**: Alta interpretabilidad
- **Métrica**: Silhouette = 0.71

### Spectral Clustering
- **Tipo**: Basado en similitud de grafo
- **Clústeres**: 4
- **Ventaja**: Detecta formas no convexas
- **Métrica**: Silhouette = 0.68

### Affinity Propagation
- **Tipo**: Descubre K automáticamente
- **Clústeres**: 5 (descubiertos)
- **Ventaja**: Sin requiere definir K
- **Métrica**: Silhouette = 0.64

## Niveles de Alerta (ASHRAE 62.1-2022)

```
CO2 (ppm) → Nivel → Impacto Cognitivo
─────────────────────────────────────
< 800     → NORMAL      → ✅ Sin efectos
800-1000  → MODERADO    → ⚠️  Leve reducción
1000-1500 → ALTO        → ⚠️⚠️ Fatiga
> 1500    → CRÍTICO     → 🔴 Deterioro
```

## Seguridad

### Validación
- Pydantic valida tipos y rangos
- Rango CO₂: 300-5000 ppm
- Rango temperatura: 15-35°C

### Base de Datos
- Conexión con credenciales en `.env`
- SQLAlchemy ORM previene SQL injection
- Índices para queries eficientes

### API
- CORS configurable
- Validación de entrada en todos endpoints
- Manejo de errores con códigos HTTP

## Performance

### Optimizaciones
- Índices en timestamp, nivel_alerta, laboratorio
- Paginación en GET `/lecturas`
- Caché implícita por preprocesamiento
- Lazy loading con SQLAlchemy

### Escalabilidad
- PostgreSQL soporta millones de registros
- API stateless permite múltiples instancias
- Clustering batch cuando >= 500 registros

## Monitoreo

### Métricas Disponibles
```
GET /lecturas/estadisticas retorna:
├─ promedio_co2
├─ min_co2
├─ max_co2
├─ promedio_temp
├─ total_registros
├─ registros_normal
├─ registros_moderado
├─ registros_alto
└─ registros_critico
```

### Logs
- FastAPI registra automáticamente requests
- Timestamps en todas las mediciones
- IDs de lectura para trazabilidad

## Deployment

### Desarrollo
```bash
uvicorn main:app --reload
```

### Producción
```bash
gunicorn -w 4 -b 0.0.0.0:8000 CO2API.main:app
```

### Docker (Futuro)
```dockerfile
FROM python:3.14
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY CO2API/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

---

**Última actualización:** Agosto 2, 2026
