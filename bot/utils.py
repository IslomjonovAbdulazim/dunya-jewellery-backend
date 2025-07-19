"""Simple utility functions for the bot"""

import re
import config
from .constants import *

# Global user states
user_states = {}

def escape_markdown(text):
    """Escape special characters for Telegram markdown"""
    if not text:
        return ""

    # Escape special markdown characters
    special_chars = ['*', '_', '`', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')

    return text

def is_admin(user_id):
    """Check if user is admin"""
    return user_id in config.ADMIN_CHAT_IDS

def get_user_state(user_id):
    """Get user state"""
    return user_states.get(user_id)

def set_user_state(user_id, state):
    """Set user state"""
    user_states[user_id] = state

def clear_user_state(user_id):
    """Clear user state"""
    if user_id in user_states:
        del user_states[user_id]

def format_product_for_client(product):
    """Format product for client"""
    try:
        title = getattr(product, 'title', 'Nomsiz mahsulot')
        description = getattr(product, 'description', None) or DEFAULT_DESCRIPTION

        sizes = product.get_sizes_list() if hasattr(product, 'get_sizes_list') else []
        sizes_text = ", ".join([str(s) for s in sizes]) if sizes else DEFAULT_SIZES

        return PRODUCT_TEMPLATE_CLIENT.format(
            title,
            description,
            sizes_text
        )
    except Exception as e:
        return f"❌ Mahsulot ma'lumotini ko'rsatishda xatolik"

def format_product_for_admin(product):
    """Format product for admin"""
    try:
        status = "✅" if getattr(product, 'is_active', False) else "❌"
        title = getattr(product, 'title', 'Nomsiz mahsulot')
        description = getattr(product, 'description', None) or DEFAULT_DESCRIPTION

        sizes = product.get_sizes_list() if hasattr(product, 'get_sizes_list') else []
        sizes_text = ", ".join([str(s) for s in sizes]) if sizes else DEFAULT_ADMIN_SIZES

        file_ids = product.get_file_ids_list() if hasattr(product, 'get_file_ids_list') else []
        image_count = len(file_ids)

        product_id = getattr(product, 'id', 'N/A')

        return PRODUCT_TEMPLATE_ADMIN.format(
            status,
            title,
            description,
            sizes_text,
            image_count,
            product_id
        )
    except Exception as e:
        return f"❌ Mahsulot ma'lumotini ko'rsatishda xatolik (ID: {getattr(product, 'id', 'N/A')})"

def parse_sizes(text):
    """Parse sizes from text"""
    try:
        return [float(s.strip()) for s in text.split(',') if s.strip()]
    except ValueError:
        return None

def format_contact_for_admin(contact):
    """Format contact for admin"""
    try:
        status = "✅" if contact.is_active else "❌"

        # Safely get contact fields
        label = contact.label or "Nomsiz"
        telegram = contact.telegram_username or "Yo'q"
        phone = contact.phone_number or "Yo'q"
        instagram = contact.instagram_username or "Yo'q"
        contact_id = getattr(contact, 'id', 'N/A')

        return CONTACT_TEMPLATE_ADMIN.format(
            status,
            label,
            telegram,
            phone,
            instagram,
            contact_id
        )
    except Exception as e:
        # Fallback if formatting fails
        return f"❌ Kontakt ma'lumotini ko'rsatishda xatolik (ID: {getattr(contact, 'id', 'N/A')})"

def format_contact_for_client(contact):
    """Format contact for client"""
    telegram = f"@{contact.telegram_username}" if contact.telegram_username else "❌"
    phone = contact.phone_number if contact.phone_number else "❌"
    instagram = f"@{contact.instagram_username}" if contact.instagram_username else "❌"

    return CONTACT_TEMPLATE_CLIENT.format(
        contact.label,
        telegram,
        phone,
        instagram
    )

def admin_required(func):
    """Admin decorator"""
    async def wrapper(update, context):
        user_id = update.effective_user.id
        if not is_admin(user_id):
            if update.callback_query:
                await update.callback_query.answer(ACCESS_DENIED)
            else:
                await update.message.reply_text(ACCESS_DENIED)
            return
        return await func(update, context)
    return wrapper