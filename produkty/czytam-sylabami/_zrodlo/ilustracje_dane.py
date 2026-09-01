# -*- coding: utf-8 -*-
"""Briefy ilustracji. Jeden na wyraz — obrazek zastępuje podpowiedź rodzica.

Wyrazy nieilustrowalne (MIMO, DATA, LATA, NOSI, MAMY, PAPA) briefu nie mają
i zostają przy podpowiedzi czytanej przez rodzica. Lepszy brak obrazka niż
obrazek, którego dziecko nie rozszyfruje.
"""

# wyraz -> co ma być w kadrze (styl dokłada renderer/ilustracje.py)
WYRAZY = {
    "ALA": "A small girl with short dark hair in a blue dress, standing and waving.",
    "OLA": "A small girl with two blonde plaits in a green dress, holding a flower.",
    "ULA": "A small girl with curly ginger hair in a sand-coloured dress, smiling.",
    "MAMA": "A mother in a navy jumper, smiling warmly, seen from the waist up.",
    "TATA": "A father in a blue shirt with short beard, smiling, seen from the waist up.",
    "BRAT": "An older boy of about nine in a green t-shirt, arms crossed, grinning.",
    "LALA": "A simple rag doll toy with yarn hair and a sand-coloured dress.",
    "LUPA": "A large magnifying glass with a persimmon orange rim and a navy handle.",
    "MAPA": "An open paper map with simple blue rivers and green land shapes.",
    "PUMA": "A sand-coloured wild cat, a puma, standing in profile.",
    "KOT": "A grey domestic cat sitting upright, tail curled around its paws.",
    "KOTY": "Three cats of different colours sitting next to each other in a row.",
    "DOM": "A simple detached house with a pitched roof, one door and two windows.",
    "DOMY": "Three simple houses of different heights standing side by side.",
    "LAS": "A group of five simple trees, pine and deciduous mixed, forming a small wood.",
    "KINO": "A cinema screen with three rows of empty seats seen from behind.",
    "KUNA": "A slender brown marten with a cream chest, standing on all fours.",
    "NUTA": "A single large musical note, a crotchet, in navy blue.",
    "SOWA": "An owl with big round eyes perched on a short branch, front view.",
    # Sama kula waty na białym tle jest nie do rozpoznania — potrzebny
    # kontekst skali i opakowanie.
    "WATA": "A round pack of white cotton wool with a blue paper band around it, and two loose cotton balls resting beside it.",
    "SANIE": "A wooden sledge with curved runners, seen from the side.",
    "NOGA": "A single human leg from hip to foot, wearing a blue sock and shoe.",
    "NOS": "A simple friendly cartoon face seen in profile, the nose clearly visible.",
    "KOZA": "A white goat with small curved horns, standing in profile.",
    "ZUPA": "A bowl of soup with steam rising and a spoon resting beside it.",
    "WAZA": "A tall soup tureen with a lid and two handles.",
    "SZAFA": "A tall wooden wardrobe with two doors, one slightly open.",
    "ŻABA": "A green frog sitting, seen from the front.",
    "MUCHA": "A single housefly with translucent wings, seen from above.",
    "CHATA": "A small wooden log cabin with a steep roof and a chimney.",
    "RAK": "A river crayfish with two large claws, seen from above.",
    "ROWER": "A bicycle seen from the side, with a navy frame.",
    "RURA": "A length of metal pipe with a bend in the middle.",
}

# Tydzień 1 uczy rozpoznawania samogłoski na początku wyrazu — obrazek
# pokazuje przedmiot, dziecko zakreśla literę.
PODPOWIEDZI_T1 = {
    "ANANAS": "A whole pineapple with a green leafy crown.",
    "OKO": "A single human eye, open, with lashes and a blue iris.",
    "UCHO": "A single human ear seen from the side.",
    "IGŁA": "A sewing needle with a long blue thread through its eye.",
    "EKRAN": "A computer monitor on a stand, screen blank and pale.",
    "OSA": "A wasp with yellow and black striped body, seen from above.",
    "ULICA": "A short street with two simple houses and a road running between them.",
    "INDYK": "A turkey with a fanned tail, seen from the side.",
}

OKLADKA = (
    "A hedgehog holding an oversized magnifying glass with a persimmon orange "
    "rim, looking through it at a large open book. Beside the hedgehog sits a "
    "small girl of about six, cross-legged, reading aloud from the same book."
)

# Otwarcie tygodnia — jedna scena na kartę rodzica, żeby program miał rytm.
TYGODNIE = {
    1: "A child's mouth open wide saying AAA, drawn as a simple friendly face, front view.",
    2: "A mother and a small child sitting at a kitchen table with a sheet of paper between them.",
    3: "A child's hand pointing at a large printed syllable on a sheet of paper.",
    4: "Two small girls sitting on the floor, one holding a doll, the other holding a ball.",
    5: "A father and child reading a short sentence together from a card.",
    6: "A child at a table with a row of picture cards laid out in front of them.",
    7: "An owl perched on a branch next to a child holding a sheet of paper.",
    8: "A child looking closely at three letter blocks pushed together to make one short word.",
    9: "A child counting three syllable cards laid out in a row on a table.",
    10: "A child pointing at two letters printed side by side on a large card.",
    11: "A boy on a bicycle riding past a tree, seen from the side.",
    12: "A small girl sitting alone in an armchair, reading a small book by herself.",
}
