# CV / Resume build

Single source of truth for Fares Amir Hassen's Resume and CV, plus machine-readable
companions for AI agents and ATS systems.

## Files

- `data.py` — all content (contact, experience, education, certs, skills, languages).
  **Edit this**, never the generated files.
- `build.py` — renders the documents.

## Outputs (written to `../assets/`)

| File | Purpose |
|------|---------|
| `Fares-Amir-Hassen-Resume.pdf` | 1-page concise resume (European norm) |
| `Fares-Amir-Hassen-CV.pdf` | 2-page comprehensive CV (European norm) |
| `Fares-Amir-Hassen-Resume.txt` | Plain-text resume (AI/ATS friendly) |
| `Fares-Amir-Hassen-CV.txt` | Plain-text CV |
| `resume.json` | [JSON Resume schema](https://jsonresume.org) — structured data for AI agents |

All PDFs have selectable text (not images) and embedded metadata (title, author, keywords)
for parsing. The website links `resume.json` via `<link rel="alternate" type="application/json">`
and embeds JSON-LD `Person` schema in `index.html`.

## Rebuild

Requires a headless Chromium/Chrome and `pypdf`.

```bash
python3 -m venv .venv && .venv/bin/pip install pypdf
.venv/bin/python build.py
```

Timeline data follows the LinkedIn-generated resume. Street address and photo are
intentionally omitted from the public PDFs (privacy + 2026 anti-bias norms).
