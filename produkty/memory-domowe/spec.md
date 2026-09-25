# Memory domowe — specyfikacja

Dane katalogowe pochodzą z `web/mockup/p-memory-domowe.html` przez
`produkty/_katalog.json`. Nie zmieniaj ich tutaj ręcznie.

| pole | wartość | źródło |
|---|---|---|
| slug | `memory-domowe` | prototyp |
| archetyp | **KARTY** | decyzja: talia do wycięcia, 8–9 kart na A4 |
| tytuł | Memory domowe | prototyp |
| podtytuł | Cztery zestawy po 48 kart | prototyp |
| wiek | 3–8 lat | prototyp |
| kategoria | gry / memory | okruszki prototypu |
| cena | 29 zł | prototyp |
| **objętość** | **52 stron** | tabela `.specs`, klucz „Objętość" |
| autor | Michał Ptak | prototyp — **nie wchodzi do PDF-a** (`brand.md`) |

---

## Dla kogo

Dla trzylatka i dla wieczoru, kiedy nikt nie ma siły na nic skomplikowanego.

*(zdanie z persymonowej belki na `p-memory-domowe.html` — cytat co do znaku)*

## Warunek wejścia

Dziecko utrzymuje uwagę przez pięć minut przy stole i rozumie zasadę „odkryj dwie”.

## Obietnica

Dziecko gra z wami w memory kartami, które zna — i wygrywa wystarczająco często, żeby chcieć grać dalej.

## Progresja

Cztery komplety: zwierzęta, jedzenie, pojazdy i emocje. Wersja dla młodszych ma 24 karty zamiast 48 — zaczynacie od niej.

## Zakres darmowego fragmentu

Komplet „zwierzęta” w całości, **13 stron**: instrukcja przygotowania, sześć arkuszy kart z podpisami i trzy arkusze bez podpisów.

*(Korekta wobec szacunku 10 stron: komplet liczy 24 pary i kończy się na stronie 13. Fragment tniemy po pełnych stronach od początku pliku, więc ucięcie na dziesiątej dałoby niepełną talię — bezużyteczną, bo memory wymaga kompletu par.)*

## Czego ten materiał NIE robi

- Nie uczy czytania. Karty są obrazkowe.
- Nie jest testem pamięci. Nie liczcie, ile par kto zapamiętał.
- Nie ma wersji na jedną osobę — to gra we dwoje albo więcej.

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
