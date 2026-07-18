from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

BTN_SERVICES = "Услуги"
BTN_CO2 = "Что такое CO₂"
BTN_REQUEST = "Оставить заявку"
BTN_CONTACT = "Контакты"

CALLBACK_SERVICES = "menu:services"
CALLBACK_CO2 = "menu:co2"
CALLBACK_REQUEST = "menu:request"
CALLBACK_CONTACT = "menu:contact"

OBJECT_APARTMENT = "Квартира / дом"
OBJECT_OFFICE = "Офис"
OBJECT_INSTITUTION = "Школа / клиника"
OBJECT_OTHER = "Другое"

CONFIRM_YES = "Да, отправить"
CONFIRM_NO = "Нет, отменить"


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(BTN_SERVICES), KeyboardButton(BTN_CO2)],
            [KeyboardButton(BTN_REQUEST), KeyboardButton(BTN_CONTACT)],
        ],
        resize_keyboard=True,
    )


def main_menu_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(BTN_SERVICES, callback_data=CALLBACK_SERVICES),
                InlineKeyboardButton(BTN_CO2, callback_data=CALLBACK_CO2),
            ],
            [
                InlineKeyboardButton(BTN_REQUEST, callback_data=CALLBACK_REQUEST),
                InlineKeyboardButton(BTN_CONTACT, callback_data=CALLBACK_CONTACT),
            ],
        ]
    )


def object_type_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(OBJECT_APARTMENT), KeyboardButton(OBJECT_OFFICE)],
            [KeyboardButton(OBJECT_INSTITUTION), KeyboardButton(OBJECT_OTHER)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def confirm_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton(CONFIRM_YES), KeyboardButton(CONFIRM_NO)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
