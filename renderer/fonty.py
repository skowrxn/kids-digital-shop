#!/usr/bin/env python3
"""Robi statyczne kroje z fontów wariacyjnych. Uruchamiane raz, wynik w repo.

Po co: Chromium drukując do PDF-a osadza INSTANCJĘ fontu wariacyjnego jako
Type3 — czyli obrysy glifów, nie prawdziwy krój. Plik puchnie, tekst gorzej
się zaznacza i formalnie nie mamy „osadzonych czcionek". Statyczna instancja
osadza się poprawnie jako Type0/CID.

Wejście to pełne pliki wariacyjne z repozytorium google/fonts (SIL OFL).
Wyjście: renderer/fonts/<Rodzina>-<waga>.woff2, po jednym pliku na wagę,
z kompletem znaków potrzebnych po polsku (bez dzielenia na latin/latin-ext,
więc w CSS nie ma unicode-range i nie ma czym się pomylić).

  python3 renderer/fonty.py <katalog-z-ttf>
"""
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parent.parent
WYJSCIE = ROOT / "renderer" / "fonts"

#: rodzina -> (wzorzec pliku wariacyjnego, wagi, stałe osie)
KROJE = {
    "PlusJakartaSans": ("PlusJakartaSans*.ttf", [400, 600, 700, 800], {}),
    "BricolageGrotesque": ("*ricolageGrotesque*.ttf", [700], {"opsz": 14, "wdth": 100}),
}

#: Polski komplet: ASCII + polskie diakrytyki + typografia, której używa print.css
ZNAKI = (
    "".join(chr(c) for c in range(0x20, 0x7F))
    + "ĄĆĘŁŃÓŚŹŻąćęłńóśźż"
    + "„”‘’—–…·×÷°§«»"
    + "→←↑↓✓✕"
    + "€zł"
)


def zrob(zrodlo: Path, rodzina: str, wagi, stale, wzorzec):
    pliki = sorted(zrodlo.glob(wzorzec))
    if not pliki:
        sys.exit(f"BŁĄD: nie znaleziono {wzorzec} w {zrodlo}")
    src = pliki[0]
    wyniki = []
    for waga in wagi:
        f = TTFont(src)
        osie = dict(stale)
        osie["wght"] = waga
        dostepne = {a.axisTag for a in f["fvar"].axes} if "fvar" in f else set()
        osie = {k: v for k, v in osie.items() if k in dostepne}
        if osie:
            f = instancer.instantiateVariableFont(f, osie, inplace=False, updateFontNames=True)

        opcje = subset.Options()
        opcje.flavor = "woff2"
        opcje.desubroutinize = True
        opcje.layout_features = ["kern", "liga", "ccmp", "locl", "mark", "mkmk"]
        opcje.name_IDs = ["*"]
        opcje.notdef_outline = True
        s = subset.Subsetter(options=opcje)
        s.populate(text=ZNAKI)
        s.subset(f)

        cel = WYJSCIE / f"{rodzina}-{waga}.woff2"
        f.flavor = "woff2"
        f.save(cel)
        f.close()
        wyniki.append((cel, cel.stat().st_size))
    return wyniki


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    zrodlo = Path(sys.argv[1])
    WYJSCIE.mkdir(parents=True, exist_ok=True)
    for rodzina, (wzorzec, wagi, stale) in KROJE.items():
        for cel, rozmiar in zrob(zrodlo, rodzina, wagi, stale, wzorzec):
            print(f"  {cel.name:34} {rozmiar / 1024:6.1f} kB")
    # kontrola: żaden plik wynikowy nie może być wariacyjny
    for p in sorted(WYJSCIE.glob("*.woff2")):
        f = TTFont(p)
        if "fvar" in f:
            sys.exit(f"BŁĄD: {p.name} nadal jest wariacyjny — Chromium zrobi z niego Type3")
        f.close()
    print("Wszystkie kroje statyczne.")


if __name__ == "__main__":
    main()
