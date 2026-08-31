#!/usr/bin/env python3
"""Wyciąga dane produktów z prototypu web/mockup/ do produkty/_katalog.json.

Prototyp jest JEDYNYM źródłem prawdy o katalogu. Ten skrypt nigdy nic nie
wymyśla i niczego nie wnioskuje z tytułu — czego nie ma w mockupie, zostaje
jako null i ląduje w sekcji "braki".

Podział ról:
  katalog.html   → KOMPLETNA lista 48 produktów. index.html pokazuje tylko
                   wybrane półki (42 z 48) i NIE nadaje się na listę wejściową.
  p-<slug>.html  → wszystkie szczegóły jednego produktu
  k-<cat>.html   → nazwy kategorii i pełne listy podkategorii

Dwie pułapki prototypu, obie obsłużone:

1. Mega-menu siedzi w nagłówku KAŻDEJ strony i niesie 36 kart produktowych.
   Naiwne zliczanie kart w katalog.html daje 84, nie 48 — deduplikujemy po
   slugu, a wynik konfrontujemy ze zbiorem plików p-*.html (musi się zgadzać
   co do sztuki w obie strony).
2. Na stronie produktowej to samo mega-menu niesie własne <h1>, .card
   i .price. Dlatego każdą stronę tniemy najpierw do <section class="product">,
   a okruszki bierzemy z akapitu tuż przed tą sekcją.

Uruchom:  python3 renderer/katalog.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dom import parsuj, zwin  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MOCKUP = ROOT / "web" / "mockup"
OUT = ROOT / "produkty" / "_katalog.json"

WIEK = re.compile(r"^(?:[\d,]+\s*[–-]\s*[\d,]+\s*(?:lat|lata)|dowolny)$")


def karty(korzen):
    """Karty produktowe -> {slug: {tytul, wiek, autor, cena_pln}}.

    Deduplikacja po slugu: ta sama karta bywa i w mega-menu, i na półce.
    """
    out = {}
    for a in korzen.znajdz_wszystkie("a", klasa="card"):
        m = re.fullmatch(r"p-([a-z0-9-]+)\.html", a.atrybuty.get("href", ""))
        if not m:
            continue
        d = {}
        for klucz, klasa in (("tytul", "card__title"), ("meta", "card__meta"),
                             ("cena_raw", "card__price")):
            w = a.znajdz("span", klasa=klasa)
            if w:
                d[klucz] = zwin(w.tekst)
        if "·" in d.get("meta", ""):
            wiek, autor = d.pop("meta").split("·", 1)
            d["wiek"], d["autor"] = wiek.strip(), autor.strip()
        if d.get("cena_raw"):
            n = re.search(r"\d+", d.pop("cena_raw").replace(" ", ""))
            d["cena_pln"] = int(n.group()) if n else None
        slug = m.group(1)
        if slug not in out or len(d) > len(out[slug]):
            out[slug] = d
    return out


def okruszki(korzen):
    """Katalog › Kategoria › Podkategoria — jedyne źródło przypisania.

    Bierzemy akapit leżący bezpośrednio przed <section class="product">,
    żeby nie złapać linków kategorii z paska nawigacji.
    """
    for p in korzen.znajdz_wszystkie("p", klasa="small"):
        linki = p.dzieci_tag("a")
        if not (linki and linki[0].atrybuty.get("href") == "katalog.html"):
            continue
        d = {}
        for a in linki[1:]:
            m = re.fullmatch(r"k-([a-z]+)\.html(?:#([a-z-]+))?", a.atrybuty.get("href", ""))
            if not m:
                continue
            if m.group(2):
                d["podkategoria"], d["podkategoria_nazwa"] = m.group(2), zwin(a.tekst)
            else:
                d["kategoria"], d["kategoria_nazwa"] = m.group(1), zwin(a.tekst)
        if d:
            return d
    return {}


def strona_produktu(html):
    """Wszystkie dane jednego produktu z p-<slug>.html."""
    korzen = parsuj(html)
    sekcja = korzen.znajdz("section", klasa="product")
    if sekcja is None:
        return {}

    d = okruszki(korzen)

    for klucz, tag, klasa in (("tytul", "h1", None), ("podtytul", "p", "lede")):
        w = sekcja.znajdz(tag, klasa=klasa)
        if w:
            d[klucz] = zwin(w.tekst)

    pigulki_blok = sekcja.znajdz("div", klasa="pills")
    if pigulki_blok:
        pigulki = [zwin(s.tekst) for s in pigulki_blok.znajdz_wszystkie("span", klasa="pill")]
        d["pigulki"] = pigulki
        for p in pigulki:
            if WIEK.match(p):
                d["wiek"] = p
        d["w_klubie"] = "W Klubie" in pigulki
        d["zweryfikowany_tworca"] = "Zweryfikowany twórca" in pigulki

    cena = sekcja.znajdz("span", klasa="price__now")
    if cena:
        n = re.search(r"\d+", zwin(cena.tekst).replace(" ", ""))
        d["cena_pln"] = int(n.group()) if n else None

    ocena = sekcja.znajdz("div", klasa="rating")
    if ocena:
        m = re.search(r"([\d,]+)\s*·\s*(\d+)\s*opini", zwin(ocena.tekst))
        if m:
            d["ocena"] = float(m.group(1).replace(",", "."))
            d["opinie"] = int(m.group(2))

    specs_blok = sekcja.znajdz("dl", klasa="specs")
    if specs_blok:
        specs = {}
        for wiersz in specs_blok.znajdz_wszystkie("div", klasa="spec"):
            dt, dd = wiersz.znajdz("dt"), wiersz.znajdz("dd")
            if dt and dd:
                specs[zwin(dt.tekst).rstrip(":").lower()] = zwin(dd.tekst)
        d["specs"] = specs
        for klucz in ("objętość", "objetosc"):
            if klucz in specs:
                n = re.search(r"\d+", specs[klucz])
                if n:
                    d["strony"] = int(n.group())
                break
        for k in ("format", "druk", "licencja", "aktualizacje"):
            if k in specs:
                d[k] = specs[k]

    autor = sekcja.znajdz("div", klasa="author")
    if autor:
        akapity = [zwin(p.tekst) for p in autor.znajdz_wszystkie("p")]
        if akapity:
            d["autor"] = akapity[0]
        if len(akapity) > 1:
            # rola z prototypu — do produktu NIE trafia, patrz marka/brand.md
            d["autor_rola_prototyp"] = akapity[1]

    nota = sekcja.znajdz("p", klasa="preview__note")
    if nota:
        d["nota_podgladu"] = zwin(nota.tekst)
        d["darmowy_fragment"] = "darmo" in d["nota_podgladu"].lower()
        m = re.search(r"(\w+)\s+pierwsz\w+\s+stron", d["nota_podgladu"])
        if m:
            d["podgladow_na_stronie"] = m.group(1)

    # opis: akapity kolumny lewej. Bierzemy tylko bezpośrednie dzieci .stack,
    # więc rating, podgląd i buybox odpadają same z siebie.
    kolumna = sekcja.znajdz("div", klasa="stack")
    if kolumna:
        akapity = []
        for p in kolumna.dzieci_tag("p"):
            tresc = zwin(p.tekst)
            if not tresc or "lede" in p.klasy:
                continue
            if "--persimmon" in p.styl:
                d["dla_kogo"] = tresc          # najważniejsze zdanie produktu
            else:
                akapity.append(tresc)
        if akapity:
            d["opis_akapity"] = akapity
    return d


def kategorie_z_mockupu():
    """Nazwy kategorii i pełne listy podkategorii z k-*.html."""
    out = {}
    for f in sorted(MOCKUP.glob("k-*.html")):
        cat = f.stem[2:]
        korzen = parsuj(f.read_text(encoding="utf-8"))
        panel = korzen.znajdz("div", klasa="mega__panel", **{"data-cat": cat})
        meta = {"nazwa": None, "opis": None, "podkategorie": [],
                "deklarowana_liczba_produktow": None}
        if panel:
            intro = panel.znajdz("div", klasa="mega__intro")
            if intro:
                h3, p = intro.znajdz("h3"), intro.znajdz("p")
                meta["nazwa"] = zwin(h3.tekst) if h3 else None
                meta["opis"] = zwin(p.tekst) if p else None
                for a in intro.znajdz_wszystkie("a"):
                    m = re.fullmatch(r"k-%s\.html#([a-z-]+)" % cat, a.atrybuty.get("href", ""))
                    if m and not any(s["id"] == m.group(1) for s in meta["podkategorie"]):
                        meta["podkategorie"].append({"id": m.group(1), "nazwa": zwin(a.tekst)})
                n = re.search(r"Zobacz (\d+) materia", zwin(intro.tekst))
                meta["deklarowana_liczba_produktow"] = int(n.group(1)) if n else None
        out[cat] = meta
    return out


def main():
    if not MOCKUP.exists():
        sys.exit(f"BŁĄD: brak {MOCKUP}")

    katalog_html = MOCKUP / "katalog.html"
    pliki = {f.stem[2:]: f for f in sorted(MOCKUP.glob("p-*.html"))}

    if katalog_html.exists():
        z_katalogu = karty(parsuj(katalog_html.read_text(encoding="utf-8")))
        zrodlo = "katalog.html"
    else:
        z_katalogu, zrodlo = {}, "p-*.html (brak katalog.html)"

    slugi = sorted(set(z_katalogu) | set(pliki))
    produkty = {}
    for slug in slugi:
        d = dict(z_katalogu.get(slug, {}))   # karta jako fallback
        if slug in pliki:                    # strona produktowa nadpisuje
            d.update(strona_produktu(pliki[slug].read_text(encoding="utf-8")))
        produkty[slug] = dict(sorted(d.items()))

    kategorie = kategorie_z_mockupu()
    for cat, meta in kategorie.items():
        meta["produkty"] = sorted(s for s, d in produkty.items() if d.get("kategoria") == cat)

    braki = {
        "produktow": len(produkty),
        "zrodlo_listy": zrodlo,
        "w_katalogu_bez_strony_p": sorted(set(z_katalogu) - set(pliki)),
        "strona_p_bez_karty_w_katalogu": sorted(set(pliki) - set(z_katalogu)),
        "kategorie_niepelne": {
            c: {"deklarowane": m["deklarowana_liczba_produktow"],
                "znalezione": len(m["produkty"])}
            for c, m in kategorie.items()
            if m["deklarowana_liczba_produktow"] not in (None, len(m["produkty"]))},
    }
    for pole in ("strony", "kategoria", "podkategoria", "dla_kogo",
                 "podtytul", "autor", "cena_pln", "wiek", "opis_akapity"):
        puste = sorted(s for s, d in produkty.items() if not d.get(pole))
        if puste:
            braki[f"brak_{pole}"] = puste

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(
        {"zrodlo": "web/mockup/", "kategorie": kategorie,
         "produkty": produkty, "braki": braki},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Zapisano {OUT.relative_to(ROOT)}")
    print(f"  lista z: {zrodlo}")
    print(f"  kategorii: {len(kategorie)}   produktów: {len(produkty)}"
          f"   stron p-*.html: {len(pliki)}")
    czyste = True
    for k, v in braki.items():
        if isinstance(v, (list, dict)) and v:
            czyste = False
            print(f"  BRAK {k}: {len(v)} -> {', '.join(list(v)[:6])}"
                  f"{' …' if len(v) > 6 else ''}")
    if czyste:
        print("  braków: 0 — komplet danych katalogowych")


if __name__ == "__main__":
    main()
