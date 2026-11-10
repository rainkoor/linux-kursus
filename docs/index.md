# Linuxi ja BSD kursus - nullist süsteemihalduseni

<p align="center">
  <img src="pildid/logod/tux.svg" alt="Tux, Linuxi pingviin" title="Tux - Linuxi maskott (Larry Ewing)" height="110">
  &nbsp;&nbsp;
  <img src="pildid/logod/bsd-daemon.svg" alt="BSD deemon" title="BSD deemon ehk Beastie - BSD maskott (Marshall Kirk McKusick)" height="110">
</p>

Eestikeelne avatud õppematerjal Linuxi (ja BSD) õppimiseks: esimesest käsust kuni teenuste paigaldamise, skriptimise ja süsteemi sisemise toimimise mõistmiseni.

Materjal on loodud Haapsalu Kutsehariduskeskuse (HKHK) IT-õppe tarbeks, kuid on kirjutatud nii, et sobib ka iseseisvaks õppimiseks.

## Kellele see kursus on mõeldud?

- **Kutseõppe IT-õppijatele**, kes alustavad Linuxiga nullist.
- **Iseõppijatele**, kes soovivad süsteemset eestikeelset materjali.
- **Õpetajatele**, kes otsivad valmis kava, laboritöid ja enesekontrolli küsimusi.

**Eeldused:** arvuti tavakasutaja oskused. Varasemat Linuxi kogemust ei ole vaja.

### Kellele milline osa sobib?

| Osa | Kellele | Mida õppija pärast oskab |
|---|---|---|
| **Põhiosa**<br>moodulid 1–9, ~84 h | Kõigile IT-õppijatele, kes alustavad Linuxiga nullist: kutseõppe esimese kursuse õppijad, iseõppijad, aga ka tugispetsialistid, võrguhaldurid ja arendajad, kes vajavad töös käsurida. Eeldab ainult arvuti tavakasutaja oskusi. | Kasutab käsurida enesekindlalt ja haldab iseseisvalt üht Linuxi serverit: kasutajad ja õigused, paketid, teenused, lihtsad skriptid, võrk, SSH, kettad ning varundus ja taastamine. Teemad katavad suures osas algtaseme sertifikaadi LPI Linux Essentials nõuded. |
| **Süvendusosa**<br>moodulid 10–20, ~98 h + lõpuprojekt | Süsteemihalduse eriala õppijatele (nt IT-süsteemide nooremspetsialist) ja iseõppijatele, kes tahavad töötada Linuxi administraatorina. Eeldab põhiosa läbimist või samaväärset kogemust. | Paigaldab, turvab ja hooldab tüüpilisi serveriteenuseid (veeb, andmebaasid, DNS, failiserver), seadistab keerukamaid võrke (IPv6, VLAN, VPN), lahendab alglaadimise ja jõudluse probleeme ning tunneb automatiseerimise ja seire põhimõtteid. Teemad ja tase on lähedased tuntud Linuxi sertifikaatide nõuetele: Red Hat RHCSA, Linux Foundation LFCS, CompTIA Linux+ ja LPI LPIC-1. Eksamiks valmistudes võrdle kursust sertifikaadi ametliku teemade loendiga. |
| **Valikmoodulid**<br>moodulid 21–29 | Edasijõudnutele ja huvilistele, kes on süvendusosa (või selle vajalikud moodulid) läbinud ja tahavad mõnda valdkonda lähemalt tundma õppida. Õpetaja saab valida moodulid rühma vajaduste järgi; kiiremad õppijad saavad neid teha iseseisvalt. | Sõltub moodulist: tulemüür, võrgust paigaldus, e-posti server, kataloogiteenused ja domeen, töölaua Linux, virtualiseerimine, Kubernetes või FreeBSD. Osa mooduleid (nt Kubernetes) on sissejuhatavad: teema põhjalikum käsitlus on HKHK õppijal teistes erialaainetes. |

Iga mooduli alguses on kirjas tema **eeldused**, nii et valikmooduleid ei pea tegema järjest.

## Ülesehitus

