from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import User
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
session = Session(engine)


def check_user(user_id: int, user_language: str) -> str:
    """Registra un usuario si no existe y retorna el idioma de los mensajes bot

    Args:
        user_id (int): id del usuario en Telegram
        user_language (str): es el idioma configurado en la app de telegram
    """

    user = session.query(User).filter_by(user_id=user_id).first()

    if user:

        return user.bot_language

    new_user = User(user_id=user_id, user_language=user_language)
    session.add(new_user)
    session.commit()

    return new_user.bot_language


def update_lang(user_id: int) -> None:
    """Cambia el idioma de los mensajes del bot"""

    user = session.query(User).filter_by(user_id=user_id).first()

    if user.bot_language == "es":

        user.bot_language = "en"

        session.commit()

        return

    user.bot_language = "es"

    session.commit()


def select_all_id() -> tuple:
    """Devuelve todos los id de los usuarios que usan el bot"""

    result = session.execute(select(User.user_id))

    return result


def count_users() -> int:
    """Devuelve la cantidad de usuarios"""

    result = session.query(User).count()

    return result


def get_new_target(user_id: int) -> str:
    """En caso de que el idioma del texto sea el mismo que el idioma
    del usuario se seleccionará el idioma alternativo
    """

    result = session.query(User).filter_by(user_id=user_id).first()

    return result.alternative_lang


def change_alt_lang(user_id: int, lang_code: str) -> None:
    """Cambia el idioma alternativo del usuario"""

    user = session.query(User).filter_by(user_id=user_id).first()

    user.alternative_lang = lang_code

    session.commit()
