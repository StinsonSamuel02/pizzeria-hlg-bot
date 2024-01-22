import logging
import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler

import commands
from db import Database
from messages import message_handler, conv_handler, queryHandler, shop_conv_handler
from models import User, Product

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,")

logger = logging.getLogger()


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def init_tables():
    User.create_users_table()
    Product.create_products_table()


def main():
    """Start the bot."""

    app = ApplicationBuilder().token(os.getenv('TOKEN')).build()

    Database.initialise(database=os.getenv('POSTGRES_DB'), user=os.getenv('POSTGRES_USER'),
                        password=os.getenv('POSTGRES_PASSWORD'), host=os.getenv('POSTGRES_HOST'))
    init_tables()

    app.add_error_handler(error)

    app.add_handlers(
        [
            CommandHandler(command, getattr(commands, command))
            for command in commands.get_all_commands()
        ]

    )

    app.add_handler(MessageHandler(filters.COMMAND, commands.unknown))
    app.add_handler(conv_handler)
    app.add_handler(shop_conv_handler)
    app.add_handler(MessageHandler(filters.TEXT, message_handler))
    app.add_handler(CallbackQueryHandler(queryHandler))
    app.run_polling()


if __name__ == "__main__":
    main()
