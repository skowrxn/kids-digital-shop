# Design system Lupy

Źródłem prawdy dla implementacji jest `web/mockup/style.css`. Ten plik opisuje
**reguły**, których w CSS nie widać — czyli dlaczego coś wygląda tak, a nie inaczej,
i czego nie wolno zmienić.

System został zaadaptowany z publicznego systemu projektowego strony
`neuro-ai-phi.vercel.app` (sekcje "System" i "Graphics" pod przełącznikiem na dole
strony). Warto go otworzyć, jeśli potrzebujesz kontekstu dla decyzji, których tu nie
opisano — ale w razie rozbieżności **wiążący jest ten plik i `style.css`**, bo
zmieniliśmy rytm i gęstość, żeby to był marketplace, a nie landing.

---

## Paleta

Dziesięć barw. Nie dodawaj żadnej innej — nawet odcienia.

| token | hex | rola |
|---|---|---|
| `ink` | `#1E2D4D` | tekst główny, ciemne płaszczyzny, ciała na ilustracjach |
| `aizome` | `#3E62A8` | linki, ubrania na ilustracjach |
| `slate` | `#7C8FA8` | tekst drugorzędny, półtony |
| `paper` | `#F7F4ED` | tło strony i tło druku |
| `fold` | `#E4DED2` | obramowania miękkie, wypełnienie pasków |
| `persimmon` | `#E2643C` | **wyłącznie akcja i akcent** |
| `ochre` | `#C9A227` | oceny, gwiazdki, nagrody |
| `moss` | `#5C7A4A` | stan poprawny, weryfikacja |
| `madder` | `#B33F3F` | stan błędny |
| `midnight` | `#141B33` | ciemne pasma, stopka |

**Reguła persymonu.** Na ekranie: raz, maksymalnie dwa razy na widoczny obszar —
główne CTA i aktywny stan. Nigdy jako kolor ceny, tytułu ani tła sekcji.
Na ilustracji: **dokładnie raz na obrazek**, zwykle obręcz lupy Bruna.
To jest ta jedna decyzja, która sprawia, że zestaw czyta się jako premium,
a nie jako zabawka.

---

## Typografia

Dwie rodziny, obie na licencji SIL OFL (wolno osadzać w PDF i self-hostować).

- **Bricolage Grotesque 700** — display. Wyłącznie nagłówki i wordmark.
- **Plus Jakarta Sans** — cały interfejs i cała treść.

| rola | krój | rozmiar | uwagi |
|---|---|---|---|
| `display-xl` | Bricolage 700 | 68px / −0.025em | małe litery, **jeden na stronę**, tylko na landingach |
| `display` | Bricolage 700 | 50px / −0.02em | małe litery, nagłówki sekcji na landingach |
| `shelf__title` | Bricolage 700 | 28px / −0.02em | małe litery, nagłówki półek w sklepie |
| `h1` | Jakarta 700 | 34px | tylko hero, **nigdy większy**, nigdy w kolorze akcentu |
| `lede` | Jakarta 600 | 18px | slate |
| `eyebrow` | Jakarta 800 | 13px | wersaliki, slate, oszczędnie |
| `label` | Jakarta 800 | 15px | wersaliki, +0.6px, przyciski |

Nagłówki display są **pisane małą literą**. To celowe i konsekwentne.

---

## Przyciski — „the lip"

Sygnaturowy element systemu. Wypełnienie i twardy cień żyją na `::before`
z `z-index:-1`. `box-shadow: 0 4px 0` bez podanego koloru, żeby `currentColor`
malował lip.

- `:active` — cień się zeruje, przycisk spada o 4px (`translate`, nie `transform`)
- `:hover` — unosi się o 2px, lip rośnie do 6px, `brightness(1.08)`
- hover **obowiązkowo** w `@media (hover:hover)`
- promień 14px w części marketingowej, 18px w aplikacji

---

## Głębia

**Zero rozmytych cieni. Nigdzie.** Głębia to twarde obramowania i lip.

To najważniejsza reguła w całym systemie. W momencie, w którym pod kartą produktu
pojawi się miękki szary cień, sklep zaczyna wyglądać jak każdy inny marketplace
z gotowego kitu. Karty mają obramowanie `2px solid fold`, które na hover ciemnieje
do `ink`. Tyle.

