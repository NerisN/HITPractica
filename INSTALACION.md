# Guía de Instalación - Sistema de Monitoreo de CO₂

## 1. Instalar PostgreSQL

### macOS (usando Homebrew)
```bash
brew install postgresql@16
brew services start postgresql@16
```

### Windows
1. Descargar instalador desde: https://www.postgresql.org/download/windows/
2. Ejecutar el instalador
3. Anotar la contraseña del usuario `postgres`
4. Agregar PostgreSQL al PATH

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install postgresql-16 postgresql-contrib-16
sudo systemctl start postgresql
```

## 2. Crear Base de Datos

```bash
# Conectarse a PostgreSQL
psql -U postgres

# Crear base de datos
CREATE DATABASE co2_monitoreo;

# Crear usuario (opcional)
CREATE USER co2_admin WITH PASSWORD 'tu_contraseña_segura';
GRANT ALL PRIVILEGES ON DATABASE co2_monitoreo TO co2_admin;

# Salir
\q
```

## 3. Configurar Credenciales

```bash
# En la raíz del proyecto, crear .env
cp .env.example .env

# Editar .env con tus credenciales
# Ejemplo:
# DATABASE_URL=postgresql://postgres:password@localhost:5432/co2_monitoreo
```

## 4. Instalar Dependencias Python

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno
source venv/bin/activate  # macOS/Linux
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## 5. Inicializar Base de Datos

### Opción 1: Usar el script SQL
```bash
psql -U postgres -f setup_db.sql
```

### Opción 2: Dejar que FastAPI cree las tablas
La primera vez que ejecutes la API, FastAPI creará automáticamente las tablas.

## 6. Ejecutar API

```bash
cd CO2API
uvicorn main:app --reload
```

La API estará disponible en: **http://localhost:8000**

## 7. Acceder a Documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 8. Generar Datos de Prueba

```bash
# Opción 1: Desde curl
curl -X POST http://localhost:8000/generar-datos?cantidad=500

# Opción 2: Ejecutar test_api.py
python test_api.py
```

## Solucionar Problemas

### Error: "connection refused"
- Verificar que PostgreSQL esté corriendo
- Revisar las credenciales en `.env`
- Verificar el puerto (por defecto 5432)

### Error: "database does not exist"
- Crear la base de datos: `createdb -U postgres co2_monitoreo`

### Error: "psycopg2.OperationalError"
- Instalar psycopg2: `pip install psycopg2-binary`

### Error de permisos en PostgreSQL
- Ejecutar: `psql -U postgres`
- Luego crear la base de datos y usuario como se describe arriba

## Verificar Instalación

```bash
# Verificar Python
python --version  # Debe ser 3.14+

# Verificar PostgreSQL
psql --version

# Verificar dependencias
pip list | grep -E "fastapi|sqlalchemy|psycopg2"
```

## Configuración para Producción

1. Cambiar `API_RELOAD=false` en `.env`
2. Usar secretos seguros en `DATABASE_URL`
3. Configurar CORS si es necesario
4. Usar servidor WSGI como Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 CO2API.main:app
```

---

**Última actualización:** Agosto 2, 2026
