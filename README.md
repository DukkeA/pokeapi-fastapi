# PokeAPI Project

El proyecto de la PokeAPI es una aplicación que proporciona una API para acceder y gestionar información sobre Pokémon. Esta API permite a los desarrolladores realizar consultas y actualizaciones específicas de Pokémon, así como obtener detalles detallados sobre ellos, como sus habilidades, tipos y sprites.

## Características principales

**Obtención de datos detallados**: Los desarrolladores pueden buscar información detallada sobre Pokémon a través de la API, incluyendo datos como nombre, habilidades, tipos y sprites.

**Actualizaciones específicas**: La API permite realizar actualizaciones específicas de Pokémon, como cambiar su nombre, habilidades, tipos y sprites.

**Validación de datos**: Se implementa una validación de datos sólida para asegurarse de que solo se acepten datos válidos y consistentes en las solicitudes de actualización.

**Acceso a datos externos**: La API puede acceder a datos externos para obtener información adicional sobre habilidades y tipos de Pokémon si no se encuentra en la base de datos local.

## Requisitos

* Python 3.11
* Postgres > 14 (Opcional, no requiere docker)
* Docker (Opcional, no requiere postgres)
* Poetry (Opcional)

## Configuracion inicial

Antes de inicializar el proyecto se deben configurar las variables de entorno generando un archivo .env basado en el archivo .env.example. Para mayor informacion del uso de las variables de entorno ir al archivo de configuracion del proyecto
`/src/settings/base.py`

```
DEBUG=
LOG_LEVEL=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
```
* Para el uso del proyecto en contenedores las credenciales de la base de datos se configuran en el archivo `docker-compose.yml`
* Para el uso del proyecto en contenedores la variable DB_HOST debe tener el mismo nombre que el contenedor de base de datos `postgres` por defecto

## Uso

**Los comandos listados estan diseñados para correr en sistemas operativos OSX y Linux, para su uso en windows pueden diferir ligeramente**

Para comenzar a utilizar la PokeAPI, sigue estos pasos:

### Poetry

#### 1. Instalacion de dependencias
```
poetry install --with test,lint
```
#### 2. Ejecutar migraciones
El proyecto debe contar con una base de datos configurada en el archivo de variables de entorno .env
```
# Option 1
poetry run alembic upgrade head

# Opcion 2
poetry run python3 manage.py migrate
```
#### 3. Inicializar servicio
El servicio por defecto se inicia en el puerto 8000, para cambiar dicho puerto se debe editar la variable de entorno
```
poetry run python3 manage.py runserver
```
#### 1. Ejecutar tests
```
poetry run pytest -v
```

### Pip

#### 1. Instalacion de dependencias
Para instalar correctamente las dependencias el proyecto debe contar con un entorno virtual debidamente configurado
```
pip install -r requirements.txt
```
#### 2. Ejecutar migraciones
El proyecto debe contar con una base de datos configurada en el archivo de variables de entorno .env
```
# Option 1
alembic upgrade head

# Opcion 2
python3 manage.py migrate
```
#### 3. Inicializar servicio
El servicio por defecto se inicia en el puerto 8000, para cambiar dicho puerto se debe editar la variable de entorno
```
python3 manage.py runserver
```
#### 1. Ejecutar tests
```
pytest -v
```

### Docker

### 1. Inicializar contenedores
Existen tres configuraciones de docker para inicializar el proyecto
* **base**: Contenedor sin base de datos
* **with_db**: Contenedor con base de datos
* **tests**: Contenedor con base de datos para pruebas
La variable de entorno que configura el host de la base de datos se debe configurar con el valor `postgres` o con el nombre respectivo del contenedor
```
# sin base de datos
docker-compose -f compose/base/docker-compose.yml up --build -d

# con base de datos
docker-compose -f compose/with_db/docker-compose.yml up --build -d
```

### 2. Ejecutar migraciones
```
# Opcion 1
docker exec poke_api alembic upgrade head

# Option 2
docker exec poke_api python3 manage.py migrate
```

#### 3. Ejecutar tests
```
docker-compose -f compose/tests/docker-compose.yml up --build -d
```

## Endpoints

### Endpoint listado general de pokemons paginado
```
GET http://localhost:8000/api/v1/pokemon?offset=0&limit=20
```
Parametros:
* offset (int): posicion de inicio de la consulta
* limit (int): Numero maximo de items por consulta

### Endpoint detalle de pokemon
```
GET http://localhost:8000/api/v1/pokemon/{id o nombre}
```

### Endpoint edicion de pokemon
```
PUT http://localhost:8000/api/v1/pokemon/{id o nombre}
```

La estructura del body de la peticion debe ser
```
{
    "name": "nombre a editar",
    "abilities": ["id o nombre de la habilidad en ingles"],
    "types": ["id o nombre del tipo en ingles"],
    "sprites": [
        {
            "type": "slug del typo 'default', 'dream_world', 'home', 'official-artwork'",
            "url": "url a editar"
        }
    ]
}
```
**El metodo put edita todo el registro con la información suministrada**