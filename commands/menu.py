from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Commands menu
    main_menu_keyboard = [
        [KeyboardButton(text='Send Location', request_location=True)],
        [KeyboardButton(text='Ofertas')],
        [KeyboardButton(text='Nuevo Producto')],
        [KeyboardButton('/about')]
    ]
    reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard,
                                          resize_keyboard=True,
                                          one_time_keyboard=True)

    # Send the message with menu
    await context.bot.send_message(chat_id=update.message.chat_id,
                                   text="En que puedo ayudarle?",
                                   reply_markup=reply_kb_markup)
