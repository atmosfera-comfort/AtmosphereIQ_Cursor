#!/usr/bin/env python3
"""PDF: Professional English in Use Marketing, p.23 (exercises 8.1–8.3)."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import Color, black, white, HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from PIL import Image, ImageDraw, ImageFont
import os

OUT_PDF = "/workspace/textbook-pdf/page23.pdf"
OUT_PNG = "/workspace/textbook-pdf/page23_preview.png"

TEAL = HexColor("#1a5f6e")
LIGHTBULB_YELLOW = HexColor("#f5d76e")
BOX_BORDER = HexColor("#222222")
DOTS = "………"


def wrap_draw(c, text, x, y, max_width, font="Times-Roman", size=10, leading=13, color=black):
    """Draw word-wrapped text; returns y after last line."""
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if c.stringWidth(trial, font, size) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for i, line in enumerate(lines):
        c.drawString(x, y - i * leading, line)
    return y - (len(lines) - 1) * leading - leading


def draw_page(c, W, H):
    # Colorless page — no background fill
    margin_l = 18 * mm
    margin_r = 18 * mm
    margin_t = 14 * mm
    content_w = W - margin_l - margin_r
    y = H - margin_t

    # Header
    c.setFont("Times-Italic", 9)
    c.setFillColor(HexColor("#333333"))
    header = "Professional English in Use Marketing"
    c.drawRightString(W - margin_r - 12 * mm, y, header)
    c.setFont("Times-Roman", 9)
    c.drawRightString(W - margin_r, y, "23")
    y -= 10 * mm

    # —— 8.1 ——
    c.setFillColor(black)
    title = "8.1 Match the types of research in the box with the research problems below. Look at A and B opposite to help you."
    y = wrap_draw(c, title, margin_l, y, content_w, "Times-Bold", 10.5, 13) - 3 * mm

    # Box with 2x2 terms — thick white columns (white cell fill, thick white vertical divider)
    box_h = 18 * mm
    box_w = content_w * 0.92
    box_x = margin_l + (content_w - box_w) / 2
    box_y = y - box_h

    # White thick columns
    c.setFillColor(white)
    c.rect(box_x, box_y, box_w, box_h, fill=1, stroke=0)
    # Thick white vertical split in the middle
    mid = box_x + box_w / 2
    c.setStrokeColor(white)
    c.setLineWidth(8)
    c.line(mid, box_y, mid, box_y + box_h)
    # Outer border + thin grid
    c.setStrokeColor(BOX_BORDER)
    c.setLineWidth(1.2)
    c.rect(box_x, box_y, box_w, box_h, fill=0, stroke=1)
    c.line(mid, box_y, mid, box_y + box_h)
    c.line(box_x, box_y + box_h / 2, box_x + box_w, box_y + box_h / 2)

    cells = [
        (0, 1, "desktop + secondary"),
        (1, 1, "qualitative + field"),
        (0, 0, "motivation + primary"),
        (1, 0, "quantitative + primary"),
    ]
    c.setFont("Times-Roman", 10)
    c.setFillColor(black)
    for col, row, text in cells:
        cx = box_x + col * (box_w / 2) + 4 * mm
        cy = box_y + row * (box_h / 2) + box_h / 4 - 1.5 * mm
        c.drawString(cx, cy, text)

    y = box_y - 5 * mm

    problems = [
        "1 The R&D department want to know why people buy mobile phones so that they can develop a new model that answers all the major needs.",
        "2 The design team want to know how consumers feel about the new layout of the company website before they finalize and launch the new homepage.",
        "3 A manager wants to have financial data on her company, her competitors and the economy in general.",
        "4 The marketing team want to have a lot of data on their consumers: age, shopping habits, email address, etc.",
    ]
    for p in problems:
        y = wrap_draw(c, p, margin_l, y, content_w, "Times-Roman", 10, 12.5) - 2.2 * mm

    y -= 3 * mm

    # —— 8.2 ——
    t82 = "8.2 Complete the sentences. Look at B opposite to help you."
    y = wrap_draw(c, t82, margin_l, y, content_w, "Times-Bold", 10.5, 13) - 3 * mm

    sentences = [
        f"1 A lot of marketing research institutes carry out {DOTS*2} surveys. They ring people at home and ask them questions.",
        f"2 A {DOTS*3} is a small discussion group, led by a {DOTS*2} who asks questions to get detailed and qualitative information.",
        f"3 A marketing research institute may prepare a lengthy {DOTS*2} survey which it posts to consumers at their homes. These {DOTS*2} surveys have questions from several different companies on them.",
        f"4 Some questionnaires are completed by the {DOTS*2} (self-administered questionnaires) and some are completed by the interviewer ({DOTS}-{DOTS} questionnaires).",
        f"5 {DOTS*3} surveys are usually carried out in-store to assess the levels of service quality and cleanliness.",
        f"6 A {DOTS*2} test is designed to find out what consumers think about packaging, and a {DOTS*2} test is to find out what they think about the flavour of a product.",
    ]
    for s in sentences:
        y = wrap_draw(c, s, margin_l, y, content_w, "Times-Roman", 10, 12.5) - 2.5 * mm

    y -= 2 * mm

    # —— 8.3 ——
    t83 = "8.3 Cross out the incorrect sentence in each group. Look at A and B opposite to help you."
    y = wrap_draw(c, t83, margin_l, y, content_w, "Times-Bold", 10.5, 13) - 3.5 * mm

    left_groups = [
        (
            "1",
            [
                "a) We carried out the research last week.",
                "b) We conducted the research last week.",
                "c) We collected the research last week.",
            ],
        ),
        (
            "2",
            [
                "a) The respondents completed a questionnaire.",
                "b) The respondents analysed a questionnaire.",
                "c) The respondents filled in a questionnaire.",
            ],
        ),
        (
            "3",
            [
                "a) We must run the data quickly.",
                "b) We must collect the data quickly.",
                "c) We must gather the data quickly.",
            ],
        ),
    ]
    right_groups = [
        (
            "4",
            [
                "a) It can take a long time to mine data.",
                "b) It can take a long time to carry out data.",
                "c) It can take a long time to analyse data.",
            ],
        ),
        (
            "5",
            [
                "a) We are filling in three focus groups.",
                "b) We are mediating three focus groups.",
                "c) We are running three focus groups.",
            ],
        ),
    ]

    col_gap = 10 * mm  # thick white gutter between columns
    col_w = (content_w - col_gap) / 2
    left_x = margin_l
    right_x = margin_l + col_w + col_gap

    # White thick column backgrounds for 8.3
    # Estimate height of two-column block
    col_block_h = 58 * mm
    col_top = y + 2 * mm
    c.setFillColor(white)
    c.rect(left_x - 1 * mm, y - col_block_h, col_w + 2 * mm, col_block_h + 3 * mm, fill=1, stroke=0)
    c.rect(right_x - 1 * mm, y - col_block_h, col_w + 2 * mm, col_block_h + 3 * mm, fill=1, stroke=0)

    def draw_groups(groups, x, start_y):
        yy = start_y
        c.setFont("Times-Roman", 10)
        c.setFillColor(black)
        for num, lines in groups:
            c.setFont("Times-Bold", 10)
            c.drawString(x, yy, num)
            yy -= 3.2 * mm
            c.setFont("Times-Roman", 9.5)
            for line in lines:
                yy = wrap_draw(c, line, x + 3 * mm, yy, col_w - 4 * mm, "Times-Roman", 9.5, 11.5) - 0.8 * mm
            yy -= 2.2 * mm
        return yy

    y_left = draw_groups(left_groups, left_x, y)
    y_right = draw_groups(right_groups, right_x, y)
    y = min(y_left, y_right) - 4 * mm

    # —— Over to you ——
    box_h = 32 * mm
    if y - box_h < 12 * mm:
        y = 12 * mm + box_h
    box_y = y - box_h

    # Teal rounded-ish rectangle (simulate with rect)
    c.setFillColor(TEAL)
    c.roundRect(margin_l, box_y, content_w, box_h, 4 * mm, fill=1, stroke=0)

    # Title
    c.setFillColor(white)
    c.setFont("Times-BoldItalic", 12)
    c.drawString(margin_l + 5 * mm, box_y + box_h - 7 * mm, "Over to you")

    # Small speech icon (simple circle + arc)
    ix = margin_l + 38 * mm
    iy = box_y + box_h - 6.5 * mm
    c.setStrokeColor(white)
    c.setLineWidth(1)
    c.circle(ix, iy, 2.2 * mm, fill=0, stroke=1)

    over_text = (
        "Think about how you would carry out market research for a completely new product "
        "(for example, a light bulb that works without electricity). What kind of research "
        "would you conduct during the development phase of the product, and what kind just "
        "before the product launch?"
    )
    text_w = content_w - 28 * mm
    wrap_draw(
        c,
        over_text,
        margin_l + 5 * mm,
        box_y + box_h - 12 * mm,
        text_w,
        "Helvetica",
        9,
        11.5,
        white,
    )

    # Lightbulb on the right
    bx = margin_l + content_w - 12 * mm
    by = box_y + box_h / 2
    c.setFillColor(LIGHTBULB_YELLOW)
    c.circle(bx, by + 1 * mm, 5 * mm, fill=1, stroke=0)
    c.setFillColor(HexColor("#e8c84a"))
    c.rect(bx - 2 * mm, by - 5 * mm, 4 * mm, 3 * mm, fill=1, stroke=0)
    # rays
    c.setStrokeColor(LIGHTBULB_YELLOW)
    c.setLineWidth(1.2)
    for dx, dy in [(-8, 4), (-7, 8), (-3, 10), (3, 10), (7, 8), (8, 4)]:
        c.line(bx, by + 3 * mm, bx + dx * 0.7, by + 3 * mm + dy * 0.7)

    # Footer
    c.setFillColor(HexColor("#444444"))
    c.setFont("Times-Italic", 8)
    c.drawCentredString(W / 2, 8 * mm, "Professional English in Use Marketing")
    c.setFont("Times-Roman", 8)
    c.drawRightString(W - margin_r, 8 * mm, "23")


def build_pdf():
    W, H = A4
    c = canvas.Canvas(OUT_PDF, pagesize=A4)
    draw_page(c, W, H)
    c.save()
    print("PDF:", OUT_PDF)


def build_preview():
    """Raster preview via reportlab → temporary render using PIL composite."""
    # Render a simple preview by converting PDF with pdftoppm if available,
    # otherwise draw a simplified PIL version matching layout for sharing.
    try:
        import subprocess

        out = "/workspace/textbook-pdf/_preview"
        r = subprocess.run(
            ["pdftoppm", "-png", "-r", "120", "-singlefile", OUT_PDF, out],
            capture_output=True,
            text=True,
        )
        if r.returncode == 0 and os.path.exists(out + ".png"):
            os.rename(out + ".png", OUT_PNG)
            print("PNG:", OUT_PNG)
            return
    except FileNotFoundError:
        pass

    # Fallback: white page preview note
    img = Image.new("RGB", (595, 842), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((40, 40), "See page23.pdf", fill=(0, 0, 0))
    img.save(OUT_PNG)
    print("PNG (fallback):", OUT_PNG)


if __name__ == "__main__":
    build_pdf()
    build_preview()
