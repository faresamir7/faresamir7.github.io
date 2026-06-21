#!/usr/bin/env python3
"""Build Resume (1-page) + CV (comprehensive) as PDF, TXT, and JSON Resume.

Outputs to ../assets/. Run from the cv-build/ directory.
PDF rendering uses headless Chromium for accurate, selectable-text output.
"""
import html
import json
import os
import subprocess
import sys
import tempfile

import data as D

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "assets"))
os.makedirs(ASSETS, exist_ok=True)

ACCENT = "#9c1b1b"  # muted professional red (on-brand, print-safe)
INK = "#1a1a1a"
SUB = "#555"

CSS = """
@page { size: A4; margin: 14mm 15mm; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  color: %(INK)s; font-size: 10pt; line-height: 1.42;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
a { color: %(ACCENT)s; text-decoration: none; }
header { border-bottom: 2px solid %(ACCENT)s; padding-bottom: 8px; margin-bottom: 12px; }
h1 { font-size: 22pt; letter-spacing: 0.5px; color: %(INK)s; }
.role { font-size: 11pt; color: %(ACCENT)s; font-weight: 600; margin-top: 2px; }
.contact { font-size: 8.6pt; color: %(SUB)s; margin-top: 6px; }
.contact span { white-space: nowrap; }
.contact .sep { color: #bbb; margin: 0 6px; }
h2 {
  font-size: 10.5pt; text-transform: uppercase; letter-spacing: 1.2px;
  color: %(ACCENT)s; border-bottom: 1px solid #ddd;
  padding-bottom: 3px; margin: 14px 0 8px;
}
.summary { font-size: 9.6pt; color: #333; text-align: justify; }
.job { margin-bottom: 10px; page-break-inside: avoid; }
.job-head { display: flex; justify-content: space-between; align-items: baseline; }
.job-title { font-weight: 700; font-size: 10pt; }
.job-company { color: %(ACCENT)s; font-weight: 600; }
.job-meta { font-size: 8.6pt; color: %(SUB)s; white-space: nowrap; padding-left: 10px; }
ul { list-style: none; margin: 4px 0 0; }
li { position: relative; padding-left: 12px; margin-bottom: 2.5px; font-size: 9.3pt; color: #333; }
li::before { content: "\\2013"; position: absolute; left: 0; color: %(ACCENT)s; }
.edu-item, .cert-item { margin-bottom: 6px; page-break-inside: avoid; }
.edu-degree { font-size: 9.3pt; color: #333; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 2px 24px; }
.skill-row { margin-bottom: 5px; font-size: 9.3pt; }
.skill-label { font-weight: 700; color: %(INK)s; }
.cert-name { font-weight: 600; }
.cert-meta { color: %(SUB)s; font-size: 8.8pt; }
.inline-list { font-size: 9.3pt; color: #333; }
.lang-line { font-size: 9.3pt; }
.lang-line b { color: %(INK)s; }
footer { margin-top: 12px; font-size: 7.6pt; color: #999; text-align: center; border-top: 1px solid #eee; padding-top: 6px; }

/* Compact overrides for the 1-page resume */
body.compact { font-size: 9.4pt; line-height: 1.26; }
body.compact h1 { font-size: 20pt; }
body.compact h2 { margin: 7px 0 4px; font-size: 9.8pt; }
body.compact .summary { font-size: 9pt; }
body.compact header { padding-bottom: 6px; margin-bottom: 9px; }
body.compact .job { margin-bottom: 5px; }
body.compact li { font-size: 8.9pt; margin-bottom: 1px; }
body.compact .edu-item, body.compact .cert-item { margin-bottom: 3px; }
body.compact .skill-row { margin-bottom: 2px; font-size: 8.9pt; }
body.compact .cert-item { font-size: 8.8pt; }
body.compact .cert-meta { font-size: 8.2pt; }
body.compact footer { margin-top: 8px; }
""" % {"INK": INK, "ACCENT": ACCENT, "SUB": SUB}


def esc(s):
    return html.escape(str(s))


def contact_html():
    c = D.CONTACT
    parts = [
        f'<span>{esc(c["email"])}</span>',
        f'<span>{esc(c["phone"])}</span>',
        f'<span>{esc(c["location"])}</span>',
        f'<a href="{c["linkedin_url"]}">{esc(c["linkedin_label"])}</a>',
        f'<a href="{c["github_url"]}">{esc(c["github_label"])}</a>',
        f'<a href="{c["website_url"]}">{esc(c["website_label"])}</a>',
    ]
    return '<span class="sep">|</span>'.join(parts)


