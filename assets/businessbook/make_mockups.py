#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
COVER = HERE / "book-cover.png"

CREAM = (249, 246, 240, 255)
SPINE = (7, 63, 58, 255)
SPINE_HI = (12, 95, 88, 255)
SPINE_LO = (4, 42, 39, 255)


def shadow_layer(size, box, radius=22, blur=42, alpha=110):
    shadow = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(shadow)
    d.rounded_rectangle(box, radius=radius, fill=(8, 18, 16, alpha))
    return shadow.filter(ImageFilter.GaussianBlur(blur))


def build_book(cover, cover_size=(560, 840), spine_w=64):
    cw, ch = cover_size
    base = cover.resize(cover_size, Image.Resampling.LANCZOS).convert("RGBA")

    spine = Image.new("RGBA", (spine_w, ch), SPINE)
    sd = ImageDraw.Draw(spine)
    for x in range(0, spine_w, 6):
        shade = SPINE_HI if (x // 6) % 2 == 0 else SPINE_LO
        sd.line((x, 0, x, ch), fill=shade, width=1)
    sd.line((spine_w - 2, 0, spine_w - 2, ch), fill=(0, 0, 0, 70), width=2)

    book = Image.new("RGBA", (spine_w + cw, ch), (0, 0, 0, 0))
    book.alpha_composite(spine, (0, 0))
    book.alpha_composite(base, (spine_w, 0))

    edge = Image.new("RGBA", (spine_w + cw, ch), (0, 0, 0, 0))
    ed = ImageDraw.Draw(edge)
    ed.rectangle((spine_w, 0, spine_w + 4, ch), fill=(0, 0, 0, 36))
    ed.rectangle((spine_w + cw - 3, 0, spine_w + cw, ch), fill=(220, 220, 215, 255))
    book.alpha_composite(edge, (0, 0))

    return book


def make_hero(cover):
    W, H = 1400, 1100
    canvas = Image.new("RGBA", (W, H), CREAM)
    book = build_book(cover, cover_size=(540, 800), spine_w=58)
    book = book.rotate(-6, expand=True, resample=Image.Resampling.BICUBIC)

    bx = (W - book.width) // 2
    by = (H - book.height) // 2 - 10

    sx0 = bx + 30
    sy0 = by + 70
    sx1 = bx + book.width - 20
    sy1 = by + book.height + 6
    canvas.alpha_composite(shadow_layer((W, H), (sx0, sy0, sx1, sy1), 36, 56, 100))
    canvas.alpha_composite(book, (bx, by))
    canvas.save(HERE / "mockup-hero.png")


def make_feature(cover):
    W, H = 1600, 1200
    canvas = Image.new("RGBA", (W, H), CREAM)

    book = build_book(cover, cover_size=(620, 920), spine_w=70)
    book = book.rotate(-3, expand=True, resample=Image.Resampling.BICUBIC)

    bx = (W - book.width) // 2
    by = (H - book.height) // 2 - 20

    sx0 = bx + 60
    sy0 = by + 110
    sx1 = bx + book.width - 40
    sy1 = by + book.height + 30
    canvas.alpha_composite(shadow_layer((W, H), (sx0, sy0, sx1, sy1), 40, 70, 130))

    glow_box = (bx - 60, by - 40, bx + book.width + 60, by + book.height + 40)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse(glow_box, fill=(94, 228, 210, 26))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    canvas.alpha_composite(glow)

    canvas.alpha_composite(book, (bx, by))
    canvas.save(HERE / "mockup-feature.png")


def make_flat(cover):
    W, H = 1200, 1500
    canvas = Image.new("RGBA", (W, H), CREAM)
    book = build_book(cover, cover_size=(720, 1080), spine_w=42)
    bx = (W - book.width) // 2
    by = (H - book.height) // 2 - 40
    canvas.alpha_composite(shadow_layer((W, H), (bx + 20, by + 60, bx + book.width - 10, by + book.height + 20), 30, 50, 105))
    canvas.alpha_composite(book, (bx, by))
    canvas.save(HERE / "mockup-flat.png")


def main():
    cover = Image.open(COVER).convert("RGBA")
    make_hero(cover)
    make_feature(cover)
    make_flat(cover)


if __name__ == "__main__":
    main()
