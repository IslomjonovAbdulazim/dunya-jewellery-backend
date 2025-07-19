"""Start and help handlers"""

from telegram import Update
from telegram.ext import ContextTypes

from ..utils import is_admin
from ..constants import *
from ..keyboards import get_admin_reply_keyboard, get_client_inline_keyboard

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user_id = update.effective_user.id

    if is_admin(user_id):
        # Admin gets reply keyboard
        reply_markup = get_admin_reply_keyboard()
        await update.message.reply_text(
            ADMIN_WELCOME,
            reply_markup=reply_markup
        )
    else:
        # Client gets inline keyboard
        reply_markup = get_client_inline_keyboard()
        await update.message.reply_text(
            CLIENT_WELCOME,
            reply_markup=reply_markup
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    user_id = update.effective_user.id

    if is_admin(user_id):
        await update.message.reply_text(ADMIN_HELP)
    else:
        await update.message.reply_text(CLIENT_HELP)