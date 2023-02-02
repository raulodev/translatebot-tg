import time
import logging

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

from database import models
from database import db

from languages import langs
from utils import util

from translator import Translator

from config import API_ID, API_HASH, TOKEN, OWNER, lang_code

regex_lang = "|".join(lang_code)


logging.basicConfig(
    format="%(levelname)s (%(asctime)s) :%(message)s",
    level=logging.INFO,
    datefmt="%d/%m/%Y %I:%M:%S %p",
)

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)


@app.on_message(filters.command("start"))
async def start(client, msg):
    """inicia la interacción con el bot"""

    bot_lang, message, btn_rateme, btn_change_botlang = util.get_data(msg)

    await msg.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        btn_rateme, url="https://t.me/BotsArchive/2137"
                    ),
                    InlineKeyboardButton(
                        btn_change_botlang, callback_data="change_lang"
                    ),
                ]
            ]
        ),
    )

    botcommand = langs["start"]["botcommand"][bot_lang]

    await client.set_bot_commands(commands=[BotCommand("tr", botcommand)])


@app.on_message(
    filters.private
    & ~filters.command(["start", "tr", "send", "stats"])
    & ~filters.group
    | filters.caption & ~filters.group
)
async def translate_pv(client, msg):
    """traduce en el chat privado con el bot"""

    message = msg.text

    user_language = msg.from_user.language_code
    user_id = msg.from_user.id

    bot_lang = db.check_user(user_id, user_language)

    # si es un archivo entonces el texto a traducir será
    # el  caption
    if msg.caption:

        message = msg.caption

    translate = Translator(message, user_id, target=user_language)

    reply = langs["translate_pv"]["text"][bot_lang].format(translate)
    button = langs["translate_pv"]["btn"][bot_lang]

    await msg.reply_text(
        reply,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(button, callback_data="change_translate")]
            ]
        ),
    )


@app.on_message(
    filters.group & filters.command("tr") & ~filters.command(["start", "send", "stats"])
)
async def traducir_gp(client, msg):
    """traduce en los grupos"""

    user_id = msg.from_user.id
    user_lang = msg.from_user.language_code

    bot_lang = db.check_user(user_id, user_lang)

    if msg.reply_to_message:

        message = msg.reply_to_message.text

        if msg.reply_to_message.caption:

            message = msg.reply_to_message.caption

        translate = Translator(message, user_id, user_lang)

        await msg.reply_text(langs["traducir_gp"]["text"][bot_lang].format(translate))

        return

    message = langs["traducir_gp"]["alert"][bot_lang]

    await msg.reply_text(message)


@app.on_message(filters.command("stats"))
async def stats(client, msg):
    """Muestra cuantos usuarios hay en el bot"""

    count = db.count_users()

    bot_lang = db.check_user(
        user_id=msg.from_user.id,
        user_language=msg.from_user.language_code,
    )

    message = langs["stats"][bot_lang].format(count)

    await msg.reply_text(message)


@app.on_message(filters.user([OWNER]) & filters.command("send"))
async def broudcast(client, msg):
    """Envía un mensaje masivo a todos los usuarios"""

    message = msg.text.replace("/send", "")

    result = db.select_all_id()
    # cantidad de mensajes que no se lograron enviar
    failed = 0
    for row in result:
        user_id = row[0]
        try:
            await client.send_message(user_id, message)
            # dormir 0.5 segundos para no despertar el antispam
            time.sleep(0.5)
        except:

            logging.info("No se pudo enviar el mensage al id {user_id}")

            failed = +1

    await msg.reply_text(f"Broudcast terminado ,fallados {failed}")


@app.on_callback_query(filters.regex("^change_lang$"))
async def toggle_lang(client, msg):
    """Cambia el idioma del mensaje principal del bot"""

    db.update_lang(user_id=msg.from_user.id)

    _, message, btn_rateme, btn_change_lang = util.get_data(msg)

    await msg.edit_message_text(
        message,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=btn_rateme, url="https://t.me/BotsArchive/2137"
                    ),
                    InlineKeyboardButton(
                        text=btn_change_lang, callback_data="change_lang"
                    ),
                ]
            ]
        ),
    )


@app.on_callback_query(filters.regex("^change_translate$"))
async def change_translate(client, msg):
    """muestra los otros idiomas habilitados en para traducir los mensajes"""

    bot_lang = db.check_user(
        user_id=msg.from_user.id,
        user_language=msg.from_user.language_code,
    )

    # texto que mostrará el botón
    languages = langs["change_translate"][bot_lang]

    markup = []
    for index, row in enumerate(languages):
        markup.append(InlineKeyboardButton(text=row, callback_data=lang_code[index]))

    new_markup = util.make_keypad(markup)

    await msg.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(new_markup))


@app.on_callback_query(filters.regex(f"^({regex_lang})$"))
async def again(client, msg):
    """vuelve a traducir el texo y cambia el idioma alternativo del usario"""

    # separa el mensaje del bot del texto enviado por el usuario
    rows = msg.message.text.split("\n\n")
    done_msg = rows[0]
    # texto a traducir
    message = "\n\n".join(rows[1:])

    user_id = msg.from_user.id
    new_user_language = msg.data

    bot_lang = db.check_user(user_id, msg.from_user.language_code)

    translate = Translator(message, user_id, target=new_user_language)

    # mostrar alerta de que ha sido cambiado el idioma
    await app.answer_callback_query(
        callback_query_id=msg.id, text=langs["again"][bot_lang], show_alert=False
    )

    await msg.edit_message_text(f"<b>{done_msg}</b>\n\n{translate}")

    # actualizar BD
    db.change_alt_lang(user_id, new_user_language)


if __name__ == "__main__":

    models.Base.metadata.create_all(db.engine)

    app.run()
