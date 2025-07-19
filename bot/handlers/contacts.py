"""Simple contact management handlers"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import get_db_session
from models import Contact
from ..utils import admin_required, set_user_state, format_contact_for_admin
from ..constants import *
from ..keyboards import get_contacts_list_keyboard, get_delete_contact_confirmation_keyboard

@admin_required
async def show_admin_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show contacts list for admin"""
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
        keyboard = [[InlineKeyboardButton(BTN_ADD_CONTACT, callback_data="admin_add_contact")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await edit_message(NO_CONTACTS_ADMIN, reply_markup=reply_markup)
        return

    # Create contact list
    contact_list = f"{CONTACT_MANAGEMENT_HEADER}\n\n"
    for contact in contacts:
        status = "✅" if contact.is_active else "❌"
        contact_list += f"{status} {contact.id} - {contact.label}\n"

    contact_list += f"\n📋 Jami: {len(contacts)} ta\n\n👆 Kontaktni tanlang:"

    reply_markup = get_contacts_list_keyboard(contacts)

    await edit_message(
        contact_list,
        reply_markup=reply_markup
    )

@admin_required
async def show_single_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show single contact details"""
    query = update.callback_query
    await query.answer()

    try:
        contact_id = int(query.data.split("_")[2])

        db = get_db_session()
        contact = db.query(Contact).filter(Contact.id == contact_id).first()
        db.close()

        if not contact:
            await query.edit_message_text(CONTACT_NOT_FOUND)
            return

        message = format_contact_for_admin(contact)

        back_keyboard = [
            [InlineKeyboardButton(BTN_BACK_TO_LIST, callback_data="admin_contacts")],
            [InlineKeyboardButton(BTN_EDIT, callback_data=f"edit_contact_{contact.id}")],
            [InlineKeyboardButton(BTN_DELETE, callback_data=f"delete_contact_{contact.id}")]
        ]
        reply_markup = InlineKeyboardMarkup(back_keyboard)

        # Try to edit message, if it fails send new message
        try:
            await query.edit_message_text(
                message,
                reply_markup=reply_markup
            )
        except Exception as edit_error:
            # If editing fails, send a new message
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=message,
                reply_markup=reply_markup
            )

    except Exception as e:
        # Handle any other errors
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="❌ Kontakt ma'lumotini olishda xatolik",
        )

@admin_required
async def start_add_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start contact creation"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        chat_id = query.message.chat_id
        send_message = lambda text, **kwargs: context.bot.send_message(chat_id, text, **kwargs)
    else:
        user_id = update.effective_user.id
        send_message = update.message.reply_text

    set_user_state(user_id, {
        'action': 'add_contact',
        'step': 'label'
    })

    await send_message(ADD_CONTACT_START)

@admin_required
async def start_edit_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start editing contact"""
    query = update.callback_query
    await query.answer()

    contact_id = int(query.data.split("_")[2])
    user_id = query.from_user.id

    db = get_db_session()
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db.close()

    if not contact:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=CONTACT_NOT_FOUND
        )
        return

    set_user_state(user_id, {
        'action': 'edit_contact',
        'step': 'label',
        'contact_id': contact_id,
        'current_contact': contact
    })

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=f"📝 Kontakt tahrirlash: {contact.label}\n\n{EDIT_CONTACT_LABEL}"
    )

@admin_required
async def confirm_delete_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask for contact deletion confirmation"""
    query = update.callback_query
    await query.answer()

    contact_id = int(query.data.split("_")[2])

    db = get_db_session()
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db.close()

    if not contact:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=CONTACT_NOT_FOUND
        )
        return

    reply_markup = get_delete_contact_confirmation_keyboard(contact_id)
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=DELETE_CONTACT_CONFIRMATION.format(contact.label),
        reply_markup=reply_markup
    )

@admin_required
async def delete_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete contact after confirmation"""
    query = update.callback_query
    await query.answer()

    contact_id = int(query.data.split("_")[3])

    db = get_db_session()
    contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if not contact:
        db.close()
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=CONTACT_NOT_FOUND
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