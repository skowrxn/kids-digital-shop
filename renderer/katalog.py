#!/usr/bin/env python3
"""Wyciąga dane produktów z prototypu web/mockup/ do produkty/_katalog.json.

Prototyp jest JEDYNYM źródłem prawdy o katalogu: tytuł, podtytuł, cena, wiek,
liczba stron, autor, kategoria, podkategoria. Ten skrypt nigdy nic nie wymyśla —
czego nie ma w mockupie, zostaje jako null i ląduje w sekcji "braki".

Priorytet źródeł dla jednego produktu:
  p-<slug>.html  (pełne dane: .specs, opis, podtytuł, okruszki)
  index.html / katalog.html / k-*.html  (karta: tytuł, wiek, autor, cena)

Uruchom:  python3 renderer/katalog.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOCKUP = ROOT / "web" / "mockup"
OUT = ROOT / "produkty" / "_katalog.json"


def txt(html):
    """HTML -> goły tekst, encje rozwinięte, białe znaki zwinięte."""
    s = re.sub(r"<[^>]+>", " ", html)
    for a, b in [("&nbsp;", " "), ("&amp;", "&"), ("&mdash;", "—"),
                 ("&ndash;", "–"), ("&quot;", '"'), ("&#39;", "'"),
                 ("&lt;", "<"), ("&gt;", ">")]:
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()


def parse_karty(html):
    """Karty produktów z dowolnej strony listingowej."""
    found = {}
    for m in re.finditer(r'<a class="card[^"]*" href="p-([a-z0-9-]+)\.html">(.*?)</a>',
                         html, re.S):
        slug, body = m.group(1), m.group(2)
        d = {}
        for key, pat in [("tytul", r'card__title">(.*?)</span>'),
                         ("meta", r'card__meta">(.*?)</span>'),
                         ("cena_raw", r'card__price[^"]*">(.*?)</span>'),
                         ("badge", r'card__badge[^"]*">(.*?)</span>'),
                         ("ocena_raw", r'card__rate[^"]*">(.*?)</span>')]:
            mm = re.search(pat, body, re.S)
            if mm:
                d[key] = txt(mm.group(1))
        # meta ma postać "5–7 lat · Marta Zielińska"
        if "·" in d.get("meta", ""):
            wiek, autor = d.pop("meta").split("·", 1)
            d["wiek"] = wiek.strip()
            d["autor"] = autor.strip()
        if d.get("cena_raw"):
            c = re.search(r"(\d+)", d["cena_raw"].replace(" ", " "))
            d["cena_pln"] = int(c.group(1)) if c else None
        if d.get("ocena_raw"):
            o = re.search(r"([\d,]+)\s*\((\d+)\)", d["ocena_raw"])
            if o:
                d["ocena"] = float(o.group(1).replace(",", "."))
                d["opinie"] = int(o.group(2))
        d["w_klubie"] = d.get("badge") == "W Klubie"
        d["darmowy_fragment_na_karcie"] = d.get("badge") == "Darmowy fragment"
        for k in ("cena_raw", "ocena_raw", "badge"):
            d.pop(k, None)
        # scalamy: wygrywa wariant z większą liczbą pól
        if slug not in found or len(d) > len(found[slug]):
            found[slug] = d
    return found


def parse_kategorie(html):
    """data-cat -> {nazwa, opis, podkategorie[], slugi_w_menu[]}"""
    cats = {}
    for m in re.finditer(
            r'<div class="mega__panel" data-cat="([a-z]+)">(.*?)'
            r'(?=<div class="mega__panel"|<section|<main|\Z)', html, re.S):
        cat, body = m.group(1), m.group(2)
        h3 = re.search(r"<h3>(.*?)</h3>", body, re.S)
        p = re.search(r"<p>(.*?)</p>", body, re.S)
        cats[cat] = {
            "nazwa": txt(h3.group(1)) if h3 else None,
            "opis": txt(p.group(1)) if p else None,
            "podkategorie": [{"id": a, "nazwa": txt(b)} for a, b in
                             re.findall(r'k-[a-z]+\.html#([a-z-]+)">([^<]+)</a>', body)],
            "slugi_w_menu": re.findall(r'card[^"]*" href="p-([a-z0-9-]+)\.html"', body),
        }
        n = re.search(r"Zobacz (\d+) materia", body)
        cats[cat]["deklarowana_liczba_produktow"] = int(n.group(1)) if n else None
    return cats


def parse_strona_produktu(html):
    """Pełne dane z p-<slug>.html. Zwraca tylko to, co faktycznie znalazł."""
    d = {}
    h1 = re.search(r'class="[^"]*\bh1\b[^"]*"[^>]*>(.*?)</h1>', html, re.S) \
        or re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if h1:
        d["tytul"] = txt(h1.group(1))
    sub = re.search(r'class="[^"]*(?:lede|prod__sub)[^"]*"[^>]*>(.*?)</p>', html, re.S)
    if sub:
        d["podtytul"] = txt(sub.group(1))

    # tabela .specs -> klucz: wartość  (m.in. „Objętość")
    specs = {}
    sm = re.search(r'class="specs"[^>]*>(.*?)</(?:table|dl|ul|div)>', html, re.S)
    if sm:
        blok = sm.group(1)
        pary = re.findall(r"<(?:dt|th)[^>]*>(.*?)</(?:dt|th)>\s*"
                          r"<(?:dd|td)[^>]*>(.*?)</(?:dd|td)>", blok, re.S)
        if not pary:
            pary = re.findall(r'<span[^>]*>(.*?)</span>\s*<span[^>]*>(.*?)</span>',
                              blok, re.S)
        specs = {txt(k).rstrip(":").lower(): txt(v) for k, v in pary}
    if specs:
        d["specs"] = specs
        for klucz in ("objętość", "objetosc", "liczba stron", "stron"):
            if klucz in specs:
                n = re.search(r"(\d+)", specs[klucz])
                if n:
                    d["strony"] = int(n.group(1))
                break

    okr = re.findall(r'<a[^>]*href="k-([a-z]+)\.html(?:#([a-z-]+))?"', html)
    if okr:
        d["kategoria"] = okr[0][0]
        if okr[0][1]:
            d["podkategoria"] = okr[0][1]

    dk = re.search(r'class="[^"]*(?:forwhom|dla-kogo|prod__who)[^"]*"[^>]*>(.*?)</', html, re.S)
    if dk:
        d["dla_kogo"] = txt(dk.group(1))

    op = re.search(r'class="[^"]*prod__desc[^"]*"[^>]*>(.*?)</div>', html, re.S)
    if op:
        akapity = [txt(x) for x in re.findall(r"<p[^>]*>(.*?)</p>", op.group(1), re.S)]
        if akapity:
            d["opis_akapity"] = akapity
    return d


def main():
    if not MOCKUP.exists():
        sys.exit(f"BŁĄD: brak {MOCKUP}")

    karty, kategorie = {}, {}
    listingi = sorted(MOCKUP.glob("index.html")) + sorted(MOCKUP.glob("katalog.html")) \
        + sorted(MOCKUP.glob("k-*.html"))
    for f in listingi:
        html = f.read_text(encoding="utf-8")
        for slug, d in parse_karty(html).items():
            if slug not in karty or len(d) > len(karty[slug]):
                karty[slug] = d
        kategorie.update({k: v for k, v in parse_kategorie(html).items()
                          if k not in kategorie})

    # przypisanie kategorii na podstawie menu kategorii
    for cat, meta in kategorie.items():
        for slug in meta["slugi_w_menu"]:
            karty.setdefault(slug, {}).setdefault("kategoria", cat)

    # strony produktowe nadpisują dane z kart — są dokładniejsze
    strony_produktowe = sorted(MOCKUP.glob("p-*.html"))
    for f in strony_produktowe:
        slug = f.stem[2:]
        karty.setdefault(slug, {}).update(parse_strona_produktu(f.read_text(encoding="utf-8")))

    produkty = {s: dict(sorted(d.items())) for s, d in sorted(karty.items())}

    braki = {
        "produktow_znalezionych": len(produkty),
        "produktow_oczekiwanych": sum(
            (m.get("deklarowana_liczba_produktow") or 0) for m in kategorie.values()) or None,
        "brak_stron_p_html": sorted(
            s for s in produkty if not (MOCKUP / f"p-{s}.html").exists()),
        "brak_liczby_stron": sorted(s for s, d in produkty.items() if "strony" not in d),
        "brak_kategorii": sorted(s for s, d in produkty.items() if "kategoria" not in d),
        "brak_podkategorii": sorted(s for s, d in produkty.items() if "podkategoria" not in d),
        "brakujace_pliki_listingu": [n for n in ("katalog.html",)
                                     if not (MOCKUP / n).exists()],
        "brakujace_strony_kategorii": [f"k-{c}.html" for c in sorted(kategorie)
                                       if not (MOCKUP / f"k-{c}.html").exists()],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(
        {"zrodlo": "web/mockup/", "kategorie": kategorie,
         "produkty": produkty, "braki": braki},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Zapisano {OUT.relative_to(ROOT)}")
    print(f"  kategorii: {len(kategorie)}   produktów: {len(produkty)}")
    print(f"  stron p-*.html w mockupie: {len(strony_produktowe)}")
    for k, v in braki.items():
        if isinstance(v, list) and v:
            print(f"  BRAK {k}: {len(v)} -> {', '.join(v[:6])}"
                  f"{' …' if len(v) > 6 else ''}")


if __name__ == "__main__":
    main()