Kursus koosneb **20 moodulist** (põhiosa 1–9 ja süvendusosa 10–20), kahest proovieksamist ([põhiosa](proovieksam-pohiosa.md) ja [süvendusosa](proovieksam.md)), [lõpuprojektist](lopuprojekt.md) ning **9 valikmoodulist** (21–29: OPNsense, DHCP/PXE/iSCSI, e-posti server, OpenLDAP, Samba AD, töölaua Linux ja WSL, virtualiseerimine, Kubernetes, FreeBSD server). Iga moodul sisaldab kolme osa:

| Fail | Sisu |
|---|---|
| `index.md` | Teooria koos näidetega |
| `labor.md` | Praktiline laboritöö kindlal distributsioonil |
| `enesekontroll.md` | Küsimused ja praktilised miniülesanded, vastused avatavates plokkides |

Vaata [kursuse täielikku kava](kava.md), mõistete [eesti-inglise sõnastikku](lisad/sonastik.md) ja [käskude loendit](lisad/kasud.md). Laborikeskkonna (Proxmoxi virtuaalmasinate, võrguplaani ja distrode paigalduse) kirjeldus on lisas [Laborikeskkond ja paigaldus](lisad/paigaldus.md).

## Moodulid

### Põhiosa: Linuxi kasutamine ja haldus

<div class="grid cards" markdown>

-   :material-console:{ .lg .middle } **1. Linux ja käsurida**

    ---

    Mis on Linux, esimesed käsud, failisüsteemis liikumine ja abi leidmine.

    *8 h · Debian*

    [:octicons-arrow-right-24: Teooria](moodul-01-sissejuhatus/index.md) · [Labor](moodul-01-sissejuhatus/labor.md) · [Enesekontroll](moodul-01-sissejuhatus/enesekontroll.md)

-   :material-text-box-search-outline:{ .lg .middle } **2. Failid, tekst ja torud**

    ---

    Redaktorid, ümbersuunamine, `grep`, `awk`, `sed`, `find` ja arhiivid.

    *10 h · Debian*

    [:octicons-arrow-right-24: Teooria](moodul-02-failid-tekst-torud/index.md) · [Labor](moodul-02-failid-tekst-torud/labor.md) · [Enesekontroll](moodul-02-failid-tekst-torud/enesekontroll.md)

-   :material-account-lock:{ .lg .middle } **3. Kasutajad, grupid ja õigused**

    ---

    Kasutajad, `sudo`, failiõigused, SGID, ACL ja paroolipoliitika.

    *8 h · Ubuntu*

    [:octicons-arrow-right-24: Teooria](moodul-03-kasutajad-oigused/index.md) · [Labor](moodul-03-kasutajad-oigused/labor.md) · [Enesekontroll](moodul-03-kasutajad-oigused/enesekontroll.md)

-   :material-package-variant-closed:{ .lg .middle } **4. Tarkvara ja pakihaldus**

    ---

    `apt` ja `dnf`, hoidlad, uuendused, Snap ja Flatpak.

    *8 h · Debian, Ubuntu, AlmaLinux*

    [:octicons-arrow-right-24: Teooria](moodul-04-pakihaldus/index.md) · [Labor](moodul-04-pakihaldus/labor.md) · [Enesekontroll](moodul-04-pakihaldus/enesekontroll.md)

-   :material-cog-play:{ .lg .middle } **5. Protsessid, teenused ja systemd**

    ---

    Protsessid, systemd teenused, logid, ajastamine ja ressursipiirangud.

    *8 h · AlmaLinux*

    [:octicons-arrow-right-24: Teooria](moodul-05-protsessid-teenused/index.md) · [Labor](moodul-05-protsessid-teenused/labor.md) · [Enesekontroll](moodul-05-protsessid-teenused/enesekontroll.md)

-   :material-script-text-outline:{ .lg .middle } **6. Bashi skriptimine ja Git**

    ---

    Muutujad, tingimused, tsüklid, funktsioonid, ShellCheck ja Git.

    *16 h · Debian*

    [:octicons-arrow-right-24: Teooria](moodul-06-bash/index.md) · [Labor](moodul-06-bash/labor.md) · [Enesekontroll](moodul-06-bash/enesekontroll.md)

-   :material-lan-connect:{ .lg .middle } **7. Võrk ja SSH**

    ---

    IP ja DNS, SSH-võtmed, failide kopeerimine, tulemüür ja NTP.

    *10 h · Ubuntu*

    [:octicons-arrow-right-24: Teooria](moodul-07-vork-ssh/index.md) · [Labor](moodul-07-vork-ssh/labor.md) · [Enesekontroll](moodul-07-vork-ssh/enesekontroll.md)

