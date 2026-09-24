#!/usr/bin/env python3
"""Таблица как на референсе: бесцветный фон, белые толстые столбцы, Soyuz Grotesk Bold."""

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color, black, white
from PIL import Image, ImageDraw, ImageFont

FONT_TTF = "/workspace/table-pdf/Soyuz_Grotesk_Bold.ttf"
FONT_OTF = "/workspace/table-pdf/Soyuz_Grotesk_Bold.otf"
OUT_PDF = "/workspace/table-pdf/table.pdf"
OUT_PNG = "/workspace/table-pdf/table_preview.png"

# Текст с референса; ответы в ячейках пустые — на скрине забелены толстым белым
HEADERS = ["2.", "Франция", "СССР/Россия", "Германия"]
ROWS = [
    ["Тренер", "", "", ""],
    ["Полководец", "", "", ""],
    ["Президент (руководитель)", "", "", ""],
]

# Пропорции исходной таблицы (границы x: 87,325,563,802,1040; y: 15,66,118,169,246)
COL_WS = [238, 238, 239, 238]
ROW_HS = [51, 52, 51, 77]
SCALE = 1.5
BORDER = 2.5  # толще, чем тонкие линии на скрине
COL_EDGE = 7  # белые толстые вертикали столбцов


def scaled(values):
    return [v * SCALE for v in values]


def build_pdf():
    pdfmetrics.registerFont(TTFont("SoyuzGrotesk", FONT_TTF))

    col_ws = scaled(COL_WS)
    row_hs = scaled(ROW_HS)
    table_w = sum(col_ws)
    table_h = sum(row_hs)
    margin = 24
    page_w = table_w + 2 * margin
    page_h = table_h + 2 * margin

    c = canvas.Canvas(OUT_PDF, pagesize=(page_w, page_h))
    # Бесцветный фон: страницу не заливаем

    x0 = margin
    y0 = margin

    # Белая заливка таблицы (толстые белые столбцы)
    c.setFillColor(white)
    c.rect(x0, y0, table_w, table_h, fill=1, stroke=0)

    # Белые толстые вертикали на стыках столбцов
    c.setStrokeColor(white)
    c.setLineWidth(COL_EDGE)
    x = x0
    for cw in col_ws[:-1]:
        x += cw
        c.line(x, y0, x, y0 + table_h)

    # Тёмная сетка поверх (как структура оригинала)
    line = Color(0.1, 0.1, 0.1)
    c.setStrokeColor(line)
    c.setLineWidth(BORDER)
    c.rect(x0, y0, table_w, table_h, fill=0, stroke=1)

    x = x0
    for cw in col_ws[:-1]:
        x += cw
        c.line(x, y0, x, y0 + table_h)

    y = y0 + table_h
    for rh in row_hs[:-1]:
        y -= rh
        c.line(x0, y, x0 + table_w, y)

    font_size = 16
    c.setFillColor(black)
    c.setFont("SoyuzGrotesk", font_size)
    pad_x = 12
    pad_top = 14

    y_top = y0 + table_h
    baseline = y_top - pad_top - font_size * 0.2
    x = x0
    for i, text in enumerate(HEADERS):
        c.drawString(x + pad_x, baseline, text)
        x += col_ws[i]

    y_top = y0 + table_h - row_hs[0]
    for r, row in enumerate(ROWS):
        x = x0
        for i, text in enumerate(row):
            if text:
                if r == 2 and i == 0:
                    c.drawString(x + pad_x, y_top - pad_top - font_size * 0.2, "Президент")
                    c.drawString(
                        x + pad_x,
                        y_top - pad_top - font_size * 0.2 - font_size * 1.2,
                        "(руководитель)",
                    )
                else:
                    c.drawString(x + pad_x, y_top - pad_top - font_size * 0.2, text)
            x += col_ws[i]
        y_top -= row_hs[r + 1]

    c.save()
    print(f"PDF: {OUT_PDF}")


def build_preview_png():
    col_ws = [int(v * SCALE) for v in COL_WS]
    row_hs = [int(v * SCALE) for v in ROW_HS]
    table_w = sum(col_ws)
    table_h = sum(row_hs)
    margin = 24
    W = table_w + 2 * margin
    H = table_h + 2 * margin

    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_OTF, 24)

    x0, y0 = margin, margin
    draw.rectangle(
        [x0, y0, x0 + table_w, y0 + table_h],
        fill=(255, 255, 255, 255),
        outline=(25, 25, 25, 255),
        width=3,
    )

    x = x0
    for cw in col_ws[:-1]:
        x += cw
        draw.line([(x, y0), (x, y0 + table_h)], fill=(255, 255, 255, 255), width=COL_EDGE)
        draw.line([(x, y0), (x, y0 + table_h)], fill=(25, 25, 25, 255), width=3)

    y = y0
    for rh in row_hs[:-1]:
        y += rh
        draw.line([(x0, y), (x0 + table_w, y)], fill=(25, 25, 25, 255), width=3)

    pad_x, pad_top = 12, 10

    def put(text, tx, ty):
        draw.text((tx, ty), text, font=font, fill=(0, 0, 0, 255))

    x = x0
    for i, text in enumerate(HEADERS):
        put(text, x + pad_x, y0 + pad_top)
        x += col_ws[i]

    y = y0 + row_hs[0]
    for r, row in enumerate(ROWS):
        x = x0
        for i, text in enumerate(row):
            if text:
                if r == 2 and i == 0:
                    put("Президент", x + pad_x, y + pad_top)
                    put("(руководитель)", x + pad_x, y + pad_top + 28)
                else:
                    put(text, x + pad_x, y + pad_top)
            x += col_ws[i]
        y += row_hs[r + 1]

    img.save(OUT_PNG)
    print(f"PNG: {OUT_PNG}")


if __name__ == "__main__":
    build_pdf()
    build_preview_png()
