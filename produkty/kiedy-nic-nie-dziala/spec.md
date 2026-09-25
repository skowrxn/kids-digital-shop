# Kiedy nic nie działa — specyfikacja

Dane katalogowe pochodzą z `web/mockup/p-kiedy-nic-nie-dziala.html` przez
`produkty/_katalog.json`. Nie zmieniaj ich tutaj ręcznie.

| pole | wartość | źródło |
|---|---|---|
| slug | `kiedy-nic-nie-dziala` | prototyp |
| archetyp | **PORADNIK** | decyzja: dominująca proza czytana przez dorosłego |
| tytuł | Kiedy nic nie działa | prototyp |
| podtytuł | Co robić, gdy dziecko odmawia | prototyp |
| wiek | dowolny | prototyp |
| kategoria | rodzic / motywacja | okruszki prototypu |
| cena | 25 zł | prototyp |
| **objętość** | **40 stron** | tabela `.specs`, klucz „Objętość" |
| autor | Julia Rak | prototyp — **nie wchodzi do PDF-a** (`brand.md`) |

---

## Dla kogo

Dla rodzica, który kupił już trzy programy i żaden nie ruszył.

*(zdanie z persymonowej belki na `p-kiedy-nic-nie-dziala.html` — cytat co do znaku)*

## Warunek wejścia

Brak. To materiał dla ciebie, nie dla dziecka.

## Obietnica

Rozpoznajesz, która z czterech najczęstszych przyczyn dotyczy waszego domu, i masz jedną rzecz do sprawdzenia w tym tygodniu.

## Progresja

Cztery rozdziały, po jednej przyczynie. Każdy kończy się checklistą na tydzień. Czytasz po kolei albo od razu ten, który brzmi znajomo.

## Zakres darmowego fragmentu

Rozdział pierwszy w całości plus spis pozostałych, 10 stron.

## Czego ten materiał NIE robi

- Nie diagnozuje dziecka ani rodzica.
- Nie obiecuje, że po tygodniu dziecko samo siądzie do nauki.
- Nie jest poradnikiem wychowawczym. Dotyczy jednej rzeczy: odmowy siadania do materiałów.

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