-   :material-harddisk:{ .lg .middle } **8. Kettad, failisüsteemid ja LVM**

    ---

    Partitsioonid, failisüsteemid, fstab, LVM ja LUKS.

    *8 h · AlmaLinux*

    [:octicons-arrow-right-24: Teooria](moodul-08-kettad-lvm/index.md) · [Labor](moodul-08-kettad-lvm/labor.md) · [Enesekontroll](moodul-08-kettad-lvm/enesekontroll.md)

-   :material-backup-restore:{ .lg .middle } **9. Varundus ja taastamine**

    ---

    3-2-1, tar, rsync, restic, varundusskript ja taimer, taastamistest.

    *8 h · Debian, Ubuntu*

    [:octicons-arrow-right-24: Teooria](moodul-09-varundus/index.md) · [Labor](moodul-09-varundus/labor.md) · [Enesekontroll](moodul-09-varundus/enesekontroll.md)

</div>

### Süvendusosa: serverid ja automatiseerimine

<div class="grid cards" markdown>

-   :material-database:{ .lg .middle } **10. Salvestus: RAID, ZFS, jõudlus ja taastamine**

    ---

    Tarkvaraline RAID, ZFS, ketaste jõudlus ja andmete taastamine.

    *8 h · AlmaLinux, Ubuntu*

    [:octicons-arrow-right-24: Teooria](moodul-10-salvestus/index.md) · [Labor](moodul-10-salvestus/labor.md) · [Enesekontroll](moodul-10-salvestus/enesekontroll.md)

-   :material-chip:{ .lg .middle } **11. Kuidas Linux töötab: alglaadimine ja kernel**

    ---

    UEFI, GRUB, initramfs, kernel, systemd süvitsi ja süsteemi päästmine.

    *12 h · Debian*

    [:octicons-arrow-right-24: Teooria](moodul-11-alglaadimine-kernel/index.md) · [Labor](moodul-11-alglaadimine-kernel/labor.md) · [Enesekontroll](moodul-11-alglaadimine-kernel/enesekontroll.md)

-   :material-shield-lock:{ .lg .middle } **12. Turvalisus ja logid**

    ---

    Karastamine, SELinux, AppArmor, fail2ban, auditd, Lynis ja Wazuh.

    *10 h · AlmaLinux, Ubuntu*

    [:octicons-arrow-right-24: Teooria](moodul-12-turvalisus-logid/index.md) · [Labor](moodul-12-turvalisus-logid/labor.md) · [Enesekontroll](moodul-12-turvalisus-logid/enesekontroll.md)

-   :material-router-network:{ .lg .middle } **13. Võrgu süvendus**

    ---

    IPv6, sild, VLAN, bond, NAT, WireGuard VPN ja tcpdump.

    *8 h · Ubuntu, AlmaLinux, Debian*

    [:octicons-arrow-right-24: Teooria](moodul-13-vorgu-suvendus/index.md) · [Labor](moodul-13-vorgu-suvendus/labor.md) · [Enesekontroll](moodul-13-vorgu-suvendus/enesekontroll.md)

-   :material-docker:{ .lg .middle } **14. Konteinerid**

    ---

    Podman ja Docker, oma pilt, Compose ja Quadlet.

    *8 h · AlmaLinux*

    [:octicons-arrow-right-24: Teooria](moodul-14-konteinerid/index.md) · [Labor](moodul-14-konteinerid/labor.md) · [Enesekontroll](moodul-14-konteinerid/enesekontroll.md)

-   :material-web:{ .lg .middle } **15. Veebiserverid**

    ---

    nginx, Apache, Caddy, TLS, pöördpuhver, HAProxy ja keepalived.

    *10 h · Debian, AlmaLinux, Ubuntu*

    [:octicons-arrow-right-24: Teooria](moodul-15-veebiserverid/index.md) · [Labor](moodul-15-veebiserverid/labor.md) · [Enesekontroll](moodul-15-veebiserverid/enesekontroll.md)

