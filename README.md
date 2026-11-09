# Linuxi ja BSD kursus - nullist süsteemihalduseni

<p align="center">
  <img src="docs/pildid/logod/tux.svg" alt="Tux, Linuxi pingviin" height="110">
  &nbsp;&nbsp;
  <img src="docs/pildid/logod/bsd-daemon.svg" alt="BSD deemon" height="110">
</p>
<p align="center">
  <a href="https://www.debian.org/"><img src="docs/pildid/logod/debian.svg" alt="Debian" height="56"></a>
  &nbsp;&nbsp;&nbsp;
  <a href="https://ubuntu.com/"><img src="docs/pildid/logod/ubuntu.svg" alt="Ubuntu" height="56"></a>
  &nbsp;&nbsp;&nbsp;
  <a href="https://almalinux.org/"><img src="docs/pildid/logod/almalinux.svg" alt="AlmaLinux" height="56"></a>
</p>

Eestikeelne avatud õppematerjal Linuxi (ja BSD) õppimiseks: esimesest käsust kuni teenuste paigaldamise, skriptimise ja süsteemi sisemise toimimise mõistmiseni.

Materjal on loodud Haapsalu Kutsehariduskeskuse (HKHK) IT-õppe tarbeks, kuid on kirjutatud nii, et sobib ka iseseisvaks õppimiseks.

## Kellele see kursus on mõeldud?

- **Kutseõppe IT-õppijatele**, kes alustavad Linuxiga nullist.
- **Iseõppijatele**, kes soovivad süsteemset eestikeelset materjali.
- **Õpetajatele**, kes otsivad valmis kava, laboritöid ja enesekontrolli küsimusi.

**Eeldused:** arvuti tavakasutaja oskused. Varasemat Linuxi kogemust ei ole vaja.

## Ülesehitus

Kursus koosneb **17 moodulist** (põhiosa 1–8 ja süvendusosa 9–17), kahest proovieksamist ([põhiosa](docs/proovieksam-pohiosa.md) ja [süvendusosa](docs/proovieksam.md)), [lõpuprojektist](docs/lopuprojekt.md) ning **8 valikmoodulist** (18–25: OPNsense, DHCP/PXE/iSCSI, OpenLDAP, Samba AD, töölaua Linux ja WSL, virtualiseerimine, Kubernetes, FreeBSD server). Iga moodul sisaldab kolme osa:

| Fail | Sisu |
|---|---|
| `index.md` | Teooria koos näidetega |
| `labor.md` | Praktiline laboritöö kindlal distributsioonil |
| `enesekontroll.md` | Küsimused, praktilised miniülesanded ja vastused |

Kursuse täielik kava on failis [docs/kava.md](docs/kava.md). Mõistete eesti-inglise sõnastik on failis [docs/lisad/sonastik.md](docs/lisad/sonastik.md) ja käskude loend failis [docs/lisad/kasud.md](docs/lisad/kasud.md). Laborikeskkonna (Proxmoxi virtuaalmasinate, võrguplaani ja distrode paigalduse) kirjeldus on failis [docs/lisad/paigaldus.md](docs/lisad/paigaldus.md).

## Distributsioonid

Kursusel kasutatakse kolme distributsiooni (distrot). **Need on Haapsalu Kutsehariduskeskuse Proxmoxi labori põhilised distrod ja kogu materjal on üles ehitatud nende kolme põhjal.**

