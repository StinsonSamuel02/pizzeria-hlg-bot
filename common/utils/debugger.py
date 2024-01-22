from telegram import Update
from telegram.ext import ContextTypes


def report(context: ContextTypes.DEFAULT_TYPE, text) -> None:
    context.bot.send_message(
        chat_id="-981595294",
        text=text,
    )


"""A futuro"""