-   :material-database:{ .lg .middle } **16. Andmebaasid**

    ---

    MariaDB, PostgreSQL, SQLite, Valkey, varundus ja replikatsioon.

    *8 h · Debian, AlmaLinux*

    [:octicons-arrow-right-24: Teooria](moodul-16-andmebaasid/index.md) · [Labor](moodul-16-andmebaasid/labor.md) · [Enesekontroll](moodul-16-andmebaasid/enesekontroll.md)

-   :material-dns:{ .lg .middle } **17. DNS ja nimelahendus**

    ---

    Nimelahendus Linuxis, BIND9 primaar ja sekundaar, pöördtsoon, CoreDNS, Pi-hole, tõrkeotsing.

    *8 h · Debian, Ubuntu*

    [:octicons-arrow-right-24: Teooria](moodul-17-dns/index.md) · [Labor](moodul-17-dns/labor.md) · [Enesekontroll](moodul-17-dns/enesekontroll.md)

-   :material-folder-network:{ .lg .middle } **18. Failiserverid**

    ---

    NFS, autofs, Samba, ühiskaustade õigused, TrueNAS, varundus ja dokumenteerimine.

    *8 h · Debian, Ubuntu, Windows*

    [:octicons-arrow-right-24: Teooria](moodul-18-failiserverid/index.md) · [Labor](moodul-18-failiserverid/labor.md) · [Enesekontroll](moodul-18-failiserverid/enesekontroll.md)

-   :material-robot-industrial:{ .lg .middle } **19. Automatiseerimine**

    ---

    Ansible, rollid ja testimine, Vagrant, cloud-init ja OpenTofu.

    *10 h · AlmaLinux, Debian, Ubuntu*

    [:octicons-arrow-right-24: Teooria](moodul-19-automatiseerimine/index.md) · [Labor](moodul-19-automatiseerimine/labor.md) · [Enesekontroll](moodul-19-automatiseerimine/enesekontroll.md)

-   :material-chart-line:{ .lg .middle } **20. Seire ja jõudlus**

    ---

    Jõudluse analüüs, Prometheus, Grafana ja Uptime Kuma.

    *8 h · Debian, Ubuntu*

    [:octicons-arrow-right-24: Teooria](moodul-20-seire/index.md) · [Labor](moodul-20-seire/labor.md) · [Enesekontroll](moodul-20-seire/enesekontroll.md)

</div>

### Proovieksamid ja lõpuprojekt

<div class="grid cards" markdown>

-   :material-clipboard-check-outline:{ .lg .middle } **Proovieksamid**

    ---

    Praktilised eksamid automaatse kontrolliga: [põhiosa](proovieksam-pohiosa.md) (Debian, 2 h) ja [süvendusosa](proovieksam.md) (AlmaLinux, 4 h).

    [:octicons-arrow-right-24: Ava](proovieksam-pohiosa.md)

-   :material-flag-checkered:{ .lg .middle } **Lõpuprojekt**

    ---

    Terviklik lahendus kolmel tasemel: algtase, edasijõudnud ja meister.

    [:octicons-arrow-right-24: Ava](lopuprojekt.md)

</div>

### Valikmoodulid

<div class="grid cards" markdown>

-   :material-wall-fire:{ .lg .middle } **21. OPNsense tulemüür**

    ---

    Isoleeritud laborivõrk, tulemüür, NAT, DHCP ja DNS.

    *8 h · OPNsense (FreeBSD)*

    [:octicons-arrow-right-24: Teooria](moodul-21-opnsense/index.md) · [Labor](moodul-21-opnsense/labor.md) · [Enesekontroll](moodul-21-opnsense/enesekontroll.md)

-   :material-ip-network:{ .lg .middle } **22. DHCP, PXE ja iSCSI**

    ---

    Kea DHCP, võrgust alglaadimine, automaatne paigaldus ja iSCSI.

    *10 h · Debian*

    [:octicons-arrow-right-24: Teooria](moodul-22-dhcp-pxe-iscsi/index.md) · [Labor](moodul-22-dhcp-pxe-iscsi/labor.md) · [Enesekontroll](moodul-22-dhcp-pxe-iscsi/enesekontroll.md)

-   :material-email-outline:{ .lg .middle } **23. E-posti server**

    ---

    Postfix, Dovecot, MX, SPF, DKIM ja DMARC, rämpsposti tõrje.

    *10 h · Ubuntu, Debian*

    [:octicons-arrow-right-24: Teooria](moodul-23-e-post/index.md) · [Labor](moodul-23-e-post/labor.md) · [Enesekontroll](moodul-23-e-post/enesekontroll.md)

