# Telegram-бот AtmosphereIQ

Клиентский бот для приёма заявок, ответов про услуги и CO₂.

## Команды

| Команда | Описание |
|---------|----------|
| `/start` | Главное меню |
| `/services` | Услуги AtmosphereIQ |
| `/co2` | Объяснение CO₂ простыми словами |
| `/request` | Пошаговая заявка |
| `/contact` | Контакты |
| `/help` | Справка |
| `/cancel` | Отмена незавершённой заявки |

## Запуск

```bash
cd telegram-bot
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
py -3 main.py
```

Перед запуском укажите токен в `.env`:

```
TELEGRAM_BOT_TOKEN=ваш_токен
```

## Безопасность токена

- Токен хранится **только** в `.env` или переменных окружения сервера
- Файл `.env` добавлен в `.gitignore` и не коммитится
- В репозиторий можно класть только `.env.example` без значения
- Не вставляйте токен в код, README и логи
- Если токен мог утечь — перевыпустите его через [@BotFather](https://t.me/BotFather)

## Заявки

Заявки сохраняются локально в `data/leads.json` (файл в `.gitignore`).

## Структура

```
telegram-bot/
├── main.py              # точка входа
├── config.py            # загрузка токена
├── bot/
│   ├── handlers/        # обработчики команд
│   ├── keyboards/       # клавиатуры
│   ├── texts/           # тексты ответов
│   └── storage.py       # сохранение заявок
└── data/
    └── leads.json       # заявки (создаётся автоматически)
```
