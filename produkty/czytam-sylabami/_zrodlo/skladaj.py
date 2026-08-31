# -*- coding: utf-8 -*-
"""Składa content.json produktu „Czytam sylabami" z danych w tygodnie.py.

Bilans stron (musi wyjść dokładnie 184, zgodnie z prototypem):
    3 wstęp (tytułowa + jak korzystać ×2)
  180 dwanaście tygodni × 15 stron
    1 klucz odpowiedzi
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tygodnie import TYGODNIE, KSIAZECZKA          # noqa: E402

SYLABY_WYRAZOW = {
    "MAMA": ["MA", "MA"], "MAMY": ["MA", "MY"], "MIMO": ["MI", "MO"],
    "MAPA": ["MA", "PA"], "PAPA": ["PA", "PA"], "PUMA": ["PU", "MA"],
    "ALA": ["A", "LA"], "OLA": ["O", "LA"], "ULA": ["U", "LA"],
    "LALA": ["LA", "LA"], "LUPA": ["LU", "PA"], "BABA": ["BA", "BA"],
    "POLE": ["PO", "LE"], "BALE": ["BA", "LE"],
    "TATA": ["TA", "TA"], "DATA": ["DA", "TA"], "LATA": ["LA", "TA"],
    "DOMY": ["DO", "MY"], "LOTY": ["LO", "TY"], "BUTY": ["BU", "TY"],
    "TUBA": ["TU", "BA"], "LODY": ["LO", "DY"],
    "KINO": ["KI", "NO"], "KOTY": ["KO", "TY"], "KUNA": ["KU", "NA"],
    "NUTA": ["NU", "TA"], "MAKI": ["MA", "KI"], "PANI": ["PA", "NI"],
    "NOTA": ["NO", "TA"], "TANI": ["TA", "NI"],
    "SOWA": ["SO", "WA"], "WATA": ["WA", "TA"], "SANIE": ["SA", "NIE"],
    "NOSI": ["NO", "SI"], "KOSI": ["KO", "SI"], "WISI": ["WI", "SI"],
    "MAŁA": ["MA", "ŁA"], "BYŁA": ["BY", "ŁA"],
    "KOT": ["KOT"], "DOM": ["DOM"], "LAS": ["LAS"], "NOS": ["NOS"],
    "MAK": ["MAK"], "SOK": ["SOK"], "SEN": ["SEN"], "DÓŁ": ["DÓŁ"],
    "KOTEK": ["KO", "TEK"], "DOMEK": ["DO", "MEK"],
    "LASEK": ["LA", "SEK"], "NOSEK": ["NO", "SEK"],
    "ZUPA": ["ZU", "PA"], "KOZA": ["KO", "ZA"], "WAZA": ["WA", "ZA"],
    "NOGA": ["NO", "GA"], "GUMA": ["GU", "MA"], "ZIMA": ["ZI", "MA"],
    "CENA": ["CE", "NA"], "JAGODA": ["JA", "GO", "DA"],
    "GAZETA": ["GA", "ZE", "TA"], "JAJKO": ["JAJ", "KO"],
    "SZAFA": ["SZA", "FA"], "ŻABA": ["ŻA", "BA"], "CHATA": ["CHA", "TA"],
    "MUCHA": ["MU", "CHA"], "KOSZ": ["KOSZ"], "CZAS": ["CZAS"],
    "ŻUK": ["ŻUK"], "CZAPKA": ["CZAP", "KA"], "DACH": ["DACH"],
    "FOTEL": ["FO", "TEL"],
    "RAK": ["RAK"], "RURA": ["RU", "RA"], "ROWER": ["RO", "WER"],
    "BRAT": ["BRAT"], "TRAWA": ["TRA", "WA"], "DROGA": ["DRO", "GA"],
    "KLASA": ["KLA", "SA"], "PLECAK": ["PLE", "CAK"], "SKOK": ["SKOK"],
    "GRA": ["GRA"], "KOŃ": ["KOŃ"], "SIEĆ": ["SIEĆ"],
    "SĄ": ["SĄ"], "MAJĄ": ["MA", "JĄ"], "IDĘ": ["I", "DĘ"],
    "RĘKA": ["RĘ", "KA"], "WĄSY": ["WĄ", "SY"], "KSIĄŻKA": ["KSIĄŻ", "KA"],
}

# Podpowiedzi do ćwiczenia „wybierz wyraz". Czyta je rodzic — nie mamy
# API do generowania obrazków, więc obrazek zastępuje zdanie dorosłego.
PODPOWIEDZI = {
    "MAMA": "Osoba, która cię urodziła.", "MAPA": "Rysunek kraju albo drogi na papierze.",
    "PUMA": "Duży dziki kot.", "LALA": "Zabawka, która wygląda jak dziecko.",
    "LUPA": "Szkło, które powiększa.", "POLE": "Kawałek ziemi, na którym rośnie zboże.",
    "BALE": "Duże zabawy z tańcami.", "TATA": "Drugi rodzic, obok mamy.",
    "BUTY": "Zakładasz je na nogi.", "LODY": "Zimny słodki deser.",
    "TUBA": "Duży instrument, w który się dmucha.", "DOMY": "Budynki, w których mieszkają ludzie.",
    "KINO": "Miejsce, gdzie ogląda się filmy.", "KOTY": "Zwierzęta, które mruczą.",
    "KUNA": "Małe leśne zwierzę z długim ciałem.", "NUTA": "Znak, który mówi, co zagrać.",
    "MAKI": "Czerwone kwiaty rosnące w zbożu.", "PANI": "Dorosła kobieta.",
    "SOWA": "Ptak, który nie śpi w nocy.", "WATA": "Miękkie białe kłaczki z apteki.",
    "SANIE": "Jeździ się na nich po śniegu.", "KOT": "Zwierzę, które mruczy.",
    "DOM": "Budynek, w którym mieszkasz.", "LAS": "Miejsce, gdzie rośnie dużo drzew.",
    "NOS": "Masz go na środku twarzy.", "MAK": "Małe czarne ziarenka na bułce.",
    "SOK": "Pijesz go, na przykład z jabłek.", "SEN": "To, co ci się śni w nocy.",
    "KOTEK": "Mały kot.", "DOMEK": "Mały dom.", "LASEK": "Mały las.", "NOSEK": "Mały nos.",
    "ZUPA": "Jesz ją łyżką z talerza.", "KOZA": "Zwierzę z rogami, daje mleko.",
    "WAZA": "Naczynie, w którym podaje się zupę.", "NOGA": "Chodzisz na dwóch.",
    "GUMA": "Ścierasz nią ołówek.", "ZIMA": "Pora roku ze śniegiem.",
    "CENA": "Mówi, ile coś kosztuje.", "JAGODA": "Małe ciemne leśne owoce.",
    "GAZETA": "Czyta się ją, są w niej wiadomości.", "JAJKO": "Znosi je kura.",
    "SZAFA": "Wieszasz w niej ubrania.", "ŻABA": "Zielone zwierzę, które skacze.",
    "CHATA": "Mały drewniany dom.", "MUCHA": "Owad, który brzęczy nad stołem.",
    "KOSZ": "Wrzucasz do niego śmieci.", "CZAS": "Pokazuje go zegar.",
    "ŻUK": "Owad z twardym pancerzem.", "CZAPKA": "Zakładasz ją na głowę zimą.",
    "DACH": "Jest na górze domu, chroni przed deszczem.", "FOTEL": "Miękkie krzesło z oparciem.",
    "RAK": "Zwierzę z wody, ma szczypce.", "RURA": "Płynie przez nią woda.",
    "ROWER": "Ma dwa koła i pedały.", "BRAT": "Chłopiec, który ma tych samych rodziców co ty.",
    "TRAWA": "Zielona, rośnie na trawniku.", "DROGA": "Jeżdżą po niej samochody.",
    "KLASA": "Pokój w szkole, gdzie się uczysz.", "PLECAK": "Nosisz go na plecach do szkoły.",
    "SKOK": "Robisz go, kiedy podskakujesz.", "GRA": "Gracie w nią przy stole.",
    "KOŃ": "Duże zwierzę, można na nim jeździć.", "SIEĆ": "Łowi się nią ryby.",
    "RĘKA": "Masz na niej pięć palców.", "WĄSY": "Rosną nad ustami. Kot też je ma.",
    "KSIĄŻKA": "Ma strony i się ją czyta.", "MAJĄ": "Mówimy tak, gdy ktoś coś posiada.",
    "IDĘ": "Mówisz tak, gdy się gdzieś wybierasz.", "SĄ": "Mówimy tak o kilku osobach.",
    "BABA": "Inaczej: starsza kobieta.", "PAPA": "Mówimy tak na pożegnanie.",
    "ALA": "Imię dziewczynki.", "OLA": "Imię dziewczynki.", "ULA": "Imię dziewczynki.",
    "DATA": "Mówi, którego dnia coś było.", "LATA": "Najcieplejsza pora roku, w liczbie mnogiej.",
    "LOTY": "Podróże samolotem.", "NOTA": "Krótka notatka.", "TANI": "Kosztuje mało.",
    "NOSI": "Trzyma coś i idzie.", "KOSI": "Ścina trawę.", "WISI": "Trzyma się w powietrzu.",
    "MAŁA": "Nie duża.", "BYŁA": "Mówimy tak o czymś, co się już skończyło.",
    "MAMY": "Więcej niż jedna mama.", "MIMO": "Mimo deszczu wyszliśmy.",
    "DÓŁ": "Dziura w ziemi.", "MAK": "Małe czarne ziarenka na bułce.",
}


def kolumny(lista, n=6):
    return [lista[i:i + n] for i in range(0, len(lista), n)] or [[""]]


def dwusylabowe(wyrazy):
    return [w for w in wyrazy if len(SYLABY_WYRAZOW.get(w, [])) == 2]


def strona(nr, sufiks, typ, polecenie, dane, dla_rodzica=None):
    s = {"id": f"t{nr}-{sufiks}", "typ": typ, "polecenie": polecenie, "dane": dane}
    if dla_rodzica:
        s["dla_rodzica"] = dla_rodzica
    return s


def strony_tygodnia(t, klucz):
    """11 stron materiału dziecka. Ten sam szkielet w tygodniach 1–11."""
    nr = t["nr"]
    nowe, powt = t["sylaby"], t["powtorka_syl"]
    wyrazy = t["wyrazy"]
    strony = []

    # --- tydzień 1 nie ma jeszcze sylab spółgłoskowych ani wyrazów
    if nr == 1:
        pary = ["AO", "AU", "IE", "OU", "EY", "IA", "UO", "YI"]
        strony += [
            strona(nr, "samogloski", "sylaby_tabela", "Przeczytaj na głos.",
                   {"wiersze": kolumny(nowe, 3)},
                   "Pokazuj palcem. Dziecko mówi głoskę, nie nazwę litery."),
            strona(nr, "sciezka-1", "sylaby_sciezka", "Idź palcem i mów.",
                   {"kroki": ["A", "O", "U", "I", "E", "Y"], "meta": "Y"}),
            strona(nr, "slychac-1", "wybierz_wyraz", "Zakreśl literę, którą słyszysz.",
                   {"pozycje": [
                       {"podpowiedz_rodzica": "ANANAS", "opcje": ["A", "O", "U"], "poprawna": 0},
                       {"podpowiedz_rodzica": "OKO", "opcje": ["I", "O", "E"], "poprawna": 1},
                       {"podpowiedz_rodzica": "UCHO", "opcje": ["Y", "A", "U"], "poprawna": 2},
                       {"podpowiedz_rodzica": "IGŁA", "opcje": ["I", "E", "O"], "poprawna": 0}]},
                   "Przeczytaj wyraz i przeciągnij pierwszą głoskę: AAAnanas."),
            strona(nr, "pisanie-1", "pisanie_sylab", "Napisz po śladzie.",
                   {"wzory": ["A", "O", "U"], "linie_na_wzor": 2, "liniatura": "trzylinia"}),
            strona(nr, "pary", "sylaby_tabela", "Przeczytaj dwie naraz.",
                   {"wiersze": kolumny(pary, 4)},
                   "To jeszcze nie wyrazy. Chodzi o płynne przejście między samogłoskami."),
            strona(nr, "dyktando", "dyktando_sylabowe", "Napisz to, co usłyszysz.",
                   {"do_dyktowania": ["A", "U", "O", "I", "E", "Y"], "liniatura": "trzylinia"},
                   "Dyktuj powoli, po jednej. Nie powtarzaj więcej niż dwa razy."),
            strona(nr, "rysunek-1", "ramka_rysunkowa", "Narysuj coś na A.",
                   {"wyrazy": ["A"], "wysokosc_ramki_mm": 70},
                   "Podpowiedz: ananas, auto, arbuz. Dziecko wybiera samo."),
            strona(nr, "sciezka-2", "sylaby_sciezka", "Idź palcem i mów.",
                   {"kroki": ["O", "A", "E", "U", "Y", "I", "A"], "meta": "A"}),
            strona(nr, "slychac-2", "wybierz_wyraz", "Zakreśl literę, którą słyszysz.",
                   {"pozycje": [
                       {"podpowiedz_rodzica": "EKRAN", "opcje": ["A", "E", "Y"], "poprawna": 1},
                       {"podpowiedz_rodzica": "OSA", "opcje": ["O", "U", "I"], "poprawna": 0},
                       {"podpowiedz_rodzica": "ULICA", "opcje": ["E", "A", "U"], "poprawna": 2},
                       {"podpowiedz_rodzica": "INDYK", "opcje": ["I", "Y", "O"], "poprawna": 0}]},
                   "Ta sama zasada: przeciągaj pierwszą głoskę."),
            strona(nr, "pisanie-2", "pisanie_sylab", "Napisz po śladzie.",
                   {"wzory": ["I", "E", "Y"], "linie_na_wzor": 2, "liniatura": "trzylinia"}),
            strona(nr, "rysunek-2", "ramka_rysunkowa", "Narysuj coś na O.",
                   {"wyrazy": ["O"], "wysokosc_ramki_mm": 70},
                   "Podpowiedz: oko, osa, okno."),
        ]
        klucz.append({"strona_id": f"t{nr}-slychac-1", "odpowiedzi": ["A", "O", "U", "I"]})
        klucz.append({"strona_id": f"t{nr}-slychac-2", "odpowiedzi": ["E", "O", "U", "I"]})
        klucz.append({"strona_id": f"t{nr}-dyktando", "odpowiedzi": ["A", "U", "O", "I", "E", "Y"]})
        return strony

    # --- tygodnie 2–12: stały szkielet
    dwu = (dwusylabowe(wyrazy) or dwusylabowe(t["powtorka_wyr"]))[:6]
    # Prawa kolumna bez duplikatów: LASEK i NOSEK kończą się tak samo, więc
    # SEK ma być jednym polem, do którego prowadzą dwie linie — nie dwoma
    # identycznymi polami obok siebie.
    lewa = list(dict.fromkeys(SYLABY_WYRAZOW[w][0] for w in dwu))
    prawa = list(dict.fromkeys(SYLABY_WYRAZOW[w][1] for w in dwu))
    pary = [[lewa.index(SYLABY_WYRAZOW[w][0]), prawa.index(SYLABY_WYRAZOW[w][1])]
            for w in dwu]

    do_uzup = dwu[:4] or dwusylabowe(t["powtorka_wyr"])[:4]
    # Dystraktory muszą być RÓŻNE od poprawnej i od siebie — inaczej ćwiczenie
    # nie ma jednego rozwiązania. Pula: drugie sylaby innych wyrazów tygodnia,
    # w razie potrzeby uzupełniona sylabami powtórkowymi.
    pula = list(dict.fromkeys(
        [SYLABY_WYRAZOW[x][1] for x in dwu]
        + [SYLABY_WYRAZOW[x][1] for x in dwusylabowe(t["powtorka_wyr"])]
        + [s for s in nowe + powt if len(s) <= 3]))
    poz_uzup = []
    for w in do_uzup:
        a, b = SYLABY_WYRAZOW[w]
        dystraktory = [x for x in pula if x != b][:2]
        assert len(dystraktory) == 2, f"za mało dystraktorów dla {w} w T{nr}"
        poz_uzup.append({"wzor": f"{a}__", "opcje": [b] + dystraktory, "poprawna": 0})

    do_wyb = [w for w in wyrazy if w in PODPOWIEDZI][:4] or \
             [w for w in t["powtorka_wyr"] if w in PODPOWIEDZI][:4]
    poz_wyb = []
    for w in do_wyb:
        dystr = list(dict.fromkeys(x for x in wyrazy + t["powtorka_wyr"] if x != w))[:2]
        assert len(dystr) == 2, f"za mało dystraktorów wyrazowych dla {w} w T{nr}"
        poz_wyb.append({"podpowiedz_rodzica": PODPOWIEDZI[w],
                        "opcje": [w] + dystr, "poprawna": 0})

    dyktando = (nowe[:3] + powt[:3])[:6]
    rysunkowe = [w for w in wyrazy if w in PODPOWIEDZI][:4]

    strony = [
        strona(nr, "nowe-sylaby", "sylaby_tabela", "Przeczytaj na głos.",
               {"wiersze": kolumny(nowe)},
               "Czytajcie wierszami, potem kolumnami, potem na wyrywki."),
        strona(nr, "powtorka-sylaby", "sylaby_tabela", "Przeczytaj jeszcze raz.",
               {"wiersze": kolumny(powt)},
               f"Materiał z tygodni {', '.join(map(str, t['powtorka_z']))}. "
               "Bez tego nowe sylaby wypierają stare."),
        strona(nr, "sciezka", "sylaby_sciezka", "Idź palcem i czytaj.",
               {"kroki": (nowe + powt)[:8], "meta": (nowe + powt)[7] if len(nowe + powt) > 7 else nowe[-1]}),
        strona(nr, "lacz", "lacz_sylaby", "Połącz sylaby w wyrazy.",
               {"lewa": lewa, "prawa": prawa, "pary": pary},
               "Jeśli dziecko zgaduje, zasłoń prawą kolumnę i pytaj o samą sylabę."),
        strona(nr, "wyrazy", "wyrazy_do_czytania", "Przeczytaj wyrazy.",
               {"wyrazy": [{"wyraz": w, "sylaby": SYLABY_WYRAZOW[w]}
                           for w in (wyrazy or t["powtorka_wyr"])]},
               "Kreska między sylabami znika w kolejnych tygodniach. Tu jeszcze jest."),
        strona(nr, "uzupelnij", "uzupelnij_sylabe", "Dopisz brakującą sylabę.",
               {"pozycje": poz_uzup}),
        strona(nr, "wybierz", "wybierz_wyraz", "Zakreśl właściwy wyraz.",
               {"pozycje": poz_wyb},
               "Ty czytasz podpowiedź, dziecko czyta trzy wyrazy i wybiera."),
        strona(nr, "pisanie", "pisanie_sylab", "Napisz po śladzie.",
               {"wzory": nowe[:4], "linie_na_wzor": 2, "liniatura": "trzylinia"}),
    ]

    if t["zdania"]:
        strony.append(strona(nr, "zdania", "czytanie_zdan", "Przeczytaj zdania.",
                             {"zdania": t["zdania"], "pytanie": "O kim jest pierwsze zdanie?"},
                             "Najpierw ty na głos, potem razem, potem dziecko samo."))
    else:
        strony.append(strona(nr, "sciezka-2", "sylaby_sciezka", "Idź palcem i czytaj.",
                             {"kroki": (powt + nowe)[:8],
                              "meta": (powt + nowe)[7] if len(powt + nowe) > 7 else nowe[-1]},
                             "Zdań jeszcze nie ma — za mało liter. Pierwsze będą w tygodniu 4."))

    strony += [
        strona(nr, "dyktando", "dyktando_sylabowe", "Napisz to, co usłyszysz.",
               {"do_dyktowania": dyktando, "liniatura": "trzylinia"},
               "Dyktuj po jednej sylabie. Nie literuj."),
        strona(nr, "rysunek", "ramka_rysunkowa", "Przeczytaj i narysuj.",
               {"wyrazy": rysunkowe or ["KOT"], "wysokosc_ramki_mm": 55},
               "Rysunek nie musi być ładny. Ma pokazać, że dziecko zrozumiało wyraz."),
    ]

    klucz.append({"strona_id": f"t{nr}-lacz", "odpowiedzi": dwu[:6]})
    klucz.append({"strona_id": f"t{nr}-uzupelnij",
                  "odpowiedzi": [p["opcje"][p["poprawna"]] for p in poz_uzup]})
    klucz.append({"strona_id": f"t{nr}-wybierz",
                  "odpowiedzi": [p["opcje"][p["poprawna"]] for p in poz_wyb]})
    klucz.append({"strona_id": f"t{nr}-dyktando", "odpowiedzi": dyktando})
    return strony


def strony_tygodnia_12(t, klucz):
    """Tydzień 12 łamie szkielet: 3 strony powtórki + 8 stron książeczki."""
    nr = 12
    strony = [
        strona(nr, "nowe-sylaby", "sylaby_tabela", "Przeczytaj na głos.",
               {"wiersze": kolumny(t["sylaby"], 4)},
               "Ą i Ę mają ogonek. Czyta się je przez nos."),
        strona(nr, "powtorka-sylaby", "sylaby_tabela", "Przeczytaj jeszcze raz.",
               {"wiersze": kolumny(t["powtorka_syl"])},
               "Materiał z tygodni 8, 9, 10 i 11 — wszystko naraz."),
        strona(nr, "wyrazy", "wyrazy_do_czytania", "Przeczytaj wyrazy.",
               {"wyrazy": [{"wyraz": w, "sylaby": SYLABY_WYRAZOW[w]}
                           for w in t["powtorka_wyr"] + t["wyrazy"]]},
               "Bez kreski między sylabami. Dziecko dzieli je samo, w głowie."),
    ]
    for i, k in enumerate(KSIAZECZKA, 1):
        strony.append(strona(nr, f"ksiazeczka-{i:02d}", "czytanie_zdan",
                             "Przeczytaj sam.", {"zdania": k["zdania"]},
                             "Nie czytaj razem z dzieckiem. Poczekaj pięć sekund, zanim pomożesz."
                             if i == 1 else None))
    klucz.append({"strona_id": "t12-wyrazy",
                  "odpowiedzi": t["powtorka_wyr"] + t["wyrazy"]})
    return strony


def main():
    klucz = []
    tygodnie = []
    for t in TYGODNIE:
        strony = strony_tygodnia_12(t, klucz) if t["nr"] == 12 else strony_tygodnia(t, klucz)
        assert len(strony) == 11, f"T{t['nr']}: {len(strony)} stron dziecka, ma być 11"
        nowy = {}
        if t["litery"]:
            nowy["litery"] = t["litery"]
        if t["sylaby"]:
            nowy["sylaby"] = t["sylaby"]
        if t["wyrazy"]:
            nowy["wyrazy"] = t["wyrazy"]
        nowy["opis"] = t["opis"]
        powtorka = {"z_tygodni": t["powtorka_z"]}
        if t["powtorka_syl"]:
            powtorka["sylaby"] = t["powtorka_syl"]
        if t["powtorka_wyr"]:
            powtorka["wyrazy"] = t["powtorka_wyr"]

        g = t["gra"]
        tygodnie.append({
            "nr": t["nr"], "cel": t["cel"], "poziom_trudnosci": t["poziom"],
            "nowy_material": nowy, "powtorka": powtorka,
            "material_dziecka": strony,
            "gra": {"nazwa": g["nazwa"], "cel": g["cel"], "gracze": g["gracze"],
                    "czas_min": g["czas"], "przygotowanie": g["przygotowanie"],
                    "zasady": g["zasady"], "elementy_do_wyciecia": g["elementy"]},
            "czytanka": t["czytanka"],
            "karta_rodzica": t["karta_rodzica"],
            "karta_postepu": {
                "naglowek": f"Tydzień {t['nr']} — zaznacz sam",
                "kolumny": ["pon", "wt", "śr", "czw", "pt", "sob", "ndz"],
                "wiersze": ["Przeczytałem tabelę sylab",
                            "Przeczytałem wyrazy",
                            "Zagraliśmy w grę",
                            "Przeczytałem czytankę"]},
        })

    content = {
        "meta": {
            "slug": "czytam-sylabami", "tytul": "Czytam sylabami",
            "podtytul": "12-tygodniowy program nauki czytania",
            "archetyp": "PROGRAM", "wersja": "1.0", "wiek": "5–7 lat",
            "kategoria": "czytanie", "podkategoria": "sylaby",
            "strony_deklarowane": 184, "min_pt_dziecka": 14,
        },
        "wstep": {
            "warunek_wejscia": "Dziecko rozpoznaje kilka liter i potrafi je nazwać. "
                               "Nie musi znać całego alfabetu ani umieć pisać.",
            "obietnica": "Po dwunastu tygodniach dziecko przeczyta samo ośmiostronicową "
                         "książeczkę złożoną ze zdań, które zna.",
            "ile_czasu_dziennie": "10–15 minut, pięć dni w tygodniu.",
            "jak_korzystac": [
                "Drukuj po jednym tygodniu naraz. Piętnaście stron, w poniedziałek rano.",
                "Zacznij od karty rodzica. Zajmuje minutę i mówi, co robić przez cały tydzień.",
                "Rób jedną stronę dziennie. Dwie, jeśli dziecko chce — nigdy więcej.",
                "Grę zostaw na koniec tygodnia. Działa jako nagroda i jako powtórka.",
                "Nie przechodź dalej, dopóki nie zgadza się warunek z rubryki „kiedy dalej”.",
                "Jeśli tydzień nie wyszedł, powtórz go. Program nie ma terminu.",
            ],
            "czego_nie_robi": [
                "To nie jest terapia ani diagnoza. To ćwiczenia do zrobienia w domu.",
                "Nie uczy pisania. Dziecko pisze po śladzie tylko po to, żeby zapamiętać kształt litery.",
                "Nie uczy czytania ze zrozumieniem dłuższych tekstów. Kończy się na zdaniu i książeczce.",
                "Nie ocenia dziecka i nie porównuje go z rówieśnikami.",
                "Nie zadziała w tydzień. Dwanaście tygodni to minimum, nie obietnica.",
            ],
            "kiedy_do_specjalisty": "Jeśli po tygodniu 4 dziecko nadal nie łączy dwóch liter "
                                    "w sylabę, albo jeśli nie słyszy różnicy między podobnymi "
                                    "głoskami — porozmawiaj z logopedą. To nie znaczy, że coś "
                                    "jest nie tak. Znaczy, że warto zapytać.",
        },
        "tygodnie": tygodnie,
        "klucz_odpowiedzi": klucz,
        "fragment": {
            "do_tygodnia": 1,
            "obietnica_na_stronie": "Cztery pierwsze strony z 184. Cały fragment pobierzesz "
                                    "za darmo, bez zakładania konta.",
        },
    }

    out = Path("/home/user/kids-digital-shop/produkty/czytam-sylabami/content.json")
    out.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    stron_tygodnia = [1 + len(t["material_dziecka"]) + 1 + 1 + 1 for t in tygodnie]
    razem = 3 + sum(stron_tygodnia) + 1
    print(f"Zapisano content.json")
    print(f"  tygodni: {len(tygodnie)}   stron dziecka: {sum(len(t['material_dziecka']) for t in tygodnie)}")
    print(f"  bilans stron: 3 wstęp + {sum(stron_tygodnia)} tygodnie + 1 klucz = {razem}")
    print(f"  wpisów w kluczu odpowiedzi: {len(klucz)}")


if __name__ == "__main__":
    main()