-   :material-card-account-details:{ .lg .middle } **24. OpenLDAP**

    ---

    Keskne kasutajahaldus, LDIF, TLS, SSSD ja LAM.

    *8 h · Debian, Ubuntu*

    [:octicons-arrow-right-24: Teooria](moodul-24-openldap/index.md) · [Labor](moodul-24-openldap/labor.md) · [Enesekontroll](moodul-24-openldap/enesekontroll.md)

-   :material-domain:{ .lg .middle } **25. Samba AD**

    ---

    Active Directory domeen Linuxil, Windowsi ja Linuxi kliendid.

    *10 h · Debian, Windows*

    [:octicons-arrow-right-24: Teooria](moodul-25-samba-ad/index.md) · [Labor](moodul-25-samba-ad/labor.md) · [Enesekontroll](moodul-25-samba-ad/enesekontroll.md)

-   :material-monitor:{ .lg .middle } **26. Töölaua Linux ja WSL**

    ---

    Töölaud, tarkvara, ID-kaart, Kali Linux ja WSL.

    *8 h · Ubuntu, Kali, Windows*

    [:octicons-arrow-right-24: Teooria](moodul-26-toolaud-wsl/index.md) · [Labor](moodul-26-toolaud-wsl/labor.md) · [Enesekontroll](moodul-26-toolaud-wsl/enesekontroll.md)

-   :material-server-network:{ .lg .middle } **27. Virtualiseerimine**

    ---

    KVM, Proxmox VE, Proxmox Backup Server ja XCP-ng.

    *12 h · Debian, Proxmox VE, XCP-ng*

    [:octicons-arrow-right-24: Teooria](moodul-27-virtualiseerimine/index.md) · [Labor](moodul-27-virtualiseerimine/labor.md) · [Enesekontroll](moodul-27-virtualiseerimine/enesekontroll.md)

-   :simple-kubernetes:{ .lg .middle } **28. Kubernetes: k3s**

    ---

    k3s klaster, Deployment, Ingress, Helm ja hooldus.

    *10 h · Debian*

    [:octicons-arrow-right-24: Teooria](moodul-28-kubernetes/index.md) · [Labor](moodul-28-kubernetes/labor.md) · [Enesekontroll](moodul-28-kubernetes/enesekontroll.md)

-   :simple-freebsd:{ .lg .middle } **29. FreeBSD server**

    ---

    pkg, rc.conf, ZFS-i alglaadimiskeskkonnad, pf ja jailid.

    *10 h · FreeBSD*

    [:octicons-arrow-right-24: Teooria](moodul-29-freebsd/index.md) · [Labor](moodul-29-freebsd/labor.md) · [Enesekontroll](moodul-29-freebsd/enesekontroll.md)

</div>

## Distributsioonid

Kursusel kasutatakse kolme distributsiooni (distrot). **Need on Haapsalu Kutsehariduskeskuse Proxmoxi labori põhilised distrod ja kogu materjal on üles ehitatud nende kolme põhjal.**

