"""Factory reutilizable para la creación de usuarios con su rol."""
from typing import Optional

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .utils import SeedContext


def create_user(
    ctx: SeedContext,
    username: str,
    email: str,
    first_name: str,
    last_name: str,
    role: str,
    password: str = "defaultpassword123",
) -> User:
    """Crea un usuario, le asigna el rol y lo devuelve.

    Args:
        ctx: Contexto compartido del seed.
        username: Nombre de usuario único.
        email: Email del usuario.
        first_name: Nombre.
        last_name: Apellido.
        role: Nombre del rol (debe existir en ctx.groups).
        password: Password opcional (por defecto segura para seed).

    Returns:
        Instancia del usuario creado.
    """
    user = User.objects.create_user(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password,
    )

    group: Optional[Group] = ctx.groups.get(role)
    if group is not None:
        user.groups.add(group)

    return user