"""Main bot setup and initialization"""

from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import config

from .handlers.start import start_command, help_command
from .handlers.admin import start_add_product
from .handlers.contacts import start_add_contact
from .handlers.callbacks import handle_callback_query
from .handlers.messages import handle_text_message, handle_photo, handle_keyboard_button
from .constants import BTN_ADMIN_PRODUCTS, BTN_ADMIN_CONTACTS

def setup_bot():
    """Setup bot with all handlers"""
    application = Application.builder().token(config.BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add", start_add_product))
    application.add_handler(CommandHandler("add_contact", start_add_contact))

    # Callback query handler (inline button presses)
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    # Keyboard button handlers (reply keyboard)
    application.add_handler(
        MessageHandler(
            filters.Regex(f"^{BTN_ADMIN_PRODUCTS}$|^{BTN_ADMIN_CONTACTS}$"),
            handle_keyboard_button
        )
    )

    # Photo handler for product images
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Text message handler for conversations (excluding commands and keyboard buttons)
    application.add_handler(
        MessageHandler(
            filters.TEXT &
            ~filters.COMMAND &
            ~filters.Regex(f"^{BTN_ADMIN_PRODUCTS}$|^{BTN_ADMIN_CONTACTS}$"),
            handle_text_message
        )
    )

    return application