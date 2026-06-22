#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Japanese-market documents:
  - 履歴書 (rirekisho)  — traditional standardized form
  - 職務経歴書 (shokumu-keirekisho) — career-history document

Built to Japanese conventions: 西暦 (Western years), chronological 学歴→職歴
ending with 現在に至る / 以上, a 免許・資格 table, and a 自己PR section.
Outputs to ../assets/. Uses headless Chromium + Noto Sans JP.
"""
import html
import os
import subprocess
import sys
import tempfile

import data as D

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "assets"))
os.makedirs(ASSETS, exist_ok=True)

NAME_JA = "ファレス・アミール・ハッセン"
NAME_FURIGANA = "ファレス アミール ハッセン"
NAME_LATIN = "Fares Amir Hassen"

FONT = "https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap"

# 学歴 (education) — chronological, oldest first
GAKUREKI = [
    ("2017", "9", "ESPRIT（エコール・スペリュール・プリヴェ・ダンジェニエリ・エ・ド・テクノロジ） 入学"),
    ("2022", "6", "ESPRIT ネットワークインフラ・データセキュリティ専攻 エンジニア課程 修了"),
]

# 職歴 (work history) — chronological, oldest first
SHOKUREKI = [
    ("2022", "3", "3S Standard Sharing Software 入社（ネットワークセキュリティ インターン）"),
    ("2022", "9", "契約期間満了により退職"),
    ("2023", "3", "HPE Aruba Networking 入社（ワイヤレスネットワークエンジニア）"),
    ("2025", "12", "一身上の都合により退職"),
    ("2026", "1", "Hewlett Packard Enterprise 入社（テクニカルアカウントマネージャー）"),
    ("", "", "現在に至る"),
]

# 免許・資格 (licenses & qualifications) — chronological
SHIKAKU = [
    ("2020", "11", "Google IT インフラストラクチャ・システム管理 修了証"),
    ("2021", "11", "Palo Alto Networks CIC NIST/NICE 認定"),
    ("2022", "12", "TryHackMe Jr Penetration Tester ラーニングパス 修了"),
    ("2023", "1", "CompTIA Network+ ce 取得（2026年1月 有効期限満了）"),
]

JIKO_PR = (
    "Hewlett Packard Enterprise のテクニカルアカウントマネージャーとして、ワイヤレス"
    "ネットワーク、ストレージ、サイバーセキュリティの幅広い技術領域で顧客を支援しています。"
    "Aruba ネットワーク機器の運用・トラブルシューティングからエンタープライズインフラ"
    "（HPE ProLiant、Synergy、3PAR、HPE/Brocade SAN スイッチ、HPE/Aruba スイッチ）の"
    "サポートまで、深い技術的知見を有します。顧客と HPE エンジニアリングの架け橋として、"
    "複雑な技術課題を明確でプロアクティブな成果へと変換することを得意としています。"
)

# 職務経歴書 — detailed roles (newest first)
CAREER = [
    {
        "company": "Hewlett Packard Enterprise",
        "period": "2026年1月 – 現在",
        "role": "テクニカルアカウントマネージャー",
        "bullets": [
            "アカウントにおける信頼されるテクニカルアドバイザー兼 HPE の主要窓口として、エスカレーションから解決まで技術的な関係を担当。",
            "契約済みのプロアクティブサポートサービスの提供を管理し、サービス改善を計画、定義された成果物に責任を負う。",
            "HPE ProLiant サーバー、Synergy コンポーザブルインフラ、3PAR ストレージにわたるマルチテクノロジーサポートを提供。",
            "HPE/Brocade SAN スイッチで構築された SAN ファブリックのトラブルシューティングと保守を実施。",
            "HPE および Aruba スイッチによるエンタープライズキャンパスネットワークを支援。",
        ],
    },
    {
        "company": "HPE Aruba Networking",
        "period": "2023年3月 – 2025年12月",
        "role": "ワイヤレスネットワークエンジニア",
        "bullets": [
            "Aruba モビリティコントローラー、マスター、アクセスポイントに関わる問題を全 OSI 層で診断。",
            "セキュアなワイヤレスアクセスのため最新の RADIUS 認証プロトコルを実装・構成。",
            "Aruba 機器のファームウェアアップグレードを実施し、最適な性能とセキュリティを確保。",
            "Aruba AOS 製品のリモート技術サポートを提供し、ログ分析を通じて接続問題を解決。",
            "AirWave・Central を活用し、エンタープライズ環境で Aruba Instant AP を構成。",
        ],
    },
    {
        "company": "3S Standard Sharing Software",
        "period": "2022年3月 – 2022年9月",
        "role": "ネットワークセキュリティ インターン",
        "bullets": [
            "エンタープライズネットワークノードを集中管理するモジュール式 Python Flask ウェブプラットフォームを開発。",
            "Cisco API 連携を自動化し、ネットワークインフラの一括構成を実現。",
            "セキュアな認証およびユーザーロール管理機能を、統合データベースとともに開発。",
        ],
    },
    {
        "company": "OXAHOST",
        "period": "2021年6月 – 2021年7月",
        "role": "ネットワーク技術 インターン",
        "bullets": [
            "チュニジアで唯一の CentOS ミラーを構築。",
            "新しいウェブサイトと Zimbra・cPanel を含むサービスのペネトレーションテストを実施し、セキュリティを強化。",
        ],
    },
    {
        "company": "BIAT",
        "period": "2019年8月 – 2020年9月（夏季インターン）",
        "role": "IT インターン",
        "bullets": [
            "ネットワークインフラの設計・保守・トラブルシューティングを支援。",
            "脆弱性評価とペネトレーションテストを支援し、セキュリティツール（IDS/IPS、ファイアウォール）を構成・管理。",
        ],
    },
]

SKILLS_JA = {
    "技術": "HPE ProLiant、HPE Synergy、HPE 3PAR、HPE/Brocade SAN スイッチ、HPE/Aruba スイッチ、Aruba AOS 8、Aruba Instant AP、Cisco、RADIUS、Python、シェルスクリプト、Wireshark",
    "領域": "ワイヤレスネットワーク設計、RF 技術・カバレッジ計画、ネットワークトラブルシューティング（全 OSI 層）、SAN/ストレージインフラ、サーバー展開、サイバーセキュリティ・ペネトレーションテスト、パケット解析、自動化、認証",
    "言語": "アラビア語（母語）、英語（バイリンガル）、フランス語（ビジネスレベル）、日本語（初級・会話）",
}


def esc(s):
    return html.escape(str(s))


BASE_CSS = """
@import url('%(FONT)s');
@page { size: A4; margin: 12mm 13mm; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Noto Sans JP', sans-serif; color: #111; font-size: 9.2pt; line-height: 1.5; }
.doc-title { font-size: 18pt; font-weight: 700; letter-spacing: 0.5em; text-align: center; margin-bottom: 2mm; }
.doc-date { text-align: right; font-size: 8.5pt; margin-bottom: 3mm; }
table { border-collapse: collapse; width: 99.6%%; margin: 0 auto; border: 0.9pt solid #333; }
td, th { border: 0.7pt solid #555; padding: 2mm 2.5mm; vertical-align: top; }
.label { background: #f0f0f0; font-weight: 500; white-space: nowrap; width: 22mm; }
.section-band { background: #e9e9e9; font-weight: 700; text-align: center; }
.yr { width: 14mm; text-align: center; white-space: nowrap; }
.mo { width: 10mm; text-align: center; white-space: nowrap; }
.right { text-align: right; }
.photo-box { width: 30mm; height: 40mm; border: 0.5pt solid #444; text-align: center;
             font-size: 7.5pt; color: #999; display: flex; align-items: center; justify-content: center; }
.furigana { font-size: 7pt; color: #555; }
.name-lg { font-size: 15pt; font-weight: 700; }
.muted { color: #666; font-size: 8pt; }
h2.k { font-size: 11pt; font-weight: 700; border-left: 4pt solid #9c1b1b; padding-left: 3mm;
       margin: 5mm 0 2.5mm; }
.career-block { margin-bottom: 4mm; page-break-inside: avoid; }
.career-head { display: flex; justify-content: space-between; border-bottom: 0.5pt solid #444;
               padding-bottom: 1mm; margin-bottom: 1.5mm; }
.career-co { font-weight: 700; font-size: 10pt; }
.career-role { color: #9c1b1b; font-weight: 500; }
.career-period { color: #555; font-size: 8.5pt; white-space: nowrap; }
ul { list-style: none; margin-top: 1mm; }
li { padding-left: 4mm; position: relative; margin-bottom: 0.8mm; }
li::before { content: "・"; position: absolute; left: 0; color: #9c1b1b; }
.pr-box { border: 0.5pt solid #444; padding: 3mm; line-height: 1.7; }
footer { margin-top: 4mm; text-align: center; font-size: 7pt; color: #999; }
""" % {"FONT": FONT}


def rows(items, end_marker=None):
    out = []
    for yr, mo, desc in items:
        out.append(f'<tr><td class="yr">{esc(yr)}</td><td class="mo">{esc(mo)}</td>'
                   f'<td>{esc(desc)}</td></tr>')
    if end_marker:
        out.append(f'<tr><td class="yr"></td><td class="mo"></td>'
                   f'<td class="right">{esc(end_marker)}</td></tr>')
    return "".join(out)


def build_rirekisho():
    c = D.CONTACT
    body = '<div class="doc-title">履歴書</div>'
    body += '<div class="doc-date">2026年6月 現在</div>'

    # Personal info block with photo
    body += '<table>'
    body += (
        '<tr>'
        f'<td class="label">ふりがな</td><td>{esc(NAME_FURIGANA)}</td>'
        '<td rowspan="5" style="width:32mm"><div class="photo-box">写真貼付</div></td></tr>'
        f'<tr><td class="label">氏名</td><td><span class="name-lg">{esc(NAME_JA)}</span>'
        f'<br><span class="muted">{esc(NAME_LATIN)}</span></td></tr>'
        '<tr><td class="label">生年月日</td><td>　年　月　日</td></tr>'
        f'<tr><td class="label">住所</td><td>チュニジア アリアナ（Ariana, Tunisia）</td></tr>'
        f'<tr><td class="label">連絡先</td><td>'
        f'TEL: {esc(c["phone"])}　/　Email: {esc(c["email"])}<br>'
        f'{esc(c["linkedin_label"])}　/　{esc(c["website_label"])}</td></tr>'
    )
    body += '</table>'

    # 学歴・職歴 table
    body += '<h2 class="k">学歴・職歴</h2>'
    body += '<table>'
    body += '<tr><th class="yr">年</th><th class="mo">月</th><th>学歴・職歴</th></tr>'
    body += '<tr><td class="yr"></td><td class="mo"></td><td class="section-band">学歴</td></tr>'
    body += rows(GAKUREKI)
    body += '<tr><td class="yr"></td><td class="mo"></td><td class="section-band">職歴</td></tr>'
    body += rows(SHOKUREKI, end_marker="以上")
    body += '</table>'

    # 免許・資格
    body += '<h2 class="k">免許・資格</h2>'
    body += '<table>'
    body += '<tr><th class="yr">年</th><th class="mo">月</th><th>免許・資格</th></tr>'
    body += rows(SHIKAKU, end_marker="以上")
    body += '</table>'

    # 自己PR
    body += '<h2 class="k">自己PR</h2>'
    body += f'<div class="pr-box">{esc(JIKO_PR)}</div>'

    body += f'<footer>{esc(NAME_LATIN)} ・ 履歴書 ・ {esc(c["website_label"])}</footer>'
    return wrap("履歴書", body)


def build_shokumu():
    c = D.CONTACT
    body = '<div class="doc-title">職務経歴書</div>'
    body += '<div class="doc-date">2026年6月 現在</div>'
    body += f'<div style="text-align:right;margin-bottom:3mm">{esc(NAME_JA)}（{esc(NAME_LATIN)}）</div>'

    body += '<h2 class="k">職務要約</h2>'
    body += f'<div class="pr-box">{esc(JIKO_PR)}</div>'

    body += '<h2 class="k">職務経歴</h2>'
    for j in CAREER:
        lis = "".join(f'<li>{esc(b)}</li>' for b in j["bullets"])
        body += (
            f'<div class="career-block"><div class="career-head">'
            f'<div><span class="career-co">{esc(j["company"])}</span>　'
            f'<span class="career-role">{esc(j["role"])}</span></div>'
            f'<div class="career-period">{esc(j["period"])}</div></div>'
            f'<ul>{lis}</ul></div>'
        )

    body += '<h2 class="k">活かせる経験・スキル</h2>'
    body += '<table>'
    for k, v in SKILLS_JA.items():
        body += f'<tr><td class="label">{esc(k)}</td><td>{esc(v)}</td></tr>'
    body += '</table>'

    body += '<h2 class="k">学歴</h2>'
    body += ('<div class="pr-box" style="border:none;padding:0">'
             'ESPRIT（エコール・スペリュール・プリヴェ・ダンジェニエリ・エ・ド・テクノロジ）<br>'
             'エンジニア課程（修士相当）／ ネットワークインフラ・データセキュリティ専攻　2017年 – 2022年</div>')

    body += '<div class="right" style="margin-top:4mm">以上</div>'
    body += f'<footer>{esc(NAME_LATIN)} ・ 職務経歴書 ・ {esc(c["website_label"])}</footer>'
    return wrap("職務経歴書", body)


def wrap(title, body):
    return (f'<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">'
            f'<title>{esc(title)} - {esc(NAME_LATIN)}</title><style>{BASE_CSS}</style></head>'
            f'<body>{body}</body></html>')


def render_pdf(html_str, out_pdf):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html_str)
        tmp = f.name
    chromium = next((b for b in ("chromium", "chromium-browser", "google-chrome")
                     if subprocess.run(["which", b], capture_output=True).returncode == 0), None)
    if not chromium:
        sys.exit("No Chromium/Chrome found")
    subprocess.run([chromium, "--headless", "--no-sandbox", "--disable-gpu",
                    "--no-pdf-header-footer", "--virtual-time-budget=8000",
                    f"--print-to-pdf={out_pdf}", tmp], check=True, capture_output=True)
    os.unlink(tmp)


def add_metadata(pdf_path, title):
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(pdf_path)
    w = PdfWriter()
    for p in r.pages:
        w.add_page(p)
    w.add_metadata({"/Title": title, "/Author": NAME_LATIN,
                    "/Subject": "Japanese-market career document",
                    "/Keywords": "履歴書, 職務経歴書, テクニカルアカウントマネージャー, HPE, Aruba, ネットワーク, Fares Amir Hassen",
                    "/Creator": "faresamir7.github.io CV builder"})
    with open(pdf_path, "wb") as f:
        w.write(f)


def main():
    r = os.path.join(ASSETS, "Fares-Amir-Hassen-Rirekisho-JA.pdf")
    render_pdf(build_rirekisho(), r)
    add_metadata(r, "ファレス・アミール・ハッセン — 履歴書")

    s = os.path.join(ASSETS, "Fares-Amir-Hassen-Shokumu-Keirekisho-JA.pdf")
    render_pdf(build_shokumu(), s)
    add_metadata(s, "ファレス・アミール・ハッセン — 職務経歴書")
    print("Built JA: 履歴書 + 職務経歴書")


if __name__ == "__main__":
    main()
