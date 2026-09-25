# Rozmowa z nauczycielem — specyfikacja

Dane katalogowe pochodzą z `web/mockup/p-rozmowa-z-nauczycielem.html` przez
`produkty/_katalog.json`. Nie zmieniaj ich tutaj ręcznie.

| pole | wartość | źródło |
|---|---|---|
| slug | `rozmowa-z-nauczycielem` | prototyp |
| archetyp | **PORADNIK** | decyzja: dominująca proza czytana przez dorosłego |
| tytuł | Rozmowa z nauczycielem | prototyp |
| podtytuł | Jak przygotować się na zebranie | prototyp |
| wiek | dowolny | prototyp |
| kategoria | rodzic / rozmowy | okruszki prototypu |
| cena | 25 zł | prototyp |
| **objętość** | **36 stron** | tabela `.specs`, klucz „Objętość" |
| autor | Ala Dębska | prototyp — **nie wchodzi do PDF-a** (`brand.md`) |

---

## Dla kogo

Dla rodzica przed pierwszym zebraniem albo przed trudną rozmową o dziecku.

*(zdanie z persymonowej belki na `p-rozmowa-z-nauczycielem.html` — cytat co do znaku)*

## Warunek wejścia

Brak. To materiał dla ciebie.

## Obietnica

Wchodzisz na zebranie z listą pytań i wychodzisz z zapisanymi odpowiedziami, a nie z samym wrażeniem.

## Progresja

Trzy rozdziały: przygotowanie, sama rozmowa, co potem. Arkusz notatek jest w środku i wypełniasz go na miejscu.

## Zakres darmowego fragmentu

Rozdział o przygotowaniu plus arkusz notatek, 10 stron.

## Czego ten materiał NIE robi

- Nie mówi, kto ma rację w sporze ze szkołą.
- Nie jest pismem procesowym ani wzorem skargi.
- Nie zawiera porad prawnych.

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
