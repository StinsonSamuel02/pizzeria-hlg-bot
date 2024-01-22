"""All activity related to the /start command."""
import logging

from telegram import Update
from telegram.ext import ContextTypes

import common.utils as utils

logger = logging.getLogger(__name__)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /about is issued."""

    user = utils.get_user(update)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Nombre de usuario: " + str(user["username"])
             + "\nID: " + str(user["id"])
             + "\nPrimer Nombre: " + str(user["first_name"]),
    )
