"""All activity related to the /start command."""
import logging

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from commands import menu
from common.utils import user as user_util
from models import User

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""

    user = User(user_util.get_user_id(update), user_util.get_user_first_name(update),
                user_util.get_user_last_name(update),
                user_util.get_user_name(update), user_util.get_language_code(update))

    User.save_user(user)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Pizzeria Hlg! \nEl proyecto ha comenzado \nEscriba /menu para ver las opciones",  # 1 Handle translate
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                text="Sugerir ideas", url="t.me/BarneyS_S")]
        ])
    )
