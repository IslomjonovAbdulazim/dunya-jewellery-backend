"""Simple contact management handlers"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import get_db_session
from models import Contact
from ..utils import admin_required, set_user_state, format_contact_for_admin, clear_user_state
from ..constants import *
from ..keyboards import get_contact_edit_keyboard

@admin_required
async def show_admin_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show contact info for admin"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        chat_id = query.message.chat.id
        edit_message = query.edit_message_text
    else:
        chat_id = update.effective_chat.id
        edit_message = lambda text, **kwargs: context.bot.send_message(chat_id, text, **kwargs)

    db = get_db_session()
    contact = db.query(Contact).first()  # Get the first (and only) contact
    db.close()

    if not contact:
        # Create default contact if none exists
        await create_default_contact(update, context)
        return

    message = format_contact_for_admin(contact)
    reply_markup = get_contact_edit_keyboard()

    await edit_message(
        message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def create_default_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create default contact record"""
    db = get_db_session()

    contact = Contact(
        telegram_username="dunya_jewellery",  # Will show as https://t.me/dunya_jewellery
        phone_numbers="+998901234567",  # Valid Uzbek number
        instagram_username="dunya_jewellery",  # Will show as https://instagram.com/dunya_jewellery
        is_active=True
    )

    db.add(contact)
    db.commit()
    db.close()

    await show_admin_contact(update, context)

@admin_required
async def start_edit_contact_field(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start editing specific contact field"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    field = query.data.split("_")[2]  # edit_contact_telegram -> telegram

    db = get_db_session()
    contact = db.query(Contact).first()
    db.close()

    if not contact:
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=CONTACT_NOT_FOUND
        )
        return

    set_user_state(user_id, {
        'action': 'edit_contact',
        'field': field,
        'contact': contact
    })

    if field == 'telegram':
        current_value = contact.telegram_username or CURRENT_VALUE_NONE
        prompt = EDIT_CONTACT_TELEGRAM.format(current_value)
    elif field == 'phones':
        phones = contact.get_phone_numbers_list()
        current_value = ", ".join(phones) if phones else CURRENT_VALUE_NONE
        prompt = EDIT_CONTACT_PHONES.format(current_value)
    elif field == 'instagram':
        current_value = contact.instagram_username or CURRENT_VALUE_NONE
        prompt = EDIT_CONTACT_INSTAGRAM.format(current_value)

    await context.bot.send_message(
        chat_id=query.message.chat.id,
        text=prompt,
        parse_mode='Markdown'
    )

def parse_phone_numbers(text):
    """Parse and validate Uzbek phone numbers from text"""
    if not text or text.strip() == "":
        return []

    # Split by comma and validate each number
    phones = []
    invalid_phones = []

    for phone in text.split(','):
        phone = phone.strip()
        if not phone:
            continue

        # Remove spaces, dashes, parentheses for validation
        cleaned_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

        # Validate Uzbek phone number format
        if is_valid_uzbek_phone(cleaned_phone):
            phones.append(cleaned_phone)
        else:
            invalid_phones.append(phone)

    if invalid_phones:
        raise ValueError(f"Noto'g'ri telefon raqamlar: {', '.join(invalid_phones)}")

    return phones

def is_valid_uzbek_phone(phone):
    """Validate if phone number is a proper Uzbek number"""
    # Must start with +998
    if not phone.startswith('+998'):
        return False

    # Must be exactly 13 characters (+998 + 9 digits)
    if len(phone) != 13:
        return False

    # After +998, must have exactly 9 digits
    remaining = phone[4:]  # Remove +998
    if not remaining.isdigit():
        return False

    # First digit after +998 must be 9, 7, 3, or 5 (valid Uzbek mobile prefixes)
    valid_prefixes = ['90', '91', '93', '94', '95', '97', '98', '99', '77', '71', '33', '50', '55']
    mobile_prefix = remaining[:2]

    if mobile_prefix not in valid_prefixes:
        return False

    return True

async def handle_contact_field_edit(update: Update, context: ContextTypes.DEFAULT_TYPE, state, text):
    """Handle contact field editing"""
    field = state['field']
    user_id = update.effective_user.id

    db = get_db_session()
    contact = db.query(Contact).first()

    if not contact:
        await update.message.reply_text(CONTACT_NOT_FOUND)
        db.close()
        clear_user_state(user_id)
        return

    try:
        if field == 'telegram':
            if text == '/skip':
                await update.message.reply_text("✅ Telegram o'zgartirilmadi")
            else:
                contact.telegram_username = text.replace('@', '').strip() if text.strip() else None
                await update.message.reply_text("✅ Telegram yangilandi")

        elif field == 'phones':
            if text == '/skip':
                await update.message.reply_text("✅ Telefonlar o'zgartirilmadi")
            else:
                try:
                    phones = parse_phone_numbers(text)
                    if not phones:
                        await update.message.reply_text("❌ Kamida bitta telefon raqam kiriting!\n\n📝 Format: +998901234567, +998907654321\n💡 Yana urinib ko'ring:")
                        db.close()
                        # DON'T clear user state - keep them in editing mode
                        return

                    # COMPLETELY REPLACE old phone numbers with new ones
                    contact.set_phone_numbers(phones)
                    await update.message.reply_text(f"✅ Telefon raqamlar to'liq yangilandi!\n\n📞 Yangi ro'yxat ({len(phones)} ta):\n" + "\n".join([f"  • {phone}" for phone in phones]))
                except ValueError as e:
                    await update.message.reply_text(f"❌ {str(e)}\n\n📝 To'g'ri format: +998901234567, +998907654321\n💡 Qaytadan kiriting:")
                    db.close()
                    # DON'T clear user state - keep them in editing mode
                    return

        elif field == 'instagram':
            if text == '/skip':
                await update.message.reply_text("✅ Instagram o'zgartirilmadi")
            else:
                contact.instagram_username = text.replace('@', '').strip() if text.strip() else None
                await update.message.reply_text("✅ Instagram yangilandi")

        # Success - commit changes and show final message
        db.commit()
        await update.message.reply_text(CONTACT_UPDATED)

    except Exception as e:
        await update.message.reply_text(ERROR_OCCURRED.format(str(e)))
    finally:
        db.close()
        # Clear user state only on success or unexpected error
        clear_user_state(user_id)