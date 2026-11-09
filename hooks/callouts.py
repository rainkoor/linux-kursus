"""MkDocsi hook: teisendab GitHubi stiilis märkused (> [!NOTE] jt) Materiali kastideks.

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
        if valja and valja[-1].strip():
            valja.append("")
        valja.append(f'!!! {liik} "{pealkiri.replace(chr(34), chr(39))}"')
        valja.append("")
        valja.extend(("    " + r) if r.strip() else "" for r in sisu)
        valja.append("")
    return "\n".join(valja)