def header_html():
    c = D.CONTACT
    return (
        f'<header><h1>{esc(c["name"])}</h1>'
        f'<div class="role">{esc(c["title"])}</div>'
        f'<div class="contact">{contact_html()}</div></header>'
    )


def jobs_html(max_bullets=None):
    out = []
    for j in D.EXPERIENCE:
        bullets = j["bullets"] if max_bullets is None else j["bullets"][:max_bullets]
        lis = "".join(f"<li>{esc(b)}</li>" for b in bullets)
        out.append(
            f'<div class="job"><div class="job-head">'
            f'<div><span class="job-title">{esc(j["title"])}</span>, '
            f'<span class="job-company">{esc(j["company"])}</span></div>'
            f'<div class="job-meta">{esc(j["dates"])} &middot; {esc(j["location"])}</div>'
            f'</div><ul>{lis}</ul></div>'
        )
    return "".join(out)


def edu_html():
    out = []
    for e in D.EDUCATION:
        out.append(
            f'<div class="edu-item"><div class="job-head">'
            f'<div class="job-title">{esc(e["institution"])}</div>'
            f'<div class="job-meta">{esc(e["dates"])} &middot; {esc(e["location"])}</div></div>'
            f'<div class="edu-degree">{esc(e["degree"])}</div></div>'
        )
    return "".join(out)


def certs_html(grid=True):
    items = []
    for c in D.CERTIFICATIONS:
        note = f' <span class="cert-meta">({esc(c["note"])})</span>' if c["note"] else ""
        items.append(
            f'<div class="cert-item"><span class="cert-name">{esc(c["name"])}</span>{note}'
            f'<br><span class="cert-meta">{esc(c["issuer"])} &middot; {esc(c["date"])}</span></div>'
        )
    inner = "".join(items)
    return f'<div class="two-col">{inner}</div>' if grid else inner


def skills_html():
    rows = []
    for label, vals in D.SKILLS.items():
        rows.append(
            f'<div class="skill-row"><span class="skill-label">{esc(label)}:</span> '
            f'{esc(", ".join(vals))}</div>'
        )
    return "".join(rows)


def languages_html():
    return " &nbsp;&middot;&nbsp; ".join(
        f'<b>{esc(l["language"])}</b> ({esc(l["level"])})' for l in D.LANGUAGES
    )


def page(title, body, body_class=""):
    cls = f' class="{body_class}"' if body_class else ""
    return (
        f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        f'<title>{esc(title)}</title><style>{CSS}</style></head>'
        f'<body{cls}>{body}<footer>{esc(D.CONTACT["name"])} &middot; {esc(title)} &middot; '
        f'Generated 2026 &middot; {esc(D.CONTACT["website_label"])}</footer></body></html>'
    )


def build_resume_html():
    # Concise: 1 page. Trim bullets aggressively on older roles.
    body = header_html()
    body += f'<h2>Professional Summary</h2><p class="summary">{esc(D.SUMMARY)}</p>'
    body += '<h2>Experience</h2>'
    # Current role: 4 bullets; Aruba: 3; 3S: 2; older three: 1 each -> fits one page.
    bullet_counts = [4, 3, 2, 1, 1, 1]
    out = []
    for i, j in enumerate(D.EXPERIENCE):
        n = bullet_counts[i] if i < len(bullet_counts) else 1
        lis = "".join(f"<li>{esc(b)}</li>" for b in j["bullets"][:n])
        out.append(
            f'<div class="job"><div class="job-head">'
            f'<div><span class="job-title">{esc(j["title"])}</span>, '
            f'<span class="job-company">{esc(j["company"])}</span></div>'
            f'<div class="job-meta">{esc(j["dates"])} &middot; {esc(j["location"])}</div>'
            f'</div><ul>{lis}</ul></div>'
        )
    body += "".join(out)
    body += '<h2>Education</h2>' + edu_html()
    body += '<h2>Key Skills</h2>' + skills_html()
    body += '<h2>Certifications</h2>' + certs_html(grid=True)
    body += f'<h2>Languages</h2><div class="lang-line">{languages_html()}</div>'
    return page("Resume", body, body_class="compact")


def build_cv_html():
    body = header_html()
    body += f'<h2>Professional Summary</h2><p class="summary">{esc(D.SUMMARY)}</p>'
    body += '<h2>Professional Experience</h2>' + jobs_html()  # all bullets
    body += '<h2>Education</h2>' + edu_html()
    body += '<h2>Certifications</h2>' + certs_html(grid=True)
    body += '<h2>Skills &amp; Expertise</h2>' + skills_html()
    body += f'<h2>Languages</h2><div class="lang-line">{languages_html()}</div>'
    body += f'<h2>Interests</h2><div class="inline-list">{esc(", ".join(D.INTERESTS))}</div>'
    return page("Curriculum Vitae", body)


