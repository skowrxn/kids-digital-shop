#!/usr/bin/env python3
"""Generuje schematy pięciu archetypów ze wspólnych klocków.

PROGRAM.schema.json jest pisany ręcznie i TEN SKRYPT GO NIE RUSZA — ma
własne reguły (tygodnie, interleaving), których pozostałe nie mają.

Po co generator: typy ćwiczeń muszą znaczyć to samo we wszystkich
archetypach, bo renderuje je jedno makro (`renderer/templates/_cwiczenia.html.j2`).
Pięć osobnych plików pisanych ręcznie rozjechałoby się po pierwszej poprawce.

  python3 produkty/_archetypy/_buduj_schematy.py
"""
import json
from pathlib import Path

TU = Path(__file__).resolve().parent

# --------------------------------------------------------------- dane ćwiczeń
D = {
    "tabela": {"required": ["wiersze"], "properties": {
        "wiersze": {"type": "array", "minItems": 1, "items": {
            "type": "array", "minItems": 1, "items": {"type": "string"}}},
        "naglowki_kolumn": {"type": "array", "items": {"type": "string"}}}},
    "sciezka": {"required": ["kroki"], "properties": {
        "kroki": {"type": "array", "minItems": 3, "items": {"type": "string"}},
        "meta": {"type": "string"}}},
    "lacz_pary": {"required": ["lewa", "prawa", "pary"], "properties": {
        "lewa": {"type": "array", "minItems": 2, "items": {"type": "string"}},
        "prawa": {"type": "array", "minItems": 2, "items": {"type": "string"}},
        "pary": {"type": "array", "minItems": 2, "items": {
            "type": "array", "minItems": 2, "maxItems": 2,
            "items": {"type": "integer", "minimum": 0}}}}},
    "wyrazy_do_czytania": {"required": ["wyrazy"], "properties": {
        "wyrazy": {"type": "array", "minItems": 1, "items": {
            "type": "object", "required": ["wyraz", "sylaby"],
            "additionalProperties": False,
            "properties": {"wyraz": {"type": "string"},
                           "sylaby": {"type": "array", "minItems": 1,
                                      "items": {"type": "string"}}}}}}},
    "uzupelnij": {"required": ["pozycje"], "properties": {
        "pozycje": {"type": "array", "minItems": 2, "items": {
            "type": "object", "required": ["wzor", "opcje", "poprawna"],
            "additionalProperties": False,
            "properties": {"wzor": {"type": "string"},
                           "opcje": {"type": "array", "minItems": 2,
                                     "items": {"type": "string"}},
                           "poprawna": {"type": "integer", "minimum": 0},
                           "ilustracja": {"$ref": "#/$defs/ilustracja"}}}}}},
    "wybierz": {"required": ["pozycje"], "properties": {
        "pozycje": {"type": "array", "minItems": 2, "items": {
            "type": "object", "required": ["opcje", "poprawna"],
            "additionalProperties": False,
            "description": "Albo `ilustracja`, albo `podpowiedz_rodzica` — "
                           "dziecko musi wiedzieć, o co chodzi.",
            "anyOf": [{"required": ["ilustracja"]},
                      {"required": ["podpowiedz_rodzica"]}],
            "properties": {"podpowiedz_rodzica": {"type": "string"},
                           "opcje": {"type": "array", "minItems": 2,
                                     "items": {"type": "string"}},
                           "poprawna": {"type": "integer", "minimum": 0},
                           "ilustracja": {"$ref": "#/$defs/ilustracja"}}}}}},
    "pisanie_po_sladzie": {"required": ["wzory"], "properties": {
        "wzory": {"type": "array", "minItems": 1, "items": {"type": "string"}},
        "linie_na_wzor": {"type": "integer", "minimum": 1, "maximum": 4},
        "liniatura": {"enum": ["trzylinia", "czterolinia", "gladka"]}}},
    "czytanie_zdan": {"required": ["zdania"], "properties": {
        "zdania": {"type": "array", "minItems": 1, "items": {"type": "string"}},
        "pytanie": {"type": "string"}}},
    "dyktando": {"required": ["do_dyktowania"], "properties": {
        "do_dyktowania": {"type": "array", "minItems": 2, "items": {"type": "string"}},
        "liniatura": {"enum": ["trzylinia", "czterolinia", "gladka"]}}},
    "ramka_rysunkowa": {"required": ["wyrazy"], "properties": {
        "wyrazy": {"type": "array", "minItems": 1, "maxItems": 6,
                   "items": {"type": "string"}},
        "wysokosc_ramki_mm": {"type": "integer", "minimum": 20}}},
    "formularz": {"required": ["pola"], "properties": {
        "pola": {"type": "array", "minItems": 1, "items": {
            "type": "object", "required": ["etykieta"], "additionalProperties": False,
            "properties": {"etykieta": {"type": "string"},
                           "wysokosc_mm": {"type": "integer", "minimum": 6},
                           "linie": {"type": "integer", "minimum": 0}}}}}},
    "dzialania": {"required": ["zadania"], "properties": {
        "zadania": {"type": "array", "minItems": 2, "items": {
            "type": "object", "required": ["tresc", "wynik"],
            "additionalProperties": False,
            "properties": {"tresc": {"type": "string"},
                           "wynik": {"type": "string"}}}}}},
    "sortowanie": {"required": ["elementy", "kategorie"], "properties": {
        "elementy": {"type": "array", "minItems": 4, "items": {"type": "string"}},
        "kategorie": {"type": "array", "minItems": 2, "items": {
            "type": "object", "required": ["nazwa", "naleza"],
            "additionalProperties": False,
            "properties": {"nazwa": {"type": "string"},
                           "naleza": {"type": "array", "items": {"type": "string"}}}}}}},
    "sekwencja": {"required": ["kroki", "brakujace"], "properties": {
        "kroki": {"type": "array", "minItems": 3, "items": {"type": "string"},
                  "description": "Pusty string = pole do uzupełnienia."},
        "brakujace": {"type": "array", "items": {"type": "string"},
                      "description": "Co wpada w puste pola, po kolei. Klucz odpowiedzi."}}},
    "lista_krokow": {"required": ["kroki"], "properties": {
        "kroki": {"type": "array", "minItems": 2, "items": {"type": "string"}}}},
    "proza": {"required": ["akapity"], "properties": {
        "akapity": {"type": "array", "minItems": 1, "items": {"type": "string"}}}},
    "checklista": {"required": ["pozycje"], "properties": {
        "pozycje": {"type": "array", "minItems": 2, "items": {"type": "string"}}}},
    "karty_do_wyciecia": {"required": ["karty"], "properties": {
        "karty": {"type": "array", "minItems": 1, "maxItems": 9, "items": {
            "type": "object", "required": ["awers"], "additionalProperties": False,
            "properties": {"awers": {"type": "string"},
                           "rewers": {"type": "string"},
                           "ilustracja": {"$ref": "#/$defs/ilustracja"}}}},
        "na_arkuszu": {"enum": [8, 9],
                       "description": "Reguła twarda archetypu KARTY: 8 albo 9 na A4."},
        "z_podpisami": {"type": "boolean",
                        "description": "false = wersja dla nieczytających."}}},
    "plansza_gry": {"required": ["pola"], "properties": {
        "pola": {"type": "array", "minItems": 8, "items": {"type": "string"}}}},
    "elementy_ruchome": {"required": ["elementy"], "properties": {
        "elementy": {"type": "array", "minItems": 1, "items": {
            "type": "object", "required": ["nazwa"], "additionalProperties": False,
            "properties": {"nazwa": {"type": "string"},
                           "ile": {"type": "integer", "minimum": 1}}}},
        "rzep": {"type": "string",
                 "description": "Gdzie przykleić rzep. Reguła twarda SEGREGATORA."}}},
}

