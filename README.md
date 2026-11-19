# Trepte

Zece ani de recenzii din Rafturi și Sublinieri, 2016–2026, an de an: ce am citit, cum am scris și la ce a folosit scrisul.

Pagina: https://ducu.github.io/trepte/

## Cum e făcut

- `template.html` — textul și designul paginii. Aici se scrie analiza, an de an.
- `build.py` — pune în pagină raftul cu coperți și cifrele fiecărui an și scrie `index.html`. Citește datele din repo-urile vecine, `../rafturi/data/books.json` și `../sublinieri/entries/`, deci rulează doar local, cu toate trei alături.
- `covers/` — coperțile cărților, copiate din Rafturi de `build.py`.
- `index.html` — pagina generată, publicată ca atare pe GitHub Pages.

După o modificare în `template.html`:

```
python3 build.py
git commit -am "…" && git push
```
