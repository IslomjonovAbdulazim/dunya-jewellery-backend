"""Client handlers - BETTER NAVIGATION"""

from telegram import Update, InputMediaPhoto
from telegram.ext import ContextTypes
from telegram.error import BadRequest

from database import get_db_session
from models import Product, Contact
from ..utils import format_product_for_client
from ..constants import *
from ..keyboards import get_client_after_products_keyboard, get_product_order_keyboard, get_client_inline_keyboard, get_client_back_keyboard

async def view_products_client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show products to clients with better navigation"""
    query = update.callback_query
    await query.answer()

    # Load real active products
    db = get_db_session()
    products = db.query(Product).filter(Product.is_active == True).all()
    db.close()

    if not products:
        # No products - show message with back button
        reply_markup = get_client_back_keyboard()
        await query.edit_message_text(
            NO_PRODUCTS_CLIENT,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return

    # Send header with better navigation after products
    await query.edit_message_text(
        CLIENT_PRODUCTS_HEADER,
        parse_mode='Markdown'
    )

    # Send each product
    for product in products:
        message = format_product_for_client(product)
        file_ids = product.get_file_ids_list()
        reply_markup = get_product_order_keyboard(product.id)

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
                        text=f"📞 *Mahsulot*: {product.title}",
                        reply_markup=reply_markup,
                        parse_mode='Markdown'
                    )
            except BadRequest:
                await context.bot.send_message(
                    chat_id=query.message.chat.id,
                    text=f"{message}\n\n{INVALID_IMAGES_ERROR}",
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

    # IMPORTANT: After all products, send navigation menu
    await context.bot.send_message(
        chat_id=query.message.chat.id,
        text="📋 *Barcha mahsulotlar ko'rsatildi*\n\nQuyidagi tugmalardan foydalaning:",
        reply_markup=get_client_after_products_keyboard(),
        parse_mode='Markdown'
    )

async def show_contact_info_client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show contact info for clients"""
    query = update.callback_query
    await query.answer()

    # Load real contact data
    db = get_db_session()
    contact = db.query(Contact).first()
    db.close()

    if not contact:
        # Fallback contact with back button
        reply_markup = get_client_back_keyboard()
        await query.edit_message_text(
            "📞 Bog'lanish\n\n📱 Telefon: +998901234567\n💬 Telegram: @dunya_jewellery\n📷 Instagram: https://instagram.com/dunya_jewellery",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return

    # Build contact message with real data
    contact_message = "📞 Bog'lanish ma'lumotlari\n\n"

    if contact.telegram_username:
        contact_message += f"💬 Telegram: @{contact.telegram_username}\n"

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

    # Always include back button for clean navigation
    reply_markup = get_client_back_keyboard()
    await query.edit_message_text(contact_message, reply_markup=reply_markup, parse_mode='MarkdownV2')

async def handle_order_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle order requests"""
    query = update.callback_query
    await query.answer()

    product_id = int(query.data.split("_")[1])

    # Load real data
    db = get_db_session()
    contact = db.query(Contact).first()
    product = db.query(Product).filter(Product.id == product_id).first()
    db.close()

    # Build order message
    if product:
        order_message = f"📞 Buyurtma\n\n🆔 Mahsulot: *{product.title}* (ID: {product_id})\n\n"
    else:
        order_message = f"📞 Buyurtma\n\n🆔 Mahsulot ID: {product_id}\n\n"

    if contact:
        phones = contact.get_phone_numbers_list()
        if phones:
            if len(phones) == 1:
                order_message += f"📱 Telefon: {phones[0]}\n"
            else:
                order_message += f"📱 Telefonlar:\n"
                for phone in phones:
                    order_message += f"  • {phone}\n"

        if contact.telegram_username:
            order_message += f"💬 Telegram: @{contact.telegram_username}\n"

        if contact.instagram_username:
            order_message += f"📷 Instagram: https://instagram.com/{contact.instagram_username}"
    else:
        order_message += "📱 Telefon: +998901234567\n💬 Telegram: @dunya_jewellery\n📷 Instagram: https://instagram.com/dunya_jewellery"

    # Add back button for better navigation
    reply_markup = get_client_back_keyboard()
    await query.edit_message_text(order_message, reply_markup=reply_markup, parse_mode='Markdown')

async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Back to main menu - clean navigation"""
    query = update.callback_query
    await query.answer()

    reply_markup = get_client_inline_keyboard()
    await query.edit_message_text(
        CLIENT_WELCOME,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )