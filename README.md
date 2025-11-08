# Biblioteca API

API REST desarrollada con FastAPI para gestionar una biblioteca de libros y autores.

## Descripción

API REST para gestionar una biblioteca con las siguientes funcionalidades:

- Gestión de libros y autores (CRUD)
- Búsqueda por título o autor
- Filtros por autor o año de publicación
- Paginación
- Validaciones de datos (ISBN, años, longitudes)
- Documentación interactiva (Swagger/OpenAPI)

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido para construir APIs
- **PostgreSQL**: Base de datos relacional
- **SQLAlchemy**: ORM para interactuar con la base de datos
- **Pydantic**: Validación de datos y serialización
- **Pytest**: Framework de pruebas unitarias e integración
- **Docker & Docker Compose**: Contenedorización de la aplicación
- **Uvicorn**: Servidor ASGI para ejecutar FastAPI

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.11** o superior
- **Docker** y **Docker Compose** (recomendado)
- **Git** (para clonar el repositorio)

## Instalación

### Opción 1: Usando Docker (Recomendado)

1. **Clonar el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd biblioteca-rest-api
   ```

2. **Crear archivo de variables de entorno**:
   ```bash
   cp .env.example .env
   ```
   Edita el archivo `.env` si necesitas cambiar la configuración por defecto.

3. **Construir y ejecutar los contenedores**:
   ```bash
   docker-compose up --build
   ```

   Esto iniciará:
   - PostgreSQL en el puerto 5435 (accesible desde tu máquina)
   - La API FastAPI en el puerto 8000

   **Nota:** Los contenedores se comunican internamente usando el puerto 5432 de PostgreSQL, pero desde tu máquina accederás al puerto 5435.

4. **Verificar que la aplicación está funcionando**:
   ```bash
   curl http://localhost:8000/health
   ```

### Opción 2: Instalación Local (Sin Docker)

1. **Clonar el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd biblioteca-rest-api
   ```

2. **Crear un entorno virtual**:
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar PostgreSQL**:
   - Instala PostgreSQL en tu sistema
   - Crea una base de datos llamada `biblioteca_db`
   - Crea un archivo `.env` con la siguiente configuración:
     ```
     DATABASE_URL=postgresql://usuario:password@localhost:5432/biblioteca_db
     ```

5. **Inicializar la base de datos**:
   ```bash
   python -c "from app.database import init_db; init_db()"
   ```

6. **Ejecutar la aplicación**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Ejecutar Tests

Para ejecutar los tests, asegúrate de tener las dependencias instaladas y ejecuta:

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests con cobertura
pytest --cov=app --cov-report=html

# Ejecutar tests con output detallado
pytest -v

