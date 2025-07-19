"""Utility functions for the bot"""

import config
from .constants import *

# Global user states for conversations
user_states = {}

def is_admin(user_id):
    """Check if user is admin"""
    return user_id in config.ADMIN_CHAT_IDS

def get_user_state(user_id):
    """Get user conversation state"""
    return user_states.get(user_id)

def set_user_state(user_id, state):
    """Set user conversation state"""
    user_states[user_id] = state

def clear_user_state(user_id):
    """Clear user conversation state"""
    if user_id in user_states:
        del user_states[user_id]

def format_product_for_client(product):
    """Format product for client display"""
    sizes = ", ".join([str(s) for s in product.get_sizes_list()])
    description = product.description or DEFAULT_DESCRIPTION
    sizes_text = sizes or DEFAULT_SIZES

    return PRODUCT_TEMPLATE_CLIENT.format(
        product.title,
        description,
        sizes_text
    )

def format_product_for_admin(product):
    """Format product for admin display"""
    status = "✅" if product.is_active else "❌"
    sizes = ", ".join([str(s) for s in product.get_sizes_list()])
    description = product.description or DEFAULT_DESCRIPTION
    sizes_text = sizes or DEFAULT_ADMIN_SIZES

    return PRODUCT_TEMPLATE_ADMIN.format(
        status,
        product.title,
        description,
        sizes_text,
        len(product.get_file_ids_list()),
        product.id
    )

def parse_sizes(text):
    """Parse sizes from text input"""
    try:
        return [float(s.strip()) for s in text.split(',') if s.strip()]
    except ValueError:
        return None

def format_contact_for_admin(contact):
    """Format contact for admin display"""
    status = "✅" if contact.is_active else "❌"
    telegram = contact.telegram_username or "Belgilanmagan"
    phone = contact.phone_number or "Belgilanmagan"
    instagram = contact.instagram_username or "Belgilanmagan"

    return CONTACT_TEMPLATE_ADMIN.format(
        status,
        contact.label,
        telegram,
        phone,
        instagram,
        contact.id
    )

def format_contact_for_client(contact):
    """Format contact for client display"""
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
    """Decorator to check if user is admin"""
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