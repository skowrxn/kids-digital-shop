#!/usr/bin/env python3
"""KOLEJKA.json — jedyne źródło prawdy o stanie produkcji.

Biblioteka + CLI. Każdy zapis jest atomowy (tmp + os.replace), więc
przerwana sesja nigdy nie zostawia uciętego JSON-a.

CLI:
  python3 renderer/kolejka.py status            # podsumowanie etapów
  python3 renderer/kolejka.py lista tresc 4     # 4 następne do zrobienia
  python3 renderer/kolejka.py set <slug> <etap> [--powod "..."] [--tor reklamy]
  python3 renderer/kolejka.py bootstrap         # pierwsze wypełnienie (idempotentne)
"""
import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KOLEJKA = ROOT / "KOLEJKA.json"
KATALOG = ROOT / "produkty" / "_katalog.json"

ETAPY = ["brak", "spec", "tresc", "render", "walidacja", "gotowy", "blad"]
#: etapy, po których produkt jest zamknięty i NIE wolno go przetwarzać ponownie
DOCELOWE = {"gotowy"}
MAX_PROB = 3

ARCHETYPY = ["PROGRAM", "ZESZYT", "KARTY", "SEGREGATOR", "GRY", "PORADNIK"]


def teraz():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def wczytaj():
    if not KOLEJKA.exists():
        sys.exit("BŁĄD: brak KOLEJKA.json — uruchom: python3 renderer/kolejka.py bootstrap")
    return json.loads(KOLEJKA.read_text(encoding="utf-8"))


def zapisz(dane):
    """Atomowy zapis. Sesja może paść w dowolnym momencie."""
    dane["zaktualizowano"] = teraz()
    tmp = tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=str(KOLEJKA.parent),
                                      prefix=".kolejka-", suffix=".tmp", delete=False)
    try:
        json.dump(dane, tmp, ensure_ascii=False, indent=2)
        tmp.write("\n")
        tmp.flush()
        os.fsync(tmp.fileno())
        tmp.close()
        os.replace(tmp.name, KOLEJKA)
    except BaseException:
        os.unlink(tmp.name)
        raise


def wpis(dane, slug, tor="produkty"):
    for p in dane[tor]:
        if p["slug"] == slug:
            return p
    raise KeyError(f"{slug} nie ma w KOLEJKA.json[{tor}]")


def ustaw(slug, etap, powod=None, tor="produkty"):
    """Zmienia etap jednego wpisu i NATYCHMIAST zapisuje plik.

    Wywołuj po KAŻDYM produkcie, nigdy na końcu partii.
    """
    if etap not in ETAPY:
        sys.exit(f"BŁĄD: nieznany etap {etap!r}; dozwolone: {', '.join(ETAPY)}")
    dane = wczytaj()
    p = wpis(dane, slug, tor)
    if etap == "blad":
        p["proba"] = p.get("proba", 0) + 1
        p["ostatni_blad"] = powod
        if p["proba"] < MAX_PROB:
            # jeszcze wolno próbować — cofamy na poprzedni etap roboczy
            p["etap"] = "blad"
        else:
            p["etap"] = "blad"
            p["zamkniety"] = True
    else:
        p["etap"] = etap
        p["ostatni_blad"] = None
        p.pop("zamkniety", None)
    p["zaktualizowano"] = teraz()
    zapisz(dane)
    return p


def do_zrobienia(etap_docelowy, limit=None, tor="produkty"):
    """Wpisy, które NIE osiągnęły jeszcze etapu docelowego i nie są zamknięte.

    Gwarantuje idempotencję: produkt z etapem docelowym (lub dalszym)
    nigdy nie trafia na listę.
    """
    dane = wczytaj()
    porzadek = {e: i for i, e in enumerate(ETAPY)}
    cel = porzadek[etap_docelowy]
    out = []
    for p in dane[tor]:
        if p.get("zamkniety"):
            continue
        if p["etap"] == "blad" and p.get("proba", 0) >= MAX_PROB:
            continue
        if p["etap"] != "blad" and porzadek.get(p["etap"], 0) >= cel:
            continue
        if p.get("archetyp") is None and tor == "produkty":
            continue  # brak danych wejściowych, patrz pole `blokada`
        out.append(p)
    return out[:limit] if limit else out


def status(tor="produkty"):
    dane = wczytaj()
    licz = {e: 0 for e in ETAPY}
    for p in dane[tor]:
        licz[p["etap"]] = licz.get(p["etap"], 0) + 1
    return licz, dane


# ---------------------------------------------------------------- bootstrap