# Ejecutar un archivo de tests específico
pytest app/tests/test_endpoints.py
```

Los tests incluyen:
- **Tests unitarios**: Para operaciones CRUD y validaciones
- **Tests de integración**: Para endpoints de la API
- **Tests de validación**: Para schemas de Pydantic

## Endpoints Disponibles

### Health Check

- **GET** `/health`
  - Verifica que la API está funcionando
  - **Respuesta**: `{"status": "healthy", "message": "API is running"}`

### Libros

#### Crear un libro
- **POST** `/libros`
  - Crea un nuevo libro en la biblioteca
  - **Body**:
    ```json
    {
      "titulo": "Cien años de soledad",
      "isbn": "9788437604947",
      "ano_publicacion": 1967,
      "autor_id": 1
    }
    ```
  - **Respuestas**:
    - `201 Created`: Libro creado exitosamente
    - `400 Bad Request`: Datos inválidos o autor no existe
    - `409 Conflict`: ISBN duplicado

#### Listar libros
- **GET** `/libros`
  - Lista todos los libros con filtros opcionales y paginación
  - **Query Parameters**:
    - `autor_id` (opcional): Filtrar por ID de autor
    - `ano` (opcional): Filtrar por año de publicación
    - `skip` (opcional, default: 0): Número de registros a saltar
    - `limit` (opcional, default: 10, máximo: 100): Número máximo de registros
  - **Ejemplo**: `GET /libros?ano=2000&skip=0&limit=10`
  - **Respuesta**:
    ```json
    {
      "items": [...],
      "total": 50,
      "skip": 0,
      "limit": 10
    }
    ```

#### Obtener un libro específico
- **GET** `/libros/{libro_id}`
  - Obtiene la información de un libro por su ID
  - **Respuestas**:
    - `200 OK`: Libro encontrado
    - `404 Not Found`: Libro no encontrado

#### Actualizar un libro
- **PUT** `/libros/{libro_id}`
  - Actualiza la información de un libro existente
  - **Body** (todos los campos son opcionales):
    ```json
    {
      "titulo": "Nuevo título",
      "isbn": "9788437604948",
      "ano_publicacion": 1968,
      "autor_id": 2
    }
    ```
  - **Respuestas**:
    - `200 OK`: Libro actualizado exitosamente
    - `400 Bad Request`: Datos inválidos
    - `404 Not Found`: Libro no encontrado
    - `409 Conflict`: ISBN duplicado

#### Eliminar un libro
- **DELETE** `/libros/{libro_id}`
  - Elimina un libro de la biblioteca
  - **Respuestas**:
    - `204 No Content`: Libro eliminado exitosamente
    - `404 Not Found`: Libro no encontrado

#### Buscar libros
- **GET** `/libros/buscar`
  - Busca libros por título o nombre de autor (búsqueda parcial, case-insensitive)
  - **Query Parameters**:
    - `titulo` (opcional): Término de búsqueda en el título
    - `autor` (opcional): Término de búsqueda en el nombre del autor
    - `skip` (opcional, default: 0): Número de registros a saltar
    - `limit` (opcional, default: 10, máximo: 100): Número máximo de registros
  - **Ejemplo**: `GET /libros/buscar?titulo=soledad&autor=García`
  - **Nota**: Al menos uno de los parámetros (`titulo` o `autor`) debe ser proporcionado
  - **Respuesta**:
    ```json
    {
      "items": [...],
      "total": 5,
      "skip": 0,
      "limit": 10
    }
    ```

## Documentación Interactiva

Una vez que la aplicación esté ejecutándose, puedes acceder a la documentación interactiva:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Acceso a los Servicios

Cuando la aplicación esté corriendo, podrás acceder a:

- **API REST**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **PostgreSQL** (si usas Docker): `localhost:5435`
- **PostgreSQL** (si instalaste localmente): `localhost:5432`

## Modelo de Datos

### Tabla: `autores`
- `id` (Integer, Primary Key): ID único del autor
- `nombre` (String, 200 caracteres): Nombre del autor

### Tabla: `libros`
- `id` (Integer, Primary Key): ID único del libro
- `titulo` (String, 300 caracteres): Título del libro
- `isbn` (String, 17 caracteres, Unique): ISBN del libro (10 o 13 dígitos)
- `ano_publicacion` (Integer): Año de publicación (debe ser > 1000 y <= año actual)
- `autor_id` (Integer, Foreign Key): ID del autor (relación con tabla `autores`)

### Relaciones
- Un autor puede tener muchos libros (relación uno a muchos)
- Un libro pertenece a un solo autor (relación muchos a uno)
- Al eliminar un autor, se eliminan automáticamente sus libros (CASCADE)

## Validaciones Implementadas

### ISBN
- Debe tener exactamente 10 o 13 dígitos
- Puede contener guiones, pero se limpian automáticamente
- Debe ser único en la base de datos

### Año de Publicación
- Debe ser mayor a 1000
- No puede ser mayor al año actual

### Título y Nombre de Autor
- Título: Entre 1 y 300 caracteres
- Nombre de autor: Entre 1 y 200 caracteres

## Arquitectura del Proyecto

```
biblioteca-rest-api/
├── app/
│   ├── __init__.py
│   ├── main.py           # Aplicación principal FastAPI
│   ├── database.py       # Configuración de base de datos
│   ├── models.py         # Modelos SQLAlchemy
│   ├── schemas.py        # Schemas Pydantic para validación
│   ├── crud.py           # Operaciones CRUD
│   └── tests/            # Tests con Pytest
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_crud.py
│       ├── test_schemas.py
│       └── test_endpoints.py
├── requirements.txt      # Dependencias Python
├── Dockerfile           # Imagen Docker para la API
├── docker-compose.yml   # Configuración Docker Compose
├── .env.example         # Ejemplo de variables de entorno
└── README.md           # Este archivo
```

## Tests

Ejecutar tests:
```bash
pytest
pytest --cov=app --cov-report=html
```

Los tests cubren operaciones CRUD, validaciones, manejo de errores, filtros y paginación.

## Preguntas Técnicas Adicionales

### ¿Cómo manejarías la autenticación y autorización en la API?

Para un proyecto real implementaría **JWT con OAuth2**, que es el estándar en FastAPI. La idea básica sería:

- **Un endpoint `/token`** donde el usuario envía sus credenciales y recibe un token JWT válido por 15-30 minutos
- **Las contraseñas las guardaría hasheadas con bcrypt** (nunca en texto plano)
- **Para autorización usaría roles** tipo `admin`/`editor`/`reader` dentro del token JWT
- **Los endpoints protegidos usarían `Depends()` de FastAPI** para verificar el token antes de ejecutar
- **También agregaría refresh tokens** para que no tengan que loguearse todo el tiempo

### ¿Qué estrategias utilizarías para escalar la aplicación?

Depende del nivel de tráfico, pero iría por etapas:

**Corto plazo:**
- **Redis para cachear consultas frecuentes** (listados de libros, búsquedas comunes)
- **Connection pooling de SQLAlchemy** (que ya está configurado)
- **Índices en la BD** en los campos que más se consultan

**Si crece más:**
- **Load balancer (Nginx)** distribuyendo entre varias instancias de la API
- **Read replicas de PostgreSQL** para separar lecturas y escrituras
- **Horizontal scaling con Docker/Kubernetes**

**Adicionales:**
- **Rate limiting** para evitar abuso
- **Async/await en operaciones pesadas** (aunque FastAPI ya lo soporta bien)

### ¿Cómo implementarías la paginación en los endpoints que devuelven listas de libros?

Ya está implementada en este proyecto con el patrón **limit-offset**. Básicamente uso query parameters `skip` y `limit`, con defaults de `skip=0` y `limit=10`.

El cálculo es simple: `offset = skip`, y con SQLAlchemy aplico `.limit()` y `.offset()` al query.

En la respuesta incluyo metadata útil como `total` de items, `skip`, `limit`, etc. También puse un límite máximo de 100 items por página para que nadie intente traer miles de registros de una sola vez.

Para bases de datos muy grandes consideraría **cursor-based pagination** (usando el último ID visto), que es más eficiente, pero para este caso limit-offset funciona bien.

### ¿Cómo asegurarías la seguridad de la aplicación?

Varios puntos clave:

**Lo básico:**
- **SQL injection ya está cubierto** porque uso solo SQLAlchemy ORM, nada de queries concatenadas
- **Validaciones con Pydantic** en todos los endpoints
- **CORS configurado correctamente** (no poner `*` en producción)
- **HTTPS obligatorio** en producción

**Adicionales importantes:**
- **Rate limiting** para prevenir ataques de fuerza bruta
- **Headers de seguridad** (X-Frame-Options, Content-Security-Policy, etc.)
- **Secrets en variables de entorno**, nunca hardcodeados
- **Mantener dependencias actualizadas** (revisar vulnerabilidades con Safety)

**A nivel de BD:**
- **Constraints UNIQUE** donde corresponda
- **Validaciones también a nivel de base de datos** como backup

La idea es tener **varias capas de seguridad**, no depender de una sola cosa.

## Licencia

Este proyecto fue desarrollado como parte de una prueba técnica.

## Autor

Desarrollado siguiendo las mejores prácticas de desarrollo backend con Python y FastAPI.

