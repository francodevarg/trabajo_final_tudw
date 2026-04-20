# 🚀 Django Backend + Docker (Dev / Prod Ready)

Backend Django dockerizado con soporte completo para:

* 🧪 Desarrollo (hot reload)
* 🚀 Producción (Gunicorn)
* 🐘 PostgreSQL
* 🧑‍💻 Dev Containers (VS Code)

---

# 🧠 Arquitectura

El proyecto está dividido en:

```
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

# ⚙️ Modos de ejecución

El sistema soporta 2 modos:

| Modo   | Descripción                             |
| ------ | --------------------------------------- |
| `dev`  | Desarrollo con `runserver` + hot reload |
| `prod` | Producción con `gunicorn`               |

---

# 🚀 Quick Start

## 🟢 Desarrollo

```bash
./setup.sh dev
```

👉 Levanta:

* Django con `runserver`
* PostgreSQL
* Volúmenes montados (hot reload)

---

## 🔴 Producción

```bash
./setup.sh prod
```

👉 Levanta:

* Django con `gunicorn`
* Código dentro del contenedor (sin volumen)

---

# 🧠 Cómo funciona

## 🔹 setup.sh

* Crea `.env` si no existe
* Detecta UID/GID del sistema
* Define:

  * `APP_MODE` → dev / prod
  * `BUILD_TARGET` → development / production
* Ejecuta docker-compose

---

## 🔹 docker-compose.yml

* Usa variables dinámicas:

  * `APP_MODE`
  * `BUILD_TARGET`
* Monta volúmenes en dev
* Usa usuario del host (evita problemas de permisos)

---

## 🔹 entrypoint.sh

Decide cómo correr Django:

```bash
dev  → python manage.py runserver
prod → gunicorn
```

También:

* Espera a PostgreSQL
* Ejecuta migraciones
* Ejecuta collectstatic

---

# 🐳 Comandos útiles

## Ver logs

```bash
docker compose -f config/docker-compose.yml logs -f django_backend
```

## Entrar al contenedor

```bash
docker compose -f config/docker-compose.yml exec django_backend bash
```

## Parar todo

```bash
docker compose -f config/docker-compose.yml down
```

## Reset completo

```bash
docker compose -f config/docker-compose.yml down -v
```

## Rebuild sin cache

```bash
docker compose -f config/docker-compose.yml build --no-cache
```

---

# 🧑‍💻 Variables de entorno

Archivo: `src/.env`

```env
POSTGRES_DB=django_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_pass
POSTGRES_PORT=5432

APP_PORT=8000

DJANGO_SETTINGS_MODULE=myapp.settings
DJANGO_DIR=/workspace/src
```

---

# 👤 Usuario del contenedor

El contenedor corre con tu usuario local:

```bash
LOCAL_UID
LOCAL_GID
```

👉 Evita problemas de permisos con volúmenes

---

# ⚠️ Troubleshooting

## ❌ No conecta a la DB

```bash
docker compose ps
```

---

## ❌ No encuentra manage.py

👉 Revisar volumen:

```
../src:/workspace/src
```

---

## ❌ Cambios no impactan

👉 Asegurarse de estar en modo `dev`

---


# 🧠 Filosofía del proyecto

* Simplicidad primero
* Dev ≠ Prod (bien separados)
* Docker como entorno único
* Escalable a producción real

---

# 🧑‍💻 Autor

Franco Narváez 🚀

---
