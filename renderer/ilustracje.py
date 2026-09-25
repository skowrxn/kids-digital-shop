#!/usr/bin/env python3
"""Ilustracje przez kie.ai (gpt-image-2). Cache na dysku, idempotentnie.

  export KIE_API_KEY=...
  python3 renderer/ilustracje.py <slug>          # dogeneruj brakujące
  python3 renderer/ilustracje.py <slug> --raport # tylko pokaż, czego brakuje
  python3 renderer/ilustracje.py <slug> --od-nowa <id> [<id>...]

Klucz API czytamy WYŁĄCZNIE ze zmiennej środowiskowej. Nie zapisujemy go
do repo, do manifestu ani do logów.

Skąd się biorą zlecenia: z pól `ilustracja` w content.json. Prompt jest
częścią danych produktu, tak samo jak treść zadania — patrz CLAUDE.md sek. 2.

Post-produkcja jest tu, a nie w rendererze, bo bramka 12% pokrycia tuszem
dotyczy wariantu czarno-białego: model zwraca obrazek z pełnym tłem, które
na laserówce zabiłoby całą stronę. Dlatego każdy plik idzie w dwóch
wersjach: <id>.png (kolor) i <id>-bw.png (do druku domyślnego).
"""
import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.kie.ai/api/v1"
MODEL = "gpt-image-2-text-to-image"
#: CDN z wynikami odrzuca domyślny User-Agent Pythona (403), więc podajemy własny.
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

#: Blokada stylu. Doklejana do KAŻDEGO promptu, żeby 50 obrazków wyglądało
#: jak jeden zestaw, a nie jak 50 niepowiązanych. Reguły z marka/design-system.md.
STYL = (
    "Children's book illustration, flat gouache painting with matte texture. "
    "Blocky simplified forms, each surface cut into a few large decisive planes "
    "with painterly shading inside the facet. "
    "NO black outlines, NO ink contours, NO line art — form is described by "
    "colour planes only. "
    "Palette limited to six colours drawn from: deep navy #1E2D4D, blue #3E62A8, "
    "slate #7C8FA8, warm sand #E4DED2, moss green #5C7A4A, ochre #C9A227. "
    "Exactly ONE small accent of persimmon orange #E2643C per image, no more. "
    "PURE WHITE background #FFFFFF, completely plain and empty. "
    "NO drop shadow, NO ground line, NO floor, NO frame, NO border, NO text, "
    "NO letters, NO watermark. "
    "Single subject centred with generous white margin around it. "
    "Light overall — large areas of the image must stay pure white, because "
    "this is printed on a home laser printer. "
    "PEOPLE ARE DRAWN, NEVER PHOTOGRAPHED: stylised storybook characters with "
    "oversized heads, stocky bodies, short limbs and big shoes. Simple dot eyes "
    "and a simple mouth. NOT photorealistic, NOT a portrait, NOT a real person, "
    "no realistic skin texture, no realistic hair strands, no 3D render."
)

#: Ile pikseli tła zostawiamy tolerancji przy wybielaniu (0–255).
PROG_TLA = 232
#: Docelowe pokrycie tuszem pojedynczej ilustracji w wariancie BW.
CEL_POKRYCIA_BW = 0.15


def klucz():
    k = os.environ.get("KIE_API_KEY", "").strip()
    if not k:
        sys.exit("BŁĄD: brak KIE_API_KEY w środowisku.\n"
                 "  export KIE_API_KEY=...   (klucza nie zapisujemy w repo)")
    return k


