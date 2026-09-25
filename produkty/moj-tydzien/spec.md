# Mój tydzień — specyfikacja

Dane katalogowe pochodzą z `web/mockup/p-moj-tydzien.html` przez
`produkty/_katalog.json`. Nie zmieniaj ich tutaj ręcznie.

| pole | wartość | źródło |
|---|---|---|
| slug | `moj-tydzien` | prototyp |
| archetyp | **ZESZYT** | decyzja: bloki ćwiczeń bez sekwencji między blokami |
| tytuł | Mój tydzień | prototyp |
| podtytuł | Planer nauki dla rodzica | prototyp |
| wiek | dowolny | prototyp |
| kategoria | rodzic / planowanie | okruszki prototypu |
| cena | 19 zł | prototyp |
| **objętość** | **32 stron** | tabela `.specs`, klucz „Objętość" |
| autor | zespół Lupy | prototyp — **nie wchodzi do PDF-a** (`brand.md`) |

---

## Dla kogo

Dla rodzica, który ma materiały, ale nigdy nie wie, kiedy je zrobić.

*(zdanie z persymonowej belki na `p-moj-tydzien.html` — cytat co do znaku)*

## Warunek wejścia

Brak. Planer wypełnia rodzic.

## Obietnica

W niedzielę wieczorem w pięć minut rozpisujesz tydzień i wiesz, co odpuszczasz.

## Progresja

Trzy bloki: planer podstawowy, wersja dla dwojga i trojga dzieci, oraz arkusze podsumowania miesiąca. Bloki nie mają kolejności — bierzesz ten, który pasuje do twojej logistyki.

## Zakres darmowego fragmentu

Blok podstawowy w całości, 10 stron: cztery tygodnie planera i instrukcja.

## Czego ten materiał NIE robi

- Nie planuje za ciebie. Rubryki są puste.
- Nie jest kalendarzem rodzinnym ani listą zakupów.
- Nie ma dat — wpisujesz własne, więc planer nie traci ważności.

**Uwaga:** ta sekcja **nie jest renderowana w PDF-ie** (decyzja z 2026-09-25).
Zostaje jako dana w `content.json` (`wstep.czego_nie_robi`) i zasila tę
specyfikację oraz kreacje reklamowe.

## Ograniczenia produkcyjne

- **Bez ilustracji.** Ten produkt nie ma pól `ilustracja` — materiał jest
  zaprojektowany tak, żeby działał bez obrazków.
- Wariant domyślny czarno-biały, ≤12% pokrycia tuszem na stronie.
- Minimum **12 pt** dla wszystkiego, co czyta dziecko.
- Stopka: tylko tytuł i numer strony.
- Wszystkie rubryki do wypełnienia są **puste** — żadnych danych dziecka.
