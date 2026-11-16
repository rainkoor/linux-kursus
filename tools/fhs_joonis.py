#!/usr/bin/env python3
"""Joonistab Linuxi failisüsteemi hierarhia (FHS) skeemi: docs/pildid/fhs.svg.

Juurkataloog on vasakul, esimese taseme kataloogid ühes joondatud tulbas
ja teise taseme kataloogid nende kõrval - igaühel lühike selgitus.
Sisu muutmiseks muuda allolevat loendit PUU ja käivita:

    python3 tools/fhs_joonis.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

# (kataloog, selgitus, [(alamkataloog, selgitus), ...])
PUU = [
    ("/bin, /sbin", "põhikäsud - viidad kataloogidele /usr/bin, /usr/sbin", []),
    ("/boot", "alglaadimiseks vajalikud failid", [
        ("vmlinuz-…", "kernel"),
        ("initrd.img-…", "ajutine algfailisüsteem draiveritega"),
        ("grub/", "alglaadija GRUB seadistus"),
    ]),
    ("/dev", "seadmefailid: kettad, terminalid, …", [
        ("sda, sda1, nvme0n1", "ketas ja selle partitsioon"),
        ("tty1, pts/0", "terminalid"),
        ("null", "„prügikast“: kõik siia kirjutatu kaob"),
    ]),
    ("/etc", "süsteemi ja teenuste seadistusfailid", [
        ("passwd, group", "kasutajad ja grupid"),
        ("fstab", "püsivalt haagitavad failisüsteemid"),
        ("ssh/", "SSH-serveri ja -kliendi seadistus"),
        ("systemd/", "teenuste ja süsteemi seadistus"),
    ]),
    ("/home", "tavakasutajate kodukataloogid", [
        ("mari/", "kasutaja mari failid ja isiklikud seaded"),
    ]),
    ("/lib", "teegid - viit kataloogile /usr/lib", []),
    ("/media, /mnt", "haagitud andmekandjad", [
        ("/media/mari/USB", "automaatselt haagitud USB-mälu (töölaual)"),
        ("/mnt/andmed", "käsitsi ajutiselt haagitud ketas"),
    ]),
    ("/opt", "kolmandate osapoolte lisatarkvara", [
        ("google/chrome/", "nt tootja paketiga paigaldatud programm"),
    ]),
    ("/proc, /sys", "virtuaalsed: kerneli, protsesside ja seadmete info", [
        ("/proc/1234/", "protsessi 1234 info"),
        ("/proc/cpuinfo", "protsessori info"),
        ("/sys/class/net/", "võrguliidesed"),
    ]),
    ("/root", "juurkasutaja kodukataloog", []),
    ("/run", "töötava süsteemi ajutised andmed (kaovad taaskäivitusel)", []),
    ("/srv", "serveriteenuste andmed", [
        ("www/", "nt veebilehe failid"),
    ]),
    ("/tmp", "ajutised failid kõigile kasutajatele", []),
    ("/usr", "paigaldatud programmid ja nende failid", [
        ("bin/", "käsud, mida kõik kasutavad (ls, cp, ssh)"),
        ("sbin/", "halduskäsud (useradd, fdisk)"),
        ("lib/", "teegid: programmide ühine kood (.so failid)"),
        ("share/", "andmed ja dokumentatsioon (man-lehed)"),
        ("local/", "käsitsi paigaldatud tarkvara"),
    ]),
    ("/var", "muutuvad andmed", [
        ("log/", "logifailid"),
        ("lib/", "programmide andmed (nt andmebaasid)"),
        ("cache/", "vahemälu (nt allalaaditud paketid)"),
        ("spool/", "järjekorrad (e-post, printimine, cron)"),
    ]),
]

RIDA = 34          # rea kõrgus
VAHE = 10          # vahe kataloogide rühmade vahel
X_TYVI = 110       # juurest tuleva püstjoone x
X1, L1 = 140, 470  # 1. taseme kastid
X_HARU = X1 + L1 + 25
X2, L2 = X_HARU + 25, 450  # 2. taseme kastid
LAIUS = X2 + L2 + 20
KAST_K = 26        # kasti kõrgus

V = {
    "taust": "#ffffff", "joon": "#7a7f9a",
    "juur_t": "#3f51b5", "juur_tekst": "#ffffff",
    "k1_t": "#e8eaf6", "k1_aar": "#3f51b5",
    "k2_t": "#f5f5f5", "k2_aar": "#9e9e9e",
    "nimi": "#1a237e", "selg": "#37474f",
}


def kast(x, y, laius, nimi, selgitus, taust, aar, rasvane=True):
    t = [f'<rect x="{x}" y="{y}" width="{laius}" height="{KAST_K}" rx="4" fill="{taust}" stroke="{aar}"/>']
    ty = y + KAST_K / 2 + 5
    kaal = ' font-weight="bold"' if rasvane else ""
    t.append(
        f'<text x="{x + 10}" y="{ty}" font-size="14">'
        f'<tspan fill="{V["nimi"]}" font-family="DejaVu Sans Mono, Consolas, monospace"{kaal}>{escape(nimi)}</tspan>'
        f'<tspan fill="{V["selg"]}" dx="10">{escape(selgitus)}</tspan></text>'
    )
    return t


def main():
    osad = []
    y = 20
    keskpunktid = []
    for nimi, selg, lapsed in PUU:
        ridu = max(1, len(lapsed))
        ryhma_k = ridu * RIDA
        y1 = y + (ryhma_k - RIDA) / 2  # 1. taseme kast rühma keskel
        k1y = y1 + (RIDA - KAST_K) / 2
        keskpunktid.append(k1y + KAST_K / 2)
        osad += kast(X1, k1y, L1, nimi, selg, V["k1_t"], V["k1_aar"])
        osad.append(f'<line x1="{X_TYVI}" y1="{k1y + KAST_K/2}" x2="{X1}" y2="{k1y + KAST_K/2}" stroke="{V["joon"]}" stroke-width="1.5"/>')
        if lapsed:
            lk = []
            for i, (ln, ls) in enumerate(lapsed):
                ly = y + i * RIDA + (RIDA - KAST_K) / 2
                lk.append(ly + KAST_K / 2)
                osad += kast(X2, ly, L2, ln, ls, V["k2_t"], V["k2_aar"], rasvane=False)
                osad.append(f'<line x1="{X_HARU}" y1="{ly + KAST_K/2}" x2="{X2}" y2="{ly + KAST_K/2}" stroke="{V["joon"]}" stroke-width="1.2"/>')
            osad.append(f'<line x1="{X1 + L1}" y1="{k1y + KAST_K/2}" x2="{X_HARU}" y2="{k1y + KAST_K/2}" stroke="{V["joon"]}" stroke-width="1.2"/>')
            osad.append(f'<line x1="{X_HARU}" y1="{min(lk + [k1y + KAST_K/2])}" x2="{X_HARU}" y2="{max(lk + [k1y + KAST_K/2])}" stroke="{V["joon"]}" stroke-width="1.2"/>')
        y += ryhma_k + VAHE
    korgus = y + 10
    # juur ja tüvi
    jy = (keskpunktid[0] + keskpunktid[-1]) / 2
    osad.append(f'<line x1="{X_TYVI}" y1="{keskpunktid[0]}" x2="{X_TYVI}" y2="{keskpunktid[-1]}" stroke="{V["joon"]}" stroke-width="1.5"/>')
    osad.append(f'<line x1="80" y1="{jy}" x2="{X_TYVI}" y2="{jy}" stroke="{V["joon"]}" stroke-width="1.5"/>')
    osad.append(f'<rect x="20" y="{jy - 22}" width="60" height="44" rx="6" fill="{V["juur_t"]}"/>')
    osad.append(f'<text x="50" y="{jy + 8}" font-size="24" font-weight="bold" fill="{V["juur_tekst"]}" text-anchor="middle" font-family="DejaVu Sans Mono, Consolas, monospace">/</text>')
    osad.append(f'<text x="50" y="{jy + 40}" font-size="12" fill="{V["selg"]}" text-anchor="middle">juur</text>')

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{LAIUS}" height="{korgus}" viewBox="0 0 {LAIUS} {korgus}" '
        f'font-family="Inter, Roboto, Segoe UI, DejaVu Sans, Arial, sans-serif" role="img">\n'
        f'<title>Linuxi failisüsteemi hierarhia (FHS)</title>\n'
        f'<rect width="100%" height="100%" fill="{V["taust"]}"/>\n'
        + "\n".join(osad) + "\n</svg>\n"
    )
    siht = Path(__file__).resolve().parent.parent / "docs" / "pildid" / "fhs.svg"
    siht.write_text(svg, encoding="utf-8")
    print(f"Kirjutatud: {siht} ({LAIUS}x{korgus})")


if __name__ == "__main__":
    main()
