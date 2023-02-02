from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String

Base = declarative_base()


class User(Base):

    __tablename__ = "user"

    id: int = Column(Integer, primary_key=True)

    # el id de usuario en Telegram
    user_id: int = Column(BigInteger)

    # (bot_language) el idioma en que debe aparecer los mensajes del bot
    # por defecto es español :) ver 'language.py'
    bot_language: str = Column(String, default="es")

    # (user_language) el idioma del usuario que viene configurado
    # en la app de telegram
    user_language: str = Column(String)

    # (alternative_lang) idioma al que debe ser traducidos los mensajes
    # en caso de que el idioma del texto introducido sea el mismo
    # que el idioma del usuario
    alternative_lang: str = Column(String, default="en")

    def __init__(self, user_id: int, user_language: str) -> None:
        self.user_id = user_id
        self.user_language = user_language