#: typy, które MAJĄ odpowiedzi — walidator wymaga dla nich klucza
Z_ODPOWIEDZIAMI = ["lacz_pary", "uzupelnij", "wybierz", "dyktando",
                   "dzialania", "sortowanie", "sekwencja"]

ILUSTRACJA = {
    "type": "object", "required": ["id", "brief"], "additionalProperties": False,
    "description": "Zlecenie na ilustrację. `brief` opisuje TYLKO kadr — styl "
                   "dokłada renderer/ilustracje.py. `id` jest per motyw, nie per "
                   "pozycja, żeby ten sam motyw nie kosztował dwa razy.",
    "properties": {"id": {"type": "string", "pattern": "^[a-z0-9-]+$"},
                   "brief": {"type": "string", "minLength": 10},
                   "proporcje": {"enum": ["1:1", "3:2", "2:3", "16:9"]}},
}


def strona(dozwolone):
    return {
        "type": "object",
        "required": ["id", "typ", "polecenie", "dane"],
        "additionalProperties": False,
        "properties": {
            "id": {"type": "string", "pattern": "^[a-z0-9][a-z0-9-]*$"},
            "typ": {"enum": dozwolone},
            "polecenie": {"type": "string", "maxLength": 60,
                          "description": "Do dziecka albo do rodzica. Maks. 8 słów."},
            "dla_rodzica": {"type": "string"},
            "dane": {"type": "object"},
        },
        "allOf": [{"if": {"properties": {"typ": {"const": t}}},
                   "then": {"properties": {"dane": {"$ref": f"#/$defs/d_{t}"}}}}
                  for t in dozwolone],
    }


