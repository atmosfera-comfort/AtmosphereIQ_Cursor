#!/usr/bin/env python3
"""UGC Influencers — 7-slide PDF presentation (Swiss / lemon-yellow style)."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT_PDF = ROOT / "UGC_inflyuensery.pdf"
ARTIFACT = Path("/opt/cursor/artifacts/UGC_inflyuensery.pdf")

# 16:9 slide
W, H = 1280, 720

YELLOW = HexColor("#F2FF00")
YELLOW_SOFT = HexColor("#FFF56A")
BLACK = HexColor("#0A0A0A")
GRAY = HexColor("#6B6B6B")
GRAY_LIGHT = HexColor("#F2F2F2")
GRAY_MID = HexColor("#E6E6E6")
GRAY_DARK = HexColor("#2A2A2A")
WHITE = white

FONT_REG = "Inter"
FONT_MED = "InterMed"
FONT_BOLD = "InterBold"


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont(FONT_REG, "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"))
    pdfmetrics.registerFont(TTFont(FONT_MED, "/usr/share/fonts/truetype/macos/Inter-Medium.ttf"))
    pdfmetrics.registerFont(TTFont(FONT_BOLD, "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"))


def rounded_rect(c: canvas.Canvas, x, y, w, h, r, fill=None, stroke=None, sw=0):
    c.saveState()
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(sw)
    op = 1 if fill is not None else 0
    if stroke is not None:
        op = 1 if fill is not None else 0
        c.roundRect(x, y, w, h, r, stroke=1 if stroke is not None else 0, fill=1 if fill is not None else 0)
    else:
        c.roundRect(x, y, w, h, r, stroke=0, fill=1 if fill is not None else 0)
    c.restoreState()


def draw_star(c: canvas.Canvas, x, y, size=14, color=YELLOW):
    """Simple 8-point asterisk-like star."""
    c.saveState()
    c.setFillColor(color)
    c.setStrokeColor(color)
    c.setLineWidth(2.2)
    c.setLineCap(1)
    for angle in range(0, 180, 45):
        c.saveState()
        c.translate(x, y)
        c.rotate(angle)
        c.line(0, -size, 0, size)
        c.restoreState()
    c.restoreState()


def draw_header(c: canvas.Canvas, page_label: str = "UGC Influencers"):
    y = H - 36
    c.setFillColor(BLACK)
    c.setFont(FONT_MED, 10)
    c.drawString(48, y, "@ATMOSPHEREIQ")
    c.setFillColor(GRAY)
    c.setFont(FONT_REG, 10)
    c.drawCentredString(W * 0.38, y, "15 сентября 2026")
    c.drawCentredString(W * 0.62, y, page_label)
    c.setFillColor(BLACK)
    c.setFont(FONT_MED, 10)
    c.drawRightString(W - 48, y, "2026")
    # thin rule
    c.setStrokeColor(GRAY_MID)
    c.setLineWidth(0.8)
    c.line(48, y - 14, W - 48, y - 14)


def wrap_text(c: canvas.Canvas, text: str, font: str, size: float, max_width: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if c.stringWidth(trial, font, size) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_paragraph(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    max_width: float,
    font: str = FONT_REG,
    size: float = 12,
    leading: float = 18,
    color=GRAY_DARK,
    max_lines: int | None = None,
) -> float:
    c.setFillColor(color)
    c.setFont(font, size)
    lines = wrap_text(c, text, font, size, max_width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for i, line in enumerate(lines):
        c.drawString(x, y - i * leading, line)
    return y - len(lines) * leading


def clip_round_image(c: canvas.Canvas, path: Path, x, y, w, h, r=28):
    """Draw image covering the rounded frame (object-fit: cover)."""
    c.saveState()
    p = c.beginPath()
    p.roundRect(x, y, w, h, r)
    c.clipPath(p, stroke=0, fill=0)
    img = ImageReader(str(path))
    iw, ih = img.getSize()
    scale = max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(img, x + (w - dw) / 2, y + (h - dh) / 2, width=dw, height=dh, mask="auto")
    c.restoreState()


def slide_title(c: canvas.Canvas):
    draw_header(c, "Презентация")

    # left stats cluster
    c.setFillColor(BLACK)
    c.setFont(FONT_BOLD, 42)
    c.drawString(48, H - 160, "72%")
    c.setFont(FONT_REG, 13)
    c.setFillColor(GRAY)
    draw_paragraph(
        c,
        "покупателей доверяют UGC больше, чем классической рекламе бренда",
        48,
        H - 190,
        280,
        size=12,
        leading=16,
        color=GRAY,
    )

    c.setFillColor(BLACK)
    c.setFont(FONT_BOLD, 28)
    c.drawString(48, H - 300, "UGC = доверие")
    draw_star(c, 250, H - 292, size=10)

    # massive title on the right
    c.setFillColor(BLACK)
    c.setFont(FONT_BOLD, 78)
    c.drawRightString(W - 48, H - 220, "UGC")
    c.drawRightString(W - 48, H - 300, "инфлюенсеры")

    # yellow accent pill
    rounded_rect(c, W - 260, H - 360, 212, 36, 18, fill=YELLOW)
    c.setFillColor(BLACK)
    c.setFont(FONT_MED, 12)
    c.drawCentredString(W - 154, H - 348, "контент · доверие · рост")

    # bottom black textured band
    clip_round_image(c, ASSETS / "tex_waves.jpg", 48, 48, W - 96, 200, r=36)
    # dark overlay for readability
    c.setFillColor(Color(0, 0, 0, alpha=0.45))
    c.roundRect(48, 48, W - 96, 200, 36, stroke=0, fill=1)

    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 22)
    c.drawString(80, 180, "Что внутри")
    draw_star(c, 230, 188, size=8, color=YELLOW)

    items = [
        ("01", "Определение"),
        ("02", "Макро и микро"),
        ("03", "Монетизация"),
        ("04", "Примеры"),
        ("05", "Площадки"),
    ]
    x0 = 80
    step = 220
    for i, (num, label) in enumerate(items):
        x = x0 + i * step
        c.setFillColor(YELLOW)
        c.setFont(FONT_BOLD, 11)
        c.drawString(x, 130, num)
        c.setFillColor(WHITE)
        c.setFont(FONT_REG, 13)
        c.drawString(x + 28, 130, label)

    c.setFillColor(GRAY_MID)
    c.setFont(FONT_REG, 11)
    c.drawString(80, 78, "Краткий гид по работе с UGC-инфлюенсерами")


def slide_definition(c: canvas.Canvas):
    draw_header(c, "Определение")

    # left image
    clip_round_image(c, ASSETS / "tex_sphere.jpg", 48, 100, 420, 500, r=40)

    # yellow year/keyword badge
    rounded_rect(c, 78, 130, 110, 40, 20, fill=YELLOW)
    c.setFillColor(BLACK)
    c.setFont(FONT_BOLD, 14)
    c.drawCentredString(133, 144, "UGC")

    # right content
    c.setFillColor(BLACK)
    c.setFont(FONT_BOLD, 48)
    c.drawString(520, H - 170, "Что такое")
    c.drawString(520, H - 230, "UGC-инфлюенсер")

    draw_paragraph(
        c,
        "UGC (User-Generated Content) — контент, который создают обычные люди "
        "и авторы, а не рекламный отдел бренда: обзоры, сторис, распаковки, отзывы.",
        520,
        H - 290,
        700,
        size=14,
        leading=22,
        color=GRAY_DARK,
    )

    # two columns
    col_w = 330
    left_x, right_x = 520, 870
    y0 = 320

    rounded_rect(c, left_x - 16, y0 - 150, col_w, 200, 24, fill=GRAY_LIGHT)
    rounded_rect(c, right_x - 16, y0 - 150, col_w, 200, 24, fill=YELLOW)

    c.setFillColor(BLACK)
    c.setFont(FONT_BOLD, 16)
    c.drawString(left_x, y0 + 20, "Суть формата")
    draw_paragraph(
        c,
        "Инфлюенсер показывает продукт «своим голосом»: без студийного глянца, "
        "ближе к реальному опыту аудитории.",
        left_x,
        y0 - 10,
        col_w - 40,
        size=12,
        leading=17,
        color=GRAY_DARK,
    )

    c.setFont(FONT_BOLD, 16)
    c.drawString(right_x, y0 + 20, "Зачем бренду")
    draw_paragraph(
        c,
        "Растёт доверие, охваты и вовлечённость. Аудитория чаще сохраняет "
        "и пересылает такой контент друзьям.",
        right_x,
        y0 - 10,
        col_w - 40,
        size=12,
        leading=17,
        color=BLACK,
    )

    c.setFillColor(GRAY)
    c.setFont(FONT_REG, 11)
    c.drawString(520, 70, "Коротко: не «реклама про бренд», а «история человека о продукте».")


def slide_types(c: canvas.Canvas):
    draw_header(c, "Виды инфлюенсеров")

    c.setFillColor(BLACK)
    c.setFont(FONT_BOLD, 44)
    c.drawString(48, H - 130, "Макро и микро")
    draw_paragraph(
        c,
        "Выбор зависит от цели: охват или глубокое доверие ниши.",
        48,
        H - 170,
        700,
        size=14,
        leading=20,
        color=GRAY,
    )

    # four pillars inspired by reference — focus on macro/micro + nano/mega context
    cards = [
        {
            "bg": YELLOW,
            "num": "01",
            "title": "Микро",
            "range": "10K–100K",
            "text": "Высокий engagement, близкий контакт с аудиторией, доступные интеграции.",
            "fg": BLACK,
        },
        {
            "bg": BLACK,
            "num": "02",
            "title": "Макро",
            "range": "100K–1M",
            "text": "Широкий охват и узнаваемость. Подходит для запусков и имиджа бренда.",
            "fg": WHITE,
        },
        {
            "bg": GRAY_LIGHT,
            "num": "03",
            "title": "Нано",
            "range": "1K–10K",
            "text": "Максимум доверия в узкой нише. Часто лучший ROI для локальных кампаний.",
            "fg": BLACK,
        },
        {
            "bg": GRAY_DARK,
            "num": "04",
            "title": "Мега",
            "range": "1M+",
            "text": "Звёздный статус и вирусный потенциал. Бюджет выше, контроль сложнее.",
            "fg": WHITE,
        },
    ]

    gap = 20
    card_w = (W - 96 - 3 * gap) / 4
    card_h = 420
    y = 70

    for i, card in enumerate(cards):
        x = 48 + i * (card_w + gap)
        rounded_rect(c, x, y, card_w, card_h, 28, fill=card["bg"])

        c.setFillColor(card["fg"])
        c.setFont(FONT_BOLD, 22)
        c.drawString(x + 24, y + card_h - 50, card["title"])

        # accent badge
        badge_bg = BLACK if card["bg"] == YELLOW else (YELLOW if card["bg"] in (BLACK, GRAY_DARK) else BLACK)
        badge_fg = YELLOW if badge_bg == BLACK else BLACK
        rounded_rect(c, x + 24, y + card_h - 100, 100, 28, 14, fill=badge_bg)
        c.setFillColor(badge_fg)
        c.setFont(FONT_MED, 11)
        c.drawCentredString(x + 74, y + card_h - 90, card["range"])

        draw_paragraph(
            c,
            card["text"],
            x + 24,
            y + card_h - 140,
            card_w - 48,
            size=13,
            leading=18,
            color=card["fg"],
        )

        c.setFillColor(card["fg"])
        c.setFont(FONT_BOLD, 48)
        c.drawString(x + 24, y + 36, card["num"])


def slide_monetization(c: canvas.Canvas):
    draw_header(c, "Монетизация")

    # left dark column with stacked cards
    rounded_rect(c, 48, 60, 460, 580, 36, fill=BLACK)

    methods = [
        ("01", "Партнёрства с брендами", "Фикс или бартер за интеграцию в Reels / Shorts / посты."),
        ("02", "Аффилиат и промокоды", "Процент с продаж по уникальной ссылке или коду."),
        ("03", "Собственные продукты", "Мерч, гайды, курсы, подписки на закрытый контент."),
        ("04", "UGC-услуги агентствам", "Съёмка контента «под ключ» без обязательной публикации у себя."),
    ]

    for i, (num, title, desc) in enumerate(methods):
        y = 560 - i * 120
        bg = YELLOW if i == 1 else GRAY_DARK
        fg = BLACK if i == 1 else WHITE
        rounded_rect(c, 72, y - 70, 412, 100, 22, fill=bg)
        c.setFillColor(fg)
        c.setFont(FONT_BOLD, 12)
        c.drawString(92, y + 5, num)
        c.setFont(FONT_BOLD, 15)
        c.drawString(130, y + 5, title)
        draw_paragraph(c, desc, 92, y - 25, 370, size=11, leading=15, color=fg)

    # right side
    c.setFillColor(BLACK)
    c.setFont(FONT_BOLD, 48)
    c.drawString(560, H - 160, "Как зарабатывают")
    c.drawString(560, H - 220, "инфлюенсеры")

    draw_paragraph(
        c,
        "Модель дохода строится вокруг внимания аудитории: чем выше доверие, "
        "тем дороже интеграция и стабильнее повторные сделки с брендами.",
        560,
        H - 280,
        660,
        size=14,
        leading=22,
        color=GRAY_DARK,
    )

    # tip cards
    rounded_rect(c, 560, 120, 300, 160, 24, fill=GRAY_LIGHT)
    rounded_rect(c, 880, 120, 340, 160, 24, fill=YELLOW)

    c.setFillColor(BLACK)
    c.setFont(FONT_BOLD, 14)
    c.drawString(584, 240, "Для бренда")
    draw_paragraph(
        c,
        "Сравнивайте не только цену, но и ER, качество UGC и соответствие нише.",
        584,
        210,
        250,
        size=12,
        leading=16,
        color=GRAY_DARK,
    )

    c.setFont(FONT_BOLD, 14)
    c.drawString(904, 240, "Для автора")
    draw_paragraph(
        c,
        "Микс форматов снижает риск: бартер + аффилиат + платные съёмки.",
        904,
        210,
        290,
        size=12,
        leading=16,
        color=BLACK,
    )


def slide_examples(c: canvas.Canvas):
    draw_header(c, "Примеры")

    c.setFillColor(BLACK)
    c.setFont(FONT_BOLD, 48)
    c.drawString(48, H - 140, "Примеры")
    c.drawString(48, H - 200, "инфлюенсеров")

    draw_paragraph(
        c,
        "Два узнаваемых формата UGC-авторов: beauty-микро и lifestyle-макро.",
        48,
        H - 250,
        520,
        size=14,
        leading=20,
        color=GRAY,
    )

    # Example frames — vertical “phone” panels
    clip_round_image(c, ASSETS / "tex_ribs.jpg", 560, 80, 300, 540, r=40)
    rounded_rect(c, 590, 470, 210, 78, 20, fill=YELLOW)
    c.setFillColor(BLACK)
    c.setFont(FONT_BOLD, 14)
    c.drawString(610, 515, "Пример 01")
    c.setFont(FONT_MED, 12)
    c.drawString(610, 492, "Микро · Beauty")

    clip_round_image(c, ASSETS / "tex_sphere.jpg", 900, 80, 300, 540, r=40)
    rounded_rect(c, 930, 470, 210, 78, 20, fill=WHITE)
    c.setFillColor(BLACK)
    c.setFont(FONT_BOLD, 14)
    c.drawString(950, 515, "Пример 02")
    c.setFont(FONT_MED, 12)
    c.drawString(950, 492, "Макро · Lifestyle")

    # left detail cards
    rounded_rect(c, 48, 280, 470, 150, 24, fill=GRAY_LIGHT)
    c.setFillColor(BLACK)
    c.setFont(FONT_BOLD, 18)
    c.drawString(72, 390, "Аня · beauty UGC")
    draw_paragraph(
        c,
        "≈ 45K в Instagram. Распаковки, «до/после», честные отзывы. "
        "Сильная сторона — высокий ER и сохраняемость Reels.",
        72,
        360,
        420,
        size=12,
        leading=17,
        color=GRAY_DARK,
    )

    rounded_rect(c, 48, 90, 470, 160, 24, fill=BLACK)
    c.setFillColor(YELLOW)
    c.setFont(FONT_BOLD, 18)
    c.drawString(72, 210, "Макс · lifestyle")
    draw_paragraph(
        c,
        "≈ 320K в TikTok / YouTube Shorts. День-из-жизни, гаджеты, путешествия. "
        "Даёт охват и узнаваемость бренда на широкую аудиторию.",
        72,
        180,
        420,
        size=12,
        leading=17,
        color=WHITE,
    )


def slide_platforms(c: canvas.Canvas):
    draw_header(c, "Площадки")

    clip_round_image(c, ASSETS / "tex_noise.jpg", 48, H - 320, 720, 220, r=32)

    c.setFillColor(BLACK)
    c.setFont(FONT_BOLD, 48)
    c.drawString(48, 280, "Где размещают")
    c.drawString(48, 220, "рекламу")

    draw_paragraph(
        c,
        "Площадку выбирают под формат контента и привычки аудитории.",
        48,
        170,
        500,
        size=14,
        leading=20,
        color=GRAY,
    )

    platforms = [
        ("TikTok", "Короткие ролики, тренды, вирусный охват", YELLOW, BLACK),
        ("Instagram", "Reels, Stories, карусели, Telegram-переходы", GRAY_LIGHT, BLACK),
        ("YouTube", "Shorts и длинные обзоры с глубоким доверием", BLACK, WHITE),
        ("Telegram", "Каналы и боты: прогрев и повторные касания", GRAY_DARK, WHITE),
    ]

    for i, (name, desc, bg, fg) in enumerate(platforms):
        row = i // 2
        col = i % 2
        x = 800 + col * 220
        y = 420 - row * 170
        rounded_rect(c, x, y, 200, 150, 24, fill=bg)
        c.setFillColor(fg)
        c.setFont(FONT_BOLD, 18)
        c.drawString(x + 20, y + 100, name)
        draw_paragraph(c, desc, x + 20, y + 70, 160, size=11, leading=15, color=fg)

    # bottom accent
    rounded_rect(c, 48, 60, 280, 44, 22, fill=YELLOW)
    c.setFillColor(BLACK)
    c.setFont(FONT_MED, 12)
    c.drawCentredString(188, 76, "Омниканал = сильнее эффект")


def slide_conclusion(c: canvas.Canvas):
    draw_header(c, "Вывод")

    # top two cards
    rounded_rect(c, 48, H - 280, 560, 180, 28, fill=YELLOW)
    clip_round_image(c, ASSETS / "tex_waves.jpg", 640, H - 280, 592, 180, r=28)

    c.setFillColor(BLACK)
    c.setFont(FONT_BOLD, 22)
    c.drawString(80, H - 150, "Главный вывод")
    draw_paragraph(
        c,
        "UGC-инфлюенсеры продают не «картинку», а доверие. "
        "Микро — для конверсии, макро — для охвата.",
        80,
        H - 190,
        500,
        size=13,
        leading=18,
        color=BLACK,
    )

    c.setFillColor(BLACK)
    c.setFont(FONT_BOLD, 56)
    c.drawCentredString(W / 2, 300, "Начните с ниши,")
    c.drawCentredString(W / 2, 230, "а не с охватов")

    draw_paragraph(
        c,
        "Выберите площадку под аудиторию, сравните ER и качество контента, "
        "зафиксируйте KPI: охват, сохранения, переходы, продажи по промокоду.",
        W / 2 - 360,
        160,
        720,
        size=14,
        leading=20,
        color=GRAY_DARK,
    )

    # CTA
    rounded_rect(c, W / 2 - 180, 70, 360, 48, 24, fill=BLACK)
    c.setFillColor(YELLOW)
    c.setFont(FONT_BOLD, 14)
    c.drawCentredString(W / 2, 88, "Следующий шаг: пилот с 2–3 микроавторами")


def build() -> Path:
    register_fonts()
    c = canvas.Canvas(str(OUT_PDF), pagesize=(W, H))
    c.setTitle("UGC инфлюенсеры")
    c.setAuthor("AtmosphereIQ")
    c.setSubject("Презентация: UGC-инфлюенсеры")
    slides = [
        slide_title,
        slide_definition,
        slide_types,
        slide_monetization,
        slide_examples,
        slide_platforms,
        slide_conclusion,
    ]
    for i, fn in enumerate(slides):
        fn(c)
        c.showPage()
    c.save()

    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_bytes(OUT_PDF.read_bytes())
    print(f"PDF: {OUT_PDF}")
    print(f"Artifact: {ARTIFACT}")
    return OUT_PDF


if __name__ == "__main__":
    build()
