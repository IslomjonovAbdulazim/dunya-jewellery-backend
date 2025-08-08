"""Simple admin handlers - INLINE KEYBOARD ONLY"""

from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import BadRequest

from database import get_db_session
from models import Product
from ..utils import admin_required, format_product_for_admin, set_user_state
from ..constants import *
from ..keyboards import get_products_list_keyboard, get_delete_confirmation_keyboard

@admin_required
async def show_admin_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show products list for admin - INLINE ONLY"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        chat_id = query.message.chat.id
        edit_message = lambda text, **kwargs: query.edit_message_text(text, **kwargs)
    else:
        chat_id = update.effective_chat.id
        edit_message = lambda text, **kwargs: context.bot.send_message(chat_id, text, **kwargs)

    # Load real products from database
    db = get_db_session()
    products = db.query(Product).all()
    db.close()

    if not products:
        await edit_message(NO_PRODUCTS_ADMIN, parse_mode='Markdown')
        return

    # Create clean product list
    product_list = f"{ALL_PRODUCTS_HEADER}\n\n"
    for product in products:
        status = "✅" if product.is_active else "❌"
        title = product.title[:25] + "..." if len(product.title) > 25 else product.title
        product_list += f"{status} {product.id} - {title}\n"

    product_list += f"\n📋 Jami: {len(products)} ta\n\n👆 Mahsulotni tanlang:"

    reply_markup = get_products_list_keyboard(products)
    await edit_message(product_list, reply_markup=reply_markup, parse_mode='Markdown')

@admin_required
async def show_single_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show single product details"""
    query = update.callback_query
    await query.answer()

    product_id = int(query.data.split("_")[2])

    db = get_db_session()
    product = db.query(Product).filter(Product.id == product_id).first()
    db.close()

    if not product:
        await query.edit_message_text(PRODUCT_NOT_FOUND, parse_mode='Markdown')
        return

    message = format_product_for_admin(product)
    file_ids = product.get_file_ids_list()

    # Create action buttons
    back_keyboard = [
        [InlineKeyboardButton(BTN_BACK_TO_LIST, callback_data="admin_products")],
        [InlineKeyboardButton(BTN_EDIT, callback_data=f"edit_{product.id}")],
        [InlineKeyboardButton(BTN_DELETE, callback_data=f"delete_{product.id}")]
    ]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    if file_ids:
        try:
            if len(file_ids) == 1:
                await context.bot.send_photo(
                    chat_id=query.message.chat.id,
                    photo=file_ids[0],
                    caption=message,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            else:
                # Multiple images
                media = []
                for i, file_id in enumerate(file_ids):
                    if i == 0:
                        media.append(InputMediaPhoto(media=file_id, caption=message, parse_mode='Markdown'))
                    else:
                        media.append(InputMediaPhoto(media=file_id))

                await context.bot.send_media_group(chat_id=query.message.chat.id, media=media)
                await context.bot.send_message(
                    chat_id=query.message.chat.id,
                    text=f"🔧 *{product.title}* - Boshqaruv",
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
        except BadRequest:
            await context.bot.send_message(
                chat_id=query.message.chat.id,
                text=f"{message}\n\n{INVALID_FILE_ID_ERROR}",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    else:
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

@admin_required
async def start_add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start product creation"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        chat_id = query.message.chat.id
        send_message = lambda text, **kwargs: context.bot.send_message(chat_id, text, **kwargs)
    else:
        user_id = update.effective_user.id
        send_message = update.message.reply_text

    set_user_state(user_id, {
        'action': 'add',
        'step': 'title'
    })

    await send_message(ADD_PRODUCT_START, parse_mode='Markdown')

@admin_required
async def start_edit_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start product editing"""
    query = update.callback_query
    await query.answer()

    product_id = int(query.data.split("_")[1])
    user_id = query.from_user.id

    db = get_db_session()
    product = db.query(Product).filter(Product.id == product_id).first()
    db.close()

    if not product:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=PRODUCT_NOT_FOUND,
            parse_mode='Markdown'
        )
        return

    set_user_state(user_id, {
        'action': 'edit',
        'step': 'title',
        'product_id': product_id,
        'current_product': product
    })

    await context.bot.send_message(
        chat_id=query.message.chat.id,
        text=f"📝 *Tahrirlash*: {product.title}\n\n{EDIT_TITLE_PROMPT}",
        parse_mode='Markdown'
    )

@admin_required
async def confirm_delete_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask for deletion confirmation"""
    query = update.callback_query
    await query.answer()

    product_id = int(query.data.split("_")[1])

    db = get_db_session()
    product = db.query(Product).filter(Product.id == product_id).first()
    db.close()

    if not product:
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=PRODUCT_NOT_FOUND,
            parse_mode='Markdown'
        )
        return

    reply_markup = get_delete_confirmation_keyboard(product_id)
    await context.bot.send_message(
        chat_id=query.message.chat.id,
        text=DELETE_CONFIRMATION.format(product.title),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

@admin_required
async def delete_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete product after confirmation"""
    query = update.callback_query
    await query.answer()

    product_id = int(query.data.split("_")[2])

    db = get_db_session()
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        db.close()
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=PRODUCT_NOT_FOUND,
            parse_mode='Markdown'
        )
        return

    product_title = product.title
    db.delete(product)
    db.commit()
    db.close()

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=PRODUCT_DELETED.format(product_title),
        parse_mode='Markdown'
    )

async def cancel_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel deletion"""
    query = update.callback_query
    await query.answer(DELETE_CANCELLED)