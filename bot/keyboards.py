"""Simple keyboard layouts"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from .constants import *

def get_admin_reply_keyboard():
    """Admin reply keyboard"""
    keyboard = [
        [KeyboardButton(BTN_ADMIN_PRODUCTS), KeyboardButton(BTN_ADMIN_CONTACT)]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_client_inline_keyboard():
    """Client inline keyboard"""
    keyboard = [
        [InlineKeyboardButton(BTN_PRODUCTS, callback_data="view_products")],
        [InlineKeyboardButton(BTN_CONTACT, callback_data="contact")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_client_back_keyboard():
    """Back button for clients"""
    keyboard = [
        [InlineKeyboardButton(BTN_BACK_MAIN, callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_product_order_keyboard(product_id):
    """Order button for product"""
    keyboard = [
        [InlineKeyboardButton(BTN_ORDER, callback_data=f"order_{product_id}")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_product_keyboard(product_id):
    """Admin product buttons"""
    keyboard = [
        [InlineKeyboardButton(BTN_EDIT, callback_data=f"edit_{product_id}")],
        [InlineKeyboardButton(BTN_DELETE, callback_data=f"delete_{product_id}")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_products_list_keyboard(products):
    """Product list keyboard"""
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
    """Contact edit options keyboard"""
    keyboard = [
        [InlineKeyboardButton(BTN_EDIT_TELEGRAM, callback_data="edit_contact_telegram")],
        [InlineKeyboardButton(BTN_EDIT_PHONES, callback_data="edit_contact_phones")],
        [InlineKeyboardButton(BTN_EDIT_INSTAGRAM, callback_data="edit_contact_instagram")]
    ]
    return InlineKeyboardMarkup(keyboard)