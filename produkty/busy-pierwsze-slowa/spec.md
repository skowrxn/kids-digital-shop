# Busy book: Pierwsze słowa — specyfikacja

Dane katalogowe pochodzą z `web/mockup/p-busy-pierwsze-slowa.html` przez
`produkty/_katalog.json`. Nie zmieniaj ich tutaj ręcznie.

| pole | wartość | źródło |
|---|---|---|
| slug | `busy-pierwsze-slowa` | prototyp |
| archetyp | **SEGREGATOR** | decyzja: plansza bazowa z elementami ruchomymi na rzep |
| tytuł | Busy book: Pierwsze słowa | prototyp |
| podtytuł | Segregator Montessori, 140 stron | prototyp |
| wiek | 2–4 lata | prototyp |
| kategoria | busy / maluch | okruszki prototypu |
| cena | 59 zł | prototyp |
| **objętość** | **140 stron** | tabela `.specs`, klucz „Objętość" |
| autor | Kasia Wrona | prototyp — **nie wchodzi do PDF-a** (`brand.md`) |

---

## Dla kogo

Dla dwulatka, który chce robić to samo co starsze rodzeństwo.

*(zdanie z persymonowej belki na `p-busy-pierwsze-slowa.html` — cytat co do znaku)*

## Warunek wejścia

Dziecko chwyta przedmioty palcami i utrzymuje uwagę przez kilka minut.

## Obietnica

Segregator, który dwulatek otwiera sam i robi to samo, co starsze rodzeństwo przy stole.

## Progresja

Sześć sekcji rosnących trudnością: dopasowanie kolorów, kształtów, par, kategorii, sekwencji i pierwszych słów. Każda sekcja zaczyna się instrukcją przygotowania.

## Zakres darmowego fragmentu

Sekcja pierwsza w komplecie, 11 stron: instrukcja, plansza i elementy ruchome.

## Czego ten materiał NIE robi

- Nie uczy czytania ani liczenia.
- Nie jest gotowy od razu — wymaga wydrukowania, zalaminowania i naklejenia rzepów.
- Nie nadaje się dla dziecka, które wkłada drobne elementy do ust.

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
