# Sistema Pokedex con PostgreSQL y MongoDB

## Datos de los estudiantes
- **Nombres:** Joffre Verdezoto, Raúl Luna
- **Carrera:** Ing. Informática

## Descripción

Este proyecto consiste en el desarrollo de una aplicación web tipo Pokedex utilizando Django como framework principal. El sistema permite administrar información de Pokémon y entrenadores mediante operaciones CRUD, integrando dos motores de bases de datos: PostgreSQL como base de datos relacional principal y MongoDB como base de datos NoSQL para almacenar información complementaria y realizar sincronización entre ambas bases de datos.


## Características principales

- CRUD completo de Pokémon en PostgreSQL.
- CRUD completo de Pokémon en MongoDB.
- CRUD de entrenadores.
- Inicio de sesión para administración.
- Sincronización PostgreSQL → MongoDB.
- Sincronización MongoDB → PostgreSQL.
- Historial de sincronizaciones.
- Registro de errores encontrados y errores resueltos durante la sincronización.
- Almacenamiento de imágenes de los Pokémon.
- Registro de información adicional en MongoDB:
  - Favorito.
  - Comentarios.
  - Etiquetas.
  - Veces visto.
  - Última visita.

---

# Tecnologías utilizadas

- Python 3.x
- Django
- PostgreSQL
- MongoDB
- Bootstrap 5
- Font Awesome
- HTML5
- CSS3

---

# Requisitos

Antes de ejecutar el proyecto se debe tener instalado:

- Python 3.x
- PostgreSQL
- MongoDB Community Edition
- pip

---

# Instalación

## 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
```

Entrar a la carpeta del proyecto.

## 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 3. Configurar PostgreSQL

Crear una base de datos en PostgreSQL.

Importar el archivo:

```
database/pokedex.sql
```

---

## 4. Configurar MongoDB

Iniciar el servicio de MongoDB.

Importar las colecciones:

```
database/pokemon_details.json
database/sync_logs.json
```

---

## 5. Ejecutar el proyecto

Desde la carpeta del proyecto ejecutar:

```bash
python manage.py runserver
```

Abrir el navegador en:

```
http://127.0.0.1:8000/
```

---

# Estructura del proyecto

```
ProyectoFinal/

backend/
    Código fuente del proyecto Django

database/
    pokedex.sql
    pokemon_details.json
    sync_logs.json

docs/
    Documentación técnica
    Manual de usuario
    Informe del proyecto

README.md
```

---

# Funcionalidades

## PostgreSQL

- Agregar Pokémon.
- Editar Pokémon.
- Eliminar Pokémon.
- Visualizar Pokémon.
- CRUD de entrenadores.

## MongoDB

- Agregar Pokémon.
- Editar Pokémon.
- Eliminar Pokémon.
- Administrar favoritos.
- Administrar comentarios.
- Administrar etiquetas.

## Sincronización

- PostgreSQL → MongoDB.
- MongoDB → PostgreSQL.
- Historial de sincronizaciones.
- Registro de errores encontrados.
- Registro de errores corregidos.

---

# Observaciones

PostgreSQL funciona como base de datos principal del sistema, mientras que MongoDB almacena información complementaria de cada Pokémon y permite la sincronización bidireccional entre ambas bases de datos.


