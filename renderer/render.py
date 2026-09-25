#!/usr/bin/env python3
"""content.json + archetyp -> PDF-y i podglądy.

  python3 renderer/render.py <slug>            # pelny.pdf + fragment.pdf + podglądy
  python3 renderer/render.py <slug> --kolor    # dodatkowo pelny-kolor.pdf
  python3 renderer/render.py <slug> --html     # zostaw _build.html do podejrzenia

Wyjście: produkty/<slug>/out/{pelny.pdf,fragment.pdf,podglad-01..04.png}

Wariant domyślny jest CZARNO-BIAŁY. Kolor powstaje osobno, jako pelny-kolor.pdf.
Fonty wchodzą jako base64 w <style>, żeby render działał bez sieci i żeby
Chromium na pewno je osadził w PDF-ie.
"""
import argparse
import base64
import json
import re
import subprocess
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

sys.path.insert(0, str(Path(__file__).resolve().parent))
from przegladarka import otworz  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RENDERER = ROOT / "renderer"
FONTY = RENDERER / "fonts"

#: (rodzina CSS, waga). Pliki są STATYCZNE — patrz renderer/fonty.py.
#: Font wariacyjny osadza się w PDF-ie jako Type3 (obrysy glifów), nie jako
#: prawdziwy krój. Jeden plik na wagę, z pełnym polskim kompletem znaków,
#: więc w CSS nie ma unicode-range.
KROJE = [
    ("Plus Jakarta Sans", 400), ("Plus Jakarta Sans", 600),
    ("Plus Jakarta Sans", 700), ("Plus Jakarta Sans", 800),
    ("Bricolage Grotesque", 700),
]


