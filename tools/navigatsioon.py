#!/usr/bin/env python3
"""Loob GitHubi jaoks navigatsioonilingid ja README sisukorra mkdocs.yml menüü järgi.

Käivita repo juurkaustas pärast lehtede lisamist, ümbernimetamist või menüü muutmist:

    python3 tools/navigatsioon.py

- Iga lehe lõppu kirjutatakse (või uuendatakse) rida „← eelmine · Sisukord · järgmine →“
  märgendite <!-- navigatsioon --> ja <!-- /navigatsioon --> vahele.
- README.md-s uuendatakse sisukord märgendite <!-- sisukord --> ja <!-- /sisukord --> vahel.

Veebilehel eemaldab navigatsioonirea hook hooks/callouts.py, sest MkDocs Material näitab
eelmise ja järgmise lehe linke ise.
"""
import os
import re
import yaml

JUUR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(JUUR, "docs")


class Laadija(yaml.SafeLoader):
    pass


Laadija.add_multi_constructor("tag:yaml.org,2002:python/", lambda l, s, n: None)


def menyy():
    with open(os.path.join(JUUR, "mkdocs.yml"), encoding="utf-8") as f:
        nav = yaml.load(f, Loader=Laadija)["nav"]
    lehed, puu = [], []

    def kaik(osad, tase):
        for osa in osad:
            (nimi, sisu), = osa.items()
            if isinstance(sisu, str):
                lehed.append(sisu)
                puu.append((tase, nimi, sisu))
            else:
                puu.append((tase, nimi, None))
                kaik(sisu, tase + 1)

    kaik(nav, 0)
    return lehed, puu


def pealkiri(leht):
    with open(os.path.join(DOCS, leht), encoding="utf-8") as f:
        for rida in f:
            if rida.startswith("# "):
                return rida[2:].strip()
    return leht


def suht(lahte, siht):
    return os.path.relpath(os.path.join(DOCS, siht), os.path.dirname(os.path.join(DOCS, lahte))).replace(os.sep, "/")


def navigatsioon(lehed):
    lehed = [l for l in lehed if l != "index.md"]
    for i, leht in enumerate(lehed):
        osad = []
        if i > 0:
            osad.append(f"[← {pealkiri(lehed[i-1])}]({suht(leht, lehed[i-1])})")
        sisukord = os.path.relpath(os.path.join(JUUR, "README.md"),
                                   os.path.dirname(os.path.join(DOCS, leht))).replace(os.sep, "/")
        osad.append(f"[Sisukord]({sisukord}#sisukord)")
        if i < len(lehed) - 1:
            osad.append(f"[{pealkiri(lehed[i+1])} →]({suht(leht, lehed[i+1])})")
        plokk = "<!-- navigatsioon -->\n---\n\n" + " · ".join(osad) + "\n<!-- /navigatsioon -->\n"
        tee = os.path.join(DOCS, leht)
        with open(tee, encoding="utf-8") as f:
            sisu = f.read()
        sisu = re.sub(r"\n*<!-- navigatsioon -->.*?<!-- /navigatsioon -->\n?", "\n", sisu, flags=re.S)
        sisu = sisu.rstrip("\n") + "\n\n" + plokk
        with open(tee, "w", encoding="utf-8") as f:
            f.write(sisu)


def sisukord(puu):
    read = []
    for tase, nimi, leht in puu:
        if leht == "index.md":
            continue
        if leht is None:
            if tase == 0:
                read.append(f"\n**{nimi}**\n")
            else:
                moodul = next((l for t, n, l in puu[puu.index((tase, nimi, None)) + 1:] if l), None)
                alam = [(n, l) for t, n, l in puu[puu.index((tase, nimi, None)) + 1:puu.index((tase, nimi, None)) + 4] if l]
                lingid = " · ".join(f"[{n.lower()}](docs/{l})" for n, l in alam[1:])
                read.append(f"- [{nimi}](docs/{alam[0][1]})" + (f" - {lingid}" if lingid else ""))
        elif tase == 0:
            read.append(f"- [{nimi}](docs/{leht})")
        elif tase == 1:
            read.append(f"- [{nimi}](docs/{leht})")
    tekst = "\n".join(read).strip() + "\n"
    tee = os.path.join(JUUR, "README.md")
    with open(tee, encoding="utf-8") as f:
        readme = f.read()
    uus = re.sub(r"<!-- sisukord -->.*?<!-- /sisukord -->",
                 "<!-- sisukord -->\n" + tekst + "<!-- /sisukord -->", readme, flags=re.S)
    with open(tee, "w", encoding="utf-8") as f:
        f.write(uus)


if __name__ == "__main__":
    lehed, puu = menyy()
    navigatsioon(lehed)
    sisukord(puu)
    print(f"Navigatsioon: {len(lehed) - 1} lehte; README sisukord uuendatud.")
