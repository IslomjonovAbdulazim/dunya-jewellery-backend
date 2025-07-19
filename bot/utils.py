"""Simple utility functions for the bot"""

import re
import config
from .constants import *

# Global user states
user_states = {}

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
    """Format product for client display"""
    try:
        title = getattr(product, 'title', 'Nomsiz mahsulot')
        description = getattr(product, 'description', None) or DEFAULT_DESCRIPTION

        # Get sizes and format them nicely
        sizes = product.get_sizes_list() if hasattr(product, 'get_sizes_list') else []
        if sizes:
            sizes.sort()
            sizes_text = ", ".join([str(s) for s in sizes])
        else:
            sizes_text = DEFAULT_SIZES

        return PRODUCT_TEMPLATE_CLIENT.format(title, description, sizes_text)
    except Exception as e:
        return "❌ Mahsulot ma'lumotini ko'rsatishda xatolik"

def format_product_for_admin(product):
    """Format product for admin display"""
    try:
        status = "✅" if getattr(product, 'is_active', False) else "❌"
        title = getattr(product, 'title', 'Nomsiz mahsulot')
        description = getattr(product, 'description', None) or DEFAULT_DESCRIPTION

        # Truncate long descriptions
        if len(description) > 100:
            description = description[:97] + "..."

        # Get sizes and format them
        sizes = product.get_sizes_list() if hasattr(product, 'get_sizes_list') else []
        if sizes:
            sizes.sort()
            sizes_text = ", ".join([str(s) for s in sizes])
        else:
            sizes_text = DEFAULT_ADMIN_SIZES

        # Get image count
        file_ids = product.get_file_ids_list() if hasattr(product, 'get_file_ids_list') else []
        image_count = len(file_ids)
        product_id = getattr(product, 'id', 'N/A')

        return PRODUCT_TEMPLATE_ADMIN.format(status, title, description, sizes_text, image_count, product_id)
    except Exception as e:
        return f"❌ Mahsulot ma'lumotini ko'rsatishda xatolik (ID: {getattr(product, 'id', 'N/A')})"

def parse_sizes(text):
    """Parse sizes from text input - SIMPLE VERSION"""
    if not text or not text.strip():
        return []

    try:
        sizes = []
        for size_str in text.split(','):
            size_str = size_str.strip()
            if size_str:
                size = float(size_str)
                # Simple validation: 1-1000 (very loose)
                if 1.0 <= size <= 1000.0:
                    sizes.append(size)
                else:
                    return None  # Invalid size

        return sorted(list(set(sizes))) if sizes else []
    except ValueError:
        return None

def format_contact_for_admin(contact):
    """Format contact for admin display"""
    try:
        # Telegram with @username (works inside Telegram bot)
        telegram = f"@{contact.telegram_username}" if contact.telegram_username else "Yo'q"

        # Phone numbers (raw format for click-to-call)
        phones = contact.get_phone_numbers_list()
        phones_text = ", ".join(phones) if phones else "Yo'q"

        # Instagram with clickable link
        instagram = f"https://instagram.com/{contact.instagram_username}" if contact.instagram_username else "Yo'q"

        return CONTACT_TEMPLATE_ADMIN.format(telegram, phones_text, instagram)
    except Exception as e:
        return f"❌ Kontakt ma'lumotini ko'rsatishda xatolik (ID: {getattr(contact, 'id', 'N/A')})"

def format_contact_for_client(contact):
    """Format contact for client display"""
    # Telegram with @username (works inside Telegram bot)
    telegram = f"@{contact.telegram_username}" if contact.telegram_username else "❌"

    # Phone numbers (raw format for click-to-call)
    phones = contact.get_phone_numbers_list()
    phones_text = ", ".join(phones) if phones else "❌"

    # Instagram with clickable link
    instagram = f"https://instagram.com/{contact.instagram_username}" if contact.instagram_username else "❌"

    return CONTACT_TEMPLATE_CLIENT.format(telegram, phones_text, instagram)

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