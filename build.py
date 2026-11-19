#!/usr/bin/env python3
"""Builds index.html from template.html with per-year stats and cover shelves,
using ../rafturi/data/books.json and ../sublinieri/entries/."""
import html, json, os, re, shutil
from email.utils import parsedate_to_datetime

HERE = os.path.dirname(os.path.abspath(__file__))
RAFTURI = os.path.join(HERE, '..', 'rafturi')
SUBLINIERI = os.path.join(HERE, '..', 'sublinieri', 'entries')

data = json.load(open(os.path.join(RAFTURI, 'data', 'books.json')))
by_id = {b['book_id']: b for b in data['read'] + data['currently']}
years = sorted(data['years'])
quotes = {}
for f in os.listdir(SUBLINIERI):
    if f.endswith('.md'):
        quotes[f[:4]] = quotes.get(f[:4], 0) + 1

def words(b):
    return len(re.sub('<[^>]+>', ' ', b['user_review']).split())

os.makedirs(os.path.join(HERE, 'covers'), exist_ok=True)
rows = {}
shelves = {}
for y in years:
    books = [by_id[i] for i in data['years'][y] if i in by_id]
    books.sort(key=lambda b: parsedate_to_datetime(b['user_read_at'].strip()).timestamp() if b['user_read_at'].strip() else 0)
    reviewed = [b for b in books if b['user_review'].strip()]
    w = sum(words(b) for b in reviewed)
    rows[y] = dict(books=len(books), reviewed=len(reviewed), words=w, quotes=quotes.get(y, 0))
    # covers grouped by rating, best first; read order inside each group
    groups = {}
    for b in books:
        src = os.path.join(RAFTURI, 'covers', b['book_id'] + '.jpg')
        if not os.path.exists(src):
            continue
        shutil.copyfile(src, os.path.join(HERE, 'covers', b['book_id'] + '.jpg'))
        stars = int(b['user_rating'] or 0)
        t = html.escape(f"{b['title']} — {b['author_name']}", quote=True)
        groups.setdefault(stars, []).append(f'<img src="covers/{b["book_id"]}.jpg" alt="{t}" title="{t}" loading="lazy">')
    parts = []
    for stars in sorted(groups, reverse=True):
        label = '★' * stars + '<span class="off">' + '★' * (5 - stars) + '</span>' if stars else 'fără stele'
        aria = f'{stars} stele' if stars else 'fără stele'
        parts.append(f'<div class="shelf-group" aria-label="{aria}"><span class="stars">{label}</span>'
                     f'<div class="covers">{"".join(groups[stars])}</div></div>')
    shelves[y] = '<div class="shelf" aria-label="Cărți citite în ' + y + '">' + ''.join(parts) + '</div>'

def num(n):
    return f'{n:,}'.replace(',', '.')

def stats(y):
    r = rows[y]
    return (f'<p class="stats"><b>{r["books"]}</b> cărți · <b>{r["reviewed"]}</b> recenzii · '
            f'<b>{num(r["words"])}</b> cuvinte · <b>{r["quotes"]}</b> sublinieri</p>')

out = open(os.path.join(HERE, 'template.html')).read()
for y in years:
    out = out.replace(f'<!--STATS:{y}-->', stats(y)).replace(f'<!--SHELF:{y}-->', shelves[y])
open(os.path.join(HERE, 'index.html'), 'w').write(out)
print({y: (r['books'], r['words']) for y, r in rows.items()})
