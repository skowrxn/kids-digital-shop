# Karty rutyn: poranek i wieczór — specyfikacja

Dane katalogowe pochodzą z `web/mockup/p-karty-rutyn.html` przez
`produkty/_katalog.json`. Nie zmieniaj ich tutaj ręcznie.

| pole | wartość | źródło |
|---|---|---|
| slug | `karty-rutyn` | prototyp |
| archetyp | **KARTY** | decyzja: talia do wycięcia, 8–9 kart na A4 |
| tytuł | Karty rutyn: poranek i wieczór | prototyp |
| podtytuł | 48 kart i tablica | prototyp |
| wiek | 3–7 lat | prototyp |
| kategoria | rutyny / plan-dnia | okruszki prototypu |
| cena | 29 zł | prototyp |
| **objętość** | **56 stron** | tabela `.specs`, klucz „Objętość" |
| autor | Ala Dębska | prototyp — **nie wchodzi do PDF-a** (`brand.md`) |

---

## Dla kogo

Dla domu, w którym poranek to codziennie ta sama awantura.

*(zdanie z persymonowej belki na `p-karty-rutyn.html` — cytat co do znaku)*

## Warunek wejścia

Dziecko rozpoznaje przedmioty na obrazkach i potrafi wykonać prostą czynność samodzielnie. Czytać nie musi.

## Obietnica

Dziecko samo przechodzi przez poranek i wieczór, przesuwając kartę po każdej zrobionej rzeczy — bez przypominania za każdym razem.

## Progresja

Dwie talie po 24 karty: poranek i wieczór. W obrębie talii kolejność ustalacie sami — to nie jest kurs, tylko narzędzie. Trzecia talia to karty puste do dopisania własnych.

## Zakres darmowego fragmentu

Pełna talia poranna, 12 stron: instrukcja, arkusze kart i dwie zabawy.

## Czego ten materiał NIE robi

- Nie jest systemem nagród ani kar. Karty pokazują kolejność, nie oceniają.
- Nie zadziała sama z siebie. Przez pierwszy tydzień przechodzicie przez nie razem.
- Nie zastępuje rozmowy o tym, dlaczego rano trzeba wyjść z domu o ósmej.

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
