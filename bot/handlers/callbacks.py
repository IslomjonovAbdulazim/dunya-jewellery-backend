"""Simple callback query handlers - UNIFIED INTERFACE"""

from telegram import Update
from telegram.ext import ContextTypes

from ..utils import is_admin
from .client import view_products_client, handle_order_request, back_to_main_menu, show_contact_info_client
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
    """Route callback queries - UNIFIED INTERFACE"""
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id

    try:
        # UNIFIED BUTTONS - Same interface, different functionality based on user type
        if data == "view_products":
            if is_admin(user_id):
                # Admin clicks "💍 Mahsulotlar" → sees admin products management
                await show_admin_products(update, context)
            else:
                # Client clicks "💍 Mahsulotlar" → sees client products view
                await view_products_client(update, context)

        elif data == "contact":
            if is_admin(user_id):
                # Admin clicks "📞 Bog'lanish" → sees admin contact management
                await show_admin_contact(update, context)
            else:
                # Client clicks "📞 Bog'lanish" → sees client contact info
                await show_contact_info_client(update, context)

        # CLIENT-SPECIFIC CALLBACKS
        elif data.startswith("order_"):
            await handle_order_request(update, context)
        elif data == "back_to_main":
            await back_to_main_menu(update, context)

        # ADMIN-SPECIFIC CALLBACKS (only admins can trigger these)
        elif data == "admin_products":
            if is_admin(user_id):
                await show_admin_products(update, context)
        elif data == "admin_add":
            if is_admin(user_id):
                await start_add_product(update, context)
        elif data.startswith("view_product_"):
            if is_admin(user_id):
                await show_single_product(update, context)
            else:
                await query.answer("❌ Noma'lum buyruq")
                return
        elif data.startswith("edit_contact_"):
            if is_admin(user_id):
                await start_edit_contact_field(update, context)
            else:
                await query.answer("❌ Sizga ruxsat yo'q")
                return
        elif data.startswith("edit_"):
            if is_admin(user_id):
                await start_edit_product(update, context)
        elif data.startswith("delete_"):
            if is_admin(user_id):
                await confirm_delete_product(update, context)
        elif data.startswith("confirm_delete_"):
            if is_admin(user_id):
                await delete_product(update, context)

        # GENERAL CALLBACKS
        elif data == "cancel_delete":
            await cancel_delete(update, context)

        # Unknown callback
        else:
            await query.answer("❌ Noma'lum buyruq")

    except Exception as e:
        # Handle any callback errors gracefully
        await query.answer("❌ Xatolik yuz berdi")
        print(f"Callback error: {e}")  # For debugging