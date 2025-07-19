"""Callback query handlers for inline button presses"""

from telegram import Update
from telegram.ext import ContextTypes

from .client import view_products_client, show_contact_info, handle_order_request, back_to_main_menu
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
    show_admin_contacts,
    start_add_contact,
    start_edit_contact,
    confirm_delete_contact,
    delete_contact,
    show_single_contact
)

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Route callback queries to appropriate handlers"""
    query = update.callback_query
    data = query.data

    # Client callbacks
    if data == "view_products":
        await view_products_client(update, context)
    elif data == "contact":
        await show_contact_info(update, context)
    elif data.startswith("order_"):
        await handle_order_request(update, context)
    elif data == "back_to_main":
        await back_to_main_menu(update, context)

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

    # Admin contact callbacks
    elif data == "admin_contacts":
        await show_admin_contacts(update, context)
    elif data == "admin_add_contact":
        await start_add_contact(update, context)
    elif data.startswith("view_contact_"):
        await show_single_contact(update, context)
    elif data.startswith("edit_contact_"):
        await start_edit_contact(update, context)
    elif data.startswith("delete_contact_"):
        await confirm_delete_contact(update, context)
    elif data.startswith("confirm_delete_contact_"):
        await delete_contact(update, context)

    # General callbacks
    elif data == "cancel_delete":
        await cancel_delete(update, context)

    # Unknown callback
    else:
        await query.answer("Unknown action")