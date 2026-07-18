from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards.menus import CALLBACK_CO2
from bot.texts import messages


async def co2_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(messages.CO2)


async def co2_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query.data != CALLBACK_CO2:
        return
    await query.answer()
    await query.message.reply_text(messages.CO2)