def meta(archetyp):
    return {
        "type": "object",
        "required": ["slug", "tytul", "archetyp", "wersja", "wiek",
                     "strony_deklarowane", "min_pt_dziecka"],
        "additionalProperties": False,
        "properties": {
            "slug": {"type": "string", "pattern": "^[a-z0-9-]+$"},
            "tytul": {"type": "string"}, "podtytul": {"type": "string"},
            "archetyp": {"const": archetyp},
            "wersja": {"type": "string", "pattern": r"^\d+\.\d+$"},
            "wiek": {"type": "string"},
            "kategoria": {"type": "string"}, "podkategoria": {"type": "string"},
            "strony_deklarowane": {"type": "integer", "minimum": 8},
            "min_pt_dziecka": {"type": "integer", "minimum": 11},
            "ilustracja": {"$ref": "#/$defs/ilustracja"},
        },
    }


WSTEP = {
    "type": "object",
    "required": ["dla_kogo", "obietnica", "jak_korzystac", "czego_nie_robi"],
    "additionalProperties": False,
    "properties": {
        "dla_kogo": {"type": "string"},
        "obietnica": {"type": "string"},
        "warunek_wejscia": {"type": "string"},
        "ile_czasu_dziennie": {"type": "string"},
        "jak_korzystac": {"type": "array", "minItems": 3, "items": {"type": "string"}},
        "czego_nie_robi": {
            "type": "array", "minItems": 2, "items": {"type": "string"},
            "description": "NIE renderujemy tego w PDF-ie (decyzja z 2026-09-25). "
                           "Zostaje jako dana dla spec.md i kreacji reklamowych."},
        "kiedy_do_specjalisty": {"type": "string"},
    },
}

KLUCZ = {"type": "array", "items": {
    "type": "object", "required": ["strona_id", "odpowiedzi"],
    "additionalProperties": False,
    "properties": {"strona_id": {"type": "string"},
                   "odpowiedzi": {"type": "array", "items": {"type": "string"}}}}}

FRAGMENT = {
    "type": "object", "required": ["do_strony", "obietnica_na_stronie"],
    "additionalProperties": False,
    "description": "Żelazna zasada 1: minimum 10 stron.",
    "properties": {"do_strony": {"type": "integer", "minimum": 10},
                   "obietnica_na_stronie": {"type": "string"}}}


