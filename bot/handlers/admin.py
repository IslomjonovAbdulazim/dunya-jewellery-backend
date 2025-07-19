"""Admin handlers for product management"""

from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import BadRequest

from database import get_db_session
from models import Product
from ..utils import admin_required, format_product_for_admin, set_user_state
from ..constants import *
from ..keyboards import get_admin_product_keyboard, get_delete_confirmation_keyboard, get_products_list_keyboard

@admin_required
async def show_admin_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show products list for admin to select from"""
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
    products = db.query(Product).all()
    db.close()

    if not products:
        await edit_message(NO_PRODUCTS_ADMIN)
        return

    # Create product list text
    product_list = f"{ALL_PRODUCTS_HEADER}\n\n"
    for product in products:
        status = "✅" if product.is_active else "❌"
        product_list += f"{status} *{product.id}* - {product.title}\n"

    product_list += f"\n📋 Jami: {len(products)} ta mahsulot\n\n👆 Mahsulotni tanlang:"

    # Get keyboard with product buttons
    reply_markup = get_products_list_keyboard(products)

    await edit_message(
        product_list,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

@admin_required
async def show_single_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show individual product details with admin controls"""
    query = update.callback_query
    await query.answer()

    product_id = int(query.data.split("_")[2])  # view_product_123

    db = get_db_session()
    product = db.query(Product).filter(Product.id == product_id).first()
    db.close()

    if not product:
        await query.edit_message_text(PRODUCT_NOT_FOUND)
        return

    # Format product details
    message = format_product_for_admin(product)
    file_ids = product.get_file_ids_list()
    reply_markup = get_admin_product_keyboard(product.id)

    # Add back button
    back_keyboard = [
        [InlineKeyboardButton(BTN_BACK_TO_LIST, callback_data="admin_products")],
        [InlineKeyboardButton(BTN_EDIT, callback_data=f"edit_{product.id}")],
        [InlineKeyboardButton(BTN_DELETE, callback_data=f"delete_{product.id}")]
    ]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    if file_ids:
        try:
            if len(file_ids) == 1:
                # Single image
                await context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=file_ids[0],
                    caption=message,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
            else:
                # Multiple images as media group
                # Filter out invalid file_ids
                valid_file_ids = []
                for file_id in file_ids:
                    if file_id and len(file_id) > 10:  # Basic validation
                        valid_file_ids.append(file_id)

                if valid_file_ids:
                    media = []
                    for i, file_id in enumerate(valid_file_ids):
                        if i == 0:
                            media.append(InputMediaPhoto(media=file_id, caption=message, parse_mode='Markdown'))
                        else:
                            media.append(InputMediaPhoto(media=file_id))

                    await context.bot.send_media_group(
                        chat_id=query.message.chat_id,
                        media=media
                    )

                    # Send admin buttons separately
                    await context.bot.send_message(
                        chat_id=query.message.chat_id,
                        text=f"🔧 *{product.title}* - Boshqaruv",
                        parse_mode='Markdown',
                        reply_markup=reply_markup
                    )
                else:
                    # No valid images - send text only
                    await context.bot.send_message(
                        chat_id=query.message.chat_id,
                        text=f"{message}\n\n{INVALID_IMAGES_ERROR}",
                        parse_mode='Markdown',
                        reply_markup=reply_markup
                    )
        except BadRequest as e:
            # Handle invalid file_ids gracefully
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"{message}\n\n{INVALID_FILE_ID_ERROR}",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            print(f"Error sending media for product {product.id}: {e}")
    else:
        # No images - send text with admin buttons
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=message,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

@admin_required
async def start_add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the product creation process"""
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

    # Set user state for product creation
    set_user_state(user_id, {
        'action': 'add',
        'step': 'title'
    })

    await send_message(ADD_PRODUCT_START, parse_mode='Markdown')

@admin_required
async def start_edit_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start editing a product"""
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
            text=PRODUCT_NOT_FOUND
        )
        return

    # Set user state for editing
    set_user_state(user_id, {
        'action': 'edit',
        'step': 'title',
        'product_id': product_id,
        'current_product': product
    })

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=f"📝 Tahrirlash: *{product.title}*\n\n{EDIT_TITLE_PROMPT}",
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
            chat_id=query.message.chat_id,
            text=PRODUCT_NOT_FOUND
        )
        return

    reply_markup = get_delete_confirmation_keyboard(product_id)
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=DELETE_CONFIRMATION.format(product.title),
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

@admin_required
async def delete_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Actually delete the product after confirmation"""
    query = update.callback_query
    await query.answer()

    product_id = int(query.data.split("_")[2])

    db = get_db_session()
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        db.close()
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=PRODUCT_NOT_FOUND
        )
        return

    product_title = product.title
    db.delete(product)
    db.commit()
    db.close()

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=PRODUCT_DELETED.format(product_title)
    )

async def cancel_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel product deletion"""
    query = update.callback_query
    await query.answer(DELETE_CANCELLED)