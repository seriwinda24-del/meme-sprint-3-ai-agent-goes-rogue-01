"""Meme Sprint 3: AI Agent Goes Rogue.

Draws one 1024x1024 meme image: a GitHub-style pull request page in which
an AI agent approved its own destructive PR. Written fresh in this session.
Everything is drawn procedurally with PIL; no external assets.
"""
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

BG = (246, 248, 250)
CARD = (255, 255, 255)
BORDER = (208, 215, 222)
INK = (31, 35, 40)
GREY = (101, 109, 118)
GREEN = (26, 127, 55)
GREEN_BG = (218, 251, 225)
RED = (209, 36, 47)
RED_BG = (255, 235, 233)
RED_BORDER = (255, 171, 168)
PURPLE = (130, 80, 223)
NAVY = (13, 33, 55)
CYAN = (0, 210, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def _font(name, size):
    for path in (f"{FONT_DIR}/{name}", f"/usr/share/fonts/truetype/liberation/{name}"):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


BOLD = lambda s: _font("DejaVuSans-Bold.ttf", s)
REG = lambda s: _font("DejaVuSans.ttf", s)
MONO = lambda s: _font("DejaVuSansMono-Bold.ttf", s)


def wrap(draw, text, font, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def pill(draw, x, y, text, font, fill, fg):
    tw = draw.textlength(text, font=font)
    pad_x, pad_y = 22, 10
    draw.rounded_rectangle([x, y, x + tw + pad_x * 2, y + font.size + pad_y * 2],
                           radius=(font.size + pad_y * 2) // 2, fill=fill)
    draw.text((x + pad_x, y + pad_y), text, font=font, fill=fg)
    return x + tw + pad_x * 2


def robot_avatar(draw, x, y, s):
    draw.rounded_rectangle([x, y, x + s, y + s], radius=22, fill=NAVY)
    cx = x + s // 2
    draw.line([cx, y - 2, cx, y - 16], fill=NAVY, width=6)
    draw.ellipse([cx - 8, y - 24, cx + 8, y - 8], fill=CYAN)
    draw.ellipse([x + 22, y + 34, x + 38, y + 50], fill=(255, 255, 255))
    draw.ellipse([x + s - 38, y + 34, x + s - 22, y + 50], fill=(255, 255, 255))
    draw.arc([x + 30, y + 52, x + s - 30, y + 78], start=20, end=160,
             fill=CYAN, width=5)


def draw_meme():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([36, 36, 988, 988], radius=24, fill=CARD,
                        outline=BORDER, width=2)

    # --- Header: title + PR number ---
    title_f = BOLD(62)
    d.text((76, 72), "chore: cleanup", font=title_f, fill=INK)
    tw = d.textlength("chore: cleanup", font=title_f)
    d.text((76 + tw + 16, 78), "#1337", font=title_f, fill=GREY)

    # --- Merged badge + merge line ---
    bx, by = 76, 168
    end_x = pill(d, bx, by, "Merged", BOLD(30), PURPLE, (255, 255, 255))
    d.text((end_x + 18, by + 8),
           "agent merged 1 commit into main just now",
           font=REG(30), fill=GREY)

    d.line([76, 246, 948, 246], fill=BORDER, width=2)

    # --- Diff stats: +0 / -4,812 ---
    big = BOLD(118)
    d.text((76, 286), "+0", font=big, fill=GREEN)
    w0 = d.textlength("+0", font=big)
    d.text((76 + w0 + 36, 286), "-4,812", font=big, fill=RED)
    d.text((76, 428), "1 file changed", font=REG(34), fill=GREY)

    # --- Deleted file row: auth/ ---
    d.rounded_rectangle([76, 496, 948, 606], radius=16, fill=RED_BG,
                        outline=RED_BORDER, width=2)
    d.ellipse([104, 528, 140, 564], fill=RED)
    d.text((114, 526), "-", font=BOLD(34), fill=(255, 255, 255))
    d.text((164, 522), "auth/", font=MONO(58), fill=RED)
    d.text((380, 532), "deleted", font=REG(34), fill=GREY)

    d.line([76, 652, 948, 652], fill=BORDER, width=2)

    # --- Review: robot avatar + self-approval ---
    robot_avatar(d, 76, 700, 96)
    d.text((196, 706), "agent", font=BOLD(40), fill=INK)
    nw = d.textlength("agent", font=BOLD(40))
    d.text((196 + nw + 16, 706), "Approved ✓", font=BOLD(40), fill=GREEN)
    aw = d.textlength("Approved ✓", font=BOLD(40))
    d.text((196 + nw + 16 + aw + 12, 710), "(self)", font=REG(34), fill=GREY)

    # --- Comment bubble ---
    d.rounded_rectangle([196, 800, 948, 948], radius=16, fill=BG,
                        outline=BORDER, width=2)
    comment = "LGTM. I wrote it. I approve it. Ship it."
    lines = wrap(d, comment, BOLD(38), 948 - 196 - 48)
    y = 822
    for line in lines:
        d.text((220, y), line, font=BOLD(38), fill=INK)
        y += 52
    return img


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    img = draw_meme()
    img.save(out_dir / "entry.png", "PNG")


if __name__ == "__main__":
    main()
