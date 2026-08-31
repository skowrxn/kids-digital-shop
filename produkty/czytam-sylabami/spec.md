# Czytam sylabami — specyfikacja

Dane katalogowe pochodzą z `web/mockup/p-czytam-sylabami.html`
przez `produkty/_katalog.json`. Nie zmieniaj ich tutaj ręcznie.

| pole | wartość | źródło |
|---|---|---|
| slug | `czytam-sylabami` | prototyp |
| archetyp | **PROGRAM** | decyzja: sztywna sekwencja, trudność rośnie |
| tytuł | Czytam sylabami | prototyp |
| podtytuł | 12-tygodniowy program nauki czytania | prototyp |
| wiek | 5–7 lat | prototyp |
| kategoria | czytanie / sylaby (Czytanie sylabami) | okruszki prototypu |
| cena | 79 zł | prototyp |
| **objętość** | **184 strony** | tabela `.specs`, klucz „Objętość" |
| autor | Marta Zielińska | prototyp — **nie wchodzi do PDF-a** (`brand.md`) |

---

## Dla kogo

Dla dziecka, które zna litery, ale nie potrafi ich połączyć w słowo.

*(zdanie z persymonowej belki na `p-czytam-sylabami.html` — cytat co do znaku)*

## Warunek wejścia

Dziecko rozpoznaje przynajmniej kilka liter i potrafi je nazwać. Nie musi
znać całego alfabetu ani umieć pisać. Musi wysiedzieć przy stole
dziesięć minut.

Jeśli dziecko nie rozpoznaje jeszcze żadnej litery — najpierw
„Litery od zera", potem ten program.

## Obietnica

Po dwunastu tygodniach dziecko przeczyta samo ośmiostronicową książeczkę
złożoną ze zdań, które zna. Nie „będzie czytać płynnie" — przeczyta
tę jedną książeczkę, samo, na głos.

## Progresja

Dwanaście tygodni, jeden poziom trudności na tydzień, bez przeskoków.
Kolejność spółgłosek wynika z trudności artykulacyjnej i odróżnialności
kształtu, nie z alfabetu.

| tydzień | co dochodzi | poziom |
|---|---|---|
| 1 | samogłoski A O U I E Y | 1 |
| 2 | M — pierwsze sylaby otwarte | 2 |
| 3 | P | 3 |
| 4 | L, B | 4 |
| 5 | T, D | 5 |
| 6 | K, N | 6 |
| 7 | S, W | 7 |
| 8 | **sylaba zamknięta** (KOT, DOM) | 8 |
| 9 | Z, C, G, J | 9 |
| 10 | dwuznaki SZ, CZ, Ż, CH, DZ | 10 |
| 11 | R i zbiegi spółgłoskowe (BRAT, TRAWA) | 11 |
| 12 | zdania i książeczka — pełna powtórka | 12 |

**Reguła twarda:** `poziom_trudnosci` rośnie monotonicznie. Każdy tydzień
od drugiego powtarza materiał z co najmniej dwóch poprzednich tygodni
(interleaving) — nie tylko wprowadza nowy. Walidator to sprawdza.

Tydzień 8 jest znanym miejscem, w którym dzieci się zacinają. Dlatego
istnieje osobny produkt „Sylaby zamknięte — dogrywka" i karta rodzica
w tygodniu 8 wprost do niego kieruje.

## Budowa tygodnia — 15 stron

| strona | co |
|---|---|
| 1 | karta rodzica: co powiedzieć, na co uważać, kiedy dalej |
| 2–12 | materiał dziecka, 11 stron |
| 13 | gra tygodnia |
| 14 | czytanka |
| 15 | karta postępu (pusta) |

**Bilans do 184 stron:** 3 strony wstępu (tytułowa + „jak korzystać" ×2)
+ 12 × 15 = 180 + 1 strona klucza odpowiedzi = **184**. Zgadza się
z prototypem co do strony, bez tolerancji ±2.

Jedenaście stron dziecka to stały szkielet, ten sam w każdym tygodniu —
zmieniają się dane, nie układ:

1. tabela nowych sylab (duży stopień pisma)
2. tabela powtórkowa z poprzednich tygodni
3. ścieżka sylab do przeczytania palcem
4. łączenie sylab w wyrazy
5. wyrazy z podziałem na sylaby
6. uzupełnianie brakującej sylaby
7. wybór wyrazu (podpowiedź czyta rodzic)
8. pisanie sylab po śladzie
9. czytanie zdań *(tygodnie 1–3: dodatkowa ścieżka sylab — zdań jeszcze nie ma)*
10. dyktando sylabowe
11. ramka rysunkowa: przeczytaj i narysuj

## Zakres darmowego fragmentu

**Cały tydzień 1 plus wstęp: strony 1–18.** Osiemnaście stron, w tym
komplet materiału dziecka, gra, czytanka i karta rodzica.

Prototyp obiecuje: *„Cztery pierwsze strony z 184. Cały fragment
pobierzesz za darmo, bez zakładania konta."* Fragment musi tę obietnicę
pokryć — walidator porównuje.

## Czego ten materiał NIE robi

- **Nie jest terapią ani diagnozą.** To ćwiczenia do domu.
- **Nie uczy pisania.** Dziecko pisze po śladzie, żeby zapamiętać kształt.
  Nauka pisania to „Litery pisane" i „Piszę bez nacisku".
- **Nie uczy czytania ze zrozumieniem dłuższych tekstów.** Kończy się
  na zdaniu i ośmiostronicowej książeczce. Dalej idzie
  „Czytam i rozumiem".
- **Nie ocenia dziecka i nie porównuje go z rówieśnikami.** Karta postępu
  porównuje dziecko z nim samym sprzed tygodnia.
- **Nie zadziała w tydzień.** Dwanaście tygodni to minimum, nie obietnica
  marketingowa. Wolniej jest w porządku.

## Ograniczenia produkcyjne

- **Bez ilustracji.** Nie mamy API do generowania obrazów, więc materiał
  jest zaprojektowany tak, żeby ich nie potrzebować: gdzie normalnie
  byłby obrazek, jest ramka, w której **rysuje dziecko**, albo podpowiedź
  słowna, którą **czyta rodzic**. To nie jest brak do załatania później —
  to jest decyzja projektowa.
- **Bez nagrań.** Materiał nie odsyła do wideo ani audio.
- Wariant domyślny czarno-biały, ≤12% pokrycia tuszem na stronie.
- Minimum **14 pt** dla wszystkiego, co czyta dziecko. Tabele sylab 28 pt.
- Karta postępu jest **zawsze pusta** — żadnych danych dziecka w pliku.
