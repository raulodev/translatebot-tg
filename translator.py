from deep_translator import GoogleTranslator
from langdetect import detect
from database import db


def Translator(message: str, user_id: int, target: str) -> str:
    """Traduce el texto

    Args:
        message (str): texto a traducir
        user (str): id del usuario
        target (str): idioma al que se traducirá el texto

    Returns:
        str: la traducción del texto
    """

    # si el idioma del texto es el mismo que el idioma del usuario
    # se usará el idioma alterativo
    detected_langs = detect(message)

    if target == detected_langs:

        target = db.get_new_target(user_id)

    try:

        init = GoogleTranslator(source="auto", target=target)

        result: str = init.translate(message)

        return result

    except Exception as err:

        print("error:", err)

        return ":("
