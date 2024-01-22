import base64
import io

from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters

from commands import menu, buy
from models import Product

OFERTAS = 'Ofertas'
NUEVO_PRODUCTO = 'Nuevo Producto'

PRODUCT_NAME, PRODUCT_PRICE, PRODUCT_IMG = range(3)

product_pos = 0
products = []


def decode_base64_img(img_base64):
    img_bytes = base64.b64decode(img_base64)
    stream = io.BytesIO(img_bytes)
    image = Image.open(stream)

    # Convertir la imagen en un flujo de bytes
    image_byte_stream = io.BytesIO()
    image.save(image_byte_stream, format='JPEG')
    image_byte_stream.seek(0)
    return image_byte_stream


async def message_handler(update: Update, context: CallbackContext):
    text = update.message.text

    if text == OFERTAS:
        # Enviar mensaje de "cargando" mientras se obtienen los datos
        loading_message = await context.bot.send_message(chat_id=update.effective_chat.id, text='Cargando ofertas...')

        global products
        products = Product.get_all_products()

        buttons = []
        if product_pos > 0:
            buttons.append(InlineKeyboardButton("◀️", callback_data='back'))
        buttons.append(InlineKeyboardButton("🛒", callback_data='shop'))
        if product_pos < len(products) - 1:
            buttons.append(InlineKeyboardButton("▶️", callback_data='next'))

        # Eliminar el mensaje de "cargando"
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=loading_message.message_id)
        context.user_data['message'] = await context.bot.send_photo(chat_id=update.effective_chat.id,
                                                                    photo=decode_base64_img(
                                                                        products[product_pos].img_url),
                                                                    caption=f'{products[product_pos].name}\n{products[product_pos].price}$',
                                                                    reply_markup=InlineKeyboardMarkup([buttons]))


async def add_product_name_handler(update: Update, context: CallbackContext):
    await update.message.reply_text(text='Nombre del producto')
    return PRODUCT_NAME


async def enter_product_price_handler(update: Update, context: CallbackContext):
    await update.message.reply_text(text='Precio del producto')
    context.user_data['product_name'] = update.message.text
    return PRODUCT_PRICE


async def enter_product_img_handler(update: Update, context: CallbackContext):
    context.user_data['product_price'] = update.message.text
    await update.message.reply_text(text='Imagen del Producto')
    return PRODUCT_IMG


async def save_product_data_handler(update: Update, context: CallbackContext):
    photo_file = await update.message.photo[-1].get_file()
    photo_bytes = await photo_file.download_as_bytearray()

    # Convertir la imagen a base64
    img_base64 = base64.b64encode(photo_bytes).decode('utf-8')

    Product.save_product(
        Product(context.user_data['product_name'], context.user_data['product_price'], img_base64))

    await update.message.reply_text('Producto Guardado Correctamente')
    await menu(update, context)

    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex(NUEVO_PRODUCTO), add_product_name_handler)],
    states={
        PRODUCT_NAME: [MessageHandler(filters.ALL, enter_product_price_handler)],
        PRODUCT_PRICE: [MessageHandler(filters.ALL, enter_product_img_handler)],
        PRODUCT_IMG: [MessageHandler(filters.ALL, save_product_data_handler)],
    },
    fallbacks=[]
)


async def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    await update.callback_query.answer()

    global product_pos, products

    if 'next' in query or 'back' in query:
        if 'next' in query:
            product_pos += 1
        elif 'back' in query:
            if product_pos > 0:
                product_pos -= 1
            else:
                product_pos = 0

        # Enviar mensaje de "cargando" mientras se realizan los cambios
        loading_message = await context.bot.send_message(chat_id=update.effective_chat.id, text='Cargando...')

        products = Product.get_all_products()
        buttons = []
        if product_pos > 0:
            buttons.append(InlineKeyboardButton("◀️", callback_data='back'))
        buttons.append(InlineKeyboardButton("🛒", callback_data='shop'))
        if product_pos < len(products) - 1:
            buttons.append(InlineKeyboardButton("▶️", callback_data='next'))

        await context.bot.edit_message_media(chat_id=update.effective_chat.id,
                                             message_id=context.user_data['message'].message_id,
                                             media=InputMediaPhoto(
                                                 decode_base64_img(products[product_pos].img_url),
                                                 caption=f'{products[product_pos].name}\n{products[product_pos].price}$'),
                                             reply_markup=InlineKeyboardMarkup([buttons]))
        # Eliminar el mensaje de "cargando"
        await context.bot.delete_message(chat_id=update.effective_chat.id,
                                         message_id=loading_message.message_id)
    elif 'shop' in query:
        await buy(update, context, products[product_pos])
