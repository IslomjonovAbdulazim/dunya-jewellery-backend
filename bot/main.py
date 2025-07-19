"""Simple bot setup"""

from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import config

from .handlers.start import start_command, help_command
from .handlers.admin import start_add_product
from .handlers.contacts import show_admin_contact
from .handlers.callbacks import handle_callback_query
from .handlers.messages import handle_text_message, handle_photo, handle_keyboard_button
from .constants import BTN_ADMIN_PRODUCTS, BTN_ADMIN_CONTACT

def setup_bot():
    """Setup bot with handlers"""
    app = Application.builder().token(config.BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", start_add_product))
    app.add_handler(CommandHandler("edit_contact", show_admin_contact))

    # Callbacks
    app.add_handler(CallbackQueryHandler(handle_callback_query))

    # Keyboard buttons
    app.add_handler(
        MessageHandler(
            filters.Regex(f"^{BTN_ADMIN_PRODUCTS}$|^{BTN_ADMIN_CONTACT}$"),
            handle_keyboard_button
        )
    )

    # Photos
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Text messages
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND &
            ~filters.Regex(f"^{BTN_ADMIN_PRODUCTS}$|^{BTN_ADMIN_CONTACT}$"),
            handle_text_message
        )
    )

    return app