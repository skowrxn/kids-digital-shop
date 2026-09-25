#!/usr/bin/env python3
"""Bramki jakości. Build produktu pada, jeśli którakolwiek nie przejdzie.

Uruchamiaj w pętli buildu, nie ręcznie.

  python3 renderer/validate.py schema <slug>    # schemat + reguły treści
  python3 renderer/validate.py pdf <slug>       # bramki na wyrenderowanych PDF-ach
  python3 renderer/validate.py <slug>           # wszystko, co się da

Kod wyjścia 0 = przeszło, 1 = padło.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHETYPY = ROOT / "produkty" / "_archetypy"

# --------------------------------------------------------------- frazy zakazane
# Rdzenie z marka/brand.md, sekcja „Frazy zakazane". Dopasowanie po rdzeniu —
# odmiana nie ma znaczenia.
RDZENIE_A = ["terapi", "terapeut", "diagnoz", "leczen", "wylecz", "leczni", "kuracj",
             "zaburze", "dysleks", "dysgraf", "dyskalk", "adhd", "autyz", "asperger",
             "wada wymowy", "wada postawy", "niepełnospraw", "objaw", "symptom",
             "rokowani", "recept", "dawkowani", "nerwic", "depresj", "trauma",
             "opóźnienie rozwoju", "opóźniony rozwój", "korekcj", "korygowani"]
RDZENIE_B = ["gwarantujemy", "gwarancja efektu", "na pewno nauczy", "dogoni rówieśnik",
             "nie zostanie w tyle", "lepszy niż inne dzieci", "przewyższy",
             "przygotuje do szkoły w 100", "cudowne dziecko", "zdolniejsze"]
RDZENIE_C = ["stracisz czas", "zmarnujesz", "będzie za późno", "ostatni moment",
             "zostanie w tyle", "zaniedbani", "twoja wina", "jeśli teraz nie zaczniesz"]

#: Zdania, w których wolno użyć rdzenia z sekcji A: przekierowanie do specjalisty
#: albo jawne rozgraniczenie. Wzorzec z prototypu: „Nie zastępują diagnozy".
WYJATKI_SKIEROWANIE = [
    r"nie (?:zastępuj|zastąpi)\w*\s+(?:diagnoz|terapi|wizyt|logoped)\w*",
    r"(?:porozmawiaj|umów się|idź|zgłoś się|warto pójść)\s+\w*\s*"
    r"(?:do\s+)?(?:logoped|pediatr|specjalist|psycholog)\w*",
    r"nie (?:jest|są) (?:to )?(?:terapi|diagnoz)\w*",
    r"to nie jest terapia ani diagnoza",
    r"lista sygnałów, przy których warto",
]

#: Nazwy własne z prototypu — dopuszczone po dokładnym dopasowaniu.
NAZWY_WLASNE = ["mowa startuje", "opóźniony rozwój mowy"]


def bez_ogonkow(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn").lower()


def zbierz_teksty(obj, sciezka="", pomin=("id", "typ", "slug", "archetyp", "wersja")):
    """Wszystkie stringi w drzewie JSON, ze ścieżką — do raportowania."""
    if isinstance(obj, str):
        yield sciezka, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k not in pomin:
                yield from zbierz_teksty(v, f"{sciezka}.{k}" if sciezka else k, pomin)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from zbierz_teksty(v, f"{sciezka}[{i}]", pomin)


def frazy_zakazane(dane):
    """Zwraca listę (sciezka, fraza, sekcja). Pusta = czysto."""
    trafienia = []
    for sciezka, tekst in zbierz_teksty(dane):
        low = tekst.lower()
        if any(n in low for n in NAZWY_WLASNE):
            continue
        chroniony = any(re.search(w, low) for w in WYJATKI_SKIEROWANIE)
        for sekcja, rdzenie in (("A", RDZENIE_A), ("B", RDZENIE_B), ("C", RDZENIE_C)):
            for r in rdzenie:
                if r in low:
                    if sekcja == "A" and chroniony:
                        continue
                    trafienia.append((sciezka, r, sekcja))
    return trafienia


# ------------------------------------------------------------------ reguły treści
def reguly_wspolne(c, schemat, bledy, ostrz):
    """Bramki niezależne od archetypu, liczone na stronach-ćwiczeniach."""
    strony = wszystkie_strony(c)

    ident = [s["id"] for s in strony]
    duble = {i for i in ident if ident.count(i) > 1}
    if duble:
        bledy.append(f"powtórzone id stron: {sorted(duble)}")

    z_odp = set(schemat.get("x-typy-z-odpowiedziami", []))
    maja = {k["strona_id"] for k in c.get("klucz_odpowiedzi", [])}
    for s in strony:
        if s["typ"] in z_odp and s["id"] not in maja:
            bledy.append(f"{s['id']}: typ {s['typ']} wymaga klucza odpowiedzi")
        if len(s["polecenie"].split()) > 8:
            bledy.append(f"{s['id']}: polecenie ma {len(s['polecenie'].split())} słów, maks. 8")

        d = s["dane"]
        if s["typ"] == "lacz_pary":
            for a, b in d["pary"]:
                if a >= len(d["lewa"]) or b >= len(d["prawa"]):
                    bledy.append(f"{s['id']}: para [{a},{b}] poza zakresem kolumn")
            for kol in ("lewa", "prawa"):
                dubel = {x for x in d[kol] if d[kol].count(x) > 1}
                if dubel:
                    bledy.append(f"{s['id']}: kolumna {kol} ma powtórzone pola {dubel}")
            bez = set(range(len(d["lewa"]))) - {a for a, _ in d["pary"]}
            if bez:
                bledy.append(f"{s['id']}: pola lewej kolumny bez pary: {sorted(bez)}")
        if s["typ"] in ("uzupelnij", "wybierz"):
            for i, p in enumerate(d["pozycje"]):
                if p["poprawna"] >= len(p["opcje"]):
                    bledy.append(f"{s['id']}: pozycja {i} — indeks poprawnej poza opcjami")
                if len(set(p["opcje"])) != len(p["opcje"]):
                    bledy.append(f"{s['id']}: pozycja {i} — powtórzona opcja, "
                                 "ćwiczenie nie ma jednego rozwiązania")
            odp = [p["opcje"][p["poprawna"]] for p in d["pozycje"]]
            if len(odp) > 2 and len(set(odp)) < 2:
                bledy.append(f"{s['id']}: wszystkie {len(odp)} odpowiedzi to {odp[0]!r} — "
                             "dziecko trafia bez czytania")
        if s["typ"] == "karty_do_wyciecia":
            na = d.get("na_arkuszu", 9)
            if len(d["karty"]) > na:
                bledy.append(f"{s['id']}: {len(d['karty'])} kart przy siatce {na} na A4")
        if s["typ"] == "sekwencja":
            puste = sum(1 for k in d["kroki"] if k == "")
            if puste != len(d["brakujace"]):
                bledy.append(f"{s['id']}: {puste} pustych pól, "
                             f"{len(d['brakujace'])} odpowiedzi w `brakujace`")

    # żadnych danych dzieci — nigdzie w produkcie
    for sciezka, tekst in zbierz_teksty(c):
        if re.search(r"\b(imię dziecka|nazwisko dziecka|data urodzenia)\b", tekst.lower()):
            bledy.append(f"{sciezka}: prosi o dane dziecka — {tekst[:40]!r}")


def reguly_zeszyt(c, bledy, ostrz):
    poziomy = [b["poziom"] for b in c["bloki"]]
    if poziomy != sorted(poziomy):
        bledy.append(f"ZESZYT: bloki nie idą od najłatwiejszego — poziomy {poziomy}")


def reguly_karty(c, bledy, ostrz):
    for t in c["talie"]:
        for s in t["arkusze"]:
            if s["typ"] != "karty_do_wyciecia":
                continue
            na = s["dane"].get("na_arkuszu")
            if na not in (8, 9):
                bledy.append(f"{s['id']}: KARTY wymaga 8 albo 9 kart na A4, jest {na}")
        if not t.get("bez_podpisow"):
            ostrz.append(f"talia {t['nazwa']!r} bez wersji dla nieczytających")


def reguly_gry(c, bledy, ostrz):
    for g in c["gry"]:
        if len(g["zasady"]) > 8:
            bledy.append(f"gra {g['nazwa']!r}: {len(g['zasady'])} kroków zasad "
                         "— nie zmieszczą się na jednej stronie")
        wymaga = " ".join(g["zasady"] + g.get("przygotowanie", [])).lower()
        ma_arkusze = bool(g.get("arkusze"))
        for slowo in ("pionek", "pionk", "kostk"):
            if slowo in wymaga and not ma_arkusze:
                bledy.append(f"gra {g['nazwa']!r}: zasady mówią o {slowo!r}, "
                             "ale w pliku nie ma arkuszy z elementami")
                break


def reguly_segregator(c, bledy, ostrz):
    for k in c["sekcje"]:
        if k["instrukcja_przygotowania"]["typ"] != "lista_krokow":
            ostrz.append(f"sekcja {k['temat']!r}: instrukcja przygotowania nie jest listą kroków")
        if k["elementy_ruchome"]["typ"] != "elementy_ruchome":
            bledy.append(f"sekcja {k['temat']!r}: brak listy elementów do zalaminowania")
        elif not k["elementy_ruchome"]["dane"].get("rzep"):
            bledy.append(f"sekcja {k['temat']!r}: brak informacji, gdzie przykleić rzep")


def reguly_program(c, bledy, ostrz):
    tygodnie = c["tygodnie"]

    poziomy = [t["poziom_trudnosci"] for t in tygodnie]
    for a, b in zip(poziomy, poziomy[1:]):
        if b <= a:
            bledy.append(f"PROGRAM: trudność nie rośnie monotonicznie ({a} -> {b})")
            break

    # interleaving — każdy tydzień poza pierwszym powtarza materiał wcześniejszy
    for t in tygodnie:
        if t["nr"] == 1:
            continue
        zt = t["powtorka"]["z_tygodni"]
        if not zt:
            bledy.append(f"T{t['nr']}: brak interleavingu — pusta lista powtorka.z_tygodni")
        if any(x >= t["nr"] for x in zt):
            bledy.append(f"T{t['nr']}: powtórka wskazuje na tydzień nie wcześniejszy: {zt}")
        if not (t["powtorka"].get("sylaby") or t["powtorka"].get("wyrazy")):
            bledy.append(f"T{t['nr']}: powtórka nie zawiera żadnego materiału")

    # plan powtórek: nowy materiał nie może wracać jako nowy
    widziane = {}
    for t in tygodnie:
        for s in t["nowy_material"].get("sylaby", []):
            if s in widziane:
                bledy.append(f"T{t['nr']}: sylaba {s!r} już wprowadzona w T{widziane[s]}")
            else:
                widziane[s] = t["nr"]

    # ta sama strona nie może powtarzać wyrazu częściej, niż zakłada plan
    for t in tygodnie:
        for s in t["material_dziecka"]:
            if s["typ"] == "wyrazy_do_czytania":
                w = [x["wyraz"] for x in s["dane"]["wyrazy"]]
                dubel = {x for x in w if w.count(x) > 1}
                if dubel:
                    bledy.append(f"{s['id']}: wyraz powtórzony na jednej stronie: {dubel}")

    if c["fragment"].get("do_tygodnia", 1) < 1:
        bledy.append("fragment: musi obejmować co najmniej jeden pełny tydzień")


def wszystkie_strony(c):
    """Każda strona-ćwiczenie w dokumencie, niezależnie od archetypu."""
    a = c["meta"]["archetyp"]
    if a == "PROGRAM":
        return [s for t in c["tygodnie"] for s in t["material_dziecka"]]
    if a == "ZESZYT":
        return [s for b in c["bloki"] for s in b["cwiczenia"]]
    if a == "KARTY":
        return [s for t in c["talie"] for s in t["arkusze"]]
    if a == "SEGREGATOR":
        return [s for k in c["sekcje"] for s in
                [k["instrukcja_przygotowania"], k["plansza_bazowa"],
                 k["elementy_ruchome"], *k.get("dodatkowe", [])]]
    if a == "GRY":
        return [s for g in c["gry"] for s in
                ([g["plansza"]] if g.get("plansza") else []) + g.get("arkusze", [])]
    if a == "PORADNIK":
        return [s for r in c["rozdzialy"] for s in r["strony"]] + c.get("checklisty", [])
    return []


def bilans_stron(c):
    """Ile stron wyjdzie z danych. Musi zgadzać się ze `strony_deklarowane`.

    Liczy dokładnie to, co składa szablon danego archetypu — jeśli któryś
    szablon zmieni układ stron, to miejsce trzeba poprawić razem z nim.
    """
    a = c["meta"]["archetyp"]
    klucz = 1 if c.get("klucz_odpowiedzi") else 0
    if a == "PROGRAM":
        n = 3  # tytułowa + jak korzystać + plan tygodni
        for t in c["tygodnie"]:
            n += 1 + len(t["material_dziecka"]) + 3   # karta rodzica, gra, czytanka, postęp
        return n + klucz
    n = 2  # okładka + jak korzystać
    if a == "ZESZYT":
        n += sum(1 + len(b["cwiczenia"]) for b in c["bloki"])
    elif a == "KARTY":
        n += sum(1 + len(t["arkusze"]) for t in c["talie"])
        n += len(c.get("instrukcja_zabaw", []))
    elif a == "SEGREGATOR":
        n += sum(3 + len(k.get("dodatkowe", [])) for k in c["sekcje"])
    elif a == "GRY":
        n += sum(1 + (1 if g.get("plansza") else 0) + len(g.get("arkusze", []))
                 for g in c["gry"])
    elif a == "PORADNIK":
        n += sum(len(r["strony"]) + (1 if r.get("do_zrobienia_w_tym_tygodniu") else 0)
                 for r in c["rozdzialy"])
        n += len(c.get("checklisty", []))
    return n + klucz


# ------------------------------------------------------------------------ wejścia
def waliduj_schema(slug):
    import jsonschema

    kat = ROOT / "produkty" / slug
    plik = kat / "content.json"
    if not plik.exists():
        return [f"brak {plik.relative_to(ROOT)}"], []
    c = json.loads(plik.read_text(encoding="utf-8"))
    arch = c.get("meta", {}).get("archetyp")
    schemat_plik = ARCHETYPY / f"{arch}.schema.json"
    if not schemat_plik.exists():
        return [f"brak schematu {schemat_plik.name}"], []

    bledy, ostrz = [], []
    schemat = json.loads(schemat_plik.read_text(encoding="utf-8"))
    walidator = jsonschema.Draft202012Validator(schemat)
    for e in sorted(walidator.iter_errors(c), key=lambda e: list(e.path)):
        bledy.append("schemat: " + "/".join(map(str, e.path)) + ": " + e.message)

    if bledy:
        return bledy, ostrz

    for sciezka, fraza, sekcja in frazy_zakazane(c):
        bledy.append(f"fraza zakazana [{sekcja}] {fraza!r} w {sciezka}")

    reguly_wspolne(c, schemat, bledy, ostrz)
    for nazwa, funkcja in (("PROGRAM", reguly_program), ("ZESZYT", reguly_zeszyt),
                           ("KARTY", reguly_karty), ("GRY", reguly_gry),
                           ("SEGREGATOR", reguly_segregator)):
        if arch == nazwa:
            funkcja(c, bledy, ostrz)

    n = bilans_stron(c)
    dekl = c["meta"]["strony_deklarowane"]
    if abs(n - dekl) > 2:
        bledy.append(f"bilans stron {n} != deklarowane {dekl} (tolerancja ±2)")
    elif n != dekl:
        ostrz.append(f"bilans stron {n}, deklarowane {dekl} — w tolerancji, ale się nie zgadza")

    spec = kat / "spec.md"
    if spec.exists():
        m = re.search(r"\|\s*\*\*objętość\*\*\s*\|\s*\*\*(\d+)", spec.read_text(encoding="utf-8"), re.I)
        if m and int(m.group(1)) != dekl:
            bledy.append(f"spec.md deklaruje {m.group(1)} stron, content.json {dekl}")
    return bledy, ostrz


def waliduj_pdf(slug):
    """Bramki wymagające wyrenderowanych plików. Uruchamiane po render.py."""
    import fitz

    kat = ROOT / "produkty" / slug
    out = kat / "out"
    c = json.loads((kat / "content.json").read_text(encoding="utf-8"))
    bledy, ostrz = [], []

    pelny, fragment = out / "pelny.pdf", out / "fragment.pdf"
    if not pelny.exists():
        return [f"brak {pelny.relative_to(ROOT)}"], []
    if not fragment.exists():
        bledy.append("brak fragment.pdf — żelazna zasada 1, produkt nie może być gotowy")

    d = fitz.open(pelny)
    dekl = c["meta"]["strony_deklarowane"]
    if abs(d.page_count - dekl) > 2:
        bledy.append(f"pelny.pdf ma {d.page_count} stron, spec deklaruje {dekl} (tolerancja ±2)")

    najgorsza, maks = None, 0.0
    for i, strona in enumerate(d, 1):
        pix = strona.get_pixmap(dpi=72, colorspace=fitz.csGRAY)
        prog = 250
        niebiale = sum(1 for b in pix.samples if b < prog)
        pokrycie = niebiale / (pix.width * pix.height)
        if pokrycie > maks:
            maks, najgorsza = pokrycie, i
        if pokrycie > 0.12:
            bledy.append(f"strona {i}: pokrycie tuszem {pokrycie:.1%} > 12%")
    ostrz.append(f"najciemniejsza strona: {najgorsza} ({maks:.1%} pokrycia)")

    # tekst poza obszarem zadruku: A4 595×842 pt, marginesy 15 mm (42.5 pt),
    # lewy 22 mm (62.4 pt)
    L, P, G, D = 62.4, 595.3 - 42.5, 42.5, 842.0 - 42.5
    for i, strona in enumerate(d, 1):
        for b in strona.get_text("blocks"):
            x0, y0, x1, y1 = b[:4]
            if x0 < L - 1 or x1 > P + 1 or y0 < G - 1 or y1 > D + 1:
                bledy.append(f"strona {i}: tekst poza obszarem zadruku "
                             f"({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f})")
                break
    d.close()

    # Stopień pisma. Podłoga z design-system.md: 14 pt dla dzieci uczących się
    # czytać, 11 pt wszędzie indziej. Sprawdzamy tylko tekst, który się CZYTA —
    # ciągi dłuższe niż 12 znaków, spoza pasa stopki i nie pisane wersalikami.
    # Krótsze ciągi, stopka i etykiety wersalikowe to chrome — mogą być mniejsze.
    d = fitz.open(pelny)
    min_pt = c["meta"].get("min_pt_dziecka", 14)
    za_male = {}
    for i, strona in enumerate(d, 1):
        for b in strona.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for sp in l["spans"]:
                    tekst = sp["text"].strip()
                    if sp["bbox"][1] > 780:      # pas stopki — numer, tytuł, adres
                        continue
                    if tekst.isupper():          # etykieta wersalikowa = chrome
                        continue
                    if len(tekst) > 12 and sp["size"] < 10.9:
                        za_male.setdefault(round(sp["size"], 1), (i, tekst[:40]))
    for rozmiar, (i, probka) in sorted(za_male.items()):
        bledy.append(f"strona {i}: tekst {rozmiar}pt poniżej podłogi 11pt: {probka!r}")
    d.close()

    if fragment.exists():
        f = fitz.open(fragment)
        if f.page_count < 10:
            bledy.append(f"fragment.pdf ma {f.page_count} stron, minimum to 10")
        f.close()
    return bledy, ostrz


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tryb", choices=["schema", "pdf", "wszystko"], nargs="?", default="wszystko")
    ap.add_argument("slug")
    a = ap.parse_args()

    bledy, ostrz = [], []
    if a.tryb in ("schema", "wszystko"):
        b, o = waliduj_schema(a.slug)
        bledy += b
        ostrz += o
    if a.tryb in ("pdf", "wszystko") and (ROOT / "produkty" / a.slug / "out" / "pelny.pdf").exists():
        b, o = waliduj_pdf(a.slug)
        bledy += b
        ostrz += o

    for o in ostrz:
        print(f"  uwaga: {o}")
    if bledy:
        print(f"PADŁO: {a.slug} — {len(bledy)} błędów")
        for b in bledy[:40]:
            print(f"  - {b}")
        if len(bledy) > 40:
            print(f"  … i {len(bledy) - 40} więcej")
        sys.exit(1)
    print(f"OK: {a.slug} — wszystkie bramki przeszły ({a.tryb})")


if __name__ == "__main__":
    main()
