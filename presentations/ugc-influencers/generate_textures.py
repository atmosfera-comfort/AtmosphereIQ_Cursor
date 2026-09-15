#!/usr/bin/env python3
"""Generate abstract grayscale textures for the UGC presentation."""

from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)
RNG = random.Random(42)


def save(img: Image.Image, name: str) -> None:
    path = OUT / name
    img.save(path, quality=95)
    print(f"wrote {path}")


def texture_waves(w=900, h=500) -> Image.Image:
    img = Image.new("RGB", (w, h), (18, 18, 18))
    px = img.load()
    for y in range(h):
        for x in range(w):
            v = (
                0.55 * math.sin(x * 0.018 + y * 0.01)
                + 0.35 * math.sin(y * 0.035 + x * 0.004)
                + 0.25 * math.sin((x + y) * 0.012)
            )
            g = int(28 + (v + 1.2) * 55)
            g = max(12, min(210, g))
            px[x, y] = (g, g, g)
    return img.filter(ImageFilter.GaussianBlur(1.2))


def texture_sphere(size=700) -> Image.Image:
    img = Image.new("RGB", (size, size), (12, 12, 12))
    draw = ImageDraw.Draw(img)
    cx = cy = size // 2
    r = size // 2 - 20
    for i in range(r, 0, -1):
        t = i / r
        g = int(20 + (1 - t) ** 1.6 * 170)
        # slight highlight offset
        ox = int((1 - t) * 35)
        oy = int((1 - t) * -40)
        draw.ellipse(
            [cx - i + ox, cy - i + oy, cx + i + ox, cy + i + oy],
            fill=(g, g, g),
        )
    # ring grooves
    for k in range(8):
        rr = int(r * (0.35 + k * 0.07))
        shade = 30 + k * 8
        draw.ellipse(
            [cx - rr, cy - rr, cx + rr, cy + rr],
            outline=(shade, shade, shade),
            width=3,
        )
    return img.filter(ImageFilter.GaussianBlur(0.8))


def texture_ribs(w=420, h=720) -> Image.Image:
    img = Image.new("RGB", (w, h), (16, 16, 16))
    draw = ImageDraw.Draw(img)
    for i in range(0, w, 14):
        shade = 22 + (i // 14 % 7) * 12
        draw.rectangle([i, 0, i + 8, h], fill=(shade, shade, shade))
    # curved overlay feel
    overlay = Image.new("L", (w, h), 0)
    od = ImageDraw.Draw(overlay)
    for y in range(0, h, 28):
        amp = 18 + (y % 90) // 10
        pts = [(x, y + int(math.sin(x * 0.04) * amp)) for x in range(0, w, 4)]
        if len(pts) > 1:
            od.line(pts, fill=90, width=2)
    img = Image.composite(img.point(lambda p: min(255, p + 40)), img, overlay)
    return img.filter(ImageFilter.GaussianBlur(0.6))


def texture_noise_panel(w=640, h=360) -> Image.Image:
    img = Image.new("RGB", (w, h), (24, 24, 24))
    px = img.load()
    for y in range(h):
        for x in range(w):
            n = RNG.randint(0, 40)
            base = 30 + int(70 * abs(math.sin(x * 0.02) * math.cos(y * 0.03)))
            g = max(10, min(180, base + n))
            px[x, y] = (g, g, g)
    return img.filter(ImageFilter.GaussianBlur(1.5))


def texture_liquid(w=800, h=420) -> Image.Image:
    img = Image.new("RGB", (w, h), (14, 14, 14))
    px = img.load()
    for y in range(h):
        for x in range(w):
            v = math.sin(x * 0.03 + math.sin(y * 0.02) * 3) * math.cos(y * 0.04)
            g = int(40 + (v + 1) * 70)
            px[x, y] = (g, g, g)
    return img.filter(ImageFilter.GaussianBlur(2))


if __name__ == "__main__":
    save(texture_waves(), "tex_waves.jpg")
    save(texture_sphere(), "tex_sphere.jpg")
    save(texture_ribs(), "tex_ribs.jpg")
    save(texture_noise_panel(), "tex_noise.jpg")
    save(texture_liquid(), "tex_liquid.jpg")
