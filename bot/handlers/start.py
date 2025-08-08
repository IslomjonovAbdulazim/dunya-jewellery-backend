"""Start and help handlers - UNIFIED INTERFACE"""

from telegram import Update
from telegram.ext import ContextTypes

from ..utils import is_admin
from ..constants import *
from ..keyboards import get_client_inline_keyboard  # Same for both admin and client

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - SAME INTERFACE FOR BOTH"""
    user_id = update.effective_user.id

    if is_admin(user_id):
        # Admin sees same interface as client but gets admin functionality
        reply_markup = get_client_inline_keyboard()
        await update.message.reply_text(
            CLIENT_WELCOME,  # Same welcome message
            reply_markup=reply_markup,
            parse_mode='MarkdownV2'
        )
    else:
        # Client gets same interface
        reply_markup = get_client_inline_keyboard()
        await update.message.reply_text(
            CLIENT_WELCOME,
            reply_markup=reply_markup,
            parse_mode='MarkdownV2'
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    user_id = update.effective_user.id

    if is_admin(user_id):
        await update.message.reply_text(ADMIN_HELP, parse_mode='MarkdownV2')
    else:
        await update.message.reply_text(CLIENT_HELP, parse_mode='MarkdownV2')