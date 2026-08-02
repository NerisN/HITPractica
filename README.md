# Sistema de Monitoreo de CO₂ - Universidad Estatal de Sonora

Sistema integrado de monitoreo de calidad del aire en laboratorios de Ingeniería de Software, compuesto por:
- **Hardware IoT**: ESP32 + Sensor MQ-135 (costo: $653 MXN)
- **API REST**: FastAPI + PostgreSQL con 6 endpoints funcionales
- **Análisis de datos**: Clustering no supervisado (GMM, Spectral Clustering, Affinity Propagation)

## 📋 Requisitos

- Python 3.14+
- PostgreSQL 16
- pip

## 🚀 Instalación

### 1. Clonar repositorio
```bash
git clone https://github.com/NerisN/HITPractica.git
cd HITPractica
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
```bash
# Copiar archivo de configuración
cp .env.example .env

# Editar .env con tus credenciales PostgreSQL
# DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/co2_monitoreo
```

### 5. Ejecutar API
```bash
cd CO2API
uvicorn main:app --reload
```

La API estará disponible en: **http://localhost:8000**
Documentación interactiva: **http://localhost:8000/docs**

## 📡 Endpoints REST

| Método | Endpoint | Descripción | Respuesta |
|--------|----------|-------------|-----------|
| **POST** | `/lecturas` | ESP32 envía nueva medición | 201 + objeto lectura |
| **GET** | `/lecturas` | Historial con paginación | Lista de lecturas |
| **GET** | `/lecturas/ultima` | Última medición | Objeto lectura |
| **GET** | `/lecturas/reporte` | Filtrar por rango de fechas | Lista filtrada |
| **GET** | `/lecturas/estadisticas` | Estadísticas generales | Métricas CO2 y temperatura |
| **DELETE** | `/lecturas/{id}` | Eliminar registro por ID | Confirmación |

## 🔬 Endpoints de Análisis

### Clustering (GMM, Spectral, Affinity Propagation)
```bash
POST /clustering/analizar
```
Ejecuta análisis de clustering cuando hay 500+ registros.

### Generar Datos de Prueba
```bash
POST /generar-datos?cantidad=500
```
Crea dataset simulado con 500 registros de CO2.

## 📊 Niveles de Alerta (ASHRAE 62.1-2022)

| Nivel | Rango (ppm) | Impacto |
|-------|-------------|--------|
| 🟢 NORMAL | < 800 | Sin efectos adversos |
| 🟡 MODERADO | 800-1,000 | Leve reducción de concentración |
| 🟠 ALTO | 1,000-1,500 | Fatiga, somnolencia moderada |
| 🔴 CRÍTICO | > 1,500 | Deterioro cognitivo significativo |

## 🧪 Prueba Rápida

```bash
# 1. Generar datos de prueba
curl -X POST http://localhost:8000/generar-datos?cantidad=500

# 2. Obtener estadísticas
curl http://localhost:8000/lecturas/estadisticas

# 3. Ejecutar clustering
curl -X POST http://localhost:8000/clustering/analizar

# 4. Obtener última lectura
curl http://localhost:8000/lecturas/ultima
```

## 🏗️ Estructura del Proyecto

```
HITPractica/
├── CO2API/
│   ├── main.py              # API REST con FastAPI
│   ├── models.py            # Modelos SQLAlchemy
│   ├── database.py          # Configuración PostgreSQL
│   ├── schemas.py           # Esquemas Pydantic
│   ├── clustering.py        # Algoritmos de clustering
│   ├── data_generator.py    # Generador de datos simulados
│   └── __init__.py
├── requirements.txt         # Dependencias Python
├── .env.example             # Plantilla de configuración
└── README.md               # Este archivo
```

## 📦 Tecnologías

- **FastAPI 0.115.0**: Framework de API REST de alto rendimiento
- **SQLAlchemy 2.0.35**: ORM para PostgreSQL
- **PostgreSQL 16**: Base de datos relacional
- **Pydantic 2.9.2**: Validación de datos
- **scikit-learn 1.4+**: Algoritmos de machine learning
- **pandas 2.0+**: Análisis y manipulación de datos

## 🔧 Variables de Entorno

```env
DATABASE_URL=postgresql://user:password@localhost:5432/co2_monitoreo
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
```

## 📝 Ejemplo de Consulta

**Crear lectura:**
```bash
curl -X POST http://localhost:8000/lecturas \
  -H "Content-Type: application/json" \
  -d '{
    "co2_ppm": 950.5,
    "temperatura": 23.2,
    "laboratorio": "Lab-Sw-01"
  }'
```

**Respuesta:**
```json
{
  "id": 1,
  "co2_ppm": 950.5,
  "temperatura": 23.2,
  "laboratorio": "Lab-Sw-01",
  "nivel_alerta": "MODERADO",
  "timestamp": "2026-08-02T10:30:45"
}
```

## 📚 Documentación

- Documentación interactiva: `http://localhost:8000/docs`
- Schema OpenAPI: `http://localhost:8000/openapi.json`

## 👥 Equipo

- Castro Huerta Neri Emmanuel
- Espinoza Esquer Leonardo Antonio
- Medina Bojorquez Dilan Arian

**Profesor:** Dominguez Hurtado José Martín  
**Grupo:** 001  
**Institución:** Universidad Estatal de Sonora

## 📄 Licencia

Proyecto académico - Universidad Estatal de Sonora

---

**Última actualización:** Agosto 2, 2026
