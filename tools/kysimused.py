#!/usr/bin/env python3
"""Koostab laboritöö lõppu aruande küsimuste loendi.

Kasutus: python3 tools/kysimused.py [docs/moodul-XX-.../labor.md ...]

Ilma argumentideta uuendab kõiki laboritöid, kus loend juba on (märgend
<!-- kysimused -->). Argumendiga lisab loendi ka uutele laboritöödele.
Loend pannakse õpetaja märkuse ette; olemasolev loend kirjutatakse üle.
Käivita pärast küsimuste muutmist uuesti, seejärel tools/navigatsioon.py.
"""
import pathlib
import re
import sys

JUUR = pathlib.Path(__file__).resolve().parent.parent
KYSIMUS = re.compile(r"^\*\*([A-Z]\d+)\.\*\*\s*(.*)$")
PLOKK = re.compile(r"\n*<!-- kysimused -->.*?<!-- /kysimused -->\n*", re.S)
OPETAJALE = "> [!NOTE]\n> **Õpetajale:**"


SAMM = re.compile(r"^\*\*(\d+\.\d+)\*\*")
OSA = re.compile(r"^## (\d+)\. osa\b")


def kysimused(tekst):
    """Küsimused koos viitega punktile, mille juures neid küsitakse."""
    tulemus = []
    koodis = False
    koht = ""
    for rida in tekst.split("\n"):
        if rida.lstrip().startswith("```"):
            koodis = not koodis
            continue
        if koodis:
            continue
        if OSA.match(rida):
            koht = f"{OSA.match(rida).group(1)}. osa"
        elif SAMM.match(rida):
            koht = f"punkt {SAMM.match(rida).group(1)}"
        elif rida.startswith("## "):
            koht = rida[3:].strip()
        m = KYSIMUS.match(rida)
        if m:
            viide = f" *({koht})*" if koht else ""
            tulemus.append(f"- **{m.group(1)}.**{viide} {m.group(2)}")
    return tulemus


def uuenda(tee):
    tekst = tee.read_text(encoding="utf-8")
    tekst = PLOKK.sub("\n\n", tekst)
    loend = kysimused(tekst)
    if not loend:
        print(f"{tee}: küsimusi ei leitud")
        return
    plokk = (
        "<!-- kysimused -->\n"
        "## Aruande küsimused\n\n"
        "Kõik selle laboritöö küsimused ühes kohas. Sulgudes on punkt, mille juures küsimust küsitakse. "
        "Kopeeri loend oma aruande alguseks ja kirjuta vastus iga küsimuse alla. "
        "Kus küsitakse käsku, kirjuta üles kogu käsk.\n\n"
        + "\n".join(loend)
        + "\n<!-- /kysimused -->\n\n---\n\n"
    )
    if OPETAJALE in tekst:
        i = tekst.index(OPETAJALE)
        eel = tekst[:i].rstrip("\n")
        if eel.endswith("---"):
            eel = eel[:-3].rstrip("\n")
        tekst = eel + "\n\n---\n\n" + plokk + tekst[i:]
    else:
        tekst = tekst.rstrip("\n") + "\n\n---\n\n" + plokk
    tekst = re.sub(r"\n---\n(?:\s*\n---\n)+", "\n---\n", tekst)
    tee.write_text(tekst, encoding="utf-8")
    print(f"{tee.relative_to(JUUR)}: {len(loend)} küsimust")


def main():
    if len(sys.argv) > 1:
        failid = [pathlib.Path(a).resolve() for a in sys.argv[1:]]
    else:
        failid = [f for f in sorted((JUUR / "docs").glob("moodul-*/labor.md"))
                  if "<!-- kysimused -->" in f.read_text(encoding="utf-8")]
    for f in failid:
        uuenda(f)


if __name__ == "__main__":
    main()
