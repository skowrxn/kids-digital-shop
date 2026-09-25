# Lupa — marka, ton głosu, frazy zakazane

Dokument wiążący. Każdy tekst w tym repo — opis produktu, instrukcja dla
rodzica, nagłówek reklamy, nazwa ćwiczenia — przechodzi przez te reguły.
Walidator (`renderer/validate.py`) egzekwuje sekcję „Frazy zakazane"
automatycznie i wywala build.

---

## Kim jesteśmy

Lupa sprzedaje materiały do druku, które rodzic odpala w domu, bez
przygotowania i bez sprzętu. Kartka, ołówek, dwadzieścia minut.

Konkurencja to Etsy i grupy na Facebooku: PDF-y bez kolejności, bez
instrukcji, bez informacji, czy to w ogóle na wiek twojego dziecka.
Nasza przewaga jest jedna i trzeba ją słychać w każdym zdaniu:
**wiadomo, co robicie w tym tygodniu, a co dopiero za miesiąc.**

Maskotka to Bruno — jeż z przewymiarowaną lupą. Występuje w grafice,
nie w tekście. Nie pisz „Bruno ci pomoże".

---

## Do kogo mówimy

Do rodzica. Nigdy do dziecka, nigdy do nauczyciela, nigdy do „opiekuna".
Dziecko jest w trzeciej osobie: „twoje dziecko", „on", „ona", „dziecko".

Rodzic ma mało czasu, trochę poczucia winy i zero cierpliwości do żargonu.
Wie, co go boli. Nie wie, co z tym zrobić.

Pełne profile: `marka/icp.md`.

---

## Ton głosu

Wzorzec to opisy produktów w `web/mockup/p-*.html` i teksty na `index.html`.
Zanim napiszesz cokolwiek dłuższego niż nagłówek, przeczytaj jeden z nich.

**Pięć reguł:**

1. **Druga osoba, liczba pojedyncza.** „Usiądziesz z dzieckiem", nie
   „Rodzic siada z dzieckiem". Nie „Państwo".
2. **Konkret zamiast obietnicy.** Nie „rozwija kompetencje czytelnicze",
   tylko „po ośmiu tygodniach dziecko przeczyta zdanie z trzech wyrazów".
   Liczba, czynność albo scena. Nic innego nie jest konkretem.
3. **Zdania krótkie.** Średnia poniżej 15 słów. Jedna myśl na zdanie.
4. **Zero żargonu pedagogicznego.** Lista niżej.
5. **Przyznajemy ograniczenia.** Każdy `spec.md` ma sekcję „czego to nie
   robi" i to nie jest asekuracja prawnicza, tylko powód, dla którego
   ktoś nam uwierzy.

**Nagłówki display piszemy małą literą** — reguła z `design-system.md`,
obowiązuje też w PDF-ach.

**Nie mówimy tak:**

