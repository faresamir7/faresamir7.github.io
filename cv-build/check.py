#!/usr/bin/env python3
"""Site self-check. Run: python3 cv-build/check.py [repo_root]  -> exit 1 on any regression.

Catches the bug classes that actually bit this repo: a CSS rule targeting a class the
markup never uses (gold.css silently did nothing for weeks), i18n key drift across
en/fr/ar/ja, a dead local asset or in-page anchor, missing social-preview tags,
text colours failing WCAG AA on the page background, and junk tracked in git.
"""
import os
import re
import subprocess
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BG = "#08070A"
LANGS = ("fr", "ar", "ja")
fail = []


def text(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


html = text("index.html")
css = "".join(text(s) for s in re.findall(r'<link rel="stylesheet" href="([^"]+)"', html))  # cascade order as linked
css_clean = "\n".join(l for l in re.sub(r"/\*.*?\*/", "", css, flags=re.S).splitlines() if "http" not in l)
js = "".join(text("js/" + f) for f in sorted(os.listdir(ROOT + "/js")) if f.endswith(".js"))

# 1. selectors pointing at classes that exist in neither the markup nor the JS
html_cls = set()
for m in re.findall(r'class="([^"]+)"', html):
    html_cls.update(m.split())
for c in sorted(set(re.findall(r"\.([A-Za-z][A-Za-z0-9_-]*)", css_clean))):
    if c not in html_cls and c not in js:
        fail.append(f"dead CSS selector .{c}")

# 2. i18n: every language block has the same keys, and covers every data-i18n in the page
used = set(re.findall(r'data-i18n="([^"]+)"', html))
i18n = text("js/i18n.js")
blocks = {}
for lang in LANGS:
    m = re.search(r"\n  %s: \{(.*?)\n  \}," % lang, i18n, re.S)
    if not m:
        fail.append(f"no '{lang}' block in i18n.js")
        continue
    blocks[lang] = set(re.findall(r'"([^"]+)":', m.group(1)))
    for key in sorted(used - blocks[lang]):
        fail.append(f"{lang} missing key {key}")
for lang in blocks:
    for key in sorted(set().union(*blocks.values()) - blocks[lang]):
        fail.append(f"{lang} missing key {key} (other languages have it)")

# 3. local assets and in-page anchors resolve
for ref in sorted(set(re.findall(r'(?:href|src)="([^"]+)"', html))):
    if ref.startswith(("http", "mailto:", "data:", "#")):
        continue
    if not os.path.exists(os.path.join(ROOT, ref)):
        fail.append(f"missing asset {ref}")
ids = set(re.findall(r'id="([^"]+)"', html))
for anchor in sorted(set(re.findall(r'href="#([^"]+)"', html))):
    if anchor not in ids:
        fail.append(f"broken anchor #{anchor}")

# 4. social preview tags + the image they point at
for tag in ("og:title", "og:description", "og:url", "og:image", "twitter:card"):
    if f'property="{tag.split(":")[0]}:{tag.split(":")[1]}"' not in html and f'name="{tag}"' not in html:
        fail.append(f"no {tag} meta")
img = re.search(r'og:image" content="https?://[^"]*/([\w./-]+\.png)"', html)
if img and not os.path.exists(os.path.join(ROOT, "assets", os.path.basename(img.group(1)))):
    fail.append("og:image points at a missing file")


# 5. small text must clear WCAG AA (4.5:1) on the page background
def contrast(hex_a, hex_b=BG):
    def lum(h):
        h = h.lstrip("#")
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        v = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        v = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in v]
        return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
    l1, l2 = sorted([lum(hex_a), lum(hex_b)], reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


SMALL_TEXT = r"(\.cert-item p|\.project-meta|\.timeline-date|\.edu-date|\.download-meta|\.contact-label|\.detail-label|\.lang-btn|\.footer p|\.hero-greeting)"
for sel in sorted(set(re.findall(SMALL_TEXT, css_clean))):
    # last matching rule wins: gold.css is the override layer
    blocks = list(re.finditer(re.escape(sel) + r"[^{]*\{([^}]*)\}", css_clean))
    if not blocks:
        continue
    block = blocks[-1]
    hexes = re.findall(r"#[0-9A-Fa-f]{3,6}", block.group(1))
    vars_ = re.findall(r"var\(--([\w-]+)\)", block.group(1))
    for name in vars_:
        d = re.search(r"--" + name + r":\s*(#[0-9A-Fa-f]{3,6})", css)
        hexes += [d.group(1)] if d else []
    if hexes and min(contrast(h) for h in hexes) < 4.5:
        fail.append(f"{sel} contrast {min(contrast(h) for h in hexes):.2f}:1 < 4.5 ({hexes})")

# 6. nothing junk tracked in git
tracked = subprocess.run(["git", "-C", ROOT, "ls-files"], capture_output=True, text=True).stdout.split()
for t in tracked:
    if t.endswith(".pyc") or "__pycache__" in t:
        fail.append(f"tracked junk {t}")

if fail:
    print("FAIL:\n  " + "\n  ".join(fail))
    sys.exit(1)
print(f"OK — {len(used)} data-i18n keys covered in en/fr/ar/ja, {len(tracked)} tracked files, "
      f"{len(html_cls)} markup classes, all local refs present")
