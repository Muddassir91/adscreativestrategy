#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
COVER = HERE / "book-cover.png"


def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    return mask


def shadow_layer(size, box, radius, blur=28, alpha=90):
    shadow = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(shadow)
    d.rounded_rectangle(box, radius=radius, fill=(10, 20, 18, alpha))
    return shadow.filter(ImageFilter.GaussianBlur(blur))


def paste_cover(canvas, cover, xy, size, radius=12):
    cover = cover.resize(size, Image.Resampling.LANCZOS)
    cover = cover.convert("RGBA")
    mask = rounded_mask(size, radius)
    canvas.alpha_composite(cover, xy)
    return canvas


def make_flat(cover):
    W, H = 1400, 1100
    canvas = Image.new("RGBA", (W, H), (246, 250, 249, 255))
    d = ImageDraw.Draw(canvas)
    d.rectangle((0, 0, W, H), fill=(246, 250, 249, 255))
    for i in range(9):
        x = 90 + i * 140
        d.line((x, 120, x + 280, 980), fill=(230, 240, 238, 255), width=2)
    canvas.alpha_composite(shadow_layer((W, H), (430, 105, 990, 985), 18, 34, 72))
    paste_cover(canvas, cover, (470, 90), (480, 720), 10)
    d.rounded_rectangle((438, 840, 982, 922), radius=8, fill=(255, 255, 255, 245), outline=(15, 118, 110, 255), width=3)
    d.text((470, 875), "106-page business playbook, AI master prompts included", fill=(15, 79, 74, 255))
    canvas.save(HERE / "mockup-flat.png")


def make_angled(cover):
    W, H = 1400, 1100
    canvas = Image.new("RGBA", (W, H), (249, 249, 247, 255))
    d = ImageDraw.Draw(canvas)
    d.rectangle((0, 0, W, H), fill=(249, 249, 247, 255))
    base = cover.resize((560, 840), Image.Resampling.LANCZOS).convert("RGBA")
    spine = Image.new("RGBA", (74, 840), (7, 83, 77, 255))
    sd = ImageDraw.Draw(spine)
    for x in range(0, 74, 9):
        sd.line((x, 0, x, 840), fill=(9, 99, 92, 255), width=3)
    book = Image.new("RGBA", (634, 840), (0, 0, 0, 0))
    book.alpha_composite(spine, (0, 0))
    book.alpha_composite(base, (74, 0))
    book = book.rotate(-7, expand=True, resample=Image.Resampling.BICUBIC)
    canvas.alpha_composite(shadow_layer((W, H), (410, 175, 1010, 975), 24, 40, 95))
    canvas.alpha_composite(book, (388, 95))
    d.rounded_rectangle((140, 790, 500, 890), radius=10, fill=(255, 255, 255, 245), outline=(229, 229, 229, 255), width=2)
    d.text((168, 828), "For copywriters moving into strategy", fill=(26, 26, 26, 255))
    d.text((168, 858), "and strategists learning how to sell it", fill=(15, 118, 110, 255))
    canvas.save(HERE / "mockup-angled.png")


def make_stack(cover):
    W, H = 1400, 1100
    canvas = Image.new("RGBA", (W, H), (246, 250, 249, 255))
    d = ImageDraw.Draw(canvas)
    d.rectangle((0, 0, W, H), fill=(246, 250, 249, 255))
    sizes = [(430, 645), (460, 690), (490, 735)]
    positions = [(620, 260), (520, 210), (420, 150)]
    rotations = [8, 2, -5]
    for size, pos, rot in zip(sizes, positions, rotations):
        layer = cover.resize(size, Image.Resampling.LANCZOS).convert("RGBA")
        layer = layer.rotate(rot, expand=True, resample=Image.Resampling.BICUBIC)
        x, y = pos
        canvas.alpha_composite(shadow_layer((W, H), (x + 24, y + 28, x + layer.width - 16, y + layer.height - 10), 20, 30, 58))
        canvas.alpha_composite(layer, pos)
    d.rounded_rectangle((140, 150, 430, 430), radius=10, fill=(255, 255, 255, 245), outline=(15, 118, 110, 255), width=3)
    d.text((168, 205), "Skill is crowded.", fill=(26, 26, 26, 255))
    d.text((168, 245), "Business side", fill=(15, 118, 110, 255))
    d.text((168, 275), "is the moat.", fill=(15, 118, 110, 255))
    d.line((168, 320, 350, 320), fill=(15, 118, 110, 255), width=5)
    d.text((168, 360), "Offer. Price. Sell. Deliver.", fill=(82, 82, 82, 255))
    canvas.save(HERE / "mockup-stack.png")


def main():
    cover = Image.open(COVER).convert("RGBA")
    make_flat(cover)
    make_angled(cover)
    make_stack(cover)


if __name__ == "__main__":
    main()
