"""Simple callback query handlers"""

from telegram import Update
from telegram.ext import ContextTypes

from .client import view_products_client, handle_order_request, back_to_main_menu
from .admin import (
    show_admin_products,
    start_add_product,
    start_edit_product,
    confirm_delete_product,
    delete_product,
    cancel_delete,
    show_single_product
)
from .contacts import (
    show_admin_contact,
    start_edit_contact_field
)

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Route callback queries to handlers"""
    query = update.callback_query
    data = query.data

    # Client callbacks
    if data == "view_products":
        await view_products_client(update, context)
    elif data == "contact":
        # Get real contact data from database
        from database import get_db_session
        from models import Contact

        db = get_db_session()
        contact = db.query(Contact).first()
        db.close()

        await query.answer()

        if not contact:
            # Fallback if no contact in database
            await query.edit_message_text(
                "📞 Bog'lanish\n\n📱 Telefon: +998901234567\n💬 Telegram: @dunya_jewellery\n📷 Instagram: https://instagram.com/dunya_jewellery"
            )
        else:
            # Use real contact data
            contact_message = "📞 Bog'lanish ma'lumotlari\n\n"

            # Telegram with @username (works inside Telegram)
            if contact.telegram_username:
                contact_message += f"💬 Telegram: @{contact.telegram_username}\n"

            # Phone numbers (raw format for click-to-call)
            phones = contact.get_phone_numbers_list()
            if phones:
                if len(phones) == 1:
                    contact_message += f"📱 Telefon: {phones[0]}\n"
                else:
                    contact_message += f"📱 Telefonlar:\n"
                    for phone in phones:
                        contact_message += f"  • {phone}\n"

            # Instagram with full URL
            if contact.instagram_username:
                contact_message += f"📷 Instagram: https://instagram.com/{contact.instagram_username}\n"

            await query.edit_message_text(contact_message)
    elif data.startswith("order_"):
        await handle_order_request(update, context)
    elif data == "back_to_main":
        await back_to_main_menu(update, context)

    # Admin contact callbacks (check these BEFORE general edit_)
    elif data == "admin_contact":
        await show_admin_contact(update, context)
    elif data.startswith("edit_contact_"):
        await start_edit_contact_field(update, context)

    # Admin product callbacks
    elif data == "admin_products":
        await show_admin_products(update, context)
    elif data == "admin_add":
        await start_add_product(update, context)
    elif data.startswith("view_product_"):
        await show_single_product(update, context)
    elif data.startswith("edit_"):
        await start_edit_product(update, context)
    elif data.startswith("delete_"):
        await confirm_delete_product(update, context)
    elif data.startswith("confirm_delete_"):
        await delete_product(update, context)

    # General callbacks
    elif data == "cancel_delete":
        await cancel_delete(update, context)

    # Unknown callback
    else:
        await query.answer("Noma'lum buyruq")