"""Simple keyboard layouts - UNIFIED INTERFACE"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .constants import *

# UNIFIED INTERFACE - Same buttons for both admin and client
def get_client_inline_keyboard():
    """Main menu - SAME FOR BOTH ADMIN AND CLIENT"""
    keyboard = [
        [InlineKeyboardButton(BTN_PRODUCTS, callback_data="view_products")],
        [InlineKeyboardButton(BTN_CONTACT, callback_data="contact")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_client_after_products_keyboard():
    """Navigation after viewing all products (clients only)"""
    keyboard = [
        [InlineKeyboardButton(BTN_CONTACT, callback_data="contact")],
        [InlineKeyboardButton(BTN_BACK_MAIN, callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_client_back_keyboard():
    """Simple back button for clients"""
    keyboard = [
        [InlineKeyboardButton(BTN_BACK_MAIN, callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_product_order_keyboard(product_id):
    """Order button for individual products (clients only)"""
    keyboard = [
        [InlineKeyboardButton(BTN_ORDER, callback_data=f"order_{product_id}")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ADMIN-SPECIFIC KEYBOARDS (triggered from unified buttons)
def get_products_list_keyboard(products):
    """Product list keyboard for admin"""
    keyboard = []

    # Create buttons in rows of 3
    row = []
    for product in products:
        status_icon = "✅" if product.is_active else "❌"
        button_text = f"{status_icon} {product.id}"
        row.append(InlineKeyboardButton(button_text, callback_data=f"view_product_{product.id}"))

        if len(row) == 3:
            keyboard.append(row)
            row = []

    # Add remaining buttons
    if row:
        keyboard.append(row)

    # Add "Add New" button
    keyboard.append([InlineKeyboardButton(BTN_ADD_NEW, callback_data="admin_add")])

    return InlineKeyboardMarkup(keyboard)

def get_delete_confirmation_keyboard(product_id):
    """Delete confirmation buttons"""
    keyboard = [
        [InlineKeyboardButton(BTN_CONFIRM_DELETE, callback_data=f"confirm_delete_{product_id}")],
        [InlineKeyboardButton(BTN_CANCEL, callback_data="cancel_delete")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_contact_edit_keyboard():
    """Contact edit options keyboard for admin"""
    keyboard = [
        [InlineKeyboardButton(BTN_EDIT_TELEGRAM, callback_data="edit_contact_telegram")],
        [InlineKeyboardButton(BTN_EDIT_PHONES, callback_data="edit_contact_phones")],
        [InlineKeyboardButton(BTN_EDIT_INSTAGRAM, callback_data="edit_contact_instagram")]
    ]
    return InlineKeyboardMarkup(keyboard)