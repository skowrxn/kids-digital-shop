# Generator specyfikacji — jednorazowy, nie część pipeline'u

`produkty/<slug>/spec.md` jest artefaktem i źródłem prawdy. Renderer i
subagenci czytają jego, nie ten skrypt.

`buduj.py` to zapis tego, **jak** powstała partia specyfikacji: dane
katalogowe (tytuł, cena, wiek, autor, liczba stron, „Dla kogo") ciągnie
z `produkty/_katalog.json`, czyli z prototypu, a autorska część —
obietnica, warunek wejścia, progresja, zakres fragmentu i sekcja
„czego NIE robi" — siedzi w słowniku `SPECY`.

Zostawiam go, bo trzyma w jednym miejscu decyzje, które inaczej byłyby
rozsiane po piętnastu plikach markdown. Przy drobnej poprawce edytuj
`spec.md`. Przy zmianie wzorca dla całej partii łatwiej poprawić skrypt
i przegenerować — ale wtedy nadpiszesz ręczne zmiany.

```bash
python3 produkty/_specy/buduj.py
```