| Distro | Perekond | Pakihaldur | Miks | Koduleht |
|---|---|---|---|---|
| **Debian** | Debian | `apt` | Stabiilne, levinud serverites, paljude distrode alus | [debian.org](https://www.debian.org/) |
| **Ubuntu** | Debian | `apt` | Kõige levinum pilves ja töölaual | [ubuntu.com](https://ubuntu.com/) |
| **AlmaLinux** | Red Hat (RHEL) | `dnf` | Tasuta RHEL-iga ühilduv distro, ettevõtete standard | [almalinux.org](https://almalinux.org/) |

Need kolm katavad suurema osa reaalsetest Linuxi serveritest. Teiste distrode ülevaate leiad failist [docs/lisad/distrod.md](docs/lisad/distrod.md). **Iga laboritöö on kirjutatud ühe kindla distro jaoks** (see on märgitud laboritöö alguses). Teoorias on erinevused välja toodud lõikudes **„Distrode erinevused“**.

## Kuidas materjali kasutada?

**Õppijana:** loe moodulid järjest läbi, tee iga mooduli laboritöö ja kontrolli end enesekontrolli küsimustega. Ära ainult loe - kirjuta iga käsk ise läbi ja katseta.

**Õpetajana:** kava sisaldab soovituslikku mahtu tundides ja iga mooduli õpiväljundeid. Laboritööd on mõeldud tegemiseks virtuaalmasinas (nt Proxmox VE, VirtualBox), kus õppija võib julgelt asju katki teha. Laboritööde kontrollvastused ja proovieksamite näidislahendused ei ole avalikud - need on eraldi õpetaja materjalides (küsi autorilt).

**Iseõppijana:** sobib iga virtualiseerimiskeskkond (VirtualBox, VMware, Hyper-V, UTM) või pilveserver. Iga laboritöö alguses on kirjas, millist masinat on vaja.

## Veebileht

Materjalist ehitatakse automaatselt veebileht: iga muudatus harus `main` käivitab GitHub Actionsi töövoo (`.github/workflows/veebileht.yml`), mis ehitab lehe MkDocsiga ja avaldab selle harus `gh-pages` (GitHubi seadetes *Settings* → *Pages* → *Deploy from a branch*, haru `gh-pages`).

Kohalik eelvaade:

```bash
pip install -r requirements.txt
mkdocs serve            # http://127.0.0.1:8000
```

Oma koopia tegemiseks (nt teise kooli jaoks) tee hoidlast *fork* ja lülita selle seadetes sisse GitHub Pages.

## Teiste formaatide genereerimine

Materjal on kirjutatud tavalises Markdownis, et sellest oleks lihtne teha muid formaate:

| Formaat | Kuidas |
|---|---|
| **Veebileht** | `pip install mkdocs-material`, seejärel `mkdocs serve` (eelvaade) või `mkdocs build` (staatiline leht kataloogi `site/`). Seadistus on failis `mkdocs.yml`. |
| **Word / PDF** | `pandoc docs/moodul-01-sissejuhatus/index.md -o moodul-01.docx` (PDF jaoks on vaja ka LaTeX-i, nt `-o moodul-01.pdf --pdf-engine=xelatex`) |
| **Slaidid** | Mooduli teooriast saab teha slaidid nt Marpi või Reveal.js abil või lasta tehisintellektil need Markdownist genereerida. |
| **Moodle** | MkDocsi väljundi HTML-i või pandoci abil loodud faile saab Moodle'isse üles laadida. |

Materjal kasutab peaaegu ainult tavalist Markdowni. Erandid on kaks GitHubi toetatud laiendust: **joonised** (Mermaid-koodiplokk, keeleks `mermaid`) ja **märkusekastid** (`> [!NOTE]`, `> [!TIP]`, `> [!WARNING]`). Need näevad korralikud välja nii GitHubis kui ka veebilehel; teistes vormingutes (pandoc) jäävad need tavaliseks koodiplokiks ja tsitaadiks.

## Litsents

© 2026 Rain Koor, Haapsalu Kutsehariduskeskus.

Materjal on avaldatud litsentsi [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.et) all: võid seda vabalt kasutada, muuta ja jagada, kui viitad autorile ja jagad muudetud versiooni sama litsentsi all. Vt faili [LICENSE](LICENSE).

### Logod ja maskotid

Logod ja maskotid **ei kuulu** CC BY-SA litsentsi alla - need kuuluvad oma omanikele ja on siin kasutatud ainult viitamiseks vastavatele projektidele:

- **Tux** - Larry Ewing (lewing@isc.tamu.edu), loodud programmiga The GIMP.
- **BSD deemon** - BSD Daemon Copyright 1988 by Marshall Kirk McKusick. All Rights Reserved.
- **Debian Open Use Logo** - Copyright (c) 1999 Software in the Public Interest, Inc., litsents LGPL 3+ või CC BY-SA 3.0.
- **Ubuntu** on Canonical Ltd. kaubamärk; **AlmaLinux** on AlmaLinux OS Foundationi kaubamärk. Kursus ei ole nende organisatsioonide poolt avaldatud ega heaks kiidetud.

## Panustamine

Leidsid vea või on ettepanek? Ava *issue* või tee *pull request*.