#: Przypisanie archetypów. Decyduje WYŁĄCZNIE struktura materiału, nigdy
#: cena ani objętość — to sygnały marży, nie budowy. Kryterium:
#:   sztywna sekwencja z rosnącą trudnością        -> PROGRAM
#:   bloki ćwiczeń bez sekwencji między blokami    -> ZESZYT
#:   talia do wycięcia                             -> KARTY
#:   plansza bazowa + elementy ruchome na rzep     -> SEGREGATOR
#:   zasady gry, rozgrywka                         -> GRY
#:   proza do czytania przez dorosłego             -> PORADNIK
#: Podstawą są opisy z p-<slug>.html, nie tytuły.
ARCHETYP_PRODUKTU = {
    # PROGRAM — kolejność jest treścią; trudność rośnie monotonicznie
    "czytam-sylabami": "PROGRAM",          # 12 tygodni po kolei
    "litery-od-zera": "PROGRAM",           # jedna litera na dwa dni, stała kolejność
    "czytam-po-angielsku": "PROGRAM",      # phonics od najprostszych wzorów
    "gloski-szumiace": "PROGRAM",          # ustawienie → sylaby → wyrazy → mowa
    "wierszyki-na-r": "PROGRAM",           # trzy miesiące, od pionizacji języka
    "dodawanie-bez-palcow": "PROGRAM",     # sześć tygodni jednego przejścia
    "mnozenie-bez-lez": "PROGRAM",         # osiem tygodni + powtórka co tydzień
    "pisze-bez-nacisku": "PROGRAM",        # sześć tygodni pracy nad ręką
    # ZESZYT — bloki od najłatwiejszego, w bloku kolejność dowolna
    "sylaby-dogrywka": "ZESZYT",
    "czytam-i-rozumiem": "ZESZYT",
    "licze-do-20": "ZESZYT",
    "zadania-z-trescia": "ZESZYT",
    "slyszymy-gloski": "ZESZYT",
    "mowa-startuje": "ZESZYT",             # bloki po poziomach + obserwacje rodzica
    "litery-pisane": "ZESZYT",             # bloki liter, osobny blok na mylone
    "szlaczki-i-wzory": "ZESZYT",
    "lewa-reka": "ZESZYT",
    "kiedy-jestem-zly": "ZESZYT",
    "moje-mocne-strony": "ZESZYT",
    "angielski-w-aucie": "ZESZYT",         # 30 zabaw w blokach: trasy krótkie/długie
    "jesienne-popoludnia": "ZESZYT",
    "ferie-bez-ekranu": "ZESZYT",          # 14 dni, ale trudność NIE rośnie
    "swieta-w-domu": "ZESZYT",
    "wiosna-w-doniczce": "ZESZYT",         # dziennik obserwacji = formularz
    "kosmos-dla-poczatkujacych": "ZESZYT",
    "cichy-poranek": "ZESZYT",             # wprost: „wszystko bez nożyczek”
    "tablica-obowiazkow": "ZESZYT",        # tablica + punkty = formularz
    "moj-tydzien": "ZESZYT",               # planer = formularz
    "nadrabiamy-lato": "ZESZYT",           # dwa równoległe poziomy, nie jedna sekwencja
    # KARTY — talia do wycięcia, 8–9 kart na A4, wersja bez podpisów
    "karty-rutyn": "KARTY",
    "emocjometr": "KARTY",
    "wieczor-bez-lekow": "KARTY",
    "angielski-przy-kolacji": "KARTY",     # wprost: „100 kart z obrazkami”
    "memory-domowe": "KARTY",
    "ubieram-sie-sam": "KARTY",            # obrazkowe instrukcje do powieszenia
    # SEGREGATOR — plansza bazowa + elementy ruchome na rzep
    "busy-pierwsze-slowa": "SEGREGATOR",
    "busy-przedszkolak": "SEGREGATOR",
    "teczka-pojazdy": "SEGREGATOR",
    "teczka-zwierzeta": "SEGREGATOR",
    "kto-tu-mieszka": "SEGREGATOR",        # plansze siedlisk + zwierzęta ruchome
    "moje-cialo": "SEGREGATOR",            # plansza ciała + narządy ruchome
    "mapa-polski": "SEGREGATOR",           # mapa sklejana + karty miast i rzek
    # GRY — zasady na jednej stronie, pionki i kostka w pliku
    "gry-po-angielsku": "GRY",
    "planszowki-na-start": "GRY",
    "zestaw-na-podroz": "GRY",             # gry papier-długopis, bez pionków
    "bingo-rodzinne": "GRY",
    # PORADNIK — dominująca proza, materiał czytany przez rodzica
    "kiedy-nic-nie-dziala": "PORADNIK",
    "rozmowa-z-nauczycielem": "PORADNIK",  # rozdziały + formularz na notatki
}

#: Sześć produktów flagowych — po jednym na intencję z sekcji „chcę…"
#: prototypu. To jest zakres KROKU 7 (teksty reklamowe).
FLAGOWE = {
    "karty-rutyn": "ICP-0-ekran",
    "czytam-sylabami": "ICP-1-szkola",
    "gloski-szumiace": "ICP-2-kolejka",
    "busy-pierwsze-slowa": "ICP-3-pogoda",
    "moj-tydzien": "ICP-4-system",
    "kiedy-jestem-zly": "ICP-5-zlosc",
}


