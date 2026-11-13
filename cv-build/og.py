#!/usr/bin/env python3
"""Regenerate assets/og.png (1200x630 social preview) — python3 og.py [out.png]"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG, TEXT, TEXT2, TEXT3, ACCENT = "#08070A", "#EDEBE8", "#A9A5A0", "#7C7773", "#FF2D2D"
TTC = "/usr/share/fonts/inter/Inter.ttc"


def font(size, semi=False):
    return ImageFont.truetype(TTC, size, index=12 if semi else 0)  # Inter SemiBold / Regular


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "assets/og.png"
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle((64, 96, 70, H - 96), fill=ACCENT)   # site's red rule, inset so rounded crops miss nothing

    d.text((96, 150), "TECHNICAL ACCOUNT MANAGER  ·  HPE", font=font(26), fill=TEXT2)
    d.text((96, 226), "Fares Amir", font=font(104, True), fill=TEXT)
    d.text((96, 342), "Hassen", font=font(104, True), fill=TEXT)
    d.rectangle((96, 482, 190, 486), fill=ACCENT)
    d.text((96, 518), "Network+ CE  ·  uptime & homelab infrastructure  ·  Ariana, Tunisia",
           font=font(28), fill=TEXT2)
    d.text((96, 566), "faresamir7.github.io", font=font(24), fill="#9A958F")

    img.save(out, "PNG", optimize=True)
    print(out, img.size)


if __name__ == "__main__":
    main()