| zamiast | pisz |
|---|---|
| wspomaga rozwój kompetencji | dziecko nauczy się |
| stymuluje | ćwiczy |
| holistyczne podejście | (wytnij) |
| dedykowany maluchom | dla dzieci 3–5 lat |
| innowacyjna metoda | (wytnij) |
| angażująca forma zabawy | zabawa |
| percepcja słuchowa | słyszenie różnicy między głoskami |
| motoryka mała | ręka, chwyt, nadgarstek |
| deficyt / trudność | (nazwij konkretnie: „myli b z d") |
| Państwa dziecko | twoje dziecko |
| zapraszamy do zakupu | (wytnij) |

**Emoji: nie.** Ani w produktach, ani w reklamach. Wykrzykniki: maksimum
jeden na stronę, i raczej nie.

---

## Frazy zakazane — twarda bramka

Walidator skanuje `content.json` i teksty reklamowe. Trafienie = build pada
ze statusem `blad`.

### A. Terapia, diagnoza, leczenie

Obowiązuje **wszędzie**, ze szczególną ostrością w kategoriach `logopedia`
i `emocje`. Jesteśmy materiałem do ćwiczeń w domu. Nie jesteśmy terapią.

Zakazane rdzenie (dopasowanie po rdzeniu, odmiana nie ma znaczenia):

```
terapi        (terapia, terapeutyczny, terapeuta, terapii)
diagnoz       (diagnoza, diagnostyczny, zdiagnozuj)
lecz          (leczenie, wyleczy, leczniczy)
kurac         (kuracja)
zaburz        (zaburzenie, zaburzenia mowy)
dysleks / dysgraf / dyskalk
ADHD / autyz / spektrum / Asperger
opóźnienie rozwoju / opóźniony rozwój      (jako etykieta dziecka)
wada wymowy / wada postawy
korekcja / korygowanie                      (o dziecku)
niepełnosprawn
objaw / symptom / rokowanie / wskazanie
recepta / dawkowanie
nerwica / depresja / lęk uogólniony / trauma
```

**Wyjątek, jedyny:** wolno napisać zdanie, które kieruje do specjalisty,
w formie „jeśli … , umów się do logopedy / porozmawiaj z pediatrą".
To jest przekierowanie, nie diagnoza. Walidator przepuszcza rdzeń
`logoped` i `pediatr` wyłącznie w takim zdaniu (lista wzorców w
`renderer/validate.py`, klucz `wyjatki_skierowanie`).

**Nazwa produktu „Mowa startuje" i podkategoria „Opóźniony rozwój mowy"
pochodzą z prototypu i są dozwolone jako nazwy własne** — walidator
pomija je po dokładnym dopasowaniu. Nie wolno ich rozwijać w treści.

### B. Obietnice wyniku i porównania dzieci

```
gwarantujemy / gwarancja efektu / na pewno nauczy
w X dni nauczysz dziecko czytać        (deadline na umiejętność)
dogoni rówieśników / nie zostanie w tyle
lepszy niż inne dzieci / przewyższy
przygotuje do szkoły w 100%
geniusz / cudowne dziecko / zdolniejsze
```

Nie porównujemy dziecka do innych dzieci. Nigdy. Porównujemy dziecko
do niego samego sprzed miesiąca — to jest karta postępu.

### C. Straszenie rodzica

```
stracisz czas / zmarnujesz
będzie za późno / ostatni moment
twoje dziecko zostanie w tyle
zaniedbanie / twoja wina
jeśli teraz nie zaczniesz
```

Poczucie winy to nie jest nasz kanał sprzedaży.

### D. Reklamy — reguły Meta

Pełna lista z przykładami: `marka/angles.md`, sekcja „Ograniczenia Meta".
Skrót: nigdy nie sugerujemy, że znamy cechę lub stan odbiorcy.
Zakazane konstrukcje: „Twoje dziecko ma…", „Twoje dziecko jest…",
„Czy twoje dziecko nie potrafi…", „Masz dziecko z…".
Zero przed/po w kontekście rozwoju dziecka.

---

## Autorzy

Na czas testów autorzy są **wymyśleni**. Nie są to prawdziwe osoby i nie
wolno dopisywać im tytułów zawodowych, numerów uprawnień ani miejsc pracy.
Imię i nazwisko z prototypu, nic więcej.

**Gdzie autor jest, a gdzie go nie ma.** Reguła jest zakresowa, nie zero-jedynkowa:

| miejsce | imię i nazwisko | rola („neurologopeda, 14 lat praktyki") |
|---|---|---|
| `produkty/_katalog.json` | **tak** | tak, jako `autor_rola_prototyp` |
| strony prototypu `web/mockup/` | **tak** (są tam już) | tak (są tam już) |
| strona tytułowa PDF-a | **nie** | nie |
| stopka PDF-a | nie | nie |
| teksty reklamowe `reklamy/` | **nie** | nie |

Powód rozdziału: katalog ma się zgadzać z prototypem co do znaku (żelazna
zasada 6), ale PDF i reklama to miejsca, w których wymyślone nazwisko
zaczyna działać jak dowód wiarygodności. Tam go nie dajemy.

W PDF-ie zamiast autora idzie **wydawca**: `Lupa`. Kąt reklamowy A8
(`autor`) opiera się na metodzie i strukturze materiału, nie na osobie.

**Planowana zmiana:** nazwiska zostaną docelowo zastąpione wzmianką
o współautorstwie AI. Do tego czasu zostają jak w prototypie. Kiedy
zmiana nadejdzie, ruszamy `_katalog.json` przez ekstraktor i `web/mockup/`,
a PDF-y i reklamy nie wymagają żadnej zmiany — nie ma w nich autora.

**Opinie w prototypie też są wygenerowane** (bloki `.revs`, awatary
`img/ava*.webp`). Nie cytuj ich jako prawdziwych i nie przenoś do bazy.

Obsada autorska z prototypu (`web/mockup/index.html`):

| autor | domena |
|---|---|
| Marta Zielińska | czytanie, sylaby |
| Kasia Wrona | litery, busy booki, samodzielność |
| Paweł Nowak | matematyka |
| Ala Dębska | rutyny, czytanie ze zrozumieniem, rozmowy ze szkołą |
| Julia Rak | emocje |
| Anna Bem | logopedia |
| Renata Kołodziej | logopedia, najmłodsi |
| Tom Bryant | angielski |
| Ewa Lis | grafomotoryka, pisanie |
| Iga Sobczak | nauka o świecie, teczki tematyczne |
| Michał Ptak | gry, teczki |
| zespół Lupy | materiały sezonowe i zbiorcze |

Stopka PDF-a zawiera **wyłącznie tytuł i numer strony**. Nie ma w niej
autora, adresu ani numeru wersji.

---

## Dane dzieci

Nigdzie w produkcie ani w kodzie nie ma danych żadnego dziecka. Żadnych
imion z życia, zdjęć, dat urodzenia, wyników, nagrań. Karta postępu jest
pusta i wypełnia ją rodzic u siebie w domu — my drukujemy tylko rubryki.

Imiona w treściach zadań i czytankach są **generyczne i z góry ustalone**:
Ola, Kuba, Zosia (obsada z `img/cast.png`), plus Ala, Tomek, Ewa, Adam.
Nie dobieraj imion pod dziecko użytkownika.

---

## Ilustracje w produktach

Powstają przez `renderer/ilustracje.py` (kie.ai, `gpt-image-2`). Reguły
wizualne bierzemy z `design-system.md` i są zakodowane w stałej `STYL`:
paleta z dziesięciu barw, **persymon dokładnie raz na obrazek**, białe tło,
bez czarnych konturów, bez cienia rzuconego i linii podłoża.

Co z tego wynika dla treści:

- **Obrazek zastępuje podpowiedź rodzica, nie polecenie.** Tam, gdzie dziecko
  widzi obrazek, ćwiczenie staje się samodzielne — dorosły nie musi już nic
  czytać. To jest cel, nie ozdoba.
- **Nie ilustrujemy wyrazów abstrakcyjnych.** `MIMO`, `DATA`, `NOSI` zostają
  przy podpowiedzi słownej. Obrazek, którego dziecko nie rozszyfruje, jest
  gorszy niż jego brak.
- **Bez tekstu na obrazku.** Litery na ilustracji rozpraszają dziecko, które
  dopiero uczy się czytać, i psują wersję dla nieczytających.
- **Bez twarzy udających prawdziwe osoby.** Obsada jest rysunkowa, tak jak
  `img/cast.png`.

Klucz API żyje wyłącznie w zmiennej `KIE_API_KEY`. Nie trafia do repo,
do manifestu ani do logów.

---

## Ograniczenia techniczne, które mają skutek redakcyjny

- Wariant domyślny PDF-a jest **czarno-biały**. Nie pisz „pokoloruj na
  czerwono", „zielone pole", „niebieska ramka". Odwołuj się do kształtu,
  pozycji i podpisu.
- Maksimum 12% pokrycia tuszem na stronie. Nie zamawiaj w treści dużych
  wypełnionych plam ani obszernych ramek.
- Minimum 14pt dla dzieci uczących się czytać. Krótkie polecenia.
  Instrukcja dla rodzica może być 11pt, bo to nie dziecko czyta.
- Polecenie dla dziecka: maksimum 8 słów, tryb rozkazujący, jeden czasownik.
  „Połącz sylabę z obrazkiem." Nie: „Twoim zadaniem będzie połączenie…".
