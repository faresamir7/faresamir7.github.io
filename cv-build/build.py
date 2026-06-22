#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build localized Resume + CV (EN/FR/AR) as PDF, TXT, and JSON Resume.

Japanese uses dedicated traditional templates (build_ja.py).
Outputs to ../assets/. PDF rendering uses headless Chromium.
"""
import html
import json
import os
import subprocess
import sys
import tempfile

import data as D
from translations import T

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "assets"))
os.makedirs(ASSETS, exist_ok=True)

ACCENT = "#9c1b1b"
INK = "#1a1a1a"
SUB = "#555"

# Per-language file slugs (used for PDF/TXT names + website wiring)
SLUG = {"en": "", "fr": "-FR", "ar": "-AR"}

FONT_LINK = ("https://fonts.googleapis.com/css2?"
             "family=Noto+Sans+Arabic:wght@400;500;700&display=swap")


def css(rtl=False):
    direction = "rtl" if rtl else "ltr"
    text_align = "right" if rtl else "left"
    base_font = ("'Noto Sans Arabic', 'Helvetica Neue', Arial, sans-serif" if rtl
                 else "'Helvetica Neue', Helvetica, Arial, sans-serif")
    flip = "right" if rtl else "left"
    return """
@import url('%(FONT)s');
@page { size: A4; margin: 12mm 15mm; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: %(BASE_FONT)s;
  color: %(INK)s; font-size: 10pt; line-height: 1.45;
  direction: %(DIR)s; text-align: %(TALIGN)s;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
a { color: %(ACCENT)s; text-decoration: none; }
header { border-bottom: 2px solid %(ACCENT)s; padding-bottom: 8px; margin-bottom: 12px; }
h1 { font-size: 22pt; letter-spacing: 0.3px; color: %(INK)s; }
.role { font-size: 11pt; color: %(ACCENT)s; font-weight: 700; margin-top: 2px; }
.contact { font-size: 8.6pt; color: %(SUB)s; margin-top: 6px; }
.contact .sep { color: #bbb; margin: 0 6px; }
h2 {
  font-size: 10.5pt; letter-spacing: 0.5px; color: %(ACCENT)s;
  border-bottom: 1px solid #ddd; padding-bottom: 3px; margin: 14px 0 8px;
  text-transform: uppercase;
}
.summary { font-size: 9.6pt; color: #333; text-align: justify; }
.job { margin-bottom: 10px; page-break-inside: avoid; }
.job-head { display: flex; justify-content: space-between; align-items: baseline; }
.job-title { font-weight: 700; font-size: 10pt; }
.job-company { color: %(ACCENT)s; font-weight: 700; }
.job-meta { font-size: 8.6pt; color: %(SUB)s; white-space: nowrap; padding-%(FLIP)s: 10px; }
ul { list-style: none; margin: 4px 0 0; }
li { position: relative; padding-%(FLIP)s: 12px; margin-bottom: 2.5px; font-size: 9.3pt; color: #333; }
li::before { content: "\\2013"; position: absolute; %(FLIP)s: 0; color: %(ACCENT)s; }
.edu-item, .cert-item { margin-bottom: 6px; page-break-inside: avoid; }
.edu-degree { font-size: 9.3pt; color: #333; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 2px 24px; }
.skill-row { margin-bottom: 5px; font-size: 9.3pt; }
.skill-label { font-weight: 700; color: %(INK)s; }
.cert-name { font-weight: 700; }
.cert-meta { color: %(SUB)s; font-size: 8.8pt; }
.inline-list { font-size: 9.3pt; color: #333; }
.lang-line { font-size: 9.3pt; }
.lang-line b { color: %(INK)s; }
footer { margin-top: 12px; font-size: 7.6pt; color: #999; text-align: center;
         border-top: 1px solid #eee; padding-top: 6px; }
body.compact { font-size: 9.3pt; line-height: 1.22; }
body.compact h1 { font-size: 19pt; }
body.compact h2 { margin: 6px 0 4px; }
body.compact .summary { font-size: 8.9pt; }
body.compact header { padding-bottom: 5px; margin-bottom: 8px; }
body.compact .job { margin-bottom: 4px; }
body.compact li { font-size: 8.8pt; margin-bottom: 1px; }
body.compact .edu-item, body.compact .cert-item { margin-bottom: 2px; }
body.compact .skill-row { margin-bottom: 2px; font-size: 8.8pt; }
body.compact .cert-item { font-size: 8.6pt; }
body.compact .cert-meta { font-size: 8.1pt; }
body.compact footer { margin-top: 6px; }
""" % {"FONT": FONT_LINK, "BASE_FONT": base_font, "INK": INK, "ACCENT": ACCENT,
       "SUB": SUB, "DIR": direction, "TALIGN": text_align, "FLIP": flip}


def esc(s):
    return html.escape(str(s))


class Loc:
    """Resolves content for a given language, falling back to English (data.py)."""
    def __init__(self, lang):
        self.lang = lang
        self.t = T.get(lang, {})
        self.rtl = bool(self.t.get("rtl"))
        self.ui = self.t.get("ui", {})

    def heading(self, key, en):
        return self.ui.get(key, en)

    def name(self):
        return D.CONTACT["name"]

    def title(self):
        return self.t.get("title", D.CONTACT["title"])

    def summary(self):
        return self.t.get("summary", D.SUMMARY)

    def roles(self):
        out = []
        for j in D.EXPERIENCE:
            rid = j["id"]
            tr = self.t.get("roles", {}).get(rid, {})
            out.append({
                "title": tr.get("title", j["title"]),
                "company": j["company"],
                "dates": self.t.get("dates", {}).get(rid, j["dates"]),
                "location": self.t.get("locations", {}).get(rid, j["location"]),
                "bullets": tr.get("bullets", j["bullets"]),
            })
        return out

    def education(self):
        return self.t.get("education", D.EDUCATION)

    def certifications(self):
        return self.t.get("certifications", D.CERTIFICATIONS)

    def skills(self):
        return self.t.get("skills", D.SKILLS)

    def languages(self):
        return self.t.get("languages", D.LANGUAGES)

    def interests(self):
        return self.t.get("interests", D.INTERESTS)


def contact_html():
    c = D.CONTACT
    parts = [
        f'<span dir="ltr">{esc(c["email"])}</span>',
        f'<span dir="ltr">{esc(c["phone"])}</span>',
        f'<span dir="ltr">{esc(c["location"])}</span>',
        f'<a href="{c["linkedin_url"]}" dir="ltr">{esc(c["linkedin_label"])}</a>',
        f'<a href="{c["github_url"]}" dir="ltr">{esc(c["github_label"])}</a>',
        f'<a href="{c["website_url"]}" dir="ltr">{esc(c["website_label"])}</a>',
    ]
    return '<span class="sep">|</span>'.join(parts)


def header_html(L):
    return (
        f'<header><h1>{esc(L.name())}</h1>'
        f'<div class="role">{esc(L.title())}</div>'
        f'<div class="contact">{contact_html()}</div></header>'
    )


def jobs_html(L, counts=None):
    out = []
    for i, j in enumerate(L.roles()):
        n = None if counts is None else (counts[i] if i < len(counts) else 1)
        bullets = j["bullets"] if n is None else j["bullets"][:n]
        lis = "".join(f"<li>{esc(b)}</li>" for b in bullets)
        out.append(
            f'<div class="job"><div class="job-head">'
            f'<div><span class="job-title">{esc(j["title"])}</span>, '
            f'<span class="job-company">{esc(j["company"])}</span></div>'
            f'<div class="job-meta">{esc(j["dates"])} &middot; {esc(j["location"])}</div>'
            f'</div><ul>{lis}</ul></div>'
        )
    return "".join(out)


def edu_html(L):
    out = []
    for e in L.education():
        out.append(
            f'<div class="edu-item"><div class="job-head">'
            f'<div class="job-title">{esc(e["institution"])}</div>'
            f'<div class="job-meta">{esc(e["dates"])} &middot; {esc(e["location"])}</div></div>'
            f'<div class="edu-degree">{esc(e["degree"])}</div></div>'
        )
    return "".join(out)


def certs_html(L):
    items = []
    for c in L.certifications():
        note = f' <span class="cert-meta">({esc(c["note"])})</span>' if c["note"] else ""
        items.append(
            f'<div class="cert-item"><span class="cert-name">{esc(c["name"])}</span>{note}'
            f'<br><span class="cert-meta">{esc(c["issuer"])} &middot; {esc(c["date"])}</span></div>'
        )
    return f'<div class="two-col">{"".join(items)}</div>'


def skills_html(L):
    rows = []
    for label, vals in L.skills().items():
        rows.append(
            f'<div class="skill-row"><span class="skill-label">{esc(label)}:</span> '
            f'{esc(", ".join(vals))}</div>'
        )
    return "".join(rows)


def languages_html(L):
    return " &nbsp;&middot;&nbsp; ".join(
        f'<b>{esc(x["language"])}</b> ({esc(x["level"])})' for x in L.languages()
    )


def page(title, body, L, body_class=""):
    cls = (body_class + (" " if body_class else "")).strip()
    cls_attr = f' class="{cls}"' if cls else ""
    gen = L.heading("generated", "Generated 2026")
    return (
        f'<!DOCTYPE html><html lang="{L.lang}" dir="{"rtl" if L.rtl else "ltr"}"><head>'
        f'<meta charset="utf-8"><title>{esc(title)}</title><style>{css(L.rtl)}</style></head>'
        f'<body{cls_attr}>{body}<footer>{esc(L.name())} &middot; {esc(title)} &middot; '
        f'{esc(gen)} &middot; <span dir="ltr">{esc(D.CONTACT["website_label"])}</span></footer>'
        f'</body></html>'
    )


def build_resume_html(L):
    body = header_html(L)
    body += f'<h2>{esc(L.heading("summaryHead", "Professional Summary"))}</h2>'
    body += f'<p class="summary">{esc(L.summary())}</p>'
    body += f'<h2>{esc(L.heading("expHead", "Experience"))}</h2>'
    # French runs ~15% longer; trim one bullet from the top two roles to hold 1 page.
    counts = [3, 2, 2, 1, 1, 1] if L.lang == "fr" else [4, 3, 2, 1, 1, 1]
    body += jobs_html(L, counts=counts)
    body += f'<h2>{esc(L.heading("eduHead", "Education"))}</h2>' + edu_html(L)
    body += f'<h2>{esc(L.heading("keySkillsHead", "Key Skills"))}</h2>' + skills_html(L)
    body += f'<h2>{esc(L.heading("certHead", "Certifications"))}</h2>' + certs_html(L)
    body += f'<h2>{esc(L.heading("langHead", "Languages"))}</h2>'
    body += f'<div class="lang-line">{languages_html(L)}</div>'
    return page(L.heading("resumeTitle", "Resume"), body, L, body_class="compact")


def build_cv_html(L):
    body = header_html(L)
    body += f'<h2>{esc(L.heading("summaryHead", "Professional Summary"))}</h2>'
    body += f'<p class="summary">{esc(L.summary())}</p>'
    body += f'<h2>{esc(L.heading("expHead", "Professional Experience"))}</h2>' + jobs_html(L)
    body += f'<h2>{esc(L.heading("eduHead", "Education"))}</h2>' + edu_html(L)
    body += f'<h2>{esc(L.heading("certHead", "Certifications"))}</h2>' + certs_html(L)
    body += f'<h2>{esc(L.heading("skillsHead", "Skills & Expertise"))}</h2>' + skills_html(L)
    body += f'<h2>{esc(L.heading("langHead", "Languages"))}</h2>'
    body += f'<div class="lang-line">{languages_html(L)}</div>'
    body += f'<h2>{esc(L.heading("interestsHead", "Interests"))}</h2>'
    body += f'<div class="inline-list">{esc(", ".join(L.interests()))}</div>'
    return page(L.heading("cvTitle", "Curriculum Vitae"), body, L)


def render_pdf(html_str, out_pdf):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html_str)
        tmp = f.name
    chromium = next((b for b in ("chromium", "chromium-browser", "google-chrome")
                     if subprocess.run(["which", b], capture_output=True).returncode == 0), None)
    if not chromium:
        sys.exit("No Chromium/Chrome found")
    subprocess.run([
        chromium, "--headless", "--no-sandbox", "--disable-gpu",
        "--no-pdf-header-footer", "--virtual-time-budget=8000",
        f"--print-to-pdf={out_pdf}", tmp,
    ], check=True, capture_output=True)
    os.unlink(tmp)


def add_metadata(pdf_path, title, subject, keywords):
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(pdf_path)
    w = PdfWriter()
    for p in r.pages:
        w.add_page(p)
    w.add_metadata({
        "/Title": title, "/Author": D.CONTACT["name"], "/Subject": subject,
        "/Keywords": keywords, "/Creator": "faresamir7.github.io CV builder",
    })
    with open(pdf_path, "wb") as f:
        w.write(f)


def txt_doc(L):
    c = D.CONTACT
    out = [L.name(), L.title(),
           f'{c["email"]} | {c["phone"]} | {c["location"]} | {c["linkedin_label"]} | {c["github_label"]} | {c["website_label"]}',
           "", L.heading("summaryHead", "PROFESSIONAL SUMMARY").upper(), L.summary(),
           "", L.heading("expHead", "EXPERIENCE").upper()]
    for j in L.roles():
        out.append(f'{j["title"]}, {j["company"]} ({j["dates"]}, {j["location"]})')
        for b in j["bullets"]:
            out.append(f'  - {b}')
        out.append("")
    out.append(L.heading("eduHead", "EDUCATION").upper())
    for e in L.education():
        out.append(f'{e["institution"]} ({e["dates"]}, {e["location"]})')
        out.append(f'  {e["degree"]}')
    out.append("")
    out.append(L.heading("certHead", "CERTIFICATIONS").upper())
    for cc in L.certifications():
        note = f' ({cc["note"]})' if cc["note"] else ""
        out.append(f'  - {cc["name"]} | {cc["issuer"]} | {cc["date"]}{note}')
    out.append("")
    out.append(L.heading("skillsHead", "SKILLS").upper())
    for label, vals in L.skills().items():
        out.append(f'  {label}: {", ".join(vals)}')
    out.append("")
    out.append(L.heading("langHead", "LANGUAGES").upper())
    for lg in L.languages():
        out.append(f'  - {lg["language"]}: {lg["level"]}')
    out.append("")
    out.append(L.heading("interestsHead", "INTERESTS").upper())
    out.append("  " + ", ".join(L.interests()))
    return "\n".join(out) + "\n"


KEYWORDS = ("Technical Account Manager, HPE, Aruba, wireless networking, cybersecurity, "
            "ProLiant, Synergy, 3PAR, SAN, Brocade, penetration testing, RADIUS, Python, "
            "network engineering, Tunisia")


def build_lang(lang):
    L = Loc(lang)
    slug = SLUG[lang]
    rtitle = L.heading("resumeTitle", "Resume")
    ctitle = L.heading("cvTitle", "Curriculum Vitae")

    r_pdf = os.path.join(ASSETS, f"Fares-Amir-Hassen-Resume{slug}.pdf")
    render_pdf(build_resume_html(L), r_pdf)
    add_metadata(r_pdf, f"Fares Amir Hassen \u2014 {rtitle}",
                 "Resume of Fares Amir Hassen, Technical Account Manager at HPE", KEYWORDS)

    cv_pdf = os.path.join(ASSETS, f"Fares-Amir-Hassen-CV{slug}.pdf")
    render_pdf(build_cv_html(L), cv_pdf)
    add_metadata(cv_pdf, f"Fares Amir Hassen \u2014 {ctitle}",
                 "Curriculum Vitae of Fares Amir Hassen, Technical Account Manager at HPE", KEYWORDS)

    with open(os.path.join(ASSETS, f"Fares-Amir-Hassen-Resume{slug}.txt"), "w", encoding="utf-8") as f:
        f.write(txt_doc(L))
    with open(os.path.join(ASSETS, f"Fares-Amir-Hassen-CV{slug}.txt"), "w", encoding="utf-8") as f:
        f.write(txt_doc(L))


def json_resume():
    c = D.CONTACT
    data = {
        "$schema": "https://raw.githubusercontent.com/jsonresume/resume-schema/v1.0.0/schema.json",
        "basics": {
            "name": c["name"], "label": c["title"], "email": c["email"],
            "phone": c["phone"], "url": c["website_url"], "summary": D.SUMMARY,
            "location": {"city": "Ariana", "countryCode": "TN", "region": "Tunisia"},
            "profiles": [
                {"network": "LinkedIn", "url": c["linkedin_url"], "username": "fares-amir-hassen"},
                {"network": "GitHub", "url": c["github_url"], "username": "faresamir7"},
            ],
        },
        "work": [
            {"name": j["company"], "position": j["title"], "location": j["location"],
             "startDate": j["dates"].split(" \u2013 ")[0], "endDate": j["dates"].split(" \u2013 ")[1],
             "highlights": j["bullets"]}
            for j in D.EXPERIENCE
        ],
        "education": [
            {"institution": e["institution"], "area": "Network Infrastructure and Data Security",
             "studyType": "Engineer's Degree (Master's level)", "startDate": "2017", "endDate": "2022"}
            for e in D.EDUCATION
        ],
        "certificates": [
            {"name": cc["name"], "issuer": cc["issuer"], "date": cc["date"],
             **({"note": cc["note"]} if cc["note"] else {})}
            for cc in D.CERTIFICATIONS
        ],
        "skills": [{"name": k, "keywords": v} for k, v in D.SKILLS.items()],
        "languages": [{"language": x["language"], "fluency": x["level"]} for x in D.LANGUAGES],
        "interests": [{"name": i} for i in D.INTERESTS],
        "meta": {"availableLanguages": ["en", "fr", "ar", "ja"]},
    }
    return data


def main():
    for lang in ("en", "fr", "ar"):
        build_lang(lang)
        print("Built", lang)
    with open(os.path.join(ASSETS, "resume.json"), "w", encoding="utf-8") as f:
        json.dump(json_resume(), f, indent=2, ensure_ascii=False)
    print("Built resume.json")


if __name__ == "__main__":
    main()
