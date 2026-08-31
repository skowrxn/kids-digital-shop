# Prototyp Lupy — 64 statyczne strony

Wejście, nie wyjście. **Nie modyfikuj tych plików** — służą jako źródło prawdy
dla danych produktów, tonu tekstów i wyglądu.

## Co tu jest

- `index.html` — strona główna w trybie marketplace
- `katalog.html` — pełna siatka 48 produktów
- `k-<kategoria>.html` — 12 stron kategorii z podkategoriami
- `p-<slug>.html` — 48 stron produktowych
- `klub.html`, `dla-tworcow.html` — dwie strony w trybie landing
- `style.css`, `app.js` — wspólne dla wszystkich stron
- `img/` — grafiki; `cast.png` to arkusz postaci (referencja do nowych scen)

## Skąd brać dane produktów

Tytuł, podtytuł, cena, wiek, liczba stron, autor, kategoria i podkategoria
są w `p-<slug>.html`. Liczba stron jest w tabeli `.specs` pod kluczem „Objętość".
Kategoria i podkategoria w okruszkach nawigacji na górze.

Opis produktu to dwa akapity w kolumnie lewej plus wyróżnione zdanie
„Dla kogo" na persymonowej belce. Ten ton jest wzorcem dla wszystkich tekstów
kierowanych do rodzica.

## Czego tu NIE ma

Zawartości merytorycznej materiałów — to właśnie masz wyprodukować.
Podglądy stron i awatary autorów są placeholderami do podmiany.

## Uwaga o opiniach

Opinie i twarze w blokach `.revs` są **wygenerowane na potrzeby prototypu**.
Twarze nie przedstawiają realnych osób. Nie traktuj ich jako danych produkcyjnych
i nie przenoś do bazy.