def _zadanie(prompt, proporcje="1:1"):
    dane = json.dumps({"model": MODEL,
                       "input": {"prompt": prompt, "aspect_ratio": proporcje}}).encode()
    req = urllib.request.Request(f"{API}/jobs/createTask", data=dane, method="POST",
                                 headers={"Authorization": f"Bearer {klucz()}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        o = json.loads(r.read())
    if o.get("code") != 200:
        raise RuntimeError(f"createTask: {o.get('code')} {o.get('msg')}")
    return o["data"]["taskId"]


def _czekaj(task_id, limit_s=420):
    start = time.time()
    while time.time() - start < limit_s:
        req = urllib.request.Request(f"{API}/jobs/recordInfo?taskId={task_id}",
                                     headers={"Authorization": f"Bearer {klucz()}"})
        with urllib.request.urlopen(req, timeout=60) as r:
            o = json.loads(r.read())
        d = o.get("data", {})
        if d.get("state") == "success":
            url = json.loads(d["resultJson"])["resultUrls"][0]
            return url, d.get("creditsConsumed", 0)
        if d.get("state") == "fail":
            raise RuntimeError(f"zadanie padło: {d.get('failMsg') or d.get('failCode')}")
        time.sleep(10)
    raise TimeoutError(f"{task_id}: przekroczono {limit_s}s")


def _pobierz(url, cel):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as r:
        cel.write_bytes(r.read())


def obrob(surowy: Path, kolor: Path, bw: Path, bok=640):
    """Tło na czysto białe, przycięcie do obiektu, wersja kolorowa i drukarska.

    Model zwraca kremowe tło mimo instrukcji „pure white" — bez wybielenia
    strona miałaby 100% pokrycia tuszem.
    """
    im = Image.open(surowy).convert("RGB")

    # 1. tło -> czysta biel (próbka z czterech rogów, żeby nie zgadywać)
    rogi = [im.getpixel(p) for p in
            ((2, 2), (im.width - 3, 2), (2, im.height - 3), (im.width - 3, im.height - 3))]
    tlo = tuple(sum(k[i] for k in rogi) // 4 for i in range(3))
    piksele = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = piksele[x, y]
            if abs(r - tlo[0]) < 26 and abs(g - tlo[1]) < 26 and abs(b - tlo[2]) < 26 \
                    and min(r, g, b) > PROG_TLA - 40:
                piksele[x, y] = (255, 255, 255)

    # 2. przycięcie do samego obiektu + margines, żeby skala była porównywalna
    szary = im.convert("L")
    ramka = ImageOps.invert(szary).point(lambda p: 255 if p > 18 else 0).getbbox()
    if ramka:
        m = int(max(im.size) * 0.03)
        im = im.crop((max(0, ramka[0] - m), max(0, ramka[1] - m),
                      min(im.width, ramka[2] + m), min(im.height, ramka[3] + m)))

    # 640 px wystarcza: najbardziej rozciągnięty użytek to 56 mm, czyli ~660 px
    # przy 300 dpi. Przy 900 px sam pelny-kolor.pdf ważył 41 MB.
    im = ImageOps.pad(im, (bok, bok), color=(255, 255, 255), method=Image.LANCZOS)
    _zapisz_lekko(_przezroczyste_tlo(im), kolor, kolory=96)

    # 3. wariant drukarski.
    #
    # Samo rozjaśnianie nie działa: bramka liczy piksele NIEBIAŁE, więc jasna
    # szarość kosztuje tyle samo co czerń, a obrazek robi się nieczytelny.
    # Zamiast tego podnosimy kontrast i wycinamy wszystko powyżej progu do
    # czystej bieli — zostaje rysunek z ciemnymi konturami i pustym środkiem.
    # Próg dobieramy tak, żeby zmieścić się w budżecie pokrycia.
    g = ImageOps.autocontrast(im.convert("L"), cutoff=1)
    for prog in (200, 185, 170, 155, 140, 125, 110, 95, 80):
        kandydat = g.point(
            lambda p, t=prog: 255 if p >= t else int(40 + (p / t) * 150))
        dane = kandydat.tobytes()
        pokrycie = sum(1 for p in dane if p < 250) / len(dane)
        if pokrycie <= CEL_POKRYCIA_BW:
            break
    _zapisz_lekko(_przezroczyste_tlo(kandydat.convert("RGB")), bw, kolory=32)
    return pokrycie


def _zapisz_lekko(im, cel, kolory=96):
    """PNG w palecie z alfą. Gwasz to płaskie plamy — 96 barw wystarcza,
    a plik schodzi kilkukrotnie."""
    # Dla RGBA Pillow dopuszcza wyłącznie FASTOCTREE (albo libimagequant).
    paleta = im.convert("RGBA").quantize(colors=kolory, method=Image.FASTOCTREE,
                                         dither=Image.NONE)
    paleta.save(cel, optimize=True)


def _przezroczyste_tlo(im, prog=246):
    """Tło na alfa 0, ale TYLKO to połączone z krawędzią obrazka.

    Zwykłe „każdy jasny piksel na przezroczysty" wycięłoby też białka oczu
    i rozjaśnienia wewnątrz obiektu, więc idziemy od ramki w głąb.
    Bez tego biały prostokąt obrazka odcina się od kremowego papieru
    w wariancie pełnokolorowym.

    Rozrost obszaru liczymy na numpy — pętla po pikselach w Pythonie
    zajmowała przy 900x900 kilkadziesiąt sekund na obrazek.
    """
    import numpy as np

    im = im.convert("RGBA")
    a = np.array(im)
    jasne = (a[:, :, 0] >= prog) & (a[:, :, 1] >= prog) & (a[:, :, 2] >= prog)

    tlo = np.zeros_like(jasne)
    tlo[0, :] = jasne[0, :]
    tlo[-1, :] = jasne[-1, :]
    tlo[:, 0] = jasne[:, 0]
    tlo[:, -1] = jasne[:, -1]

    while True:
        ile = int(tlo.sum())
        rosnie = tlo.copy()
        rosnie[1:, :] |= tlo[:-1, :]
        rosnie[:-1, :] |= tlo[1:, :]
        rosnie[:, 1:] |= tlo[:, :-1]
        rosnie[:, :-1] |= tlo[:, 1:]
        tlo = rosnie & jasne
        if int(tlo.sum()) == ile:
            break

    a[:, :, 3] = np.where(tlo, 0, a[:, :, 3])
    return Image.fromarray(a, "RGBA")


def zlecenia(c):
    """Wszystkie prompty z content.json, kluczowane po id ilustracji.

    Id jest per MOTYW, nie per pozycja: KOT wraca w tygodniach 8 i 9, a to
    ma być ten sam obrazek — jeden koszt i jedna spójna talia wizualna.

    Obchód stron idzie przez wszystkie_strony() z walidatora, żeby oba
    moduły widziały ten sam dokument niezależnie od archetypu.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from validate import wszystkie_strony

    out = {}

    def dodaj(i, domyslne="1:1"):
        if i:
            out[i["id"]] = (i["brief"], i.get("proporcje", domyslne))

    dodaj(c["meta"].get("ilustracja"), "3:2")
    for t in c.get("tygodnie", []):
        dodaj(t.get("ilustracja"), "3:2")
    for b in c.get("bloki", []):
        dodaj(b.get("ilustracja"), "3:2")

    for s in wszystkie_strony(c):
        dane = s.get("dane")
        if not isinstance(dane, dict):
            continue
        for p in dane.get("pozycje", []):
            if isinstance(p, dict):
                dodaj(p.get("ilustracja"))
        for k in dane.get("karty", []):
            if isinstance(k, dict):
                dodaj(k.get("ilustracja"))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("--raport", action="store_true")
    ap.add_argument("--przelicz-bw", action="store_true",
                    help="odśwież warianty drukarskie z zapisanych kolorowych, "
                         "bez wołania API i bez kosztu")
    ap.add_argument("--od-nowa", nargs="*", default=[])
    ap.add_argument("--rownolegle", type=int, default=4)
    ap.add_argument("--tylko", nargs="*", default=None,
                    help="ogranicz do podanych id — do próby stylu przed partią")
    a = ap.parse_args()

    kat = ROOT / "produkty" / a.slug
    c = json.loads((kat / "content.json").read_text(encoding="utf-8"))
    katalog = kat / "ilustracje"
    katalog.mkdir(parents=True, exist_ok=True)
    plik_manifestu = katalog / "_manifest.json"
    manifest = json.loads(plik_manifestu.read_text(encoding="utf-8")) \
        if plik_manifestu.exists() else {}

    wszystkie = zlecenia(c)

    if a.przelicz_bw:
        for ident in sorted(wszystkie):
            kolor = katalog / f"{ident}.png"
            if not kolor.exists():
                continue
            pok = obrob(kolor, kolor, katalog / f"{ident}-bw.png")
            if ident in manifest:
                manifest[ident]["pokrycie_bw"] = round(pok, 3)
            print(f"  {ident}: pokrycie BW {pok:.0%}")
        plik_manifestu.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                  encoding="utf-8")
        return

    do_zrobienia = {}
    for ident, (prompt, prop) in wszystkie.items():
        odcisk = hashlib.sha256((prompt + STYL + prop).encode()).hexdigest()[:16]
        wpis = manifest.get(ident)
        gotowy = (wpis and wpis.get("odcisk") == odcisk
                  and (katalog / f"{ident}.png").exists()
                  and (katalog / f"{ident}-bw.png").exists())
        if gotowy and ident not in a.od_nowa:
            continue
        do_zrobienia[ident] = (prompt, prop, odcisk)

    brakujace = dict(do_zrobienia)
    if a.tylko:
        do_zrobienia = {k: v for k, v in do_zrobienia.items() if k in a.tylko}

    gotowych = len(wszystkie) - len(brakujace)
    print(f"{a.slug}: {len(wszystkie)} ilustracji w content.json, "
          f"{gotowych} gotowych, {len(brakujace)} brakuje"
          + (f", w tej partii {len(do_zrobienia)}" if a.tylko else ""))
    if a.raport or not do_zrobienia:
        for ident in sorted(do_zrobienia):
            print(f"  brakuje: {ident}")
        return

    print(f"szacunkowy koszt: ~{len(do_zrobienia) * 6} kredytów")

    def zrob(pozycja):
        """Generowanie i pobieranie ponawiane OSOBNO.

        Generowanie kosztuje kredyty, pobieranie nie. Wspólna pętla oznaczała,
        że błąd pobrania kazał płacić za obrazek jeszcze raz.
        """
        ident, (prompt, prop, odcisk) = pozycja
        url = kredyty = tid = None
        for proba in range(3):
            try:
                tid = _zadanie(f"{prompt}\n\n{STYL}", prop)
                url, kredyty = _czekaj(tid)
                break
            except (urllib.error.URLError, RuntimeError, TimeoutError) as e:
                if proba == 2:
                    return ident, None, f"generowanie: {e}"
                time.sleep(6 * (proba + 1))

        surowy = katalog / f".{ident}.raw.png"
        for proba in range(4):
            try:
                _pobierz(url, surowy)
                break
            except (urllib.error.URLError, OSError) as e:
                if proba == 3:
                    return ident, None, f"pobieranie (obrazek opłacony, url={url}): {e}"
                time.sleep(5 * (proba + 1))
        try:
            pokrycie = obrob(surowy, katalog / f"{ident}.png", katalog / f"{ident}-bw.png")
        except OSError as e:
            return ident, None, f"obróbka: {e}"
        finally:
            surowy.unlink(missing_ok=True)
        return ident, {"odcisk": odcisk, "taskId": tid, "kredyty": kredyty,
                       "pokrycie_bw": round(pokrycie, 3)}, None

    udane, bledy = 0, []
    with ThreadPoolExecutor(max_workers=a.rownolegle) as pula:
        for ident, wpis, blad in pula.map(zrob, do_zrobienia.items()):
            if blad:
                bledy.append((ident, blad))
                print(f"  BŁĄD {ident}: {blad}")
                continue
            manifest[ident] = wpis
            plik_manifestu.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                      encoding="utf-8")   # zapis po KAŻDEJ ilustracji
            udane += 1
            print(f"  {ident}  pokrycie BW {wpis['pokrycie_bw']:.0%}  "
                  f"({udane}/{len(do_zrobienia)})")

    koszt = sum(w.get("kredyty", 0) for w in manifest.values())
    print(f"\ngotowe: {udane}, błędów: {len(bledy)}, łączny koszt w manifeście: {koszt:g} kredytów")
    if bledy:
        sys.exit(1)


if __name__ == "__main__":
    main()
