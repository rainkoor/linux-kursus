"""MkDocsi hook: eemaldab GitHubi navigatsiooniread ja teisendab GitHubi stiilis märkused (> [!NOTE] jt) Materiali kastideks.

Lisaks:
- märkus sildiga **Lühidalt:** saab eraldi kastitüübi (abstract);
- plokk <details><summary>…</summary> … </details> saab Materiali avatavaks kastiks
  (enesekontrolli "Vastus" ja "Lahendus" rohelise kastina);
- laboritöödes, kus on aruande küsimuste loend (<!-- kysimused -->, tools/kysimused.py),
  saavad lõigud > **Aruanne:** ja > **K1.** jt (GitHubis tsitaadiplokid) eraldi värvi kasti "kysimus" (docs/stylesheets/kursus.css).

Lähtetekstis kasutatakse GitHubi süntaksit, mis näeb värviliste kastidena välja ka
GitHubis. Veebilehe ehitamisel teeb see hook neist Materiali admonition-kastid
eestikeelse pealkirjaga. Kui märkuse esimene rida algab rasvases kirjas sildiga, mis
lõpeb kooloniga (nt **Õpetajale:**), saab sellest kasti pealkiri.
"""
import re

TYYBID = {
    "NOTE": ("note", "Märkus"),
    "TIP": ("tip", "Näpunäide"),
    "IMPORTANT": ("info", "Oluline"),
    "WARNING": ("warning", "Hoiatus"),
    "CAUTION": ("danger", "Ettevaatust"),
}
ALGUS = re.compile(r"^> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$")
SILT = re.compile(r"^\*\*([^*]+?):\*\*\s*(.*)$")


def on_page_markdown(markdown, **kwargs):
    # GitHubi navigatsioonirida (tools/navigatsioon.py) - veebilehel näitab Material seda ise
    markdown = re.sub(r"\n*<!-- navigatsioon -->.*?<!-- /navigatsioon -->\n?", "\n", markdown, flags=re.S)
    read = markdown.split("\n")
    valja = []
    koodis = False
    i = 0
    while i < len(read):
        rida = read[i]
        if rida.lstrip().startswith("```"):
            koodis = not koodis
        m = None if koodis else ALGUS.match(rida)
        if not m:
            valja.append(rida)
            i += 1
            continue
        i += 1
        sisu = []
        while i < len(read) and read[i].startswith(">"):
            sisu.append(re.sub(r"^> ?", "", read[i]))
            i += 1
        liik, pealkiri = TYYBID[m.group(1)]
        if sisu:
            s = SILT.match(sisu[0])
            if s:
                pealkiri, jark = s.group(1), s.group(2)
                sisu[0] = jark[:1].upper() + jark[1:]
                if pealkiri == "Lühidalt":
                    liik = "abstract"
        if valja and valja[-1].strip():
            valja.append("")
        valja.append(f'!!! {liik} "{pealkiri.replace(chr(34), chr(39))}"')
        valja.append("")
        valja.extend(("    " + r) if r.strip() else "" for r in sisu)
        valja.append("")
    markdown = "\n".join(valja)
    markdown = avatavad(markdown)
    if "<!-- kysimused -->" in markdown:
        markdown = kysimused(markdown)
    return markdown


DETAILS = re.compile(r"^<details>\s*\n<summary>(.*?)</summary>\s*\n(.*?)\n</details>[ \t]*$", re.M | re.S)


def avatavad(markdown):
    """<details>-plokk (näeb välja avatavana ka GitHubis) -> Materiali avatav kast."""
    def asenda(m):
        pealkiri = m.group(1).strip().replace('"', "'")
        sisu = m.group(2).strip("\n").split("\n")
        keha = "\n".join(("    " + r) if r.strip() else "" for r in sisu)
        liik = "success" if pealkiri in ("Vastus", "Lahendus") else "note"
        return f'??? {liik} "{pealkiri}"\n\n{keha}\n'
    return DETAILS.sub(asenda, markdown)


KYSIMUS = re.compile(r"^(?:> )?\*\*([A-Z]\d+)\.\*\*\s*(.*)$")
ARUANNE = re.compile(r"^(?:> )?\*\*(Aruanne|Esitamine):\*\*\s*(.*)$")


def kysimused(markdown):
    """Laboritöö küsimuste ja aruande lõigud eristuva värviga kastideks."""
    read = markdown.split("\n")
    valja = []
    koodis = False
    i = 0
    while i < len(read):
        rida = read[i]
        if rida.lstrip().startswith("```"):
            koodis = not koodis
        m = None if koodis else (KYSIMUS.match(rida) or ARUANNE.match(rida))
        if not m:
            valja.append(rida)
            i += 1
            continue
        if m.re is KYSIMUS:
            pealkiri, sisu = f"Küsimus {m.group(1)}", [m.group(2)]
        else:
            pealkiri, sisu = m.group(1), [m.group(2)]
        i += 1
        while i < len(read) and read[i].strip():
            sisu.append(read[i][2:] if read[i].startswith("> ") else read[i])
            i += 1
        sisu[0] = sisu[0][:1].upper() + sisu[0][1:]
        valja.append(f'!!! kysimus "{pealkiri}"')
        valja.append("")
        valja.extend("    " + r for r in sisu)
        valja.append("")
    return "\n".join(valja)
