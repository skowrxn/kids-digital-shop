# Głoska Sz, Ż, Cz krok po kroku — specyfikacja

Dane katalogowe pochodzą z `web/mockup/p-gloski-szumiace.html` przez
`produkty/_katalog.json`. Nie zmieniaj ich tutaj ręcznie.

| pole | wartość | źródło |
|---|---|---|
| slug | `gloski-szumiace` | prototyp |
| archetyp | **PROGRAM** | decyzja: sztywna sekwencja, trudność rośnie monotonicznie |
| tytuł | Głoska Sz, Ż, Cz krok po kroku | prototyp |
| podtytuł | Zestaw ćwiczeń logopedycznych | prototyp |
| wiek | 4–8 lat | prototyp |
| kategoria | logopedia / szumiace | okruszki prototypu |
| cena | 69 zł | prototyp |
| **objętość** | **132 stron** | tabela `.specs`, klucz „Objętość" |
| autor | Anna Bem | prototyp — **nie wchodzi do PDF-a** (`brand.md`) |

---

## Dla kogo

Dla dziecka, które seplenі, i dla rodzica czekającego w kolejce do logopedy.

*(zdanie z persymonowej belki na `p-gloski-szumiace.html` — cytat co do znaku)*

## Warunek wejścia

Dziecko potrafi naśladować ruch języka pokazany przez dorosłego i wytrzymuje pięć minut ćwiczeń.

## Obietnica

Dziecko przechodzi pełną ścieżkę dla Sz, Ż i Cz: od ustawienia języka, przez sylaby i wyrazy, po zdania.

## Progresja

Dwanaście tygodni. Kolejność jest tu najważniejsza i nie wolno jej skracać: ustawienie, izolowana głoska, sylaby otwarte, sylaby zamknięte, wyrazy, zdania, mowa spontaniczna. Każdy tydzień powtarza materiał z dwóch poprzednich.

## Zakres darmowego fragmentu

Cały tydzień 1 plus wstęp, 14 stron.

## Czego ten materiał NIE robi

- To NIE jest terapia logopedyczna i nie zastępuje wizyty u specjalisty.
- Nie stawia rozpoznania i nie mówi, czy wymowa dziecka mieści się w normie wiekowej.
- Nie nadaje się dla dziecka, które ma nieprawidłową budowę aparatu mowy — to trzeba najpierw sprawdzić u specjalisty.
- Nie zawiera nagrań. Wszystkie instrukcje są opisowe.

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
