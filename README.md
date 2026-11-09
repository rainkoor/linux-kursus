# Linuxi kursus - nullist süsteemihalduseni

Eestikeelne avatud õppematerjal Linuxi õppimiseks: esimesest käsust kuni teenuste paigaldamise, skriptimise ja süsteemi sisemise toimimise mõistmiseni.

Materjal on loodud Haapsalu Kutsehariduskeskuse (HKHK) IT-õppe tarbeks, kuid on kirjutatud nii, et sobib ka iseseisvaks õppimiseks.

## Kellele see kursus on mõeldud?

- **Kutseõppe IT-õppijatele**, kes alustavad Linuxiga nullist.
- **Iseõppijatele**, kes soovivad süsteemset eestikeelset materjali.
- **Õpetajatele**, kes otsivad valmis kava, laboritöid ja enesekontrolli küsimusi.

**Eeldused:** arvuti tavakasutaja oskused. Varasemat Linuxi kogemust ei ole vaja.

## Ülesehitus

Kursus koosneb **17 moodulist** (põhiosa 1–8 ja süvendusosa 9–17), [proovieksamist](docs/proovieksam.md), [lõpuprojektist](docs/lopuprojekt.md) ning **7 valikmoodulist** (18–24: OPNsense, DHCP/PXE/iSCSI, OpenLDAP, Samba AD, töölaua Linux ja WSL, virtualiseerimine, Kubernetes). Iga moodul sisaldab kolme osa:

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

**Õpetajana:** kava sisaldab soovituslikku mahtu tundides ja iga mooduli õpiväljundeid. Laboritööd on mõeldud tegemiseks virtuaalmasinas (nt Proxmox VE, VirtualBox), kus õppija võib julgelt asju katki teha.

**Iseõppijana:** sobib iga virtualiseerimiskeskkond (VirtualBox, VMware, Hyper-V, UTM) või pilveserver. Iga laboritöö alguses on kirjas, millist masinat on vaja.

## GitHubi panemine ja veebileht

1. Loo GitHubis uus tühi hoidla (ilma README, litsentsi ja `.gitignore`-ita - need on siin juba olemas).
2. Paki zip lahti ja saada sisu GitHubi:

    ```bash
    cd linux-kursus
    git init -b main
    git add .
    git commit -m "Linuxi kursus: esimene versioon"
    git remote add origin git@github.com:<kasutaja>/<hoidla>.git
    git push -u origin main
    ```

3. Veebilehe avaldamiseks on kaasas GitHub Actionsi töövoog `.github/workflows/veebileht.yml`: iga `main`-harusse tehtud muudatus ehitab MkDocsiga lehe ja avaldab selle harus `gh-pages`. Pärast esimest töövoo käivitust vali hoidla seadetes *Settings* → *Pages* → *Source*: *Deploy from a branch*, haru `gh-pages`, kaust `/ (root)`. Leht on aadressil `https://<kasutaja>.github.io/<hoidla>/`.

Kohalikuks eelvaateks: `pip install -r requirements.txt` ja `mkdocs serve`.

## Teiste formaatide genereerimine

Materjal on kirjutatud tavalises Markdownis, et sellest oleks lihtne teha muid formaate:

| Formaat | Kuidas |
|---|---|
| **Veebileht** | `pip install mkdocs-material`, seejärel `mkdocs serve` (eelvaade) või `mkdocs build` (staatiline leht kataloogi `site/`). Seadistus on failis `mkdocs.yml`. |
| **Word / PDF** | `pandoc docs/moodul-01-sissejuhatus/index.md -o moodul-01.docx` (PDF jaoks on vaja ka LaTeX-i, nt `-o moodul-01.pdf --pdf-engine=xelatex`) |
| **Slaidid** | Mooduli teooriast saab teha slaidid nt Marpi või Reveal.js abil või lasta tehisintellektil need Markdownist genereerida. |
| **Moodle** | MkDocsi väljundi HTML-i või pandoci abil loodud faile saab Moodle'isse üles laadida. |

Et konverteerimine töötaks igal pool, kasutatakse ainult tavalist Markdowni (pealkirjad, tabelid, koodiplokid, tsitaadiplokid). Eriomaseid laiendusi ei kasutata.

## Seis

| Osa | Seis |
|---|---|
| Kursuse kava | ✅ Valmis |
| Moodul 1 - Linux ja käsurida | ✅ Valmis |
| Moodul 2 - Failid, tekst ja torud | ✅ Valmis |
| Moodul 3 - Kasutajad, grupid ja õigused | ✅ Valmis |
| Moodul 4 - Tarkvara ja pakihaldus | ✅ Valmis |
| Moodul 5 - Protsessid, teenused ja systemd | ✅ Valmis |
| Moodul 6 - Bashi skriptimine ja Git | ✅ Valmis |
| Moodul 7 - Võrk ja SSH | ✅ Valmis |
| Moodul 8 - Kettad, failisüsteemid ja LVM | ✅ Valmis |
| Moodul 9 - Salvestus: RAID, ZFS, jõudlus ja taastamine | ✅ Valmis |
| Moodul 10 - Kuidas Linux töötab: alglaadimine ja kernel | ✅ Valmis |
| Moodul 11 - Turvalisus ja logid | ✅ Valmis |
| Moodul 12 - Konteinerid | ✅ Valmis |
| Moodul 13 - Veebiserverid | ✅ Valmis |
| Moodul 14 - Andmebaasid | ✅ Valmis |
| Moodul 15 - Võrguteenused: DNS, failijagamine, e-post ja varundus | ✅ Valmis |
| Moodul 16 - Automatiseerimine: Ansible, Vagrant ja infrastruktuur koodina | ✅ Valmis |
| Moodul 17 - Seire ja jõudlus | ✅ Valmis |
| Valikmoodul 18 - BSD praktikas: OPNsense tulemüür | ✅ Valmis |
| Valikmoodul 19 - Võrgu infrastruktuur: DHCP, PXE ja iSCSI | ✅ Valmis |
| Valikmoodul 20 - Kataloogiteenused: OpenLDAP | ✅ Valmis |
| Valikmoodul 21 - Active Directory Linuxis: Samba AD DC | ✅ Valmis |
| Valikmoodul 22 - Linux töölaual ja WSL | ✅ Valmis |
| Valikmoodul 23 - Virtualiseerimine: KVM, Proxmox VE ja XCP-ng | ✅ Valmis |
| Valikmoodul 24 - Kubernetes: k3s | ✅ Valmis |
| Proovieksam koos kontrollskriptiga | ✅ Valmis |
| Lõpuprojekt (algtase, edasijõudnud, meister) | ✅ Valmis |
| Distrode ja BSD ülevaade (lisa) | ✅ Valmis |
| UNIX-i ja Linuxi ajalugu (lisa) | ✅ Valmis |
| Sõnastik (lisa) | ✅ Valmis |
| Käskude loend (lisa) | ✅ Valmis |
| Laborikeskkond ja paigaldus (lisa) | ✅ Valmis |

## Litsents

© 2026 Rain Koor, Haapsalu Kutsehariduskeskus.

Materjal on avaldatud litsentsi [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.et) all: võid seda vabalt kasutada, muuta ja jagada, kui viitad autorile ja jagad muudetud versiooni sama litsentsi all. Vt faili [LICENSE](LICENSE).

## Panustamine

Leidsid vea või on ettepanek? Ava *issue* või tee *pull request*.
