# Lupa — pipeline produkcyjny materiałów do druku

Czytasz to na starcie sesji. Większość sesji nie ma historii rozmowy, w której
ten pipeline powstał — wszystko, czego potrzebujesz, jest tutaj i w plikach,
do których ten plik odsyła.

---

## 0. Pierwsze trzy komendy, zawsze

```bash
python3 renderer/kolejka.py status
python3 renderer/kolejka.py status --tor reklamy
python3 renderer/kolejka.py lista tresc 4
```

**Zacznij odpowiedź od jednego zdania: ile produktów jest na którym etapie.**
Dopiero potem cokolwiek rób.

---

## 1. Co budujemy

Marketplace z materiałami do druku dla rodziców dzieci 1,5–10 lat.
48 produktów, 12 kategorii po 4. Rodzic drukuje na domowej laserówce
i pracuje z dzieckiem 20 minut przy stole.

Wejściem jest **prototyp** w `web/mockup/` — 64 statyczne strony.
To jest źródło prawdy o katalogu. **Nie modyfikuj tych plików**
(wyjątek: KROK 6, podmiana placeholderów podglądów).

---

## 2. Zasada nadrzędna — treść to dane, nie proza

Nie generujemy „184 stron programu nauki czytania" jako tekstu. Nigdy.

Karta pracy to **układ**, nie akapit. Dlatego:

```
spec.md  →  content.json  →  renderer/render.py  →  out/*.pdf  →  validate.py
(człowiek/ Ty)  (Ty, dane)     (deterministycznie)                 (bramki)
```

- **Ty generujesz ustrukturyzowane dane**: listy sylab w kolejności trudności,
  pary wyrazów do różnicowania, treści zadań, instrukcje dla rodzica, klucze
  odpowiedzi. Wszystko w `content.json`, zgodnie ze schematem archetypu.
- **Renderer** zamienia JSON na PDF według stałego szablonu.

**Jeśli zaczynasz pisać treść bezpośrednio do PDF-a albo do HTML-a szablonu
z pominięciem `content.json` — zatrzymaj się. To jest błąd architektoniczny.**
Szablon opisuje układ i nie zawiera ani jednego słowa treści produktu.

Zysk: identyczne marginesy na każdej stronie, gwarantowana wersja
czarno-biała, wersja B produktu powstaje przez zmianę danych w minutę.

---

## 3. Ograniczenia środowiska — twarde

- **Brak dostępu do Anthropic API.** Nie pisz skryptów wołających
  `api.anthropic.com`. Nie proponuj Batch API. Całą treść generujesz Ty,
  w sesjach Claude Code, według kolejki.
- **Ilustracje: kie.ai, model `gpt-image-2`.** Klucz TYLKO ze zmiennej
  środowiskowej `KIE_API_KEY` — nigdy w repo, w manifeście ani w logu.
  Obsługa jest w `renderer/ilustracje.py`, szczegóły w sekcji 10a.
  **Statyków reklamowych nadal nie generujemy** — do kreacji piszesz
  brief opisowy (KROK 7), bo tam obrazek powstaje poza tym repo.
- Renderer, walidator i skrypty pomocnicze działają **całkowicie offline**,
  w Pythonie, odpalane Bashem.
- Chromium jest lokalnie, ale Playwright ma inną wersję niż zainstalowana
  przeglądarka. Zawsze podawaj ścieżkę:
  `executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"`
  (renderer robi to sam, przez `renderer/przegladarka.py`).
- Fonty leżą lokalnie w `renderer/fonts/` (Plus Jakarta Sans,
  Bricolage Grotesque, obie SIL OFL). Nie linkuj do Google Fonts w `print.css` —
  PDF ma się renderować bez sieci.

---

## 4. Gdzie leży kontekst

| plik | co z niego bierzesz |
|---|---|
| `marka/brand.md` | ton głosu, **frazy zakazane** (twarda bramka), autorzy |
| `marka/icp.md` | sześć grup docelowych, wyprowadzonych z sekcji „chcę…" prototypu |
| `marka/angles.md` | osiem kątów reklamowych + ograniczenia Meta |
| `marka/design-system.md` | paleta, typografia, reguły druku |
| `web/mockup/style.css` | implementacja referencyjna design systemu |
| `web/mockup/p-*.html` | opisy produktów — **wzorzec tonu** dla tekstów do rodzica |
| `produkty/_katalog.json` | dane katalogowe wyciągnięte z prototypu (generowane) |
| `produkty/_archetypy/` | 6 schematów JSON + 6 szablonów renderera |
| `produkty/<slug>/spec.md` | specyfikacja jednego produktu |
| `KOLEJKA.json` | **stan produkcji** |

