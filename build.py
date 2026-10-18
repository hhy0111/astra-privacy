"""Build the static privacy page with Python 3; no third-party packages."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
policy = json.loads((ROOT / "policy.json").read_text(encoding="utf-8"))
escape = html.escape
sections = []
toc = []
plain = [policy["app"], policy["title"], policy["scope"], policy["summary"]]
for section in policy["sections"]:
    sid = escape(section["id"], quote=True)
    title = escape(section["title"])
    toc.append(f'<li><a href="#{sid}">{title}</a></li>')
    paragraphs = "".join(f'<p>{escape(p)}</p>' for p in section["paragraphs"])
    links = "".join(f'<li><a href="{escape(link["url"], quote=True)}">{escape(link["label"])}</a></li>' for link in section.get("links", []))
    sections.append(f'<section id="{sid}"><h2>{title}</h2>{paragraphs}' + (f'<ul>{links}</ul>' if links else '') + '</section>')
    plain.extend(["", section["title"], *section["paragraphs"]])
    plain.extend(f'{link["label"]}: {link["url"]}' for link in section.get("links", []))
page = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<meta name="referrer" content="no-referrer">
<meta name="description" content="{escape(policy['app'])}의 개인정보처리방침. 게임 데이터, 고객지원 정보의 이용과 삭제 방법을 안내합니다.">
<title>{escape(policy['title'])} | {escape(policy['app'])}</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<a class="skip" href="#policy">본문 바로가기</a>
<header><div class="wrap"><p class="brand">ASTRA <span>HEIRS OF THE STARS</span></p>
<p class="app">{escape(policy['app'])}</p><h1>{escape(policy['title'])}</h1>
<p class="meta">{escape(policy['operator'])} · 시행일 {escape(policy['effective_date'])}</p></div></header>
<main id="policy" class="wrap">
<aside class="summary" aria-label="주요 내용"><strong>개인정보 처리 안내</strong><p>{escape(policy['summary'])}</p></aside>
<p>{escape(policy['scope'])}</p><p class="package">앱 식별자: {escape(policy['package'])}</p>
<nav aria-label="방침 목차"><h2>목차</h2><ol>{''.join(toc)}</ol></nav>
{''.join(sections)}
<div class="contact"><h2>개인정보 문의</h2><p>{escape(policy['operator'])}</p><a href="mailto:{escape(policy['email'], quote=True)}">{escape(policy['email'])}</a></div>
</main>
<footer class="wrap"><p>© 2026 {escape(policy['operator'])} · {escape(policy['app'])}</p><a href="privacy-policy.txt">텍스트 원문 보기</a><a href="#policy">본문 맨 위로</a></footer>
</body></html>
'''
(ROOT / "index.html").write_text(page, encoding="utf-8", newline="\n")
(ROOT / "privacy-policy.txt").write_text("\n\n".join(plain) + "\n", encoding="utf-8", newline="\n")
print("Built index.html and privacy-policy.txt")
