# Grafiki prototypu

## Arkusze referencyjne — NIE używaj ich bezpośrednio na stronie

**`cast.png`** (1672×941) — arkusz postaci. Pięć postaci w jednym rzędzie:
Zosia (3 l.), Ola (5 l.), Kuba (7 l.), Mama, **Bruno** (jeż z lupą, maskotka).

To jest referencja konstrukcyjna. Każdą nową scenę z postaciami generuj
z tym plikiem jako obrazem wejściowym, inaczej dostaniesz obcą obsadę zamiast
tej samej rodziny. Reguły stylu są w `marka/design-system.md`, sekcja
„Ilustracje".

**`ava_sheet.png`** (2048×2048) — siatka 3×3 z dziewięcioma portretami,
pocięta na `ava0.webp`–`ava8.webp`. Twarze są **wygenerowane i nie
przedstawiają realnych osób**. Służą wyłącznie jako placeholdery w blokach
opinii prototypu. Nie przenoś ich do bazy i nie traktuj jako danych
produkcyjnych.

## Sceny użyte na stronach

| plik | gdzie | co przedstawia |
|---|---|---|
| `hero.png` / `.webp` | strona główna, hero | Ola układa karty z literami, Bruno ogląda je przez lupę |
| `bruno.png` / `.webp` | ciemne pasma Klubu | Bruno solo, opiera się o lupę |
| `parent.png` / `.webp` | strona dla twórców | Mama tłumaczy Kubie zadanie z karty pracy |
| `creator.png` / `.webp` | strona dla twórców | nauczycielka projektuje kartę pracy |
| `shelf.png` | zapasowa, nieużyta | stos wydrukowanych stron, bez postaci |

`.png` to oryginały w pełnej rozdzielczości (1024–2048 px, po ~1,6 MB).
`.webp` to warianty użyte w HTML — 880 px szerokości, 25–35 KB.
Do druku i do nowych kompozycji bierz `.png`.

## Awatary

`ava0.webp`–`ava8.webp` — 160×160, kadry z `ava_sheet.png` czytane po kolei
wierszami: `ava0` to lewy górny, `ava8` prawy dolny.