`produkty/_katalog.json` jest generowany, nie edytowany ręcznie:

```bash
python3 renderer/katalog.py
```

Skrypt nigdy nic nie wymyśla — czego nie ma w mockupie, raportuje w sekcji
`braki`.

---

## 5. Żelazne zasady

1. **Każdy produkt MUSI mieć `fragment.pdf`.** Bez niego nie przechodzi
   do stanu `gotowy`. To jedyny powód, dla którego ktoś zaufa nowemu sklepowi
   zamiast wrócić na Etsy. Minimum 10 stron albo 1 pełny tydzień.
2. **Autorzy są na czas testów wymyśleni.** Imię i nazwisko z prototypu,
   nic więcej — bez tytułów zawodowych, uprawnień i miejsc pracy.
3. **Żadnych danych dzieci.** Nigdzie w produkcie ani w kodzie. Karta postępu
   jest pusta, wypełnia ją rodzic u siebie. Imiona w zadaniach są z góry
   ustalonej listy (`brand.md`).
4. **Język: prosty, do rodzica, drugą osobą.** Wzorzec w `web/mockup/p-*.html`.
   Konkret zamiast obietnicy, zdania poniżej 15 słów, zero żargonu.
5. **Bez Anthropic API.** Treść generujesz Ty, w sesjach. Ilustracje —
   przez `renderer/ilustracje.py`, nigdy ad hoc curl-em.
6. **Dane katalogowe muszą zgadzać się z prototypem co do znaku.**
   Tytuł, cena, wiek, autor, liczba stron, kategoria — nie wymyślaj ich
   od nowa. Jeśli czegoś nie ma w mockupie, zgłoś brak, nie zgaduj.

---

## 6. Praca z KOLEJKA.json

Jedyne źródło prawdy o stanie. Nie Twoja pamięć — plik.

Etapy: `brak → spec → tresc → render → walidacja → gotowy`, plus `blad`.

**Cztery reguły, egzekwuj bezwzględnie:**

1. Na starcie **każdej** sesji przeczytaj kolejkę i napisz jednym zdaniem,
   ile produktów jest na którym etapie.
2. Zapisuj stan **po każdym produkcie**, nie na końcu partii:
   `python3 renderer/kolejka.py set <slug> <etap>`.
   Sesja może zostać przerwana w dowolnym momencie i nic nie może się zgubić.
   Zapis jest atomowy (`tmp` + `os.replace`).
3. **Nigdy nie przetwarzaj produktu, który ma już etap docelowy.**
   Pipeline jest idempotentny. Do wyboru pracy służy wyłącznie
   `kolejka.py lista <etap> <ile>` — sam filtruje zrobione i zamknięte.
4. Po **trzech** nieudanych próbach ustaw `blad`, zapisz powód, jedź dalej:
   `kolejka.py set <slug> blad --powod "..."`. Nie zatrzymuj partii
   przez jeden produkt.

Wyczerpany limit użycia nie jest problemem. Kolejka jest na dysku,
wznawiasz w nowej sesji od tego samego miejsca.

---

## 7. Generowanie treści — partie i subagenci

- **Partiami po 4 produkty.** Po każdej partii krótkie podsumowanie i pauza,
  żeby użytkownik mógł przerwać albo kazać jechać dalej.
- **Każdy produkt w osobnym subagencie (Task).** Subagent dostaje:
  `marka/brand.md`, skill `skills/lupa-tresc/`, schemat archetypu
  z `produkty/_archetypy/` i `produkty/<slug>/spec.md`.
  Zwraca `content.json` i **zapisuje go sam** pod `produkty/<slug>/content.json`.
- **Kontekst głównej sesji ma zostać czysty.** Nie wczytuj 48 plików
  `content.json` do głównego wątku. Główna sesja czyta z subagenta
  **tylko wynik walidacji schematu**, nie całą treść.
- Waliduj `content.json` schematem **po zapisie**, w Pythonie:
  `python3 renderer/validate.py schema <slug>`.
  Przy błędzie ponów, dopisując komunikat walidatora do promptu subagenta.

Ta sama mechanika obowiązuje przy tekstach reklamowych, tor `reklamy`.

---

## 8. Sześć archetypów

Każdy archetyp = jeden schemat JSON + jeden szablon. To jest cała skala
projektu: **sześć rzeczy do zrobienia dobrze, nie czterdzieści osiem.**

