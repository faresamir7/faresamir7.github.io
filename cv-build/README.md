# CV / Resume build

Single source of truth for Fares Amir Hassen's Resume and CV, plus machine-readable
companions for AI agents and ATS systems.

## Files

- `data.py` — all content (contact, experience, education, certs, skills, languages).
  **Edit this**, never the generated files.
- `build.py` — renders the documents.

## Outputs (written to `../assets/`)

Localized Resume + CV in English, French, Arabic (RTL), plus the two
traditional Japanese-market documents.

| File | Purpose |
|------|---------|
| `Fares-Amir-Hassen-Resume.pdf` / `-FR` / `-AR` | 1-page concise resume (EN/FR/AR) |
| `Fares-Amir-Hassen-CV.pdf` / `-FR` / `-AR` | 2-page comprehensive CV (EN/FR/AR) |
| `Fares-Amir-Hassen-Rirekisho-JA.pdf` | 履歴書 — traditional Japanese resume form |
| `Fares-Amir-Hassen-Shokumu-Keirekisho-JA.pdf` | 職務経歴書 — Japanese career-history document |
| `*-Resume*.txt` / `*-CV*.txt` | Plain-text (AI/ATS friendly) |
| `resume.json` | [JSON Resume schema](https://jsonresume.org) — structured data for AI agents |

Content lives in `data.py` (English source of truth) and `translations.py`
(FR/AR). Japanese is authored directly in `build_ja.py` because the format differs.

## Rebuild

Requires a headless Chromium/Chrome and `pypdf`.

```bash
python3 -m venv .venv && .venv/bin/pip install pypdf
.venv/bin/python build.py       # EN/FR/AR resume+CV + resume.json
.venv/bin/python build_ja.py    # 履歴書 + 職務経歴書
```

Timeline data follows the LinkedIn-generated resume. Street address and photo are
intentionally omitted from the public PDFs (privacy + 2026 anti-bias norms).
