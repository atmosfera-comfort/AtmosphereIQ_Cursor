from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards.menus import CALLBACK_SERVICES
from bot.texts import messages


async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(messages.SERVICES)


async def services_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query.data != CALLBACK_SERVICES:
        return
    await query.answer()
    await query.message.reply_text(messages.SERVICES)