| archetyp | co to jest | reguła twarda |
|---|---|---|
| `PROGRAM` | sekwencyjny kurs na N tygodni | trudność **rośnie monotonicznie**; każdy tydzień powtarza materiał z poprzedniego (interleaving), nie tylko wprowadza nowy |
| `ZESZYT` | zbiór ćwiczeń bez sztywnej sekwencji | bloki od najłatwiejszego; w obrębie bloku kolejność dowolna |
| `KARTY` | talia do wycięcia | 8 lub 9 kart na A4, siatka cięcia, wersja z podpisami i bez (dla nieczytających) |
| `SEGREGATOR` | busy book / Montessori | każda plansza ma listę elementów do zalaminowania i miejsce na rzep; instrukcja przygotowania na pierwszej stronie sekcji |
| `GRY` | planszówki i gry karciane | zasady na **jednej** stronie; jeśli gra wymaga pionków lub kostki, są w pliku — nigdy „użyj własnych" |
| `PORADNIK` | materiał dla rodzica | jedyny archetyp z dominującą prozą; maks. **65 znaków w linii** |

Schematy: `produkty/_archetypy/<ARCHETYP>.schema.json`.
Szablony: `renderer/templates/<archetyp>.html.j2`.

**Typ `formularz`** (rubryki do wypełnienia ręką) jest współdzielony przez
`ZESZYT` i `PORADNIK`:

```json
{ "typ": "formularz",
  "pola": [ { "etykieta": "...", "wysokosc_mm": 12, "linie": 3 } ] }
```

