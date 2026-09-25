# Liczę do 20 na palcach i bez — specyfikacja

Dane katalogowe pochodzą z `web/mockup/p-licze-do-20.html` przez
`produkty/_katalog.json`. Nie zmieniaj ich tutaj ręcznie.

| pole | wartość | źródło |
|---|---|---|
| slug | `licze-do-20` | prototyp |
| archetyp | **ZESZYT** | decyzja: bloki ćwiczeń bez sekwencji między blokami |
| tytuł | Liczę do 20 na palcach i bez | prototyp |
| podtytuł | Matematyka konkretna, 90 stron | prototyp |
| wiek | 5–6 lat | prototyp |
| kategoria | matematyka / liczenie | okruszki prototypu |
| cena | 45 zł | prototyp |
| **objętość** | **90 stron** | tabela `.specs`, klucz „Objętość" |
| autor | Paweł Nowak | prototyp — **nie wchodzi do PDF-a** (`brand.md`) |

---

## Dla kogo

Dla przedszkolaka i pierwszaka, który liczy z pamięci, ale gubi się przy pięciu jabłkach.

*(zdanie z persymonowej belki na `p-licze-do-20.html` — cytat co do znaku)*

## Warunek wejścia

Dziecko powtarza za tobą liczby do dziesięciu, nawet jeśli nie rozumie, co znaczą.

## Obietnica

Dziecko liczy pięć jabłek i wie, że to pięć — nie tylko recytuje ciąg do dwudziestu.

## Progresja

Cztery bloki: liczenie na konkretach, przejście na papier, cyfra jako zapis, liczby do dwudziestu. Cyfra pojawia się dopiero w bloku trzecim — to celowe.

## Zakres darmowego fragmentu

Blok pierwszy w całości, 12 stron: liczenie na konkretach.

## Czego ten materiał NIE robi

- Nie uczy dodawania. To jest w „Dodawaniu bez liczenia na palcach”.
- Nie ćwiczy pisania cyfr ładnie — tylko ich rozpoznawania.
- Nie jest testem gotowości szkolnej.

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
