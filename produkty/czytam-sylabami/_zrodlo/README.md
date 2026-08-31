# Skrypt składający — jednorazowy, nie część pipeline'u

`content.json` jest artefaktem i źródłem prawdy. Renderer czyta wyłącznie jego.

Te dwa pliki to zapis tego, **jak** content.json powstał przy pierwszym
podejściu: `tygodnie.py` trzyma dane językowe (kolejność spółgłosek, listy
wyrazów, karty rodzica, gry, czytanki), `skladaj.py` rozwija je w 184-stronicową
strukturę.

Zostawiam je, bo bez nich zmiana progresji oznacza ręczną edycję 6 tysięcy
linii JSON-a. **Przy drobnej poprawce edytuj `content.json`.** Przy zmianie
progresji łatwiej poprawić `tygodnie.py` i przegenerować — ale wtedy pamiętaj,
że nadpiszesz ręczne zmiany.

Pozostałe 47 produktów powstaje inaczej: subagent pisze `content.json` wprost,
zgodnie z sekcją 7 `CLAUDE.md`. Ten skrypt nie jest wzorcem do naśladowania.

```bash
python3 produkty/czytam-sylabami/_zrodlo/skladaj.py
python3 renderer/validate.py schema czytam-sylabami
```
