import asyncio
import sys

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot.handlers.co2 import co2_command
from bot.handlers.contact import contact_command
from bot.handlers.help import help_command
from bot.handlers.lead import get_lead_handler
from bot.handlers.services import services_command
from bot.handlers.start import fallback_message, start_callback, start_command
from config import TOKEN


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(
        [
            ("start", "Главное меню"),
            ("services", "Наши услуги"),
            ("co2", "Что такое CO₂"),
            ("request", "Оставить заявку"),
            ("contact", "Контакты"),
            ("help", "Справка"),
            ("cancel", "Отменить заявку"),
        ]
    )


def main() -> None:
    application = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init)
        .build()
    )

    application.add_handler(get_lead_handler())
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("services", services_command))
    application.add_handler(CommandHandler("co2", co2_command))
    application.add_handler(CommandHandler("contact", contact_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        CallbackQueryHandler(start_callback, pattern=r"^menu:")
    )
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, fallback_message)
    )

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    if sys.version_info >= (3, 14):
        asyncio.set_event_loop(asyncio.new_event_loop())
    main()
