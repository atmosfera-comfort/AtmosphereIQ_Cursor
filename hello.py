# -*- coding: utf-8 -*-
"""Приветствие менеджера AtmosphereIQ."""

import sys


def setup_utf8_console() -> None:
    """Настраивает UTF-8 для корректного отображения русского текста в консоли Windows."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")


def main() -> None:
    setup_utf8_console()

    name = input("Введите имя менеджера AtmosphereIQ: ").strip()
    print(f"Привет, {name}! Сегодня проверим новые заявки.")


if __name__ == "__main__":
    main()
