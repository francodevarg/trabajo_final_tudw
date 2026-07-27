# Proyecto Django

## 1. Configuración inicial

Antes de ejecutar el proyecto, copiá el archivo `.env.example` y renombralo a `.env`:

```bash
cp .env.example .env
```

Luego completá las variables de entorno según corresponda.

---

## 2. Variables de entorno

Editá el archivo `.env` con los valores correspondientes.

El proyecto utiliza las siguientes variables:

```env
# Base de datos PostgreSQL
POSTGRES_DB=django_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_pass
POSTGRES_HOST=postgres_db
POSTGRES_PORT=5432

# Configuración de Django
APP_PORT=8000
DJANGO_SETTINGS_MODULE=myapp.settings
DJANGO_DIR=/workspace/src

# Configuración de correo
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicación

# Usuario ADMIN inicial
USER_ADMIN_EMAIL=admin@example.com
USER_ADMIN_USERNAME=admin
USER_ADMIN_PASSWORD=admin123
USER_ADMIN_FIRST_NAME=System
USER_ADMIN_LAST_NAME=Admin

# Usuario DOCTOR inicial
USER_DOCTOR_EMAIL=doctor@example.com
USER_DOCTOR_USERNAME=doctor
USER_DOCTOR_PASSWORD=doctor123
USER_DOCTOR_FIRST_NAME=Juan
USER_DOCTOR_LAST_NAME=Perez
```

**Importante**

Si utilizás Gmail, `EMAIL_HOST_PASSWORD` debe ser una **Contraseña de aplicación** y **no la contraseña de tu cuenta de Google**.

### Cómo obtener una contraseña de aplicación

1. Activá la **Verificación en dos pasos** de tu cuenta de Google:

   https://myaccount.google.com/security

2. Una vez habilitada, ingresá a:

   https://myaccount.google.com/apppasswords

3. Generá una nueva contraseña para la aplicación.

4. Copiá el código generado y utilizalo como valor de:

```env
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicación
```

---

## 3. Despliegue y comandos útiles

Para levantar el entorno de desarrollo ejecutá:

```bash
./setup.sh dev
```

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

---

## Seguridad

- No subas el archivo `.env` al repositorio.
- Mantené las credenciales sensibles únicamente en tu entorno local o en el servidor de despliegue.