"""Simple bot setup - CLEAN NAVIGATION"""

from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import config

from .handlers.start import start_command, help_command
from .handlers.admin import start_add_product
from .handlers.contacts import show_admin_contact
from .handlers.callbacks import handle_callback_query
from .handlers.messages import handle_text_message, handle_photo

def setup_bot():
    """Setup bot with handlers - CLEAN VERSION"""
    if not config.BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set. Please define it in the environment.")
    app = Application.builder().token(config.BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", start_add_product))
    app.add_handler(CommandHandler("edit_contact", show_admin_contact))

    # Callbacks (main navigation)
    app.add_handler(CallbackQueryHandler(handle_callback_query))

    # Photos (for admin product creation)
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Text messages (for admin workflows only)
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text_message
        )
    )

    return app