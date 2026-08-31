#!/usr/bin/env python3
"""Minimalne drzewo DOM na stdlib-owym html.parser.

Powód istnienia: strony prototypu mają głęboko zagnieżdżone <div>,
a wyciąganie ich wyrażeniem regularnym nie działa — `.*?` zatrzymuje się
na pierwszym domknięciu wewnętrznym, nie na właściwym. Parser liczy
zagnieżdżenie i zwraca poprawne poddrzewa.

Bez zależności zewnętrznych — całość ma działać offline.
"""
from html.parser import HTMLParser

PUSTE = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
         "meta", "param", "source", "track", "wbr"}


class Wezel:
    __slots__ = ("tag", "atrybuty", "dzieci", "rodzic")

    def __init__(self, tag, atrybuty=None, rodzic=None):
        self.tag = tag
        self.atrybuty = atrybuty or {}
        self.dzieci = []
        self.rodzic = rodzic

    # ------------------------------------------------------------ dostęp
    @property
    def klasy(self):
        return self.atrybuty.get("class", "").split()

    def pasuje(self, tag=None, klasa=None, **atrybuty):
        if tag and self.tag != tag:
            return False
        if klasa and klasa not in self.klasy:
            return False
        return all(self.atrybuty.get(k) == v for k, v in atrybuty.items())

    def znajdz_wszystkie(self, tag=None, klasa=None, **atrybuty):
        out = []
        for d in self.dzieci:
            if isinstance(d, Wezel):
                if d.pasuje(tag, klasa, **atrybuty):
                    out.append(d)
                out += d.znajdz_wszystkie(tag, klasa, **atrybuty)
        return out

    def znajdz(self, tag=None, klasa=None, **atrybuty):
        w = self.znajdz_wszystkie(tag, klasa, **atrybuty)
        return w[0] if w else None

    def dzieci_tag(self, tag):
        """Tylko bezpośrednie dzieci — bez schodzenia w głąb."""
        return [d for d in self.dzieci if isinstance(d, Wezel) and d.tag == tag]

    # ------------------------------------------------------------- tekst
    @property
    def tekst(self):
        """Tekst poddrzewa. <svg> pomijane — niosą etykiety i inicjały,
        które nie są treścią strony."""
        czesci = []
        for d in self.dzieci:
            if isinstance(d, str):
                czesci.append(d)
            elif d.tag != "svg":
                czesci.append(d.tekst)
        return " ".join(x for x in czesci if x)

    @property
    def styl(self):
        return self.atrybuty.get("style", "")

    def __repr__(self):
        k = "." + ".".join(self.klasy) if self.klasy else ""
        return f"<{self.tag}{k}>"


class _Budowniczy(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.korzen = Wezel("#root")
        self.stos = [self.korzen]

    def handle_starttag(self, tag, attrs):
        w = Wezel(tag, dict(attrs), self.stos[-1])
        self.stos[-1].dzieci.append(w)
        if tag not in PUSTE:
            self.stos.append(w)

    def handle_startendtag(self, tag, attrs):
        self.stos[-1].dzieci.append(Wezel(tag, dict(attrs), self.stos[-1]))

    def handle_endtag(self, tag):
        for i in range(len(self.stos) - 1, 0, -1):
            if self.stos[i].tag == tag:
                del self.stos[i:]
                return
        # domknięcie bez otwarcia — ignorujemy, prototyp bywa niechlujny

    def handle_data(self, data):
        if data.strip():
            self.stos[-1].dzieci.append(data)


def parsuj(html):
    b = _Budowniczy()
    b.feed(html)
    b.close()
    return b.korzen


def zwin(s):
    """Białe znaki -> pojedyncza spacja."""
    return " ".join(s.split())