Obsługuje planer („Mój tydzień"), tablicę punktów („Tablica obowiązków"),
dziennik obserwacji („Wiosna w doniczce") i arkusz notatek
(„Rozmowa z nauczycielem"). Rubryki są **zawsze puste** — wypełnia je rodzic
u siebie, patrz żelazna zasada 3.

**Archetyp wybiera struktura, nigdy cena ani objętość.** 96 stron za 65 zł
to nie argument za żadnym archetypem — to sygnał marży. Pytanie brzmi
wyłącznie: sztywna sekwencja (PROGRAM), bloki bez sekwencji (ZESZYT),
elementy do wycięcia (KARTY), plansza z ruchomymi elementami (SEGREGATOR),
zasady gry (GRY), czy proza czytana przez dorosłego (PORADNIK).

Granica PROGRAM/ZESZYT bywa cienka — rozstrzyga ją **monotonicznie rosnąca
trudność**. „Ferie bez ekranu" mają 14 dni po kolei, ale dzień 14 nie jest
trudniejszy od dnia 1, więc to ZESZYT, nie PROGRAM.

**Jeśli produkt nie pasuje do żadnego z sześciu — nie dodawaj siódmego.
Zapytaj użytkownika.** Prawdopodobnie źle napisana specyfikacja.

---

## 9. spec.md — co musi zawierać

Dla każdego produktu, `produkty/<slug>/spec.md`:

- archetyp
- dla kogo (jedno zdanie)
- obietnica — co dziecko będzie umiało
- warunek wejścia — co musi już umieć
- progresja
- **deklarowana liczba stron, zgodna z prototypem** (tabela `.specs`,
  klucz „Objętość" w `p-<slug>.html`)
- zakres darmowego fragmentu
- **czego materiał NIE robi** — krytyczne dla logopedii i emocji

---

## 10. Renderer

Chromium przez Playwright (print-to-PDF) + dedykowany `renderer/print.css`.
Te same tokeny designu co na stronie, pełna kontrola przez CSS Grid,
zero nowego toolchainu. Alternatywa przy problemach z typografią: Typst.
**Nie używaj ReportLab** — ręczne pozycjonowanie to ślepa uliczka przy
sześciu szablonach.

Wymagania twarde:

- A4 pionowo, marginesy 15 mm, lewy **22 mm** (dziurkacz)
- czcionki osadzone, z `renderer/fonts/`
- wariant **domyślny czarno-biały**, działa na laserówce;
  kolor osobno jako `pelny-kolor.pdf`
- żadna strona nie przekracza **12% pokrycia tuszem** w wariancie BW
  (mierzone rasteryzacją strony i zliczeniem pikseli niebiałych)
- stopka: numer strony, tytuł, `lupa.pl`, numer wersji
- bez teł pełnostronicowych i bez ramek dookoła strony
- minimum **14pt** dla dzieci uczących się czytać, **11pt** wszędzie indziej
- elementy do wycięcia: linie cięcia, minimum **3 mm** od krawędzi

```bash
python3 renderer/render.py <slug>            # pelny.pdf + fragment.pdf + podglądy
python3 renderer/render.py <slug> --kolor    # dodatkowo pelny-kolor.pdf
```

Wyjście: `produkty/<slug>/out/{pelny.pdf,fragment.pdf,podglad-01..04.png}`.

**Fonty muszą być statyczne.** `renderer/fonty.py` robi statyczne instancje
z krojów wariacyjnych. Font wariacyjny Chromium osadza w PDF-ie jako **Type3**
— obrysy glifów zamiast kroju. Nie podmieniaj plików w `renderer/fonts/`
na pobrane wprost z Google Fonts.

---

## 10a. Ilustracje

```bash
export KIE_API_KEY=...                                  # nigdy w repo
python3 renderer/ilustracje.py <slug> --raport          # czego brakuje
python3 renderer/ilustracje.py <slug>                   # dogeneruj brakujące
python3 renderer/ilustracje.py <slug> --przelicz-bw     # nowa receptura druku, bez kosztu
```

Zasady:

1. **Brief jest daną produktu**, nie parametrem skryptu. Siedzi w `content.json`
   w polu `ilustracja: { id, brief, proporcje }`. Ta sama reguła co przy
   treści: to są dane, nie proza.
2. **`id` jest per motyw, nie per pozycja.** `KOT` w tygodniu 8 i w tygodniu 9
   to jeden obrazek — jeden koszt i jedna spójna talia.
3. **Brief opisuje wyłącznie kadr.** Styl dokleja stała `STYL`
   w `renderer/ilustracje.py`: paleta z `design-system.md`, persymon dokładnie
   raz, białe tło, bez konturów, bez cienia i linii podłoża.
4. **Dwa pliki na motyw**: `<id>.png` (kolor) i `<id>-bw.png` (druk domyślny).
   Przełącza je CSS, szablon nie wie o wariancie.
5. **Cache w `_manifest.json`.** Odcisk promptu decyduje o ponownym
   generowaniu. Zapis po każdej ilustracji — przerwana sesja nic nie traci.
6. **Nie każdy wyraz da się zilustrować.** `MIMO`, `DATA`, `NOSI` briefu nie
   mają i zostają przy podpowiedzi czytanej przez rodzica. Lepszy brak obrazka
   niż obrazek, którego dziecko nie rozszyfruje.

**Post-produkcja jest obowiązkowa i nietrywialna.** Model zwraca obrazek
z pełnym tłem — bez wybielenia strona ma 100% pokrycia tuszem. Wariantu
drukarskiego **nie robi się rozjaśnianiem**: bramka liczy piksele niebiałe,
więc jasna szarość kosztuje tyle samo co czerń, a obrazek robi się nieczytelny.
Robi się go podniesieniem kontrastu i wycięciem wszystkiego powyżej progu
do czystej bieli. Próg dobiera się automatycznie pod budżet pokrycia.

---

## 11. Walidacja — bramki, których build nie przepuszcza

`renderer/validate.py`. Build produktu **pada**, jeśli:

- liczba wyrenderowanych stron ≠ liczba z `spec.md` (±2)
- jakakolwiek strona przekracza 12% pokrycia tuszem w BW
- w `PROGRAM` trudność nie rośnie monotonicznie między tygodniami
- to samo ćwiczenie/wyraz powtarza się częściej, niż zakłada plan powtórek
- brakuje `fragment.pdf` albo ma mniej niż 10 stron / 1 pełny tydzień
- tekst wychodzi poza obszar zadruku
- brakuje klucza odpowiedzi tam, gdzie archetyp go wymaga
- w materiale logopedycznym lub emocjonalnym pada sformułowanie sugerujące
  terapię, diagnozę lub leczenie (lista fraz zakazanych w `brand.md`)

Wynik zapisuj do `KOLEJKA.json` jako etap `walidacja` albo `blad` z powodem.
**Uruchamiaj walidator w pętli buildu, nie ręcznie.**

---

## 12. Teksty reklamowe

Dla każdego produktu, do `reklamy/<slug>/`:

- 3 warianty tekstu głównego, każdy pod **inny** kąt z `angles.md`
- 5 nagłówków na wariant
- **brief opisowy** na 3 statyki: co ma być w kadrze, jaki tekst na obrazku,
  która postać z obsady. Sam obrazek powstaje później, poza tym repo.
- 1 skrypt UGC (30 s, scena po scenie)

Kreacje **muszą** czytać `icp.md`, `angles.md` i `spec.md` produktu.
Każdy plik ma w nagłówku metadane `produkt`, `kat`, `grupa_docelowa` —
bez tego nie da się policzyć CPA per kąt. Walidator to sprawdza.

Ograniczenia Meta (pełna lista w `angles.md`): nigdy nie sugeruj, że znasz
cechę lub stan odbiorcy; pisz w pierwszej osobie i o wyniku; zero obietnic
medycznych; zero przed/po w kontekście rozwoju dziecka.

---

## 13. Kolejność pracy

| krok | zakres | bramka |
|---|---|---|
| 1 | `CLAUDE.md`, `brand.md`, `icp.md`, `angles.md`, `KOLEJKA.json` (48 wpisów, etap `brak`) | **zgoda użytkownika** |
| 2 | archetyp `PROGRAM` + „Czytam sylabami" end-to-end: spec → content → render → `pelny.pdf`, `fragment.pdf`, 4 podglądy PNG | **zgoda użytkownika** |
| 3 | poprawki renderera i skilla, potem pozostałe 5 archetypów + po 1 produkcie na każdy | **zgoda użytkownika** |
| 4 | walidator + testy, puszczone na 6 istniejących produktach | — |
| 5 | pozostałe 42 produkty, partiami po 4, przez subagentów; raport końcowy | pauza po każdej partii |
| 6 | podpięcie podglądów i fragmentów pod strony produktowe prototypu | — |
| 7 | teksty reklamowe dla 6 produktów flagowych | — |

**Nie przechodź dalej bez zgody użytkownika w krokach 1, 2 i 3.**
Po każdym kroku napisz krótkie podsumowanie: co powstało, co jest niepewne,
jaki jest stan kolejki.

Produkty flagowe (KROK 7), po jednym na intencję z sekcji „chcę…" prototypu:
`karty-rutyn`, `czytam-sylabami`, `gloski-szumiace`, `busy-pierwsze-slowa`,
`moj-tydzien`, `kiedy-jestem-zly`.

---

## 14. Stan wejścia

Prototyp jest **kompletny**: 64 strony HTML w `web/mockup/`, `style.css`,
`app.js` i `img/` (7 PNG + 13 WebP, w tym `cast.png`).

`produkty/_katalog.json` ma komplet danych dla wszystkich 48 produktów —
tytuł, podtytuł, cena, wiek, autor, liczba stron, kategoria, podkategoria,
zdanie „Dla kogo", opisy i tabela `.specs`. Ekstraktor raportuje
`braków: 0`. Jeśli kiedykolwiek zaraportuje więcej — **popraw ekstraktor,
nie łataj `KOLEJKA.json` ręcznie.**

Dwie pułapki prototypu, obie już obsłużone w `renderer/katalog.py`
(nie cofaj tych zabezpieczeń):

1. **Listą wejściową jest `katalog.html`, nie `index.html`.** Strona główna
   pokazuje tylko wybrane półki — 42 z 48 produktów.
2. **Mega-menu siedzi w nagłówku każdej strony** i niesie 36 kart
   produktowych oraz własne `<h1>`, `.card` i `.price`. Naiwne zliczanie
   kart w `katalog.html` daje 84, nie 48. Dlatego deduplikujemy po slugu,
   a stronę produktową tniemy najpierw do `<section class="product">`.
   Sprawdzianem poprawności jest zgodność listy ze zbiorem plików
   `p-*.html` w obie strony — ekstraktor to raportuje.

Parsowanie idzie przez `renderer/dom.py` (drzewo DOM na stdlib-owym
`html.parser`), nie przez wyrażenia regularne. Zagnieżdżonych `<div>`
nie da się poprawnie ciąć regexem — `.*?` zatrzymuje się na pierwszym
domknięciu wewnętrznym.

### Czego z prototypu NIE przenosimy do produktu

- **Rola autora.** `p-*.html` podaje przy nazwisku np. „neurologopeda,
  14 lat praktyki". Autorzy są na czas testów wymyśleni, więc ta rola
  zostaje w `_katalog.json` jako `autor_rola_prototyp` i **nie wchodzi**
  ani do PDF-a, ani do tekstów reklamowych. Patrz `marka/brand.md`.
- **Opinie i twarze.** Bloki `.revs` i pliki `img/ava*.webp` są wygenerowane
  na potrzeby makiety i nie przedstawiają realnych osób
  (`web/mockup/README.md`, `web/mockup/img/README.md`). Nie cytuj ich
  jako prawdziwych, nie przenoś do żadnej bazy.
- **Pigułka „Zweryfikowany twórca".** To element makiety, nie fakt.

### Grafiki

`img/cast.png` to arkusz obsady (Zosia, Ola, Kuba, Mama, Bruno). Służy jako
**referencja stylu** — przy briefach do kreacji reklamowych (KROK 7) i przy
pisaniu pól `ilustracja` w `content.json`. Ilustracje do produktów powstają
przez `renderer/ilustracje.py` (sekcja 10a); statyki reklamowe nadal nie —
tam zostaje brief opisowy.
