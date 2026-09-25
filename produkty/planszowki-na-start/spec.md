# Planszówki na start — specyfikacja

Dane katalogowe pochodzą z `web/mockup/p-planszowki-na-start.html` przez
`produkty/_katalog.json`. Nie zmieniaj ich tutaj ręcznie.

| pole | wartość | źródło |
|---|---|---|
| slug | `planszowki-na-start` | prototyp |
| archetyp | **GRY** | decyzja: zasady gry i rozgrywka |
| tytuł | Planszówki na start | prototyp |
| podtytuł | Sześć gier do wydruku i sklejenia | prototyp |
| wiek | 4–8 lat | prototyp |
| kategoria | gry / planszowki | okruszki prototypu |
| cena | 39 zł | prototyp |
| **objętość** | **80 stron** | tabela `.specs`, klucz „Objętość" |
| autor | Michał Ptak | prototyp — **nie wchodzi do PDF-a** (`brand.md`) |

---

## Dla kogo

Dla rodzin, które grają w niedzielę i mają dość Chińczyka.

*(zdanie z persymonowej belki na `p-planszowki-na-start.html` — cytat co do znaku)*

## Warunek wejścia

Dziecko liczy do sześciu i wytrzymuje przegraną na tyle, żeby dokończyć partię.

## Obietnica

Rodzina gra w niedzielę w coś innego niż Chińczyk, a przygotowanie zajmuje jeden wydruk i dziesięć minut z nożyczkami.

## Progresja

Sześć gier od najprostszej do najdłuższej: liczenie, kolejność, pamięć, decyzja. Każda ma wariant łatwiejszy i trudniejszy, więc rośnie razem z dzieckiem.

## Zakres darmowego fragmentu

Pierwsza gra w komplecie, 10 stron: zasady, plansza, pionki i kostka.

## Czego ten materiał NIE robi

- Nie uczy konkretnego przedmiotu szkolnego.
- Nie działa bez dorosłego przy pierwszej partii.
- Nie zawiera gier na czas — u nas nikt się nie ściga.

**Uwaga:** ta sekcja **nie jest renderowana w PDF-ie** (decyzja z 2026-09-25).
Zostaje jako dana w `content.json` (`wstep.czego_nie_robi`) i zasila tę
specyfikację oraz kreacje reklamowe.

## Ograniczenia produkcyjne

- **Bez ilustracji.** Ten produkt nie ma pól `ilustracja` — materiał jest
  zaprojektowany tak, żeby działał bez obrazków.
- Wariant domyślny czarno-biały, ≤12% pokrycia tuszem na stronie.
- Minimum **14 pt** dla wszystkiego, co czyta dziecko.
- Stopka: tylko tytuł i numer strony.
- Wszystkie rubryki do wypełnienia są **puste** — żadnych danych dziecka.