| | Distro | Miks just see? | Koduleht |
|:---:|---|---|---|
| <a href="https://www.debian.org/"><img src="pildid/logod/debian.svg" alt="Debian" title="Debian - Debian Open Use Logo" height="56"></a> | **Debian** | Stabiilne, levinud serverites, paljude distrode alus | [debian.org](https://www.debian.org/) |
| <a href="https://ubuntu.com/"><img src="pildid/logod/ubuntu.svg" alt="Ubuntu" title="Ubuntu - Canonical Ltd. kaubamärk" height="56"></a> | **Ubuntu** | Kõige levinum pilves ja töölaual | [ubuntu.com](https://ubuntu.com/) |
| <a href="https://almalinux.org/"><img src="pildid/logod/almalinux.svg" alt="AlmaLinux" title="AlmaLinux - AlmaLinux OS Foundationi kaubamärk" height="56"></a> | **AlmaLinux** | Tasuta RHEL-iga ühilduv distro, ettevõtete standard | [almalinux.org](https://almalinux.org/) |

Need kolm katavad suurema osa reaalsetest Linuxi serveritest. Teiste distrode ülevaate leiad [distrode ülevaatest](lisad/distrod.md). **Iga laboritöö on kirjutatud ühe kindla distro jaoks** (see on märgitud laboritöö alguses). Teoorias on erinevused välja toodud lõikudes **„Distrode erinevused“**.

## Kuidas materjali kasutada?

**Õppijana:** loe moodulid järjest läbi, tee iga mooduli laboritöö ja kontrolli end enesekontrolli küsimustega. Ära ainult loe - kirjuta iga käsk ise läbi ja katseta. Põhi- ja süvendusosa moodulites algab iga teema kastiga **Lühidalt**, kus on kõige tähtsam paari lausega. Pikemad taustaselgitused on peidetud plokkidesse **Loe lähemalt** - ava need, kui tahad teemast rohkem teada või kui laboritöös midagi ei õnnestu.

**Õpetajana:** kava sisaldab soovituslikku mahtu tundides ja iga mooduli õpiväljundeid. Laboritööd on mõeldud tegemiseks virtuaalmasinas (nt Proxmox VE, VirtualBox), kus õppija võib julgelt asju katki teha. Laboritööde kontrollvastused ja proovieksamite näidislahendused ei ole avalikud - need on eraldi õpetaja materjalides (küsi autorilt).

**Iseõppijana:** sobib iga virtualiseerimiskeskkond (VirtualBox, VMware, Hyper-V, UTM) või pilveserver. Iga laboritöö alguses on kirjas, millist masinat on vaja.

## Teiste formaatide genereerimine

Materjal on kirjutatud tavalises Markdownis, et sellest oleks lihtne teha muid formaate:

| Formaat | Kuidas |
|---|---|
| **Veebileht** | `pip install mkdocs-material`, seejärel `mkdocs serve` (eelvaade) või `mkdocs build` (staatiline leht kataloogi `site/`). Seadistus on failis `mkdocs.yml`. |
| **Word / PDF** | `pandoc docs/moodul-01-sissejuhatus/index.md -o moodul-01.docx` (PDF jaoks on vaja ka LaTeX-i, nt `-o moodul-01.pdf --pdf-engine=xelatex`) |
| **Slaidid** | Mooduli teooriast saab teha slaidid nt Marpi või Reveal.js abil või lasta tehisintellektil need Markdownist genereerida. |
| **Moodle** | MkDocsi väljundi HTML-i või pandoci abil loodud faile saab Moodle'isse üles laadida. |

Materjal kasutab peaaegu ainult tavalist Markdowni. Erandid on kaks GitHubi toetatud laiendust: **joonised** (Mermaid-koodiplokk, keeleks `mermaid`) ja **märkusekastid** (`> [!NOTE]`, `> [!TIP]`, `> [!WARNING]`). Need näevad korralikud välja nii GitHubis kui ka veebilehel; teistes vormingutes (pandoc) jäävad need tavaliseks koodiplokiks ja tsitaadiks. Avalehe moodulikaardid on ainult veebilehel.

## Litsents

© 2026 Rain Koor, Haapsalu Kutsehariduskeskus.

Materjal on avaldatud litsentsi [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.et) all: võid seda vabalt kasutada, muuta ja jagada, kui viitad autorile ja jagad muudetud versiooni sama litsentsi all. Vt faili LICENSE.

### Logod ja maskotid

Logod ja maskotid **ei kuulu** CC BY-SA litsentsi alla - need kuuluvad oma omanikele ja on siin kasutatud ainult viitamiseks vastavatele projektidele:

- **Tux** - Larry Ewing (lewing@isc.tamu.edu), loodud programmiga The GIMP.
- **BSD deemon** - BSD Daemon Copyright 1988 by Marshall Kirk McKusick. All Rights Reserved.
- **Debian Open Use Logo** - Copyright (c) 1999 Software in the Public Interest, Inc., litsents LGPL 3+ või CC BY-SA 3.0.
- **Ubuntu** on Canonical Ltd. kaubamärk; **AlmaLinux** on AlmaLinux OS Foundationi kaubamärk. Kursus ei ole nende organisatsioonide poolt avaldatud ega heaks kiidetud.

## Panustamine

Leidsid vea või on ettepanek? Ava *issue* või tee *pull request*.
