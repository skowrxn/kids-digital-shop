# Osiem kątów reklamowych + ograniczenia Meta

Kąt to **obietnica i sposób argumentacji**, nie temat. Ten sam produkt
sprzedany trzema kątami to trzy różne reklamy, nie trzy parafrazy.

Każdy plik w `reklamy/<slug>/` ma w nagłówku YAML:

```yaml
produkt: czytam-sylabami
kat: A3-kolejnosc
grupa_docelowa: ICP-1-szkola
format: tekst-glowny | naglowki | brief-statyk | skrypt-ugc
wersja: 1
```

`kat` i `grupa_docelowa` muszą być identyfikatorami stąd i z `icp.md`.
Bez nich nie policzymy CPA per kąt — walidator to sprawdza.

**Reguła doboru:** trzy warianty tekstu głównego = trzy różne kąty.
Nie powtarzaj kąta w obrębie jednego produktu.

---

## A1 · `oszczednosc` — Zamiast korepetycji

**Obietnica:** ta sama robota, ułamek kosztu.
**Argument:** 79 zł jednorazowo kontra 100–150 zł za godzinę, co tydzień.
Materiał zostaje na dysku i wraca przy młodszym dziecku.
**Dla kogo:** ICP-1 `szkola`, ICP-2 `kolejka`.
**Haczyk:** nie deprecjonuj specjalistów. Nie „po co ci logopeda".
Kontra jest z ceną korepetycji, nie z kompetencją człowieka.
**Zakaz:** liczby oszczędności jako gwarancji („zaoszczędzisz 4800 zł").
Podajemy cenę naszą i publiczną stawkę rynkową, resztę liczy odbiorca.

## A2 · `dwadziescia-minut` — Mieści się w wieczorze

**Obietnica:** dwadzieścia minut przy stole, bez przygotowania.
**Argument:** kartka i ołówek. Nic do zainstalowania, nic do naładowania.
Dziecko robi to z tobą, nie samo.
**Dla kogo:** ICP-0 `ekran`, ICP-5 `zlosc`.
**Haczyk:** czas musi być prawdziwy i zgodny ze `spec.md`. Jeśli blok trwa
40 minut, piszemy 40.

## A3 · `kolejnosc` — Wiesz, co robicie w tym tygodniu

**Obietnica:** koniec z chaosem plików. Jest plan i jest numer tygodnia.
**Argument:** program rozpisany tydzień po tygodniu, karta rodzica
(co powiedzieć, na co uważać, kiedy przejść dalej), karta postępu.
**Dla kogo:** ICP-4 `system`, ICP-1 `szkola`.
**To jest kąt flagowy Lupy.** Jedyna rzecz, której Etsy nie ma.
**Haczyk:** pokaż strukturę, nie opisuj jej. Statyk = rozkład tygodni.

## A4 · `zanim-doczekasz` — Zacznij, czekając na termin

**Obietnica:** nie stoisz w miejscu przez pięć miesięcy kolejki.
**Argument:** ćwiczenia do zrobienia w domu w oczekiwaniu na wizytę.
**Dla kogo:** ICP-2 `kolejka`.
**Haczyk — najostrzejszy w całym pliku.** Ten kąt istnieje wyłącznie
w towarzystwie zdania rozgraniczającego. Wzorzec z prototypu:
*„Nie zastępują diagnozy — pozwalają nie stać w miejscu."*
Bez tego zdania kreacja nie wychodzi z repo.
**Zakaz:** jakakolwiek sugestia skuteczności terapeutycznej, deadline
na umiejętność, słowo „wywołamy". Sekcja A `brand.md` w całości.

## A5 · `drukujesz-raz` — Starcza na miesiące

**Obietnica:** jedno wydrukowanie, wiele powtórzeń.
**Argument:** wersje do laminowania, elementy na rzep, wraca przy młodszym
dziecku. Koszt na jedno użycie spada do groszy.
**Dla kogo:** ICP-3 `pogoda`, ICP-0 `ekran`.
**Haczyk:** podaj czas przygotowania uczciwie. „20 minut z laminarką"
jest lepszym argumentem niż przemilczenie.

## A6 · `zaczynasz-za-darmo` — Sprawdź, zanim zapłacisz

**Obietnica:** pobierasz pełny fragment, drukujesz, robisz z dzieckiem.
Dopiero potem decydujesz.
**Argument:** darmowy fragment to nie okładka i spis treści — to pełny
tydzień albo dziesięć realnych stron.
**Dla kogo:** wszystkie ICP. Najlepszy kąt na zimny ruch i pierwszy zakup.
**Haczyk:** obietnica musi się zgadzać z `out/fragment.pdf` co do liczby
stron. Walidator porównuje.

## A7 · `nie-twoja-wina` — Problem jest przy stole, nie w dziecku

**Obietnica:** scenariusz na moment, w którym się dzieje.
**Argument:** plan ustalacie wcześniej, na spokojnie. Dziecko ma gotową
ścieżkę, zanim zacznie się gotować.
**Dla kogo:** ICP-5 `zlosc`, ICP-2 `kolejka`.
**Haczyk:** pierwsza osoba, zawsze. „U nas wieczory wyglądały tak."
Nigdy drugą osobą o stanie odbiorcy — to jednocześnie łamie Meta
i uruchamia wstyd, który tę grupę odbija.
**Zakaz:** cała sekcja C `brand.md` (straszenie, wina).

## A8 · `autor` — Ktoś to ułożył, nie wygenerował

**Obietnica:** za materiałem stoi konkretna osoba i konkretna metoda.
**Argument:** imię autora, nazwana metoda (np. sylabowa), warunek wejścia
i sekcja „czego to nie robi". Oceny wystawiają wyłącznie kupujący.
**Dla kogo:** ICP-1 `szkola`, ICP-4 `system`, ICP-2 `kolejka`.
**Haczyk:** autorzy są na czas testów wymyśleni (`brand.md`). Wolno użyć
imienia i domeny. **Nie wolno** dopisywać tytułów zawodowych, uprawnień,
stażu, miejsca pracy ani zdjęcia twarzy jako prawdziwej osoby. Dotyczy to
także roli podanej w prototypie (`autor_rola_prototyp`) i pigułki
„Zweryfikowany twórca" — to elementy makiety, nie fakty.
Brief statyku dla tego kąta opisuje postać z obsady `cast.png`, nie portret.

---

## Dobór kąta do produktu — skrót

| kategoria | kąty pierwszego wyboru |
|---|---|
| `czytanie`, `matematyka` | A3, A1, A6 |
| `logopedia` | A4, A8, A6 — **nigdy A1 jako pierwszy** |
| `emocje` | A7, A2, A6 |
| `busy`, `pory` | A5, A3, A2 |
| `rutyny` | A2, A3, A7 |
| `gry` | A2, A5, A6 |
| `grafo` | A3, A6, A8 |
| `swiat` | A5, A2, A6 |
| `rodzic` | A3, A7, A8 |

---

# Ograniczenia Meta

Egzekwowane przez `renderer/validate.py` na każdym pliku w `reklamy/`.
Trafienie = `blad`, kreacja nie wychodzi.

## 1. Nigdy nie sugeruj, że znasz cechę lub stan odbiorcy

To jest polityka personal attributes i najczęstszy powód odrzucenia
w naszej kategorii. Reguła praktyczna: **jeśli zdanie zaczyna się od
„Twoje dziecko" i po nim idzie orzeczenie o dziecku — wytnij je.**

| ❌ nie wolno | ✅ tak piszemy |
|---|---|
| Twoje dziecko jest uzależnione od ekranu | U nas wieczory schodziły na negocjacje o tablet |
| Twoje dziecko ma ADHD? | (nie istnieje żadna dopuszczalna wersja) |
| Czy twój syn czyta wolniej niż rówieśnicy? | Mój syn utknął na literowaniu. To nam pomogło ruszyć |
| Masz dziecko z wadą wymowy | Czekamy na logopedę od marca |
| Twoja córka się złości przy każdym zadaniu | Zadanie domowe kończyło się u nas płaczem |
| Wiemy, że nie masz czasu | Robimy to w dwadzieścia minut po kolacji |

Dotyczy też pytań retorycznych i drugiej osoby w domyśle
(„Rozpoznajesz to?" po opisie stanu dziecka).

## 2. Pisz w pierwszej osobie i o wyniku

Domyślna forma tekstu głównego to relacja: **„u nas wyglądało to tak →
zrobiliśmy to → tak jest teraz"**. Odbiorca sam się rozpoznaje albo nie.
My go nie etykietujemy.

Czasowniki: `zrobiliśmy`, `drukujemy`, `usiedliśmy`, `wyszło`.
Nie: `poczujesz`, `zauważysz u dziecka`, `rozwiążesz problem`.

## 3. Zero obietnic medycznych i terapeutycznych

Cała sekcja A fraz zakazanych z `brand.md`. Dodatkowo w reklamach:
zakaz sugerowania, że materiał zastępuje wizytę, przyspiesza rozwój
albo działa na jakikolwiek stan zdrowia.

Jedyne dopuszczalne zdanie o specjaliście to przekierowanie
albo rozgraniczenie: *„Nie zastępują diagnozy — pozwalają nie stać
w miejscu."*

## 4. Zero przed/po w kontekście rozwoju dziecka

Zakazane w tekście i **w briefie statyku**:

- kadr podzielony na pół z podpisami „przed / po"
- dwie próbki pisma dziecka obok siebie jako dowód postępu
- „tydzień 1 vs tydzień 12" na literach napisanych przez dziecko
- oś czasu z buźkami smutna → wesoła

**Dozwolony zamiennik:** pokaż **materiał**, nie dziecko. Rozkład dwunastu
tygodni na stole, karta postępu z pustymi rubrykami, stos wydrukowanych
kart. Postęp jest własnością materiału, nie dziecka na obrazku.

## 5. Dodatkowo, z naszej strony

- Bez emoji i bez CAPS LOCK-a w nagłówkach.
- Bez odliczania czasu i sztucznej pilności („zostało 6 sztuk" —
  to plik PDF, nie ma sztuk).
- Bez cudzych znaków towarowych (nie „metoda Montessori®", nie nazwy
  wydawnictw i platform).
- Opinie w kreacjach: **żadnych**. Opinie w prototypie są wygenerowane
  na potrzeby makiety (`web/mockup/README.md`) i nie wolno ich cytować
  jako prawdziwych.
- Bez twarzy przedstawianych jako prawdziwi klienci. Obsada `cast.png`
  jest rysunkowa i tak ma zostać.

## 6. Skrypt UGC — co wolno

30 sekund, scena po scenie, pierwsza osoba. Mówiący jest rodzicem
i mówi o sobie. Dziecko może być w kadrze przy stole, ale:
- nie pokazujemy dziecka jako dowodu postępu,
- nie wkładamy dziecku w usta oceny produktu,
- nie ma zbliżenia na zeszyt „przed" i „po".

Scena finalna zawsze pokazuje **materiał na stole**, nie minę dziecka.
