"""Simple message handlers"""

from telegram import Update
from telegram.ext import ContextTypes

from database import get_db_session
from models import Product, Contact
from ..utils import is_admin, get_user_state, clear_user_state, parse_sizes
from ..constants import *
from .admin import show_admin_products
from .contacts import show_admin_contact

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages during workflows"""
    if not is_admin(update.effective_user.id):
        return

    user_id = update.effective_user.id
    state = get_user_state(user_id)

    if not state:
        return

    text = update.message.text

    # Handle product workflows
    if state['action'] in ['add', 'edit']:
        if text == '/skip' and state['action'] == 'edit':
            await handle_skip_field(update, context, state)
            await move_to_next_step(update, context, state)
        else:
            await handle_field_input(update, context, state, text)

    # Handle contact workflows
    elif state['action'] == 'edit_contact':
        # Import here to avoid circular import
        from .contacts import handle_contact_field_edit
        await handle_contact_field_edit(update, context, state, text)
        # DON'T clear user state here - let the contact handler decide

async def handle_skip_field(update: Update, context: ContextTypes.DEFAULT_TYPE, state):
    """Handle skipping field during editing"""
    if state['step'] == 'title':
        state['title'] = state['current_product'].title
        await update.message.reply_text(f"✅ Nom o'zgartirilmadi: {state['title']}")
    elif state['step'] == 'description':
        state['description'] = state['current_product'].description
        current_desc = state['description'] or "Tavsif yo'q"
        await update.message.reply_text(f"✅ Tavsif o'zgartirilmadi: {current_desc}")
    elif state['step'] == 'sizes':
        state['sizes'] = state['current_product'].get_sizes_list()
        current_sizes = ", ".join([str(s) for s in state['sizes']]) if state['sizes'] else "O'lcham yo'q"
        await update.message.reply_text(f"✅ O'lchamlar o'zgartirilmadi: {current_sizes}")

async def handle_field_input(update: Update, context: ContextTypes.DEFAULT_TYPE, state, text):
    """Handle field input during product creation/editing"""
    if state['step'] == 'title':
        state['title'] = text
    elif state['step'] == 'description':
        state['description'] = text
    elif state['step'] == 'sizes':
        sizes = parse_sizes(text)
        if sizes is None:
            await update.message.reply_text(INVALID_SIZE_FORMAT)
            return
        state['sizes'] = sizes
    elif state['step'] == 'images' and text.lower() in ['tayyor', 'done']:
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

    await update.message.reply_text(prompt)

async def send_images_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE, state):
    """Send images prompt"""
    if state['action'] == 'edit':
        state['images'] = state['current_product'].get_file_ids_list()
        current_images = len(state['images'])
        prompt = EDIT_IMAGES_PROMPT.format(current_images)
    else:
        state['images'] = []
        prompt = ENTER_IMAGES

    await update.message.reply_text(prompt)

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
        await update.message.reply_text(ERROR_OCCURRED.format(str(e)))
    finally:
        db.close()
        clear_user_state(user_id)

async def create_new_product(update: Update, context: ContextTypes.DEFAULT_TYPE, state, db):
    """Create new product"""
    product = Product(
        title=state['title'],
        description=state['description'],
        is_active=True
    )
    product.set_sizes(state.get('sizes', []))
    product.set_file_ids(state.get('images', []))

    db.add(product)
    db.commit()
    db.refresh(product)

    await update.message.reply_text(
        PRODUCT_CREATED.format(product.title, product.id)
    )

async def update_existing_product(update: Update, context: ContextTypes.DEFAULT_TYPE, state, db):
    """Update existing product"""
    product = db.query(Product).filter(Product.id == state['product_id']).first()

    if not product:
        await update.message.reply_text(PRODUCT_NOT_FOUND)
        return

    product.title = state['title']
    product.description = state['description']
    product.set_sizes(state.get('sizes', []))
    product.set_file_ids(state.get('images', []))

    db.commit()
    await update.message.reply_text(PRODUCT_UPDATED.format(product.title))

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo uploads"""
    if not is_admin(update.effective_user.id):
        return

    user_id = update.effective_user.id
    state = get_user_state(user_id)

    if not state or state.get('step') != 'images':
        return

    # Get highest resolution photo
    file_id = update.message.photo[-1].file_id

    if 'images' not in state:
        state['images'] = []

    state['images'].append(file_id)

    await update.message.reply_text(
        IMAGE_ADDED.format(len(state['images']))
    )

async def handle_keyboard_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle keyboard button presses"""
    if not is_admin(update.effective_user.id):
        return

    text = update.message.text

    if text == BTN_ADMIN_PRODUCTS:
        await show_admin_products(update, context)
    elif text == BTN_ADMIN_CONTACT:
        await show_admin_contact(update, context)