from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards.menus import CALLBACK_CONTACT
from bot.texts import messages


async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(messages.CONTACT)


async def contact_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query.data != CALLBACK_CONTACT:
        return
    await query.answer()
    await query.message.reply_text(messages.CONTACT)
