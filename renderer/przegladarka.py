#!/usr/bin/env python3
"""Chromium przez Playwright — jedno miejsce, w którym wiemy, gdzie leży binarka.

Playwright w tym środowisku ma inną wersję niż zainstalowana przeglądarka,
więc `p.chromium.launch()` bez ścieżki pada na „Executable doesn't exist".
Każdy skrypt renderujący ma wołać `otworz()` stąd, nigdy Playwrighta wprost.
"""
import os
from contextlib import contextmanager
from glob import glob

from playwright.sync_api import sync_playwright

KANDYDACI = [
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    "/opt/pw-browsers/chromium/chrome-linux/chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
]


def sciezka_chromium():
    for s in KANDYDACI:
        if os.path.exists(s):
            return s
    for wzor in ("/opt/pw-browsers/chromium-*/chrome-linux/chrome",):
        znalezione = sorted(glob(wzor))
        if znalezione:
            return znalezione[-1]
    raise RuntimeError(
        "Nie znaleziono Chromium. Sprawdź /opt/pw-browsers/ i dopisz ścieżkę "
        "do KANDYDACI w renderer/przegladarka.py. NIE uruchamiaj "
        "`playwright install` — środowisko jest offline.")


@contextmanager
def otworz():
    """Kontekst zwracający gotową stronę Chromium."""
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=sciezka_chromium(),
                                    args=["--font-render-hinting=none",
                                          "--disable-lcd-text"])
        try:
            yield browser.new_page()
        finally:
            browser.close()


if __name__ == "__main__":
    print(sciezka_chromium())