# ------------------------------------------------------------- archetypy
ARCHETYPY = {
    "ZESZYT": dict(
        tytul="ZESZYT — zbiór ćwiczeń bez sztywnej sekwencji",
        opis="Bloki uporządkowane od najłatwiejszego. W obrębie bloku kolejność "
             "dowolna. Reguły niewyrażalne w JSON Schema sprawdza validate.py.",
        typy=["tabela", "sciezka", "lacz_pary", "wyrazy_do_czytania", "uzupelnij",
              "wybierz", "pisanie_po_sladzie", "czytanie_zdan", "dyktando",
              "ramka_rysunkowa", "formularz", "dzialania", "sortowanie",
              "sekwencja", "lista_krokow", "karty_do_wyciecia"],
        korzen={"bloki": {"type": "array", "minItems": 2, "items": {
            "type": "object", "required": ["temat", "poziom", "cwiczenia"],
            "additionalProperties": False,
            "properties": {
                "temat": {"type": "string"},
                "poziom": {"type": "integer", "minimum": 1, "maximum": 5,
                           "description": "Bloki MUSZĄ iść od najniższego poziomu."},
                "opis": {"type": "string"},
                "dla_rodzica": {"type": "array", "items": {"type": "string"}},
                "cwiczenia": {"type": "array", "minItems": 1,
                              "items": {"$ref": "#/$defs/strona"}}}}}}),
    "KARTY": dict(
        tytul="KARTY — talia do wycięcia",
        opis="8 albo 9 kart na A4, siatka cięcia, wersja z podpisami i bez "
             "(dla nieczytających).",
        typy=["karty_do_wyciecia", "lista_krokow", "tabela", "formularz", "proza"],
        korzen={"talie": {"type": "array", "minItems": 1, "items": {
            "type": "object", "required": ["nazwa", "format_mm", "arkusze"],
            "additionalProperties": False,
            "properties": {
                "nazwa": {"type": "string"},
                "format_mm": {"type": "array", "minItems": 2, "maxItems": 2,
                              "items": {"type": "integer", "minimum": 30}},
                "bez_podpisow": {"type": "boolean",
                                 "description": "Czy talia ma też wersję dla nieczytających."},
                "arkusze": {"type": "array", "minItems": 1,
                            "items": {"$ref": "#/$defs/strona"}}}}},
            "instrukcja_zabaw": {"type": "array", "minItems": 1, "items": {
                "type": "object", "required": ["nazwa", "kroki"],
                "additionalProperties": False,
                "properties": {"nazwa": {"type": "string"},
                               "wiek": {"type": "string"},
                               "kroki": {"type": "array", "minItems": 2,
                                         "items": {"type": "string"}}}}}}),
    "SEGREGATOR": dict(
        tytul="SEGREGATOR — busy book / Montessori",
        opis="Każda sekcja ma instrukcję przygotowania na pierwszej stronie, "
             "planszę bazową i listę elementów do zalaminowania z miejscem na rzep.",
        typy=["tabela", "sortowanie", "sekwencja", "lacz_pary", "wybierz",
              "elementy_ruchome", "lista_krokow", "karty_do_wyciecia",
              "ramka_rysunkowa", "formularz"],
        korzen={"sekcje": {"type": "array", "minItems": 1, "items": {
            "type": "object",
            "required": ["temat", "instrukcja_przygotowania", "plansza_bazowa",
                         "elementy_ruchome"],
            "additionalProperties": False,
            "properties": {
                "temat": {"type": "string"},
                "poziom": {"type": "integer", "minimum": 1, "maximum": 5},
                "instrukcja_przygotowania": {
                    "$ref": "#/$defs/strona",
                    "description": "ZAWSZE pierwsza strona sekcji — reguła twarda."},
                "plansza_bazowa": {"$ref": "#/$defs/strona"},
                "elementy_ruchome": {"$ref": "#/$defs/strona"},
                "dodatkowe": {"type": "array", "items": {"$ref": "#/$defs/strona"}}}}}}),
    "GRY": dict(
        tytul="GRY — planszówki i gry karciane",
        opis="Zasady na JEDNEJ stronie. Jeśli gra wymaga pionków albo kostki, "
             "są w pliku — nigdy „użyj własnych”.",
        typy=["plansza_gry", "karty_do_wyciecia", "lista_krokow", "tabela", "formularz"],
        korzen={"gry": {"type": "array", "minItems": 1, "items": {
            "type": "object",
            "required": ["nazwa", "gracze", "czas_min", "zasady", "warianty_trudnosci"],
            "additionalProperties": False,
            "properties": {
                "nazwa": {"type": "string"}, "cel": {"type": "string"},
                "gracze": {"type": "string"},
                "czas_min": {"type": "integer", "minimum": 1},
                "przygotowanie": {"type": "array", "items": {"type": "string"}},
                "zasady": {"type": "array", "minItems": 2, "items": {"type": "string"},
                           "description": "Muszą zmieścić się na jednej stronie."},
                "warianty_trudnosci": {"type": "array", "minItems": 1, "items": {
                    "type": "object", "required": ["nazwa", "zmiana"],
                    "additionalProperties": False,
                    "properties": {"nazwa": {"type": "string"},
                                   "zmiana": {"type": "string"}}}},
                "plansza": {"$ref": "#/$defs/strona"},
                "arkusze": {"type": "array", "items": {"$ref": "#/$defs/strona"},
                            "description": "Pionki, kostka, karty — wszystko w pliku."}}}}}),
    "PORADNIK": dict(
        tytul="PORADNIK — materiał dla rodzica",
        opis="Jedyny archetyp z dominującą prozą. Maksimum 65 znaków w linii "
             "pilnuje print.css; validate.py sprawdza to na wyrenderowanym PDF-ie.",
        typy=["proza", "checklista", "formularz", "lista_krokow", "tabela"],
        korzen={"rozdzialy": {"type": "array", "minItems": 2, "items": {
            "type": "object", "required": ["tytul", "strony"],
            "additionalProperties": False,
            "properties": {
                "tytul": {"type": "string"},
                "strony": {"type": "array", "minItems": 1,
                           "items": {"$ref": "#/$defs/strona"}},
                "do_zrobienia_w_tym_tygodniu": {
                    "type": "array", "minItems": 1, "items": {"type": "string"}}}}},
            "checklisty": {"type": "array", "items": {"$ref": "#/$defs/strona"}}}),
}


