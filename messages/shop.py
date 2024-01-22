from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CallbackContext, MessageHandler, filters

from commands import menu

# Agregar constantes para los estados de la conversación de compra
DELIVERY, LOCATION, ORDER = range(3)


async def enter_quantity_handler(update: Update, context: CallbackContext):
    context.user_data['quantity'] = update.message.text

    buttons = [[KeyboardButton(text='SI')], [KeyboardButton('NO')]]
    reply_kb_markup = ReplyKeyboardMarkup(buttons,
                                          resize_keyboard=True,
                                          one_time_keyboard=True)

    await update.message.reply_text(text='¿Desea entrega a domicilio?', reply_markup=reply_kb_markup)
    return DELIVERY


async def enter_delivery_handler(update: Update, context: CallbackContext):
    context.user_data['delivery_option'] = update.message.text.lower()

    if context.user_data['delivery_option'] == 'si':

        buttons = [[KeyboardButton(text='Enviar Ubicacion', request_location=True)]]
        reply_kb_markup = ReplyKeyboardMarkup(buttons,
                                              resize_keyboard=True,
                                              one_time_keyboard=True)

        await update.message.reply_text(text='Por favor, envíe su ubicación para la entrega.',
                                        reply_markup=reply_kb_markup)
        return LOCATION
    else:

        buttons = [[KeyboardButton(text='Confirmar')]]
        reply_kb_markup = ReplyKeyboardMarkup(buttons,
                                              resize_keyboard=True,
                                              one_time_keyboard=True)

        await update.message.reply_text(
            text=f"Usted comprara {context.user_data['product_selected'].name} x {context.user_data['quantity']} ===> {float(context.user_data['product_selected'].price) * float(context.user_data['quantity'])}$",
            reply_markup=reply_kb_markup)
        return ORDER


async def enter_location_handler(update: Update, context: CallbackContext):
    location = update.message.location

    buttons = [[KeyboardButton(text='Confirmar')]]
    reply_kb_markup = ReplyKeyboardMarkup(buttons,
                                          resize_keyboard=True,
                                          one_time_keyboard=True)

    await update.message.reply_text(
        text=f"Usted comprara {context.user_data['product_selected'].name} x {context.user_data['quantity']} ===> {float(context.user_data['product_selected'].price) * float(context.user_data['quantity'])}$",
        reply_markup=reply_kb_markup)
    return ORDER


async def order_confirmed_handler(update: Update, context: CallbackContext):
    await update.message.reply_text(text='¡Pedido confirmado! Gracias por su compra.')

    await menu(update, context)

    # Reiniciar los datos de la conversación
    context.user_data.clear()

    return ConversationHandler.END


shop_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex(r'^\d+$'), enter_quantity_handler)],
    states={
        DELIVERY: [MessageHandler(filters.Regex(r'\b(SI|NO)\b'), enter_delivery_handler)],
        LOCATION: [MessageHandler(filters.LOCATION, enter_location_handler)],
        ORDER: [MessageHandler(filters.Regex(r'^Confirmar$'), order_confirmed_handler)],
    },
    fallbacks=[]
)
