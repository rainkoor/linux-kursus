#!/usr/bin/env python3
"""Asendab ekraanipiltide kohatäited päris piltidega.

Materjalis on kohatäited kujul
    <!-- PILT: ../pildid/FAIL.png | kirjeldus -->
Kui fail on kaustas docs/pildid/ olemas, asendab skript kohatäite pildiga
    ![kirjeldus](../pildid/FAIL.png)
mis näeb välja ühtemoodi GitHubis ja veebilehel. Puuduvate piltide kohatäited
jäävad alles (veebilehel nähtamatud).

Kasutamine (kursuse juurkataloogis):
    python3 tools/pildid.py          # asenda ja näita, mis on veel puudu
    python3 tools/pildid.py --kuiva  # ainult näita, midagi ei muuda
"""
import re
import sys
from pathlib import Path

JUUR = Path(__file__).resolve().parent.parent
DOCS = JUUR / "docs"
KOHATAIDE = re.compile(r"<!--\s*PILT:\s*(\S+?)\s*\|\s*(.*?)\s*-->")


def main():
    kuiv = "--kuiva" in sys.argv
    asendatud, puudu = [], []
    for md in sorted(DOCS.rglob("*.md")):
        tekst = md.read_text(encoding="utf-8")

        def asenda(m):
            tee, kirjeldus = m.group(1), m.group(2)
            fail = (md.parent / tee).resolve()
            nimi = md.relative_to(JUUR)
            if not fail.is_file():
                puudu.append(f"{fail.name}  ({nimi})")
                return m.group(0)
            asendatud.append(f"{fail.name}  ->  {nimi}")
            alt = kirjeldus.replace("[", "(").replace("]", ")")
            return f"![{alt}]({tee})"

        uus = KOHATAIDE.sub(asenda, tekst)
        if uus != tekst and not kuiv:
            md.write_text(uus, encoding="utf-8")

    tegu = "Asendataks" if kuiv else "Asendatud"
    print(f"{tegu}: {len(asendatud)}")
    for r in asendatud:
        print("  +", r)
    print(f"Pilt veel puudu: {len(puudu)}")
    for r in puudu:
        print("  -", r)

    # pildid, mida ükski kohatäide ega leht ei kasuta (nt kirjaviga failinimes)
    kasutusel = set()
    for md in DOCS.rglob("*.md"):
        kasutusel.update(Path(p).name for p in re.findall(r"pildid/[\w./-]+", md.read_text(encoding="utf-8")))
    yleliigsed = [p.name for p in sorted((DOCS / "pildid").glob("*.png")) if p.name not in kasutusel]
    if yleliigsed:
        print("Kasutamata pildifailid (kontrolli failinime):")
        for n in yleliigsed:
            print("  ?", n)


if __name__ == "__main__":
    main()