def css_fontow():
    """@font-face z base64. Bez sieci, bez zależności od ścieżek."""
    kawalki = []
    for rodzina, waga in KROJE:
        plik = FONTY / f"{rodzina.replace(' ', '')}-{waga}.woff2"
        if not plik.exists():
            sys.exit(f"BŁĄD: brak fontu {plik.relative_to(ROOT)} — "
                     "uruchom renderer/fonty.py")
        b64 = base64.b64encode(plik.read_bytes()).decode()
        kawalki.append(
            f"@font-face{{font-family:'{rodzina}';font-style:normal;"
            f"font-weight:{waga};font-display:block;"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
    return "\n".join(kawalki)


def zbuduj_html(c, archetyp, kolor, tylko_strony=None):
    env = Environment(loader=FileSystemLoader(str(RENDERER / "templates")),
                      undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True)
    sys.path.insert(0, str(RENDERER))
    from validate import podziel_klucz
    tresc = env.get_template(f"{archetyp.lower()}.html.j2").render(
        c=c, klucz_strony=podziel_klucz(c))

    if tylko_strony:
        # fragment: zostawiamy tylko pierwsze N stron, numeracja się nie zmienia
        # Uwaga: strony mogą nieść dodatkowe klasy (np. strona--poradnik),
        # więc dopasowujemy PREFIKS klasy, nie całą wartość atrybutu.
        strony = re.findall(
            r'<div class="strona[^"]*">.*?</div>\s*(?=<div class="strona[^"]*">|\Z)',
            tresc, re.S)
        if len(strony) < tylko_strony:
            sys.exit(f"BŁĄD: podział na strony dał {len(strony)}, "
                     f"a fragment ma mieć {tylko_strony} — sprawdź wyrażenie "
                     "dzielące w zbuduj_html()")
        tresc = "".join(strony[:tylko_strony])

    css = (RENDERER / "print.css").read_text(encoding="utf-8")
    klasa = "kolor" if kolor else ""
    return (f'<!doctype html><html lang="pl"><head><meta charset="utf-8">'
            f'<title>{c["meta"]["tytul"]}</title>'
            f'<style>{css_fontow()}</style><style>{css}</style></head>'
            f'<body class="{klasa}">{tresc}</body></html>')


def do_pdf(strona, html, cel, katalog_roboczy):
    """Zapisuje HTML na dysk i drukuje go do PDF-a.

    HTML ląduje w katalogu PRODUKTU, nie w out/, żeby ścieżki
    `ilustracje/<id>.png` rozwiązywały się względem niego.

    Marginesy są w CSS (.strona), nie w opcjach pdf() — inaczej Chromium
    dokłada swoje i strona rozjeżdża się o kilka milimetrów.
    """
    plik = katalog_roboczy / "_build.html"
    plik.write_text(html, encoding="utf-8")
    strona.goto(plik.resolve().as_uri())
    strona.emulate_media(media="print")
    strona.wait_for_timeout(400)          # domknięcie layoutu fontów
    strona.pdf(path=str(cel), format="A4", print_background=True,
               margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
               prefer_css_page_size=True)
    return plik


def _wymagane_ilustracje(c):
    sys.path.insert(0, str(RENDERER))
    from ilustracje import zlecenia
    return sorted(zlecenia(c))


def podglady(pdf, out, ile=4, dpi=110):
    import fitz
    d = fitz.open(pdf)
    zrobione = []
    for i in range(min(ile, d.page_count)):
        cel = out / f"podglad-{i + 1:02d}.png"
        d[i].get_pixmap(dpi=dpi).save(cel)
        zrobione.append(cel)
    d.close()
    return zrobione


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("--kolor", action="store_true", help="dodatkowo pelny-kolor.pdf")
    ap.add_argument("--html", action="store_true", help="zostaw _build.html")
    a = ap.parse_args()

    kat = ROOT / "produkty" / a.slug
    plik = kat / "content.json"
    if not plik.exists():
        sys.exit(f"BŁĄD: brak {plik.relative_to(ROOT)}")
    c = json.loads(plik.read_text(encoding="utf-8"))
    archetyp = c["meta"]["archetyp"]
    out = kat / "out"
    out.mkdir(parents=True, exist_ok=True)

    # Ile stron obejmuje darmowy fragment. PROGRAM liczy pełnymi tygodniami
    # (żeby nie urwać tygodnia w pół), reszta archetypów podaje liczbę stron
    # wprost. Żelazna zasada 1: minimum 10 stron.
    if archetyp == "PROGRAM":
        do_tyg = c["fragment"]["do_tygodnia"]
        stron_fragmentu = 3 + sum(1 + len(t["material_dziecka"]) + 3
                                  for t in c["tygodnie"][:do_tyg])
        opis_fragmentu = f"wstęp + tygodnie 1–{do_tyg}"
    else:
        stron_fragmentu = c["fragment"]["do_strony"]
        opis_fragmentu = "wstęp + początek materiału"

    brak = [i for i in (kat / "content.json").exists() and _wymagane_ilustracje(c) or []
            if not (kat / "ilustracje" / f"{i}-bw.png").exists()]
    if brak:
        print(f"UWAGA: brak {len(brak)} ilustracji ({', '.join(brak[:5])}"
              f"{' …' if len(brak) > 5 else ''}) — uruchom renderer/ilustracje.py")

    with otworz() as strona:
        html_pelny = zbuduj_html(c, archetyp, kolor=False)
        build = do_pdf(strona, html_pelny, out / "pelny.pdf", kat)
        print(f"  pelny.pdf")

        html_fr = zbuduj_html(c, archetyp, kolor=False, tylko_strony=stron_fragmentu)
        do_pdf(strona, html_fr, out / "fragment.pdf", kat)
        print(f"  fragment.pdf ({stron_fragmentu} stron: {opis_fragmentu})")

        if a.kolor:
            html_k = zbuduj_html(c, archetyp, kolor=True)
            do_pdf(strona, html_k, out / "pelny-kolor.pdf", kat)
            print(f"  pelny-kolor.pdf")

    if not a.html and build.exists():
        build.unlink()

    for p in podglady(out / "pelny.pdf", out):
        print(f"  {p.name}")

    import fitz
    d = fitz.open(out / "pelny.pdf")
    n, dekl = d.page_count, c["meta"]["strony_deklarowane"]
    fonty = {f[3] for i in range(n) for f in d.get_page_fonts(i)}
    d.close()
    print(f"\n{a.slug}: {n} stron (deklarowane {dekl})")
    print(f"osadzone kroje: {', '.join(sorted(fonty)) or 'BRAK — sprawdź @font-face'}")

    kod = subprocess.run([sys.executable, str(RENDERER / "validate.py"), a.slug],
                         cwd=str(ROOT)).returncode
    sys.exit(kod)


if __name__ == "__main__":
    main()
