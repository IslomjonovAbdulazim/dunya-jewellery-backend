"""Client handlers"""

from telegram import Update, InputMediaPhoto
from telegram.ext import ContextTypes
from telegram.error import BadRequest

from database import get_db_session
from models import Product, Contact
from ..utils import format_product_for_client
from ..constants import *
from ..keyboards import get_client_back_keyboard, get_product_order_keyboard, get_client_inline_keyboard

async def view_products_client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show products to clients"""
    query = update.callback_query
    await query.answer()

    db = get_db_session()
    products = db.query(Product).filter(Product.is_active == True).all()
    db.close()

    if not products:
        reply_markup = get_client_back_keyboard()
        await query.edit_message_text(
            NO_PRODUCTS_CLIENT,
            reply_markup=reply_markup
        )
        return

    # Send header
    reply_markup = get_client_back_keyboard()
    await query.edit_message_text(
        CLIENT_PRODUCTS_HEADER,
        reply_markup=reply_markup
    )

    # Send each product
    for product in products:
        message = format_product_for_client(product)
        file_ids = product.get_file_ids_list()

        if file_ids:
            try:
                reply_markup = get_product_order_keyboard(product.id)

                if len(file_ids) == 1:
                    # Single image
                    await context.bot.send_photo(
                        chat_id=query.message.chat_id,
                        photo=file_ids[0],
                        caption=message,
                        reply_markup=reply_markup
                    )
                else:
                    # Multiple images
                    media = []
                    for i, file_id in enumerate(file_ids):
                        if i == 0:
                            media.append(InputMediaPhoto(media=file_id, caption=message))
                        else:
                            media.append(InputMediaPhoto(media=file_id))

                    await context.bot.send_media_group(
                        chat_id=query.message.chat_id,
                        media=media
                    )

                    # Send order button separately
                    await context.bot.send_message(
                        chat_id=query.message.chat_id,
                        text=f"📞 Mahsulot: {product.title}",
                        reply_markup=reply_markup
                    )
            except BadRequest:
                # Handle bad file IDs
                reply_markup = get_product_order_keyboard(product.id)
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=message,
                    reply_markup=reply_markup
                )
        else:
            # No images
            reply_markup = get_product_order_keyboard(product.id)
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=message,
                reply_markup=reply_markup
            )

async def show_contact_info_client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show contact information for clients"""
    query = update.callback_query
    await query.answer()

    db = get_db_session()
    contact = db.query(Contact).first()
    db.close()

    if not contact:
        # Fallback to default contact
        await query.edit_message_text(
            "📞 Bog'lanish\n\n📱 Telefon: +998 90 123 45 67\n💬 Telegram: @dunya_jewellery"
        )
        return

    # Build contact message
    contact_message = "📞 Bog'lanish ma'lumotlari\n\n"

    if contact.telegram_username:
        contact_message += f"💬 Telegram: https://t.me/{contact.telegram_username}\n"

    phones = contact.get_phone_numbers_list()
    if phones:
        if len(phones) == 1:
            contact_message += f"📱 Telefon: {phones[0]}\n"
        else:
            contact_message += f"📱 Telefonlar:\n"
            for phone in phones:
                contact_message += f"  • {phone}\n"

    if contact.instagram_username:
        contact_message += f"📷 Instagram: https://instagram.com/{contact.instagram_username}\n"

    await query.edit_message_text(contact_message, parse_mode='Markdown')

async def handle_order_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle order requests"""
    query = update.callback_query
    await query.answer()

    product_id = query.data.split("_")[1]

    # Get real contact data for order message
    db = get_db_session()
    contact = db.query(Contact).first()
    db.close()

    if contact:
        # Build order message with real contact data
        order_message = f"📞 Buyurtma\n\n🆔 Mahsulot: {product_id}\n\n"

        # Add phone numbers (raw format for click-to-call)
        phones = contact.get_phone_numbers_list()
        if phones:
            if len(phones) == 1:
                order_message += f"📱 Telefon: {phones[0]}\n"
            else:
                order_message += f"📱 Telefonlar:\n"
                for phone in phones:
                    order_message += f"  • {phone}\n"

        # Add Telegram (@username works inside Telegram)
        if contact.telegram_username:
            order_message += f"💬 Telegram: @{contact.telegram_username}\n"

        # Add Instagram (full URL)
        if contact.instagram_username:
            order_message += f"📷 Instagram: https://instagram.com/{contact.instagram_username}"
    else:
        # Fallback if no contact data
        order_message = f"📞 Buyurtma\n\n🆔 Mahsulot: {product_id}\n\n📱 Telefon: +998901234567\n💬 Telegram: @dunya_jewellery\n📷 Instagram: https://instagram.com/dunya_jewellery"

    await query.edit_message_text(order_message)

async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Back to main menu"""
    query = update.callback_query
    await query.answer()

    reply_markup = get_client_inline_keyboard()
    await query.edit_message_text(
        CLIENT_WELCOME,
        reply_markup=reply_markup
    )