# Litery od zera — specyfikacja

Dane katalogowe pochodzą z `web/mockup/p-litery-od-zera.html` przez
`produkty/_katalog.json`. Nie zmieniaj ich tutaj ręcznie.

| pole | wartość | źródło |
|---|---|---|
| slug | `litery-od-zera` | prototyp |
| archetyp | **PROGRAM** | decyzja: sztywna sekwencja, trudność rośnie monotonicznie |
| tytuł | Litery od zera | prototyp |
| podtytuł | Poznajemy alfabet bez pośpiechu | prototyp |
| wiek | 4–6 lat | prototyp |
| kategoria | czytanie / litery | okruszki prototypu |
| cena | 45 zł | prototyp |
| **objętość** | **96 stron** | tabela `.specs`, klucz „Objętość" |
| autor | Kasia Wrona | prototyp — **nie wchodzi do PDF-a** (`brand.md`) |

---

## Dla kogo

Dla przedszkolaka, który zaczyna pytać, co to za znaczki.

*(zdanie z persymonowej belki na `p-litery-od-zera.html` — cytat co do znaku)*

## Warunek wejścia

Dziecko pyta, co to za znaczki, i wytrzymuje przy stole dziesięć minut.

## Obietnica

Po programie dziecko rozpoznaje wszystkie litery drukowane i układa z nich swoje imię.

## Progresja

Litery po dwie na tydzień, w kolejności od najłatwiejszych do wymówienia. Każdy tydzień powtarza litery z dwóch poprzednich. Trudność rośnie monotonicznie.

## Zakres darmowego fragmentu

Cały tydzień 1 plus wstęp, 11 stron.

## Czego ten materiał NIE robi

- Nie uczy czytania sylabami. To kolejny krok: „Czytam sylabami”.
- Nie uczy pisania liter, tylko ich rozpoznawania i pisania po śladzie.
- Nie ma terminu. Jedna litera na dwa dni to sugestia, nie norma.

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
