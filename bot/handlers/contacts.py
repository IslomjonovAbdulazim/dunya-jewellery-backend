"""Contact management handlers for admin"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import get_db_session
from models import Contact
from ..utils import admin_required, set_user_state, format_contact_for_admin
from ..constants import *
from ..keyboards import get_contacts_list_keyboard, get_admin_contact_keyboard, get_delete_contact_confirmation_keyboard


@admin_required
async def show_admin_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show contacts list for admin to select from"""
    # Handle both callback queries and keyboard button presses
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        chat_id = query.message.chat_id
        edit_message = query.edit_message_text
    else:
        chat_id = update.effective_chat.id
        edit_message = lambda text, **kwargs: context.bot.send_message(chat_id, text, **kwargs)

    db = get_db_session()
    contacts = db.query(Contact).all()
    db.close()

    if not contacts:
        # Show add contact button if no contacts
        keyboard = [[InlineKeyboardButton(BTN_ADD_CONTACT, callback_data="admin_add_contact")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await edit_message(NO_CONTACTS_ADMIN, reply_markup=reply_markup)
        return

    # Create contact list text
    contact_list = f"{CONTACT_MANAGEMENT_HEADER}\n\n"
    for contact in contacts:
        status = "✅" if contact.is_active else "❌"
        contact_list += f"{status} *{contact.id}* - {contact.label}\n"

    contact_list += f"\n📋 Jami: {len(contacts)} ta kontakt\n\n👆 Kontaktni tanlang:"

    # Get keyboard with contact buttons
    reply_markup = get_contacts_list_keyboard(contacts)

    await edit_message(
        contact_list,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )


@admin_required
async def show_single_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show individual contact details with admin controls"""
    query = update.callback_query
    await query.answer()

    contact_id = int(query.data.split("_")[2])  # view_contact_123

    db = get_db_session()
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db.close()

    if not contact:
        await query.edit_message_text(PRODUCT_NOT_FOUND)  # Reuse product not found message
        return

    # Format contact details
    message = format_contact_for_admin(contact)

    # Add back button and admin controls
    back_keyboard = [
        [InlineKeyboardButton(BTN_BACK_TO_LIST, callback_data="admin_contacts")],
        [InlineKeyboardButton(BTN_EDIT, callback_data=f"edit_contact_{contact.id}")],
        [InlineKeyboardButton(BTN_DELETE, callback_data=f"delete_contact_{contact.id}")]
    ]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    await query.edit_message_text(
        message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )


@admin_required
async def start_add_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the contact creation process"""
    # Handle both callback queries and commands
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        chat_id = query.message.chat_id
        send_message = lambda text, **kwargs: context.bot.send_message(chat_id, text, **kwargs)
    else:
        user_id = update.effective_user.id
        send_message = update.message.reply_text

    # Set user state for contact creation
    set_user_state(user_id, {
        'action': 'add_contact',
        'step': 'label'
    })

    await send_message(ADD_CONTACT_START, parse_mode='Markdown')


@admin_required
async def start_edit_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start editing a contact"""
    query = update.callback_query
    await query.answer()

    contact_id = int(query.data.split("_")[2])  # edit_contact_123
    user_id = query.from_user.id

    db = get_db_session()
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db.close()

    if not contact:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=PRODUCT_NOT_FOUND  # Reuse message
        )
        return

    # Set user state for editing
    set_user_state(user_id, {
        'action': 'edit_contact',
        'step': 'label',
        'contact_id': contact_id,
        'current_contact': contact
    })

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=f"📝 Kontakt tahrirlash: *{contact.label}*\n\n{EDIT_CONTACT_LABEL}",
        parse_mode='Markdown'
    )


@admin_required
async def confirm_delete_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask for contact deletion confirmation"""
    query = update.callback_query
    await query.answer()

    contact_id = int(query.data.split("_")[2])  # delete_contact_123

    db = get_db_session()
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db.close()

    if not contact:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=PRODUCT_NOT_FOUND
        )
        return

    reply_markup = get_delete_contact_confirmation_keyboard(contact_id)
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=DELETE_CONTACT_CONFIRMATION.format(contact.label),
        parse_mode='Markdown',
        reply_markup=reply_markup
    )


@admin_required
async def delete_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Actually delete the contact after confirmation"""
    query = update.callback_query
    await query.answer()

    contact_id = int(query.data.split("_")[3])  # confirm_delete_contact_123

    db = get_db_session()
    contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if not contact:
        db.close()
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=PRODUCT_NOT_FOUND
        )
        return

    contact_label = contact.label
    db.delete(contact)
    db.commit()
    db.close()

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=CONTACT_DELETED.format(contact_label)
    )