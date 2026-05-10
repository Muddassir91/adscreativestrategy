#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent

ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
ARIAL_ITALIC = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"

WHITE = (255, 255, 255, 255)
NEAR_WHITE = (250, 251, 251, 255)
INK = (15, 17, 16, 255)
INK_SOFT = (60, 68, 65, 255)
MUTED = (110, 118, 115, 255)
RULE = (228, 232, 230, 255)
TEAL = (0, 128, 128, 255)
TEAL_DEEP = (0, 77, 77, 255)
TEAL_TINT = (240, 248, 248, 255)


def font(path, size):
    return ImageFont.truetype(path, size)


def shadow_layer(size, box, radius=24, blur=44, alpha=42):
    shadow = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(shadow)
    d.rounded_rectangle(box, radius=radius, fill=(8, 18, 16, alpha))
    return shadow.filter(ImageFilter.GaussianBlur(blur))


def avatar(d, x, y, r=22, label="C"):
    d.ellipse((x, y, x + r * 2, y + r * 2), fill=TEAL)
    f = font(ARIAL_BOLD, int(r * 1.1))
    bbox = d.textbbox((0, 0), label, font=f)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text((x + r - tw / 2, y + r - th / 2 - bbox[1]), label, font=f, fill=WHITE)


def make_inbox():
    W, H = 1600, 1200
    canvas = Image.new("RGBA", (W, H), TEAL_TINT)

    card_x0, card_y0 = 80, 70
    card_x1, card_y1 = W - 80, H - 70
    canvas.alpha_composite(shadow_layer((W, H), (card_x0 + 30, card_y0 + 60, card_x1 + 10, card_y1 + 30), 28, 56, 60))

    card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((card_x0, card_y0, card_x1, card_y1), radius=22, fill=WHITE, outline=RULE, width=2)
    canvas.alpha_composite(card)

    d = ImageDraw.Draw(canvas)

    f_title = font(ARIAL_BOLD, 38)
    f_meta = font(ARIAL, 22)
    f_sender = font(ARIAL_BOLD, 26)
    f_subject = font(ARIAL_BOLD, 28)
    f_snippet = font(ARIAL, 24)
    f_time = font(ARIAL, 20)

    pad_x = card_x0 + 36
    pad_top = card_y0 + 36

    d.text((pad_x, pad_top), "Inbox", font=f_title, fill=INK)
    d.text((pad_x, pad_top + 56), "Daily emails from CSOS", font=f_meta, fill=MUTED)

    search_y = pad_top + 110
    d.rounded_rectangle((pad_x, search_y, card_x1 - 36, search_y + 56), radius=10, fill=NEAR_WHITE, outline=RULE, width=2)
    d.text((pad_x + 22, search_y + 16), "Search inbox", font=f_meta, fill=MUTED)

    emails = [
        ("CSOS", "the $97 strategy course problem", "you didn't fail. you bought a content product when you needed a business one. here is what to run instead today...", "8:42 AM", True),
        ("CSOS", "your offer sounds like a freelancer wrote it", "and that is fine. for now. but here is the rewrite that takes the same offer from $1,500 to $5,000 without changing the deliverables...", "Yesterday", True),
        ("CSOS", "stop pricing creative strategy like a copywriter", "two charts. one rule. fifteen minutes. you can run this exercise before lunch and never quote $50/hour again...", "Mon", False),
        ("CSOS", "the worst sales call I had this week", "the prospect wasn't the problem. my offer was. four sentences I am stealing from this lesson and putting in my next pitch...", "Mon", False),
        ("CSOS", "if your DMs aren't getting replies, this is why", "founders aren't ignoring you. they are filtering you. one tweak to the first line that triples response rate. tested across 280 cold messages...", "Sun", False),
        ("CSOS", "creative strategy is not what your tweet thread says it is", "the threadbros got the framework right and the business side completely wrong. here is the part they cannot post about because it does not get likes...", "Sat", False),
        ("CSOS", "i used to charge $300 for this", "now i charge $5,000. nothing in the deliverable changed. one thing in the wrapper did. read this in 90 seconds...", "Fri", False),
        ("CSOS", "the linkedin guru tax (you're paying it)", "every cohort, course, and 'strategist mastermind' priced at $1,997 is a quiet tax on your time. one move to opt out and still get the lessons...", "Thu", False),
    ]

    list_y = search_y + 100
    row_h = 116
    text_x = pad_x + 78
    text_right = card_x1 - 36

    def truncate_to(text, font_obj, max_w):
        if d.textlength(text, font=font_obj) <= max_w:
            return text
        ellipsis = "..."
        while text and d.textlength(text + ellipsis, font=font_obj) > max_w:
            text = text[:-1]
        return text.rstrip() + ellipsis

    for i, (sender, subject, snippet, time_label, unread) in enumerate(emails):
        ry = list_y + i * row_h

        if unread:
            d.rectangle((card_x0 + 1, ry, card_x0 + 5, ry + row_h - 1), fill=TEAL)

        avatar(d, pad_x, ry + 30, r=24, label="C")

        sender_color = INK if unread else INK_SOFT
        sender_font = f_sender if unread else font(ARIAL, 24)
        d.text((text_x, ry + 22), sender, font=sender_font, fill=sender_color)

        time_color = TEAL if unread else MUTED
        time_bbox = d.textbbox((0, 0), time_label, font=f_time)
        tw = time_bbox[2] - time_bbox[0]
        d.text((text_right - tw, ry + 26), time_label, font=f_time, fill=time_color)

        subject_color = INK if unread else INK_SOFT
        subject_font = font(ARIAL_BOLD, 26) if unread else font(ARIAL_BOLD, 24)
        max_subject_w = text_right - text_x - 20
        subject_drawn = truncate_to(subject, subject_font, max_subject_w)
        d.text((text_x, ry + 54), subject_drawn, font=subject_font, fill=subject_color)

        snippet_font = font(ARIAL, 22)
        max_snippet_w = text_right - text_x
        snippet_drawn = truncate_to(snippet, snippet_font, max_snippet_w)
        d.text((text_x, ry + 86), snippet_drawn, font=snippet_font, fill=MUTED)

        if i < len(emails) - 1:
            d.line((text_x, ry + row_h, text_right, ry + row_h), fill=RULE, width=1)

    canvas.save(HERE / "mockup-inbox.png")


