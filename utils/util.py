from languages import langs
from database import db


def get_data(msg):
    """Obtiene los datos a mostrar para el comando start

    Returns :
        bot_lang (str) : el idioma de los mensajes del bot
        message (str) : el texto del mensaje principal del bot
        btn_rateme (str) : el texto del boton url
        btn_change_botlang (str) : el texto del boton para cambiar idioma
    """

    name = msg.from_user.first_name

    bot_lang = db.check_user(
        user_id=msg.from_user.id,
        user_language=msg.from_user.language_code,
    )

    message = langs["start"]["text"][bot_lang].format(name)
    btn_rateme = langs["start"]["btn_rateme"][bot_lang]
    btn_change_botlang = langs["start"]["btn_change_lang"][bot_lang]

    return bot_lang, message, btn_rateme, btn_change_botlang


def make_keypad(data: list) -> list:
    """devuelve una lista de dos columnas de botones"""

    markup = []
    for index, row in enumerate(data):
        line = []
        if index == 0:
            line.append(row)
        else:
            if index % 2 != 0:
                try:
                    line.append(row)
                    line.append(data[index + 1])
                except:
                    line.append(row)
        if line != []:
            markup.append(line)

    return markup
