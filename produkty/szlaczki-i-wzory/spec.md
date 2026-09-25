# Szlaczki i wzory — specyfikacja

Dane katalogowe pochodzą z `web/mockup/p-szlaczki-i-wzory.html` przez
`produkty/_katalog.json`. Nie zmieniaj ich tutaj ręcznie.

| pole | wartość | źródło |
|---|---|---|
| slug | `szlaczki-i-wzory` | prototyp |
| archetyp | **ZESZYT** | decyzja: bloki ćwiczeń bez sekwencji między blokami |
| tytuł | Szlaczki i wzory | prototyp |
| podtytuł | 120 stron od grubej linii do cienkiej | prototyp |
| wiek | 4–6 lat | prototyp |
| kategoria | grafo / szlaczki | okruszki prototypu |
| cena | 35 zł | prototyp |
| **objętość** | **120 stron** | tabela `.specs`, klucz „Objętość" |
| autor | Ewa Lis | prototyp — **nie wchodzi do PDF-a** (`brand.md`) |

---

## Dla kogo

Dla przedszkolaka przygotowującego się do pisania.

*(zdanie z persymonowej belki na `p-szlaczki-i-wzory.html` — cytat co do znaku)*

## Warunek wejścia

Dziecko trzyma kredkę i rysuje kreskę od punktu do punktu.

## Obietnica

Ręka dziecka schodzi z grubej kreski na cienką stopniowo, bez przeskoku, który zwykle kończy się zniechęceniem.

## Progresja

Pięć bloków po grubości linii: od 20 mm do 4 mm. W obrębie bloku kolejność dowolna. Przejście do kolejnego bloku dopiero, gdy dziecko mieści się w linii bez napinania ręki.

## Zakres darmowego fragmentu

Blok pierwszy, najgrubszy, 12 stron.

## Czego ten materiał NIE robi

- Nie uczy liter. Litery są w „Literach pisanych”.
- Nie ocenia ładności pisma.
- Nie zadziała, jeśli dziecko boli ręka — wtedy najpierw „Piszę bez nacisku”.

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
