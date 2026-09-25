# -*- coding: utf-8 -*-
"""Generuje spec.md dla partii produktów.

Dane katalogowe (tytuł, cena, wiek, autor, LICZBA STRON, kategoria, „Dla kogo")
biorą się z produkty/_katalog.json, czyli z prototypu. Reszta — obietnica,
warunek wejścia, progresja, zakres fragmentu, czego materiał nie robi — jest
autorska i siedzi w SPECY niżej.
"""
import json
from pathlib import Path

ROOT = Path("/home/user/kids-digital-shop")
KAT = json.loads((ROOT / "produkty" / "_katalog.json").read_text(encoding="utf-8"))

SPECY = {
 "karty-rutyn": dict(
   obietnica="Dziecko samo przechodzi przez poranek i wieczór, przesuwając kartę po każdej zrobionej rzeczy — bez przypominania za każdym razem.",
   warunek="Dziecko rozpoznaje przedmioty na obrazkach i potrafi wykonać prostą czynność samodzielnie. Czytać nie musi.",
   progresja="Dwie talie po 24 karty: poranek i wieczór. W obrębie talii kolejność ustalacie sami — to nie jest kurs, tylko narzędzie. Trzecia talia to karty puste do dopisania własnych.",
   fragment="Pełna talia poranna, 12 stron: instrukcja, arkusze kart i dwie zabawy.",
   nie=["Nie jest systemem nagród ani kar. Karty pokazują kolejność, nie oceniają.",
        "Nie zadziała sama z siebie. Przez pierwszy tydzień przechodzicie przez nie razem.",
        "Nie zastępuje rozmowy o tym, dlaczego rano trzeba wyjść z domu o ósmej."]),
 "emocjometr": dict(
   obietnica="Dziecko pokazuje na karcie, co czuje, zamiast odpowiadać „nic”.",
   warunek="Dziecko potrafi wskazać palcem i nazwać kilka podstawowych emocji: radość, złość, smutek.",
   progresja="Trzy talie: miny, sytuacje i natężenie. Zaczynacie od min, bo są najłatwiejsze. Talia sytuacji ma sens dopiero, gdy dziecko nazywa miny bez wahania.",
   fragment="Talia min w komplecie, 18 stron: instrukcja cięcia, karty z podpisami, karty bez podpisów, słownik min i karta pytań dla rodzica. Talia liczy 45 min, więc kończy się dopiero na stronie 18.",
   nie=["Nie jest narzędziem oceny stanu dziecka. To pomoc do rozmowy.",
        "Nie służy do rozstrzygania sporów między rodzeństwem.",
        "Nie działa w środku wybuchu. Używacie go przed albo po."]),
 "memory-domowe": dict(
   obietnica="Dziecko gra z wami w memory kartami, które zna — i wygrywa wystarczająco często, żeby chcieć grać dalej.",
   warunek="Dziecko utrzymuje uwagę przez pięć minut przy stole i rozumie zasadę „odkryj dwie”.",
   progresja="Cztery komplety: zwierzęta, jedzenie, pojazdy i emocje. Wersja dla młodszych ma 24 karty zamiast 48 — zaczynacie od niej.",
   fragment="Komplet „zwierzęta” w całości, 10 stron: instrukcja, dwa arkusze kart i trzy warianty gry.",
   nie=["Nie uczy czytania. Karty są obrazkowe.",
        "Nie jest testem pamięci. Nie liczcie, ile par kto zapamiętał.",
        "Nie ma wersji na jedną osobę — to gra we dwoje albo więcej."]),
 "planszowki-na-start": dict(
   obietnica="Rodzina gra w niedzielę w coś innego niż Chińczyk, a przygotowanie zajmuje jeden wydruk i dziesięć minut z nożyczkami.",
   warunek="Dziecko liczy do sześciu i wytrzymuje przegraną na tyle, żeby dokończyć partię.",
   progresja="Sześć gier od najprostszej do najdłuższej: liczenie, kolejność, pamięć, decyzja. Każda ma wariant łatwiejszy i trudniejszy, więc rośnie razem z dzieckiem.",
   fragment="Pierwsza gra w komplecie, 10 stron: zasady, plansza, pionki i kostka.",
   nie=["Nie uczy konkretnego przedmiotu szkolnego.",
        "Nie działa bez dorosłego przy pierwszej partii.",
        "Nie zawiera gier na czas — u nas nikt się nie ściga."]),
 "zestaw-na-podroz": dict(
   obietnica="Dwadzieścia gier, z których każda mieści się na jednej kartce i wymaga tylko długopisu.",
   warunek="Dziecko pisze albo rysuje na tyle, żeby zaznaczyć kółko i kreskę.",
   progresja="Gry pogrupowane po czasie: pięć minut, kwadrans, pół godziny. Bierzecie tę, na którą macie czas, nie po kolei.",
   fragment="Pierwsze dziesięć gier, 10 stron.",
   nie=["Nie ma tu nic do wycinania, gubienia ani składania.",
        "Nie zastąpi snu w samochodzie.",
        "Nie nadaje się dla dziecka, które jeszcze nie trzyma długopisu."]),
 "kiedy-nic-nie-dziala": dict(
   obietnica="Rozpoznajesz, która z czterech najczęstszych przyczyn dotyczy waszego domu, i masz jedną rzecz do sprawdzenia w tym tygodniu.",
   warunek="Brak. To materiał dla ciebie, nie dla dziecka.",
   progresja="Cztery rozdziały, po jednej przyczynie. Każdy kończy się checklistą na tydzień. Czytasz po kolei albo od razu ten, który brzmi znajomo.",
   fragment="Rozdział pierwszy w całości plus spis pozostałych, 10 stron.",
   nie=["Nie diagnozuje dziecka ani rodzica.",
        "Nie obiecuje, że po tygodniu dziecko samo siądzie do nauki.",
        "Nie jest poradnikiem wychowawczym. Dotyczy jednej rzeczy: odmowy siadania do materiałów."]),
 "rozmowa-z-nauczycielem": dict(
   obietnica="Wchodzisz na zebranie z listą pytań i wychodzisz z zapisanymi odpowiedziami, a nie z samym wrażeniem.",
   warunek="Brak. To materiał dla ciebie.",
   progresja="Trzy rozdziały: przygotowanie, sama rozmowa, co potem. Arkusz notatek jest w środku i wypełniasz go na miejscu.",
   fragment="Rozdział o przygotowaniu plus arkusz notatek, 10 stron.",
   nie=["Nie mówi, kto ma rację w sporze ze szkołą.",
        "Nie jest pismem procesowym ani wzorem skargi.",
        "Nie zawiera porad prawnych."]),
 "moj-tydzien": dict(
   obietnica="W niedzielę wieczorem w pięć minut rozpisujesz tydzień i wiesz, co odpuszczasz.",
   warunek="Brak. Planer wypełnia rodzic.",
   progresja="Trzy bloki: planer podstawowy, wersja dla dwojga i trojga dzieci, oraz arkusze podsumowania miesiąca. Bloki nie mają kolejności — bierzesz ten, który pasuje do twojej logistyki.",
   fragment="Blok podstawowy w całości, 10 stron: cztery tygodnie planera i instrukcja.",
   nie=["Nie planuje za ciebie. Rubryki są puste.",
        "Nie jest kalendarzem rodzinnym ani listą zakupów.",
        "Nie ma dat — wpisujesz własne, więc planer nie traci ważności."]),
 "kiedy-jestem-zly": dict(
   obietnica="Dziecko ma ustaloną wcześniej ścieżkę na moment, w którym zaczyna się gotować — i zna ją, zanim będzie potrzebna.",
   warunek="Dziecko potrafi nazwać, że jest złe, choćby po fakcie.",
   progresja="Cztery bloki: rozpoznawanie sygnałów w ciele, trzy techniki oddechowe, plan na wybuch, kącik wyciszenia. Bloki idą po kolei — plan nie zadziała, jeśli dziecko nie rozpoznaje sygnałów.",
   fragment="Blok pierwszy w całości, 11 stron: sygnały w ciele i karta „mojej złości”.",
   nie=["To nie jest materiał do robienia w trakcie awantury.",
        "Nie jest terapią ani oceną tego, czy złość dziecka jest w normie.",
        "Nie sprawi, że dziecko przestanie się złościć. Złość zostaje, zmienia się to, co dziecko z nią robi."]),
 "szlaczki-i-wzory": dict(
   obietnica="Ręka dziecka schodzi z grubej kreski na cienką stopniowo, bez przeskoku, który zwykle kończy się zniechęceniem.",
   warunek="Dziecko trzyma kredkę i rysuje kreskę od punktu do punktu.",
   progresja="Pięć bloków po grubości linii: od 20 mm do 4 mm. W obrębie bloku kolejność dowolna. Przejście do kolejnego bloku dopiero, gdy dziecko mieści się w linii bez napinania ręki.",
   fragment="Blok pierwszy, najgrubszy, 12 stron.",
   nie=["Nie uczy liter. Litery są w „Literach pisanych”.",
        "Nie ocenia ładności pisma.",
        "Nie zadziała, jeśli dziecko boli ręka — wtedy najpierw „Piszę bez nacisku”."]),
 "licze-do-20": dict(
   obietnica="Dziecko liczy pięć jabłek i wie, że to pięć — nie tylko recytuje ciąg do dwudziestu.",
   warunek="Dziecko powtarza za tobą liczby do dziesięciu, nawet jeśli nie rozumie, co znaczą.",
   progresja="Cztery bloki: liczenie na konkretach, przejście na papier, cyfra jako zapis, liczby do dwudziestu. Cyfra pojawia się dopiero w bloku trzecim — to celowe.",
   fragment="Blok pierwszy w całości, 12 stron: liczenie na konkretach.",
   nie=["Nie uczy dodawania. To jest w „Dodawaniu bez liczenia na palcach”.",
        "Nie ćwiczy pisania cyfr ładnie — tylko ich rozpoznawania.",
        "Nie jest testem gotowości szkolnej."]),
 "litery-od-zera": dict(
   obietnica="Po programie dziecko rozpoznaje dwadzieścia cztery litery drukowane (wielkie i małe) i układa z nich swoje imię.",
   warunek="Dziecko pyta, co to za znaczki, i wytrzymuje przy stole dziesięć minut.",
   progresja="Litery po dwie na tydzień, w kolejności od najłatwiejszych do wymówienia. Każdy tydzień powtarza litery z dwóch poprzednich. Trudność rośnie monotonicznie.",
   fragment="Cały tydzień 1 plus wstęp, 11 stron.",
   nie=["Nie wprowadza liter z ogonkami ani dwuznaków: Ą, Ę, Ś, Ć, Ź, Ń, CZ, SZ, RZ, CH.",
        "Nie uczy czytania sylabami. To kolejny krok: „Czytam sylabami”.",
        "Nie uczy pisania liter, tylko ich rozpoznawania i pisania po śladzie.",
        "Nie ma terminu. Jedna litera na dwa dni to sugestia, nie norma."]),
 "gloski-szumiace": dict(
   obietnica="Dziecko przechodzi pełną ścieżkę dla Sz, Ż i Cz: od ustawienia języka, przez sylaby i wyrazy, po zdania.",
   warunek="Dziecko potrafi naśladować ruch języka pokazany przez dorosłego i wytrzymuje pięć minut ćwiczeń.",
   progresja="Dwanaście tygodni. Kolejność jest tu najważniejsza i nie wolno jej skracać: ustawienie, izolowana głoska, sylaby otwarte, sylaby zamknięte, wyrazy, zdania, mowa spontaniczna. Każdy tydzień powtarza materiał z dwóch poprzednich.",
   fragment="Cały tydzień 1 plus wstęp, 14 stron.",
   nie=["To NIE jest terapia logopedyczna i nie zastępuje wizyty u specjalisty.",
        "Nie stawia rozpoznania i nie mówi, czy wymowa dziecka mieści się w normie wiekowej.",
        "Nie nadaje się dla dziecka, które ma nieprawidłową budowę aparatu mowy — to trzeba najpierw sprawdzić u specjalisty.",
        "Nie zawiera nagrań. Wszystkie instrukcje są opisowe."]),
 "busy-pierwsze-slowa": dict(
   obietnica="Segregator, który dwulatek otwiera sam i robi to samo, co starsze rodzeństwo przy stole.",
   warunek="Dziecko chwyta przedmioty palcami i utrzymuje uwagę przez kilka minut.",
   progresja="Sześć sekcji rosnących trudnością: dopasowanie kolorów, kształtów, par, kategorii, sekwencji i pierwszych słów. Każda sekcja zaczyna się instrukcją przygotowania.",
   fragment="Sekcja pierwsza w komplecie, 11 stron: instrukcja, plansza i elementy ruchome.",
   nie=["Nie uczy czytania ani liczenia.",
        "Nie jest gotowy od razu — wymaga wydrukowania, zalaminowania i naklejenia rzepów.",
        "Nie nadaje się dla dziecka, które wkłada drobne elementy do ust."]),
 "teczka-pojazdy": dict(
   obietnica="Dwadzieścia aktywności wokół jednego tematu, który dziecko i tak kocha — i nie trzeba go do nich namawiać.",
   warunek="Dziecko dopasowuje obrazek do obrazka i utrzymuje uwagę przez pięć minut.",
   progresja="Cztery sekcje: dopasowanie, liczenie, sortowanie i pierwsze słowa o pojazdach. Sekcje rosną trudnością, ale można je robić w dowolnej kolejności.",
   fragment="Sekcja pierwsza w komplecie, 10 stron.",
   nie=["Nie jest encyklopedią pojazdów.",
        "Nie uczy czytania — aktywności są obrazkowe.",
        "Wymaga zalaminowania, żeby przetrwała dłużej niż tydzień."]),
}


