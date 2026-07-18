import re

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from bot.keyboards.menus import (
    BTN_REQUEST,
    CALLBACK_REQUEST,
    CONFIRM_NO,
    CONFIRM_YES,
    OBJECT_APARTMENT,
    OBJECT_INSTITUTION,
    OBJECT_OFFICE,
    OBJECT_OTHER,
    confirm_keyboard,
    main_menu_keyboard,
    object_type_keyboard,
)
from bot.storage import save_lead
from bot.texts import messages

NAME, PHONE, OBJECT_TYPE, COMMENT, CONFIRM = range(5)

PHONE_PATTERN = re.compile(r"^(\+7|8)\d{10}$")
OBJECT_TYPES = {
    OBJECT_APARTMENT,
    OBJECT_OFFICE,
    OBJECT_INSTITUTION,
    OBJECT_OTHER,
}


def _clear_lead_data(context: ContextTypes.DEFAULT_TYPE) -> None:
    for key in ("name", "phone", "object_type", "comment"):
        context.user_data.pop(key, None)


async def request_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _clear_lead_data(context)
    await update.message.reply_text(messages.LEAD_START)
    return NAME


async def request_start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    _clear_lead_data(context)
    await query.message.reply_text(messages.LEAD_START)
    return NAME


async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    name = update.message.text.strip()
    if not name:
        await update.message.reply_text("Пожалуйста, напишите, как к вам обращаться.")
        return NAME

    context.user_data["name"] = name
    await update.message.reply_text(messages.LEAD_PHONE)
    return PHONE


async def receive_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    phone = re.sub(r"[\s\-()]", "", update.message.text.strip())
    if not PHONE_PATTERN.match(phone):
        await update.message.reply_text(messages.LEAD_INVALID_PHONE)
        return PHONE

    context.user_data["phone"] = phone
    await update.message.reply_text(
        messages.LEAD_OBJECT_TYPE,
        reply_markup=object_type_keyboard(),
    )
    return OBJECT_TYPE


async def receive_object_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    object_type = update.message.text.strip()
    if object_type not in OBJECT_TYPES:
        await update.message.reply_text(
            "Выберите тип объекта с помощью кнопок ниже.",
            reply_markup=object_type_keyboard(),
        )
        return OBJECT_TYPE

    context.user_data["object_type"] = object_type
    await update.message.reply_text(
        messages.LEAD_COMMENT,
        reply_markup=main_menu_keyboard(),
    )
    return COMMENT


async def receive_comment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    comment = update.message.text.strip()
    if comment.lower() == "пропустить":
        comment = "—"

    context.user_data["comment"] = comment
    summary = messages.LEAD_CONFIRM.format(
        name=context.user_data["name"],
        phone=context.user_data["phone"],
        object_type=context.user_data["object_type"],
        comment=comment,
    )
    await update.message.reply_text(summary, reply_markup=confirm_keyboard())
    return CONFIRM


async def receive_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answer = update.message.text.strip()
    if answer == CONFIRM_NO:
        _clear_lead_data(context)
        await update.message.reply_text(
            messages.LEAD_CANCELLED,
            reply_markup=main_menu_keyboard(),
        )
        return ConversationHandler.END

    if answer != CONFIRM_YES:
        await update.message.reply_text(
            "Нажмите «Да, отправить» или «Нет, отменить».",
            reply_markup=confirm_keyboard(),
        )
        return CONFIRM

    user = update.effective_user
    save_lead(
        {
            "telegram_user_id": user.id,
            "username": user.username,
            "name": context.user_data["name"],
            "phone": context.user_data["phone"],
            "object_type": context.user_data["object_type"],
            "comment": context.user_data["comment"],
        }
    )
    _clear_lead_data(context)
    await update.message.reply_text(
        messages.LEAD_SAVED,
        reply_markup=main_menu_keyboard(),
    )
    return ConversationHandler.END


async def cancel_lead(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _clear_lead_data(context)
    await update.message.reply_text(
        messages.LEAD_CANCELLED,
        reply_markup=main_menu_keyboard(),
    )
    return ConversationHandler.END


def get_lead_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            CommandHandler("request", request_start),
            MessageHandler(filters.Regex(f"^{re.escape(BTN_REQUEST)}$"), request_start),
            CallbackQueryHandler(request_start_callback, pattern=f"^{CALLBACK_REQUEST}$"),
        ],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_phone)],
            OBJECT_TYPE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_object_type)
            ],
            COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_comment)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel_lead)],
        allow_reentry=True,
    )
