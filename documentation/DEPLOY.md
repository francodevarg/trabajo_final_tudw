# Proyecto Django

## Configuración

Antes de ejecutar el proyecto, copiá el archivo `.env.example` y renombralo a `.env`:

```bash
cp .env.example .env
```

Luego completá las variables de entorno según corresponda.

## Variables de entorno

El archivo `.env.example` contiene las siguientes variables:

```env
POSTGRES_DB=django_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_pass
POSTGRES_HOST=postgres_db
POSTGRES_PORT=5432

APP_PORT=8000
DJANGO_SETTINGS_MODULE=myapp.settings
DJANGO_DIR=/workspace/src

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
```

## Despliegue

Para levantar el entorno de desarrollo ejecutá:

```bash
./setup.sh dev
```

---

## Comandos útiles

### Ver logs

```bash
docker compose -f config/docker-compose.yml logs -f django_backend
```

### Entrar al contenedor

```bash
docker compose -f config/docker-compose.yml exec django_backend bash
```

### Detener los servicios

```bash
docker compose -f config/docker-compose.yml down
```

### Eliminar volúmenes

```bash
docker compose -f config/docker-compose.yml down -v
```

### Reconstruir sin caché

```bash
docker compose -f config/docker-compose.yml build --no-cache
```


## Seguridad

- No subas el archivo `.env` al repositorio.
- Mantené las credenciales sensibles únicamente en tu entorno local o en el servidor de despliegue.

