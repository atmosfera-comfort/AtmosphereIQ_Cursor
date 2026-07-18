from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards.menus import (
    BTN_CO2,
    BTN_CONTACT,
    BTN_SERVICES,
    CALLBACK_CO2,
    CALLBACK_CONTACT,
    CALLBACK_SERVICES,
    main_menu_inline,
    main_menu_keyboard,
)
from bot.texts import messages


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        messages.START,
        reply_markup=main_menu_keyboard(),
    )
    await update.message.reply_text(
        "Быстрый выбор:",
        reply_markup=main_menu_inline(),
    )


async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == CALLBACK_SERVICES:
        await query.message.reply_text(messages.SERVICES)
    elif query.data == CALLBACK_CO2:
        await query.message.reply_text(messages.CO2)
    elif query.data == CALLBACK_CONTACT:
        await query.message.reply_text(messages.CONTACT)


async def fallback_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()

    if text == BTN_SERVICES:
        await update.message.reply_text(messages.SERVICES)
    elif text == BTN_CO2:
        await update.message.reply_text(messages.CO2)
    elif text == BTN_CONTACT:
        await update.message.reply_text(messages.CONTACT)
    else:
        await update.message.reply_text(messages.FALLBACK)
