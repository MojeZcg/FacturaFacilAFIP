"""Módulo para manejar la actualización de variables de entorno en el archivo .env."""

from dotenv import set_key


def update_arca_key(new_value):
    """
    Actualiza la clave ARCA_KEY en el archivo .env.

    Args:
        new_value (str): El nuevo valor para ARCA_KEY.
    """
    set_key(".env", "ARCA_KEY", new_value)