SZABLON = """# {tytul} — specyfikacja

Dane katalogowe pochodzą z `web/mockup/p-{slug}.html` przez
`produkty/_katalog.json`. Nie zmieniaj ich tutaj ręcznie.

| pole | wartość | źródło |
|---|---|---|
| slug | `{slug}` | prototyp |
| archetyp | **{archetyp}** | decyzja: {uzasadnienie} |
| tytuł | {tytul} | prototyp |
| podtytuł | {podtytul} | prototyp |
| wiek | {wiek} | prototyp |
| kategoria | {kategoria} / {podkategoria} | okruszki prototypu |
| cena | {cena} zł | prototyp |
| **objętość** | **{strony} stron** | tabela `.specs`, klucz „Objętość" |
| autor | {autor} | prototyp — **nie wchodzi do PDF-a** (`brand.md`) |

---

## Dla kogo

{dla_kogo}

*(zdanie z persymonowej belki na `p-{slug}.html` — cytat co do znaku)*

## Warunek wejścia

{warunek}

## Obietnica

{obietnica}

## Progresja

{progresja}

## Zakres darmowego fragmentu

{fragment}

## Czego ten materiał NIE robi

{nie}

**Uwaga:** ta sekcja **nie jest renderowana w PDF-ie** (decyzja z 2026-09-25).
Zostaje jako dana w `content.json` (`wstep.czego_nie_robi`) i zasila tę
specyfikację oraz kreacje reklamowe.

## Ograniczenia produkcyjne

- **Bez ilustracji.** Ten produkt nie ma pól `ilustracja` — materiał jest
  zaprojektowany tak, żeby działał bez obrazków.
- Wariant domyślny czarno-biały, ≤12% pokrycia tuszem na stronie.
- Minimum **{min_pt} pt** dla wszystkiego, co czyta dziecko.
- Stopka: tylko tytuł i numer strony.
- Wszystkie rubryki do wypełnienia są **puste** — żadnych danych dziecka.
"""