def bootstrap():
    if not KATALOG.exists():
        sys.exit("BŁĄD: brak produkty/_katalog.json — uruchom: python3 renderer/katalog.py")
    kat = json.loads(KATALOG.read_text(encoding="utf-8"))
    stare = {}
    if KOLEJKA.exists():
        for tor in ("produkty", "reklamy"):
            for p in json.loads(KOLEJKA.read_text(encoding="utf-8")).get(tor, []):
                stare[(tor, p["slug"])] = p

    produkty, reklamy = [], []
    for slug, d in sorted(kat["produkty"].items()):
        p = {
            "slug": slug,
            "tytul": d.get("tytul"),
            "archetyp": ARCHETYP_PRODUKTU.get(slug),
            "kategoria": d.get("kategoria"),
            "podkategoria": d.get("podkategoria"),
            "wiek": d.get("wiek"),
            "autor": d.get("autor"),
            "cena_pln": d.get("cena_pln"),
            "strony_prototyp": d.get("strony"),
            "etap": "brak",
            "proba": 0,
            "ostatni_blad": None,
            "zaktualizowano": teraz(),
        }
        if p["strony_prototyp"] is None:
            p["blokada"] = ("brak p-%s.html w web/mockup — nieznana „Objętość”; "
                            "spec.md nie może zadeklarować liczby stron" % slug)
        if slug in FLAGOWE:
            p["flagowy"] = True
            p["icp_glowne"] = FLAGOWE[slug]
        produkty.append(p)
        reklamy.append({
            "slug": slug,
            "etap": "brak",
            "proba": 0,
            "ostatni_blad": None,
            "flagowy": slug in FLAGOWE,
            "icp_glowne": FLAGOWE.get(slug),
            "zaktualizowano": teraz(),
        })

    # miejsca po produktach, których nie ma w mockupie (12 kategorii × 4 = 48)
    luki = []
    for cat, meta in sorted(kat["kategorie"].items()):
        maja = sum(1 for p in produkty if p["kategoria"] == cat)
        brakuje = (meta.get("deklarowana_liczba_produktow") or 0) - maja
        for i in range(max(0, brakuje)):
            slug = f"__brak-{cat}-{i + 1}"
            luki.append({
                "slug": slug,
                "tytul": None,
                "archetyp": None,
                "kategoria": cat,
                "etap": "brak",
                "proba": 0,
                "ostatni_blad": None,
                "zaktualizowano": teraz(),
                "blokada": (f"kategoria „{meta['nazwa']}” deklaruje "
                            f"{meta['deklarowana_liczba_produktow']} materiałów, "
                            f"w mockupie jest {maja}. Brakuje strony p-*.html — "
                            "nie znamy slug-a, tytułu, ceny, wieku ani autora."),
            })
    produkty += luki

    # zachowaj stan już zrobionej pracy — bootstrap jest idempotentny
    for tor, lista in (("produkty", produkty), ("reklamy", reklamy)):
        for p in lista:
            s = stare.get((tor, p["slug"]))
            if s:
                for k in ("etap", "proba", "ostatni_blad", "zamkniety"):
                    if k in s:
                        p[k] = s[k]
                p["zaktualizowano"] = s.get("zaktualizowano", p["zaktualizowano"])

    zapisz({
        "opis": "Stan produkcji. Jedyne źródło prawdy. Zapis po KAŻDYM produkcie.",
        "etapy": ETAPY,
        "max_prob": MAX_PROB,
        "produkty": produkty,
        "reklamy": reklamy,
    })
    print(f"KOLEJKA.json: {len(produkty)} produktów "
          f"({len(luki)} zablokowanych brakiem danych), {len(reklamy)} wpisów reklamowych")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("bootstrap")
    s = sub.add_parser("status")
    s.add_argument("--tor", default="produkty")
    l = sub.add_parser("lista")
    l.add_argument("etap", choices=ETAPY)
    l.add_argument("limit", nargs="?", type=int, default=4)
    l.add_argument("--tor", default="produkty")
    u = sub.add_parser("set")
    u.add_argument("slug")
    u.add_argument("etap", choices=ETAPY)
    u.add_argument("--powod")
    u.add_argument("--tor", default="produkty")
    a = ap.parse_args()

    if a.cmd == "bootstrap":
        bootstrap()
    elif a.cmd == "status":
        licz, dane = status(a.tor)
        czesci = [f"{v} {k}" for k, v in licz.items() if v]
        blok = sum(1 for p in dane[a.tor] if p.get("blokada"))
        print(f"{a.tor}: {sum(licz.values())} wpisów — " + ", ".join(czesci)
              + (f" (w tym {blok} zablokowanych brakiem danych z prototypu)" if blok else ""))
    elif a.cmd == "lista":
        for p in do_zrobienia(a.etap, a.limit, a.tor):
            print(f"{p['slug']}\t{p.get('archetyp') or '-'}\t{p['etap']}\tproba={p.get('proba', 0)}")
    elif a.cmd == "set":
        p = ustaw(a.slug, a.etap, a.powod, a.tor)
        print(f"{p['slug']} -> {p['etap']}" + (f" ({p['ostatni_blad']})" if p.get("ostatni_blad") else ""))


if __name__ == "__main__":
    main()