def zbuduj(nazwa, cfg):
    defs = {"ilustracja": ILUSTRACJA, "strona": strona(cfg["typy"])}
    for t in cfg["typy"]:
        d = dict(D[t])
        defs[f"d_{t}"] = {"type": "object", "additionalProperties": False,
                          "required": d.pop("required"), **d}
    korzen = {"meta": meta(nazwa), "wstep": WSTEP,
              **cfg["korzen"], "klucz_odpowiedzi": KLUCZ, "fragment": FRAGMENT}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://lupa.pl/schema/{nazwa}.schema.json",
        "title": cfg["tytul"], "description": cfg["opis"],
        "type": "object",
        "required": ["meta", "wstep", *cfg["korzen"], "klucz_odpowiedzi", "fragment"],
        "additionalProperties": False,
        "properties": korzen,
        "x-typy-z-odpowiedziami": [t for t in cfg["typy"] if t in Z_ODPOWIEDZIAMI],
        "$defs": defs,
    }


def main():
    import jsonschema
    for nazwa, cfg in ARCHETYPY.items():
        s = zbuduj(nazwa, cfg)
        jsonschema.Draft202012Validator.check_schema(s)
        p = TU / f"{nazwa}.schema.json"
        p.write_text(json.dumps(s, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  {p.name:26} {len(cfg['typy']):>2} typów ćwiczeń")
    print("PROGRAM.schema.json nietknięty — pisany ręcznie.")


if __name__ == "__main__":
    main()
