from telegram import Update
from telegram.ext import ContextTypes

from bot.texts import messages


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(messages.HELP)