UZASADNIENIA = {
 "PROGRAM": "sztywna sekwencja, trudność rośnie monotonicznie",
 "ZESZYT": "bloki ćwiczeń bez sekwencji między blokami",
 "KARTY": "talia do wycięcia, 8–9 kart na A4",
 "SEGREGATOR": "plansza bazowa z elementami ruchomymi na rzep",
 "GRY": "zasady gry i rozgrywka",
 "PORADNIK": "dominująca proza czytana przez dorosłego",
}

ARCHETYPY = {s["slug"]: s["archetyp"] for s in
              json.loads((ROOT / "KOLEJKA.json").read_text(encoding="utf-8"))["produkty"]}


def main():
    for slug, extra in SPECY.items():
        p = KAT["produkty"][slug]
        arch = ARCHETYPY[slug]
        wiek = p["wiek"]
        min_pt = 14 if any(w in wiek for w in ("2–4", "3–", "4–", "5–", "1,5")) else 12
        tekst = SZABLON.format(
            slug=slug, archetyp=arch, uzasadnienie=UZASADNIENIA[arch],
            tytul=p["tytul"], podtytul=p.get("podtytul", "—"), wiek=wiek,
            kategoria=p["kategoria"], podkategoria=p["podkategoria"],
            cena=p["cena_pln"], strony=p["strony"], autor=p["autor"],
            dla_kogo=p["dla_kogo"], min_pt=min_pt,
            warunek=extra["warunek"], obietnica=extra["obietnica"],
            progresja=extra["progresja"], fragment=extra["fragment"],
            nie="\n".join(f"- {x}" for x in extra["nie"]))
        kat = ROOT / "produkty" / slug
        kat.mkdir(parents=True, exist_ok=True)
        (kat / "spec.md").write_text(tekst, encoding="utf-8")
        print(f"  {slug:24} {arch:11} {p['strony']:>4} s.  min {min_pt}pt")
    print(f"{len(SPECY)} specyfikacji")


if __name__ == "__main__":
    main()
