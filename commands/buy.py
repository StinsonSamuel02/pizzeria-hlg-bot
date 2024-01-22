import logging

from telegram import Update
from telegram.ext import CallbackContext

logger = logging.getLogger(__name__)


async def buy(update: Update, context: CallbackContext, product):
    context.user_data['product_selected'] = product
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Cuantas {product.name} desea comprar?')
