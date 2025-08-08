"""Simple message handlers - NO SKIP, CLEAN"""

from telegram import Update
from telegram.ext import ContextTypes

from database import get_db_session
from models import Product, Contact
from ..keyboards import get_admin_nav_keyboard
from ..utils import is_admin, get_user_state, clear_user_state, parse_sizes
from ..constants import *

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages during workflows"""
    if not is_admin(update.effective_user.id):
        return

    user_id = update.effective_user.id
    state = get_user_state(user_id)

    if not state:
        return

    text = update.message.text

    # Handle product workflows (no /skip)
    if state['action'] in ['add', 'edit']:
        await handle_field_input(update, context, state, text)

    # Handle contact workflows
    elif state['action'] == 'edit_contact':
        from .contacts import handle_contact_field_edit
        await handle_contact_field_edit(update, context, state, text)

async def handle_field_input(update: Update, context: ContextTypes.DEFAULT_TYPE, state, text):
    """Handle field input during product creation/editing - NO SKIP"""
    if state['step'] == 'title':
        # Simple title validation
        if len(text.strip()) < 2:
            await update.message.reply_text("❌ Nom kamida 2 ta harf bo'lishi kerak!", parse_mode='Markdown')
            return
        state['title'] = text.strip()

    elif state['step'] == 'description':
        state['description'] = text.strip() if text.strip() else None

    elif state['step'] == 'sizes':
        sizes = parse_sizes(text)
        if sizes is None:
            await update.message.reply_text(INVALID_SIZE_FORMAT, parse_mode='Markdown')
            return
        state['sizes'] = sizes

    elif state['step'] == 'images' and text.lower() in ['tayyor', 'done', 'готово']:
        await save_product(update, context, state)
        return

    await move_to_next_step(update, context, state)

async def move_to_next_step(update: Update, context: ContextTypes.DEFAULT_TYPE, state):
    """Move to next step in product workflow"""
    if state['step'] == 'title':
        state['step'] = 'description'
        await send_description_prompt(update, context, state)
    elif state['step'] == 'description':
        state['step'] = 'sizes'
        await send_sizes_prompt(update, context, state)
    elif state['step'] == 'sizes':
        state['step'] = 'images'
        await send_images_prompt(update, context, state)

async def send_description_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE, state):
    """Send description prompt"""
    if state['action'] == 'edit':
        current_desc = state['current_product'].description or CURRENT_VALUE_NONE
        prompt = EDIT_DESCRIPTION_PROMPT.format(current_desc)
    else:
        prompt = ENTER_DESCRIPTION

    await update.message.reply_text(prompt, parse_mode='Markdown')

async def send_sizes_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE, state):
    """Send sizes prompt"""
    if state['action'] == 'edit':
        current_sizes = ", ".join([str(s) for s in state['current_product'].get_sizes_list()])
        current_sizes = current_sizes or CURRENT_VALUE_NONE
        prompt = EDIT_SIZES_PROMPT.format(current_sizes)
    else:
        prompt = ENTER_SIZES

    await update.message.reply_text(prompt, parse_mode='Markdown')

async def send_images_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE, state):
    """Send images prompt"""
    if state['action'] == 'edit':
        current_images = len(state['current_product'].get_file_ids_list())
        prompt = EDIT_IMAGES_PROMPT.format(current_images)
        # Start fresh for new image uploads (like phone numbers)
        state['images'] = []
        state['images_started'] = False
    else:
        state['images'] = []
        state['images_started'] = False
        prompt = ENTER_IMAGES

    await update.message.reply_text(prompt, parse_mode='Markdown')

async def save_product(update: Update, context: ContextTypes.DEFAULT_TYPE, state):
    """Save product to database"""
    db = get_db_session()
    user_id = update.effective_user.id

    try:
        if state['action'] == 'add':
            await create_new_product(update, context, state, db)
        elif state['action'] == 'edit':
            await update_existing_product(update, context, state, db)
    except Exception as e:
        await update.message.reply_text(ERROR_OCCURRED.format(str(e)), parse_mode='Markdown')
    finally:
        db.close()
        clear_user_state(user_id)

async def create_new_product(update: Update, context: ContextTypes.DEFAULT_TYPE, state, db):
    """Create new product"""
    if not state.get('title'):
        await update.message.reply_text("❌ Mahsulot nomi kiritilmagan!", parse_mode='Markdown')
        return

    product = Product(
        title=state['title'],
        description=state.get('description'),
        is_active=True
    )

    product.set_sizes(state.get('sizes', []))
    product.set_file_ids(state.get('images', []))

    db.add(product)
    db.commit()
    db.refresh(product)

    success_msg = PRODUCT_CREATED.format(product.title, product.id)
    await update.message.reply_text(success_msg, parse_mode='Markdown', reply_markup=get_admin_nav_keyboard())

async def update_existing_product(update: Update, context: ContextTypes.DEFAULT_TYPE, state, db):
    """Update existing product"""
    product = db.query(Product).filter(Product.id == state['product_id']).first()

    if not product:
        await update.message.reply_text(PRODUCT_NOT_FOUND, parse_mode='Markdown')
        return

    # Update product fields
    product.title = state['title']
    product.description = state.get('description')
    product.set_sizes(state.get('sizes', []))
    product.set_file_ids(state.get('images', []))  # COMPLETE REPLACEMENT

    db.commit()

    success_msg = PRODUCT_UPDATED.format(product.title)
    await update.message.reply_text(success_msg, parse_mode='Markdown', reply_markup=get_admin_nav_keyboard())

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo uploads - REPLACE OLD IMAGES"""
    if not is_admin(update.effective_user.id):
        return

    user_id = update.effective_user.id
    state = get_user_state(user_id)

    if not state or state.get('step') != 'images':
        return

    # Get highest resolution photo
    file_id = update.message.photo[-1].file_id

    # If this is the first photo, clear old images
    if not state.get('images_started', False):
        await update.message.reply_text(IMAGES_REPLACED, parse_mode='Markdown')
        state['images'] = []  # Clear old images
        state['images_started'] = True

    # Add new photo
    if 'images' not in state:
        state['images'] = []

    state['images'].append(file_id)
    count = len(state['images'])

    await update.message.reply_text(
        IMAGE_ADDED.format(count),
        parse_mode='Markdown'
    )