def wrap_text(d, text, font_obj, max_w):
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = (current + " " + w).strip()
        if d.textlength(test, font=font_obj) <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def make_email():
    W, H = 1600, 1200
    canvas = Image.new("RGBA", (W, H), TEAL_TINT)

    card_x0, card_y0 = 100, 80
    card_x1, card_y1 = W - 100, H - 80
    canvas.alpha_composite(shadow_layer((W, H), (card_x0 + 30, card_y0 + 60, card_x1 + 10, card_y1 + 30), 28, 56, 64))

    card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((card_x0, card_y0, card_x1, card_y1), radius=22, fill=WHITE, outline=RULE, width=2)
    canvas.alpha_composite(card)

    d = ImageDraw.Draw(canvas)

    f_subject = font(ARIAL_BOLD, 42)
    f_sender = font(ARIAL_BOLD, 26)
    f_meta = font(ARIAL, 22)
    f_body = font(ARIAL, 26)
    f_body_bold = font(ARIAL_BOLD, 26)
    f_italic = font(ARIAL_ITALIC, 26)

    pad_x = card_x0 + 56
    y = card_y0 + 56
    inner_w = card_x1 - card_x0 - 112

    d.text((pad_x, y), "Stop pricing creative strategy like a copywriter.", font=f_subject, fill=INK)
    y += 78

    avatar(d, pad_x, y, r=24, label="C")
    d.text((pad_x + 70, y), "CSOS", font=f_sender, fill=INK)
    d.text((pad_x + 70, y + 30), "to you", font=f_meta, fill=MUTED)
    time_label = "Tue 8:42 AM"
    tw = d.textlength(time_label, font=f_meta)
    d.text((card_x1 - 56 - tw, y + 4), time_label, font=f_meta, fill=MUTED)
    y += 80

    d.line((pad_x, y, card_x1 - 56, y), fill=RULE, width=1)
    y += 32

    paragraphs = [
        ("plain", "Friend,"),
        ("plain", "Pricing is not a number. It is a story you tell with the number."),
        ("plain", "Most strategists pick a price the same way a junior copywriter picks one. They look at what the last person charged. They knock 20% off so they feel competitive. They write the proposal. They wait."),
        ("bold", "That is the bug. Not the price."),
        ("plain", "When you price strategy like a copywriter, the buyer reads the proposal like an order form. Line items. Deliverables. Hours. They start mentally scoring you against the cheapest freelancer they ever hired. You lose before the call ends."),
        ("plain", "Here is the move for today."),
        ("plain", "Pick one client you are quoting this week. Before you send the price, write three sentences. What changes in their business if this works. What it costs them if they keep doing what they are doing. What you will refuse to be measured against."),
        ("italic", "Send those three sentences before the price. Not after."),
        ("plain", "Most of you will skip this. The ones who do not will close a higher offer this week."),
        ("plain", "Talk soon,"),
        ("plain", "CSOS"),
    ]

    for kind, text in paragraphs:
        f_use = f_body
        if kind == "bold":
            f_use = f_body_bold
        elif kind == "italic":
            f_use = f_italic
        lines = wrap_text(d, text, f_use, inner_w)
        for line in lines:
            color = INK if kind == "bold" else INK_SOFT
            if kind == "italic":
                color = TEAL_DEEP
            d.text((pad_x, y), line, font=f_use, fill=color)
            y += 38
        y += 12
        if y > card_y1 - 80:
            break

    canvas.save(HERE / "mockup-email.png")


def main():
    make_inbox()
    make_email()


if __name__ == "__main__":
    main()
