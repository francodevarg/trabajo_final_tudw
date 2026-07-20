# 🧠 Proyecto

## Descripción

Backend Django dockerizado con soporte para:

- 🧪 Desarrollo (hot reload)
- 🚀 Producción (Gunicorn)
- 🐘 PostgreSQL
- 🧑‍💻 Dev Containers (VS Code)

---

## 📁 Arquitectura

El proyecto está dividido en:

```text
.
├── config/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── entrypoint.sh
├── src/
│   ├── manage.py
│   └── myapp/
├── setup.sh
└── README.md
```

---

## ⚙️ Modos de ejecución

| Modo | Descripción |
|------|-------------|
| `dev` | Desarrollo con `runserver` y hot reload |
| `prod` | Producción utilizando Gunicorn |

---

## 🏗️ Funcionamiento

### `setup.sh`

El script de inicialización:

- Crea `.env` si no existe.
- Detecta el UID/GID del usuario.
- Define las variables:
  - `APP_MODE`
  - `BUILD_TARGET`
- Ejecuta Docker Compose.

### `docker-compose.yml`

Se encarga de:

- Levantar PostgreSQL.
- Construir la imagen según el modo seleccionado.
- Montar volúmenes en desarrollo.
- Ejecutar el contenedor con el usuario del host para evitar problemas de permisos.

### `entrypoint.sh`

Al iniciar el contenedor:

- Espera que PostgreSQL esté disponible.
- Ejecuta las migraciones.
- Ejecuta `collectstatic`.
- Inicia Django según el modo seleccionado:

```text
dev  → python manage.py runserver
prod → gunicorn
```

---

## 👤 Usuario del contenedor

El contenedor utiliza el mismo UID/GID que el usuario local mediante:

```text
LOCAL_UID
LOCAL_GID
```

Esto evita problemas de permisos sobre los volúmenes compartidos.

---

## 🎯 Filosofía del proyecto

- Simplicidad primero.
- Separación clara entre desarrollo y producción.
- Docker como entorno único de ejecución.
- Preparado para escalar a un entorno de producción real.