Zakazane również: gradienty na komponentach (pasmo może nieść delikatny wash),
sticky hover na dotyku.

---

## Rytm — dwa tryby

**Tryb landing** (`klub.html`, `dla-tworcow.html`): jedna myśl na ekran.
Hero 100vh, pasma feature `min(100vh, 740px)`, pasma kolorystyczne i finalne CTA
100vh, sekcje rozdzielone samą bielą. Jeden moment `display-xl` na stronę.

**Tryb marketplace** (`index.html`, `katalog.html`, `k-*.html`, `p-*.html`):
gęstość zamiast narracji. Wyszukiwarka pierwsza, przyklejony pasek kategorii,
hero skrócony do ~380px, potem półki produktów rozdzielone liniami.
Nagłówki spadają do 28px, karty są dozwolone, `display-xl` nie występuje.

Klasa `market` na `<body>` przełącza tryb.

---

## Motion — „scroll jest jedynym zegarem"

Nic nie animuje się samo z siebie poza czterema pętlami wahadłowymi:

| pętla | czas | amplituda |
|---|---|---|
| `float` | 4s | ±14px, −1.2° |
| `float-alt` | 3.4s | ±11px, +0.9° |
| `drift` | 3.7s | wahadło y+x |
| `sway` | 3.1s | ±2° od górnej krawędzi |

Pierwsza klatka równa się ostatniej, więc nie ma popu. Czasy są celowo rozstrojone
(3.1 / 3.4 / 3.7 / 4), żeby sąsiednie elementy nigdy nie zsynchronizowały się w puls.
Rotacja szczytuje w 30/70%, a uniesienie w 50% — przechył ma opóźniać wznoszenie,
bo idealnie sprzężone Y i rotacja natychmiast zdradzają pętlę CSS.

Grafika w hero przesuwana jest odległością środka elementu od środka viewportu
(rAF + passive listener), nie własnym keyframem.

Odsłony przy scrollu: IntersectionObserver z `rootMargin: -12%`.
Animuj **`translate` i `scale`, nigdy `transform`** — inaczej reveal nadpisze
transformację layoutu na tym samym elemencie.

Wszystko wyłączane pod `prefers-reduced-motion`.

---

## Ilustracje

Obsada leży w `web/mockup/img/cast.png`: Zosia (3 l.), Ola (5 l.), Kuba (7 l.),
Mama i **Bruno** — jeż z przewymiarowaną lupą, maskotka marki.

Każdą nową scenę generuj z `cast.png` jako obrazem referencyjnym. Bez tego
dostaniesz dziewięć niepowiązanych obrazków zamiast jednej obsady.

**Konstrukcja:** bryły blokowe, przewymiarowane głowy, krępe ciała, krótkie
kończyny, duże buty. Każda powierzchnia cięta na kilka dużych, zdecydowanych
płaszczyzn z malarskim cieniowaniem wewnątrz fasety. Matowa tekstura gwaszu.
Postać złapana w ruchu na przechylonej osi, kończyny asymetryczne. Twarz z realną
intencją — uniesiona brew, spojrzenie w bok, prawdziwy uśmiech.

**Zakazy:** czarne kontury i jakakolwiek kreska (formę opisuje faseta i kolor),
rozdrobnione low-poly odłamki, symetryczna poza na wprost, linia podłoża, cień
rzucony, ramka, neon, cyjan, fiolet, rekwizyty fantasy, fotorealizm i render 3D
w prawdziwej perspektywie.

Maksimum sześć barw na scenę. Persymon dokładnie raz.

---

## Druk (PDF)

Paleta i typografia bez zmian, ale reguły ekranowe nie przenoszą się wprost:

- wariant domyślny jest **czarno-biały** i musi działać na laserówce
- żadna strona nie przekracza 12% pokrycia tuszem
- brak teł pełnostronicowych i ramek dookoła strony
- lip na przyciskach nie istnieje w druku — na papierze nie ma stanów
- minimum 14pt w materiałach dla dzieci uczących się czytać, 11pt gdzie indziej
- A4, marginesy 15mm, lewy 22mm pod dziurkacz
- elementy do wycięcia: linie cięcia i minimum 3mm od krawędzi
