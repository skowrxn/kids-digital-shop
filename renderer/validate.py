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

    # klucz odpowiedzi wymagany dla typów, które mają odpowiedzi
    z_odp = {"lacz_sylaby", "uzupelnij_sylabe", "wybierz_wyraz", "dyktando_sylabowe"}
    maja_klucz = {k["strona_id"] for k in c["klucz_odpowiedzi"]}
    for t in tygodnie:
        for s in t["material_dziecka"]:
            if s["typ"] in z_odp and s["id"] not in maja_klucz:
                bledy.append(f"{s['id']}: typ {s['typ']} wymaga klucza odpowiedzi")

    # spójność ćwiczeń
    for t in tygodnie:
        for s in t["material_dziecka"]:
            d = s["dane"]
            if s["typ"] == "lacz_sylaby":
                for a, b in d["pary"]:
                    if a >= len(d["lewa"]) or b >= len(d["prawa"]):
                        bledy.append(f"{s['id']}: para [{a},{b}] poza zakresem kolumn")
                for kol in ("lewa", "prawa"):
                    dubel = {x for x in d[kol] if d[kol].count(x) > 1}
                    if dubel:
                        bledy.append(f"{s['id']}: kolumna {kol} ma powtórzone pola {dubel} — "
                                     "dziecko widzi dwa identyczne pola zamiast jednego")
                bez_linii = set(range(len(d["lewa"]))) - {a for a, _ in d["pary"]}
                if bez_linii:
                    bledy.append(f"{s['id']}: pola lewej kolumny bez pary: {sorted(bez_linii)}")
            if s["typ"] in ("uzupelnij_sylabe", "wybierz_wyraz"):
                for i, p in enumerate(d["pozycje"]):
                    if p["poprawna"] >= len(p["opcje"]):
                        bledy.append(f"{s['id']}: pozycja {i} — indeks poprawnej poza opcjami")
                    if len(set(p["opcje"])) != len(p["opcje"]):
                        ostrz.append(f"{s['id']}: pozycja {i} — powtórzona opcja")

    # karta postępu zawsze pusta — żadnych danych dziecka
    for t in tygodnie:
        for w in t["karta_postepu"]["wiersze"]:
            if re.search(r"\b(imię|imie|nazwisko|wiek dziecka|data urodzenia)\b", w.lower()):
                bledy.append(f"T{t['nr']}: karta postępu prosi o dane dziecka: {w!r}")

    # polecenia do dziecka: maks. 8 słów
    for t in tygodnie:
        for s in t["material_dziecka"]:
            if len(s["polecenie"].split()) > 8:
                bledy.append(f"{s['id']}: polecenie ma {len(s['polecenie'].split())} słów, maks. 8")

    # fragment: min. 10 stron albo 1 pełny tydzień
    if c["fragment"]["do_tygodnia"] < 1:
        bledy.append("fragment: musi obejmować co najmniej jeden pełny tydzień")


def bilans_stron(c):
    """Ile stron wyjdzie z danych. Musi zgadzać się ze `strony_deklarowane`."""
    n = 3  # tytułowa + jak korzystać ×2
    for t in c["tygodnie"]:
        n += 1 + len(t["material_dziecka"]) + 1 + 1 + 1
    return n + 1  # klucz odpowiedzi


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

    if arch == "PROGRAM":
        reguly_program(c, bledy, ostrz)

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
