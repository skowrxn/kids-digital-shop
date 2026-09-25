# Emocjometr — specyfikacja

Dane katalogowe pochodzą z `web/mockup/p-emocjometr.html` przez
`produkty/_katalog.json`. Nie zmieniaj ich tutaj ręcznie.

| pole | wartość | źródło |
|---|---|---|
| slug | `emocjometr` | prototyp |
| archetyp | **KARTY** | decyzja: talia do wycięcia, 8–9 kart na A4 |
| tytuł | Emocjometr | prototyp |
| podtytuł | Karty rozmów o uczuciach | prototyp |
| wiek | 4–9 lat | prototyp |
| kategoria | emocje / rozpoznawanie | okruszki prototypu |
| cena | 39 zł | prototyp |
| **objętość** | **64 stron** | tabela `.specs`, klucz „Objętość" |
| autor | Julia Rak | prototyp — **nie wchodzi do PDF-a** (`brand.md`) |

---

## Dla kogo

Dla dziecka, które na pytanie „co się stało” odpowiada „nic”.

*(zdanie z persymonowej belki na `p-emocjometr.html` — cytat co do znaku)*

## Warunek wejścia

Dziecko potrafi wskazać palcem i nazwać kilka podstawowych emocji: radość, złość, smutek.

## Obietnica

Dziecko pokazuje na karcie, co czuje, zamiast odpowiadać „nic”.

## Progresja

Trzy talie: miny, sytuacje i natężenie. Zaczynacie od min, bo są najłatwiejsze. Talia sytuacji ma sens dopiero, gdy dziecko nazywa miny bez wahania.

## Zakres darmowego fragmentu

Talia min w komplecie, **18 stron**: instrukcja cięcia, karty z podpisami, karty bez podpisów, słownik min i karta pytań dla rodzica.

*(Korekta wobec pierwotnego szacunku 11 stron: talia liczy 45 min, więc kończy się dopiero na stronie 18. Fragment tniemy po pełnych stronach od początku pliku, więc urwanie talii w połowie dałoby fragment bez wersji dla nieczytających.)*

## Czego ten materiał NIE robi

- Nie jest narzędziem oceny stanu dziecka. To pomoc do rozmowy.
- Nie służy do rozstrzygania sporów między rodzeństwem.
- Nie działa w środku wybuchu. Używacie go przed albo po.

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