def render_pdf(html_str, out_pdf):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html_str)
        tmp = f.name
    chromium = next((b for b in ("chromium", "chromium-browser", "google-chrome")
                     if subprocess.run(["which", b], capture_output=True).returncode == 0), None)
    if not chromium:
        sys.exit("No Chromium/Chrome found")
    subprocess.run([
        chromium, "--headless", "--no-sandbox", "--disable-gpu",
        "--no-pdf-header-footer", f"--print-to-pdf={out_pdf}", tmp,
    ], check=True, capture_output=True)
    os.unlink(tmp)


def add_metadata(pdf_path, title, subject, keywords):
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(pdf_path)
    w = PdfWriter()
    for p in r.pages:
        w.add_page(p)
    w.add_metadata({
        "/Title": title,
        "/Author": D.CONTACT["name"],
        "/Subject": subject,
        "/Keywords": keywords,
        "/Creator": "faresamir7.github.io CV builder",
    })
    with open(pdf_path, "wb") as f:
        w.write(f)


# ---- Plain-text companions (AI/ATS friendly) ----

def txt_resume():
    c = D.CONTACT
    L = [c["name"], c["title"],
         f'{c["email"]} | {c["phone"]} | {c["location"]} | {c["linkedin_label"]} | {c["github_label"]} | {c["website_label"]}',
         "", "PROFESSIONAL SUMMARY", D.SUMMARY, "", "EXPERIENCE"]
    for j in D.EXPERIENCE:
        L.append(f'{j["title"]}, {j["company"]} ({j["dates"]}, {j["location"]})')
        for b in j["bullets"]:
            L.append(f'  - {b}')
        L.append("")
    L.append("EDUCATION")
    for e in D.EDUCATION:
        L.append(f'{e["institution"]} ({e["dates"]}, {e["location"]})')
        L.append(f'  {e["degree"]}')
    L.append("")
    L.append("CERTIFICATIONS")
    for cc in D.CERTIFICATIONS:
        note = f' ({cc["note"]})' if cc["note"] else ""
        L.append(f'  - {cc["name"]} | {cc["issuer"]} | {cc["date"]}{note}')
    L.append("")
    L.append("SKILLS")
    for label, vals in D.SKILLS.items():
        L.append(f'  {label}: {", ".join(vals)}')
    L.append("")
    L.append("LANGUAGES")
    for lg in D.LANGUAGES:
        L.append(f'  - {lg["language"]}: {lg["level"]}')
    L.append("")
    L.append("INTERESTS")
    L.append("  " + ", ".join(D.INTERESTS))
    return "\n".join(L) + "\n"


def json_resume():
    """JSON Resume schema (https://jsonresume.org) — machine-readable for AI agents."""
    c = D.CONTACT
    return {
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
        "languages": [{"language": l["language"], "fluency": l["level"]} for l in D.LANGUAGES],
        "interests": [{"name": i} for i in D.INTERESTS],
    }


KEYWORDS = ("Technical Account Manager, HPE, Aruba, wireless networking, cybersecurity, "
            "ProLiant, Synergy, 3PAR, SAN, Brocade, penetration testing, RADIUS, Python, "
            "network engineering, Tunisia")

def main():
    # Resume
    r_pdf = os.path.join(ASSETS, "Fares-Amir-Hassen-Resume.pdf")
    render_pdf(build_resume_html(), r_pdf)
    add_metadata(r_pdf, "Fares Amir Hassen \u2014 Resume",
                 "Resume of Fares Amir Hassen, Technical Account Manager at HPE", KEYWORDS)
    with open(os.path.join(ASSETS, "Fares-Amir-Hassen-Resume.txt"), "w") as f:
        f.write(txt_resume())

    # CV
    cv_pdf = os.path.join(ASSETS, "Fares-Amir-Hassen-CV.pdf")
    render_pdf(build_cv_html(), cv_pdf)
    add_metadata(cv_pdf, "Fares Amir Hassen \u2014 Curriculum Vitae",
                 "Curriculum Vitae of Fares Amir Hassen, Technical Account Manager at HPE", KEYWORDS)
    with open(os.path.join(ASSETS, "Fares-Amir-Hassen-CV.txt"), "w") as f:
        f.write(txt_resume())  # same comprehensive text content

    # JSON Resume (machine-readable)
    with open(os.path.join(ASSETS, "resume.json"), "w") as f:
        json.dump(json_resume(), f, indent=2, ensure_ascii=False)

    print("Built:", os.listdir(ASSETS))


if __name__ == "__main__":
    main()
