<!-- navigatsioon -->
[Sisukord](../README.md#sisukord) · [Moodul 1. Linux ja käsurida →](moodul-01-sissejuhatus/index.md)
<!-- /navigatsioon -->

# Kursuse kava

## Eesmärk

Kursuse eesmärk on anda õppijale oskused Linuxi süsteemide igapäevaseks kasutamiseks ja haldamiseks: käsurea kindel valdamine, kasutajate, tarkvara, teenuste, võrgu ja salvestuse haldus, skriptimine ning arusaam sellest, kuidas Linux sisemiselt töötab.

Kursus algab nullist ja jõuab tasemeni, mis vastab ligikaudu algtaseme sertifikaatide (LPIC-1, CompTIA Linux+, Red Hat RHCSA) nõuetele.

## Õpiväljundid

Kursuse läbinud õppija:

1. kasutab Linuxi käsurida iseseisvalt ja leiab vajadusel abi süsteemi dokumentatsioonist;
2. haldab faile, kasutajaid, gruppe ja õigusi;
3. paigaldab ja uuendab tarkvara nii Debiani kui ka Red Hati perekonna distrodel;
4. haldab protsesse ja teenuseid ning analüüsib logisid;
5. kirjutab Bashi skripte korduvate ülesannete automatiseerimiseks;
6. seadistab võrguühendusi, SSH-d ja tulemüüri;
7. haldab kettaid, failisüsteeme ja LVM-i;
8. selgitab Linuxi alglaadimise ja kerneli toimimise põhimõtteid;
9. paigaldab, seadistab ja turvab levinud serveriteenuseid;
10. kasutab konteinereid, Giti ja automatiseerimisvahendeid ning kirjeldab infrastruktuuri koodina;
11. jälgib süsteemide jõudlust ja tervist ning seadistab seire;
12. planeerib varunduse ja taastamise ning dokumenteerib süsteemi nii, et keegi teine saab selle üle võtta.

## Maht ja ülesehitus

Kursus koosneb kolmest osast. Soovituslik kogumaht on **ca 182 kontakttundi** koos laboritöödega (põhiosa 76 h, süvendusosa 84 h, proovieksamid 2 + 4 h ja lõpuprojekt 16 h). Lisaks on **valikmoodulid (76 h)**, mida saab kasutada eraldi kursustena, süvendusena või lõpuprojekti ettevalmistuseks. Mahtu saab kohandada õppekava järgi.

### Põhiosa: Linuxi kasutamine ja haldus

| Nr | Moodul | Maht (h) | Laboritöö distro |
|---|---|---|---|
| 1 | [Linux ja käsurida](moodul-01-sissejuhatus/index.md) | 8 | Debian |
| 2 | [Failid, tekst ja torud](moodul-02-failid-tekst-torud/index.md) | 10 | Debian |
| 3 | [Kasutajad, grupid ja õigused](moodul-03-kasutajad-oigused/index.md) | 8 | Ubuntu |
| 4 | [Tarkvara ja pakihaldus](moodul-04-pakihaldus/index.md) | 6 | Debian, Ubuntu, AlmaLinux |
| 5 | [Protsessid, teenused ja systemd](moodul-05-protsessid-teenused/index.md) | 8 | AlmaLinux |
| 6 | [Bashi skriptimine ja Git](moodul-06-bash/index.md) | 16 | Debian |
| 7 | [Võrk ja SSH](moodul-07-vork-ssh/index.md) | 12 | Ubuntu |
| 8 | [Kettad, failisüsteemid ja LVM](moodul-08-kettad-lvm/index.md) | 8 | AlmaLinux |
| - | [Proovieksam: põhiosa](proovieksam-pohiosa.md) | 2 | Debian |

### Süvendusosa: serverid ja automatiseerimine

| Nr | Moodul | Maht (h) | Laboritöö distro |
|---|---|---|---|
| 9 | [Salvestus: RAID, ZFS, jõudlus ja taastamine](moodul-09-salvestus/index.md) | 8 | AlmaLinux, Ubuntu |
| 10 | [Kuidas Linux töötab: alglaadimine ja kernel](moodul-10-alglaadimine-kernel/index.md) | 12 | Debian |
| 11 | [Turvalisus ja logid](moodul-11-turvalisus-logid/index.md) | 10 | AlmaLinux, Ubuntu |
| 12 | [Konteinerid](moodul-12-konteinerid/index.md) | 8 | AlmaLinux |
| 13 | [Veebiserverid](moodul-13-veebiserverid/index.md) | 10 | Debian, AlmaLinux, Ubuntu |
| 14 | [Andmebaasid](moodul-14-andmebaasid/index.md) | 8 | Debian, AlmaLinux |
| 15 | [Võrguteenused: DNS, failijagamine, e-post ja varundus](moodul-15-vorguteenused/index.md) | 10 | Debian (15B: Ubuntu) |
| 16 | [Automatiseerimine: Ansible, Vagrant ja infrastruktuur koodina](moodul-16-automatiseerimine/index.md) | 10 | AlmaLinux, Debian, Ubuntu |
| 17 | [Seire ja jõudlus](moodul-17-seire/index.md) | 8 | Debian, Ubuntu |
| - | [Proovieksam: süvendusosa](proovieksam.md) | 4 | AlmaLinux |
| - | [Lõpuprojekt](lopuprojekt.md) (kolm taset) | 16 (12–32) | Õppija valik |

Moodul 12 annab konteinerite alused, mida serverimoodulites kasutatakse alternatiivse paigaldusviisina. Moodulites 13–15 ehitatakse samm-sammult üks „kooli väikeserver“ (veeb → andmebaasid → DNS, failid, e-post ja varundus), mida moodulites 16–17 automatiseeritakse ja seiratakse. Moodulid 16 ja 17 on **sissejuhatavad ja ülevaatlikud**: HKHK-s käsitletakse automatiseerimist ja seiret põhjalikult eraldi ainetes „IT-süsteemide automatiseerimine“ ja „IT-süsteemide monitooring“, mis läbitakse pärast Linuxi ja BSD halduse moodulit.

### Valikmoodulid

| Nr | Moodul | Maht (h) | Laboritöö distro |
|---|---|---|---|
| 18 | [BSD praktikas: OPNsense tulemüür](moodul-18-opnsense/index.md) | 8 | OPNsense (FreeBSD), Debian, Ubuntu |
| 19 | [Võrgu infrastruktuur: DHCP, PXE ja iSCSI](moodul-19-dhcp-pxe-iscsi/index.md) | 10 | Debian, AlmaLinux, Ubuntu |
| 20 | [Kataloogiteenused: OpenLDAP](moodul-20-openldap/index.md) | 8 | Debian (server), Ubuntu ja AlmaLinux (kliendid) |
| 21 | [Active Directory Linuxis: Samba AD DC](moodul-21-samba-ad/index.md) | 10 | Debian (DC), Ubuntu, AlmaLinux, Windows |
| 22 | [Linux töölaual ja WSL](moodul-22-toolaud-wsl/index.md) | 8 | Ubuntu Desktop, Kali, Windows (WSL) |
| 23 | [Virtualiseerimine: KVM, Proxmox VE ja XCP-ng](moodul-23-virtualiseerimine/index.md) | 12 | Debian, Proxmox VE, XCP-ng |
| 24 | [Kubernetes: k3s](moodul-24-kubernetes/index.md) | 10 | Debian |
| 25 | [FreeBSD server](moodul-25-freebsd/index.md) | 10 | FreeBSD |

Valikmoodulid 18–21 ehitavad üksteise peale (OPNsense'i laborivõrk → DHCP/PXE → LDAP → AD). Moodulid 22–25 on iseseisvad (moodul 24 eeldab konteinereid ja veebiservereid, moodulid 12–13; moodul 25 eeldab põhiosa ja sobib hästi pärast moodulit 18).

Laborikeskkonna ettevalmistus (HKHK Proxmoxi ligipääs, võrguplaan, virtuaalmasinad ja paigaldus) on kirjeldatud lisas [Laborikeskkond ja paigaldus](lisad/paigaldus.md). Kõik laboritööd kasutavad sama IP-plaani, nii et õppija ehitab ühe keskkonna, mis kasvab moodulist moodulisse.

## Moodulite sisu

### Moodul 1. Linux ja käsurida

**Teemad:** mis on Linux, kernel ja distributsioon, distrode perekonnad, terminal ja kest, SSH-ühendus, käsu ülesehitus, abi leidmine (`man`, `--help`), failisüsteemi hierarhia, liikumine kataloogides, failide ja kataloogide loomine, kopeerimine, teisaldamine ja kustutamine, failide sisu vaatamine, metamärgid, süsteemi info (`uname`, `hostnamectl`, `uptime`), tehisintellekt abilisena, harjutusmäng OverTheWire Bandit.

**Õpiväljundid:** õppija ühendub serveriga SSH kaudu, liigub failisüsteemis absoluutsete ja suhteliste teede abil, teeb põhitoiminguid failide ja kataloogidega ning leiab käskude kohta abi.

**Iseõppeks:** W. Shotts „The Linux Command Line“ (I osa); OverTheWire Bandit, tasemed 0–5.

### Moodul 2. Failid, tekst ja torud

**Teemad:** UNIX-i filosoofia ja käskude päritolu (GNU, POSIX, BusyBox), tekstiredaktorid (`nano`, `vim` põhitõed), väljundi ümbersuunamine (`>`, `>>`, `2>`), torud (`|`, `tee`), tekstitöötlus (`grep`, `sort`, `uniq`, `wc`, `cut`, `tr`, `awk` alused, `sed`), failide otsimine (`find`, `locate`, `which`, `type`), lingid (`ln`), arhiveerimine ja pakkimine (`tar`, `gzip`), regulaaravaldiste alused, failide võrdlemine ja paikamine (`diff`, `patch`), `xargs`.

**Õpiväljundid:** õppija redigeerib konfiguratsioonifaile, kombineerib käske torude abil ja otsib infot failidest ning failisüsteemist.

**Iseõppeks:** Shotts (I ja III osa); MIT Missing Semester - „Shell Tools and Scripting“, „Editors (Vim)“; OverTheWire Bandit, tasemed 6–15.

### Moodul 3. Kasutajad, grupid ja õigused

**Teemad:** kasutajad ja grupid (`/etc/passwd`, `/etc/group`, `/etc/shadow`), kasutajate ja gruppide haldus (`useradd`, `usermod`, `groupadd`, `passwd`, `chage`), `sudo`, `su` ja `sudoers`, failiõigused (`chmod`, `chown`, `chgrp`), numbriline ja sümboolne kuju, `umask`, erilised õigused (SUID, SGID, sticky bit), grupi jagatud kataloog, ACL-i tutvustus, uue kasutaja vaikeseaded (`/etc/skel`, `login.defs`), PAM, paroolipoliitika (`pam_pwquality`) ja konto lukustamine (`pam_faillock`).

**Õpiväljundid:** õppija loob ja haldab kasutajaid ning gruppe, määrab failidele sobivad õigused vähima õiguse põhimõttel ning seadistab paroolipoliitika.

**Iseõppeks:** Shotts (II osa); Linux Upskill Challenge.

### Moodul 4. Tarkvara ja pakihaldus

**Teemad:** paketid ja hoidlad, `apt` ja `dpkg` (Debian, Ubuntu), `dnf` ja `rpm` (AlmaLinux), süsteemi uuendamine, pakettide otsimine ja eemaldamine, paigaldusajalugu ja tagasivõtmine (`dnf history`), kolmandate osapoolte hoidlad (EPEL, PPA) ja nende riskid, tarkvara kompileerimine lähtekoodist, Snap ja Flatpak, uuenduste hea tava, väljalaske uuendamine (Debian 12 → 13, `do-release-upgrade`, ELevate), jagatud teegid (`ldd`, `ldconfig`), SUSE ja `zypper`.

**Õpiväljundid:** õppija paigaldab, uuendab ja eemaldab tarkvara kõigil kolmel distrol ning selgitab pakihaldurite erinevusi.

**Iseõppeks:** distrode dokumentatsioon (Debian Reference, AlmaLinux Wiki).

### Moodul 5. Protsessid, teenused ja systemd

**Teemad:** protsessid, PID ja olekud, `ps`, `pgrep`, `pstree`, `top`, `htop`, signaalid ja `kill`, esi- ja taustatööd (`jobs`, `fg`, `bg`, `nohup`), prioriteedid (`nice`, `renice`), systemd ja `systemctl`, teenuste haldus, unit-failid ja oma teenus, `journalctl` ja püsivad logid, ajastatud tööd (`cron`, systemd timer, `at`), ressursipiirangud (`ulimit`, `limits.conf`, systemd `MemoryMax=` ja `CPUQuota=`, `systemd-run`, `systemd-cgtop`).

**Õpiväljundid:** õppija jälgib ja haldab protsesse, käivitab, peatab ja seadistab teenuseid, ajastab töid, piirab ressursside kasutust ning leiab logidest vigu.

**Iseõppeks:** B. Ward „How Linux Works“; Arch Wiki - systemd.

### Moodul 6. Bashi skriptimine ja Git

**Teemad:** kestad (`bash`, `sh`/`dash`, `zsh`, `fish`), POSIX-ühilduvus, kesta vahetamine (`chsh`, `/etc/shells`) ja seadistusfailid, skripti ülesehitus ja shebang, muutujad ja keskkonnamuutujad, jutumärgid, argumendid, tingimused (`if`, `test`, `[[ ]]`, `case`), tsüklid (`for`, `while`, faili lugemine rea kaupa), kasutaja sisend (`read`), funktsioonid, massiivid, väljumiskoodid, sisend ja väljund, vigade käsitlemine (`set -euo pipefail`, `trap`), ShellCheck, silumine (`bash -x`), skriptide ajastamine, Git (sissekanded, tagasivõtmine, `.gitignore`, harud, konfliktid, kaughoidla).

**Õpiväljundid:** õppija kirjutab loetavaid ja töökindlaid skripte, mis automatiseerivad haldustoiminguid (nt varundus, kasutajate loomine, logide analüüs) ning hoiab need Git-hoidlas.

**Iseõppeks:** Shotts (IV osa); Greg's Wiki „BashGuide“; MIT Missing Semester.

### Moodul 7. Võrk ja SSH

**Teemad:** IP-aadressid, alamvõrgud ja marsruutimine (`ip`), masina nimi, DNS ja nimelahendus (`/etc/hosts`, systemd-resolved, `dig`), pordid ja ühendused (`ss`), võrgu seadistamine (Debiani `ifupdown`, Ubuntu Netplan, AlmaLinuxi NetworkManager ja `nmcli`), võrguprobleemide diagnoosimine, SSH võtmepõhine autentimine, `ssh-agent`, `~/.ssh/config`, tunnelid, hüppeserver (`ProxyJump`), `scp`, `rsync`, SSH-serveri karastamine, tulemüür (`nftables`, `ufw`, `firewalld`), kellaaeg ja NTP (`timedatectl`, chrony, systemd-timesyncd), lokaat ja klaviatuur (`localectl`), WireGuard VPN, IPv6 (link-local, SLAAC), sild, VLAN ja liitliides (*bond*), püsivad staatilised marsruudid.

**Õpiväljundid:** õppija seadistab võrguühenduse (ka IPv6, sild, VLAN ja liitliides), diagnoosib võrguprobleeme, kasutab SSH-võtmeid ja hüppeserverit, seadistab tulemüüri, ajasünkroonimise ja VPN-i.

**Iseõppeks:** Linux Upskill Challenge; Arch Wiki - Network configuration.

### Moodul 8. Kettad, failisüsteemid ja LVM

**Teemad:** plokkseadmed (`lsblk`, `blkid`), partitsioonid (`fdisk`, `parted`, GPT ja MBR), failisüsteemid (ext4, XFS, Btrfs), haakimine (`mount`, `/etc/fstab`), saaleala (swap), LVM (PV, VG, LV; köite suurendamine ja vähendamine, hetktõmmised), virtuaalmasina ketta suurendamine, kettakasutuse jälgimine (`df`, `du`), ketta krüpteerimine (LUKS). RAID, ZFS, jõudlus ja taastamine on moodulis 9, failisüsteemi seaded (`tune2fs`, `dumpe2fs`, `xfs_admin`), FAT32 (`mkfs.vfat`).

**Õpiväljundid:** õppija lisab süsteemi uue ketta, loob failisüsteemi ja LVM-köite, haagib selle püsivalt, suurendab köidet ja krüpteerib ketta.

**Iseõppeks:** „How Linux Works“; Red Hati dokumentatsioon (LVM).

### Moodul 9. Salvestus: RAID, ZFS, jõudlus ja taastamine

**Teemad:** RAID-i tasemed, riistvaraline ja tarkvaraline RAID (`mdadm`), ZFS (pool, vdev, dataset, hetktõmmised, `zfs send`, scrub; Proxmox ja TrueNAS), ketta jõudluse mõõtmine (`dd`, `fio`, `iostat`), ketaste tervis (SMART), partitsioonitabeli ja failide taastamine (TestDisk, PhotoRec).

**Õpiväljundid:** õppija ehitab töökindla salvestuse, vahetab rikkis ketta, mõõdab ja jälgib ketaste jõudlust ning taastab kadunud partitsioonitabeli.

**Iseõppeks:** OpenZFS dokumentatsioon; Arch Wiki - RAID, ZFS, S.M.A.R.T.

### Moodul 10. Kuidas Linux töötab: alglaadimine ja kernel

**Teemad:** alglaadimise etapid (UEFI/BIOS, GRUB, kernel, initramfs, systemd), käivituseesmärgid (target), kerneli moodulid (`lsmod`, `modprobe`), `/proc` ja `/sys`, `dmesg`, kerneli parameetrid (`sysctl`), alglaadimise analüüs (`systemd-analyze`), süsteemi taastamine (rescue-režiim, juurkasutaja parooli lähtestamine, GRUB-i parandamine taastemeedialt ja `chroot`-iga), kernelite vahetamine ja eemaldamine, DKMS, kerneli kompileerimine lähtekoodist, systemd süvitsi (sõltuvused ja järjekord, teenuse tüübid, keskkond, mallid, pesa- ja teeüksused, `.mount`/`.automount`, kasutajateenused, teenuste karastamine `systemd-analyze security`-ga, tõrkeotsing), riistvara ja udev (`lspci`, `udevadm`, udev reeglid).

**Õpiväljundid:** õppija kirjeldab alglaadimise protsessi, diagnoosib käivitusprobleeme, taastab mittekäivituva süsteemi, vahetab kasutatavat kernelit, kompileerib ja paigaldab kerneli lähtekoodist ning seadistab, karastab ja silub systemd teenuseid.

**Iseõppeks:** „How Linux Works“; Linux From Scratch (süvenemiseks).

### Moodul 11. Turvalisus ja logid

**Teemad:** turvalisuse põhimõtted, SSH karastamine, automaatsed turvauuendused, `fail2ban`, logide asukohad ja `journald`, `rsyslog` ja tsentraalne logimine, logide rotatsioon (`logrotate`), kohustuslik juurdepääsukontroll: SELinux (AlmaLinux) ja AppArmor (Ubuntu), auditeerimine (`auditd`), turvaaudit (Lynis), SIEM-i (Wazuh) tutvustus ja automaatne reageerimine, fail2ban-i vajalikkus ja alternatiivid (OpenSSH `PerSourcePenalties`, CrowdSec), kontrollsummad (`sha256sum`) ja GnuPG (allkirjad, krüpteerimine).

**Õpiväljundid:** õppija karastab serveri, jälgib logisid, lahendab SELinuxi ning AppArmori põhjustatud probleeme ja seadistab tsentraalse turvaseire koos automaatse reageerimisega.

**Iseõppeks:** CIS Benchmarks; Red Hati SELinuxi dokumentatsioon.

### Moodul 12. Konteinerid

**Teemad:** konteinerite põhimõte (nimeruumid, cgroups) ja erinevus virtuaalmasinatest, Podman ja Docker, pildid ja registrid, köited, juurkasutajata (*rootless*) konteinerid, oma pilt (Containerfile), Compose, Quadlet, automaatsed pildiuuendused.

**Õpiväljundid:** õppija käivitab teenuseid konteinerites, ehitab oma pildi, haldab konteinereid systemd teenustena ja seadistab nende automaatse uuendamise.

**Iseõppeks:** Podmani dokumentatsioon; „Podman in Action“.

### Moodul 13. Veebiserverid

**Teemad:** serveriteenuse paigaldamise töövoog, nginx (virtuaalhostid, pöördpuhver), TLS ja oma CA, Let's Encrypt, Apache (`a2ensite`, `.htaccess`, AlmaLinuxi `httpd` ja SELinux), Caddy (automaatne HTTPS), lighttpd ja teised veebiserverid, koormuse jaotus (nginx `upstream`, HAProxy, Traefik), jaoturi rikkekindlus (keepalived, VRRP), koormustest (`ab`, `wrk`), veebiserveri valik.

**Õpiväljundid:** õppija paigaldab ja turvab veebiserverid, seadistab pöördpuhvri ning rikkekindla koormuse jaotuse, mõõdab jõudlust koormustestiga ja valib olukorrale sobiva tarkvara.

**Iseõppeks:** nginx-i, Apache'i, Caddy ja HAProxy dokumentatsioon; Mozilla SSL Configuration Generator.

### Moodul 14. Andmebaasid

**Teemad:** andmebaaside liigid (relatsiooniline, manustatud, võti-väärtus, NoSQL), MariaDB (kasutajad ja õigused, kaugühendus, varundus, parooli taastamine, replikatsioon ja ülevõtt), PostgreSQL (`psql`, rollid, `pg_hba.conf`, `pg_dump`), SQLite, Valkey/Redis, nginx + PHP + MariaDB, andmebaaside turvalisus.

**Õpiväljundid:** õppija paigaldab ja haldab levinumaid andmebaase, ühendab andmebaasi veebirakendusega, varundab ja taastab andmeid ning teeb rikke korral koopia põhiserveriks.

**Iseõppeks:** MariaDB Knowledge Base, PostgreSQL-i dokumentatsioon, SQLBolt.

### Moodul 15. Võrguteenused: DNS, failijagamine, e-post ja varundus

**Teemad:** DNS-server BIND9 ning võrdlus (Unbound, dnsmasq, CoreDNS, Pi-hole), failide jagamine (NFS ja autofs, Samba, TrueNAS), e-posti saatmine (Postfix relee), varundus (3-2-1, RPO ja RTO, restic) ja taastamistest, serveri dokumenteerimine, käsiraamat ja otsuste logi.

**Õpiväljundid:** õppija lisab serverile sisevõrgu DNS-i, failijagamise ja e-posti teavitused, planeerib varunduse RPO ja RTO järgi, testib taastamist ning dokumenteerib serveri koos käsiraamatuga.

**Iseõppeks:** BIND 9, Samba Wiki, Postfixi ja resticu dokumentatsioon.

### Moodul 16. Automatiseerimine: Ansible, Vagrant ja infrastruktuur koodina

**Teemad:** automatiseerimise astmed (Bashi skriptid, cron ja systemd taimerid, Git, konteinerid, Ansible), infrastruktuur koodina, idempotentsus, Ansible (inventuur, ad-hoc käsud, mänguraamatud, mallid, käsitlejad, Vault, eri distrod, rollid ja muutujafailid), Ansible'i koodi testimine (`ansible-lint`, idempotentsuse test, Molecule), Vagrant laborikeskkonna loomiseks, virtuaalmasinad koodina (cloud-init, OpenTofu), Puppet ja teised seadistushaldurid (push vs pull).

**Õpiväljundid:** õppija seadistab mitu serverit korraga Ansible'i rollidega, testib automatiseerimiskoodi, loob virtuaalmasinad koodina ja korratava laborikeskkonna.

**Iseõppeks:** Ansible'i dokumentatsioon; J. Geerling „Ansible for DevOps“.

### Moodul 17. Seire ja jõudlus

**Teemad:** mõõdikud, logid ja häired, USE meetod, `uptime`, `top`, `vmstat`, `iostat`, `pidstat`, `sar`, `strace`, `lsof`, jõudlusprofiilid (`tuned`), Prometheus, node_exporter ja Grafana, PromQL, häired, Uptime Kuma, Zabbixi tutvustus.

**Õpiväljundid:** õppija leiab jõudlusprobleemi põhjuse süstemaatiliselt ja ehitab laborivõrgule seiresüsteemi.

**Iseõppeks:** B. Gregg „Systems Performance“; Prometheuse ja Grafana dokumentatsioon.

### Valikmoodul 18. BSD praktikas: OPNsense tulemüür

**Teemad:** isoleeritud laborivõrgu kavandamine (WAN/LAN, Proxmoxi sild või SDN), OPNsense'i paigaldus ja konsoolimenüü, veebiliides, DHCP (Dnsmasq, Kea) ja Unbound DNS, tulemüürireeglid ja aliased, NAT ja pordisuunamine, logid, varundus, FreeBSD ja Linuxi käsud.

**Õpiväljundid:** õppija ehitab OPNsense'iga isoleeritud laborivõrgu, seadistab selle DHCP, DNS-i ja tulemüürireeglid ning teeb teenuse kättesaadavaks pordisuunamisega.

**Iseõppeks:** OPNsense'i dokumentatsioon (docs.opnsense.org).

### Valikmoodul 19. Võrgu infrastruktuur: DHCP, PXE ja iSCSI

**Teemad:** DHCP tööpõhimõte (DORA, valikud, releed), Kea DHCP, ISC DHCP võrdlus, reserveeringud, PXE alglaadimine (TFTP, iPXE, BIOS ja UEFI, netboot.xyz, FOG), automaatne paigaldus (kickstart, preseed, autoinstall), iSCSI sihtmärk (`targetcli`) ja initsiaator (`iscsiadm`), CHAP.

**Õpiväljundid:** õppija seadistab laborivõrgule Linuxi DHCP-serveri, võrgust alglaadimise koos automaatse paigaldusega ja iSCSI plokksalvestuse.

**Iseõppeks:** Kea Administrator Reference Manual; Red Hati dokumentatsioon „Managing storage devices“.

### Valikmoodul 20. Kataloogiteenused: OpenLDAP

**Teemad:** tsentraalne autentimine, LDAP-i andmemudel (DIT, DN, objektiklassid, skeemid), OpenLDAP-i paigaldus ja `cn=config`, LDIF, otsingud ja muudatused, ligipääsureeglid, TLS, LDAP Account Manager, SSSD kliendid, varundus.

**Õpiväljundid:** õppija paigaldab OpenLDAP-serveri, haldab kasutajaid ja gruppe ning seadistab Linuxi masinad kataloogist autentima.

**Iseõppeks:** OpenLDAP Administrator's Guide; `man sssd-ldap`.

### Valikmoodul 21. Active Directory Linuxis: Samba AD DC

**Teemad:** Active Directory põhimõisted, Kerberos ja DNS, Samba AD domeenikontrolleri paigaldus, `samba-tool`, Windowsi kliendi liitmine ja RSAT, rühmapoliitika, Linuxi klientide liitmine (realmd, SSSD), paroolipoliitika, DNS-kirjed, teine domeenikontroller ja varundus, ligipääsu ja `sudo` piiramine gruppidega, Windows Server AD-ga liitumine, veaotsing.

**Õpiväljundid:** õppija loob vaba tarkvaraga AD domeeni ning liidab sellega Windowsi ja Linuxi masinad.

**Iseõppeks:** Samba Wiki; Red Hati dokumentatsioon „Integrating RHEL systems directly with Windows Active Directory“.

### Valikmoodul 22. Linux töölaual ja WSL

**Teemad:** töölaua Linuxi suundumused (mängud ja SteamOS, digitaalne suveräänsus, Windows 10 toe lõpp), töölaua distrod ja muutumatud distrod, graafiline süsteem (Wayland, X11, sisselogimishaldur, töölauakeskkonnad), Flatpak ja Snap, Windowsi programmide alternatiivid, Proton, haldus (uuendused, printerid, Timeshift, ID-kaart, kaugtöölaud), Kali Linux, WSL, ligipääsetavus.

**Õpiväljundid:** õppija valib sobiva töölaua distro, haldab töölaua Linuxit, kasutab Kalit vastutustundlikult ja töötab Linuxiga Windowsi sees WSL-i abil.

**Iseõppeks:** Flathubi ja ProtonDB veebilehed; Microsoft Learn - WSL; Kali dokumentatsioon.

### Valikmoodul 23. Virtualiseerimine: KVM, Proxmox VE ja XCP-ng

**Teemad:** hüperviisorite tüübid, riistvaraline tugi ja pesastatud virtualiseerimine, KVM, QEMU ja libvirt, Proxmox VE (paigaldus, hoidlad, uuendused, VM-id ja LXC, salvestus, sillad, VLAN-id, NAT, varundus (`vzdump` ja Proxmox Backup Server: deduplitseerimine, säilitusreeglid, kontroll, üksikfailide taastamine), mallid ja cloud-init mall, kasutajad ja õigused, REST API ja `pvesh`, klaster), XCP-ng (`xe`, külalistööriistad) ja Xen Orchestra. HKHK-s käsitletakse hüperviisoreid põhjalikumalt aines „Majutuskeskkonna riistvara“.

**Õpiväljundid:** õppija paigaldab ja haldab avatud hüperviisoreid, varundab ja taastab virtuaalmasinaid Proxmox Backup Serveriga, loob cloud-init malle, kasutab Proxmoxi API-t ning selgitab, kuidas Linux virtualiseerib.

**Iseõppeks:** Proxmox VE dokumentatsioon ja wiki; XCP-ng dokumentatsioon.

### Valikmoodul 24. Kubernetes: k3s

**Teemad:** konteinerite orkestreerimine ja millal seda vaja ei ole, Kubernetese ülesehitus (juhtkiht, kubelet, containerd, CNI) ja deklaratiivne haldus, distributsioonide võrdlus (kubeadm, k3s, RKE2, k0s, MicroK8s, minikube, kind, Talos), k3s mitmesõlmelise klastri paigaldus, `kubectl`, Pod, Deployment, Service, Ingress (Traefik) ja TLS, skaleerimine, järkjärguline uuendus ja tagasivõtt, ConfigMap ja Secret, püsikettad (PVC, `local-path`), Helm, sõlme hooldus, uuendamine ja varundus, kõrge kättesaadavus etcd-ga, GitOps (Argo CD, Flux).

**Õpiväljundid:** õppija ehitab k3s klastri, käivitab sellel rakenduse koos TLS-i ja püsiandmetega, uuendab ja hooldab klastrit ning oskab hinnata, millal Kubernetes on õige valik.

**Iseõppeks:** k3s ja Kubernetese dokumentatsioon; minikube või kind oma arvutis; „Kubernetes the Hard Way“.

### Valikmoodul 25. FreeBSD server

**Teemad:** BSD perekond ja FreeBSD, baassüsteem ja `/usr/local`, paigaldus ZFS juurfailisüsteemiga, GNU ja BSD tööriistade erinevused, `pkg`, pordid ja pkgbase, baassüsteemi uuendamine (`freebsd-update`), teenused rc.d süsteemiga (`rc.conf`, `sysrc`, `service`), logid, `newsyslog` ja `periodic`, kasutajad (`pw`, `vipw`, grupp `wheel`, `doas`), võrk (`ifconfig`, `rc.conf`), ZFS-i hetktõmmised ja alglaadimiskeskkonnad (`bectl`), tulemüür pf (tabelid, ühenduste piiramine), jailid, FreeBSD ja Linuxi halduse võrdlus.

**Õpiväljundid:** õppija paigaldab ja haldab FreeBSD serverit käsurealt, uuendab seda turvaliselt alglaadimiskeskkondadega, seadistab pf-i ja jaili ning võrdleb FreeBSD ja Linuxi haldust.

**Iseõppeks:** FreeBSD Handbook; „Absolute FreeBSD“ (M. W. Lucas); BastilleBSD.

### Proovieksamid

**Põhiosa** (2 h, pärast moodulit 8): praktiline eksam Debianis 7 teemaplokiga (süsteem, kasutajad, failid ja tekst, tarkvara ja ajastamine, võrk ja tulemüür, LVM, skript), tulemust kontrollib automaatne skript. Juhend: [proovieksam: põhiosa](proovieksam-pohiosa.md).

**Süvendusosa** (4 h): RHCSA stiilis praktiline eksam AlmaLinuxis: 2,5 tunniga tuleb täita 8 teemaplokki haldusülesandeid ning tulemust kontrollib automaatne skript. Juhend: [proovieksam](proovieksam.md).

### Lõpuprojekt

Täpsem juhend koos teemade, nõuete ja hindamiskriteeriumidega: [lõpuprojekt](lopuprojekt.md).

Õppija ehitab ja dokumenteerib terviklahenduse ühel kolmest tasemest:

| Tase | Eeldused | Maht | Näited |
|---|---|---|---|
| **Algtase** | moodulid 1–8 | 12 h | üks turvatud ja varundatud server, halduskriptide komplekt, oma systemd teenus |
| **Edasijõudnud** | moodulid 1–17 | 16 h | veebirakenduse platvorm, Ansible'iga hallatav serveripark, labori infrastruktuuriteenused, konteinerplatvorm |
| **Meister** | moodulid 1–17 + valikmoodulid | 24–32 h | kõrge kättesaadavusega teenus, virtualiseerimisplatvorm koodina, kooli võrk ja kasutajahaldus, turvaseire, Kubernetese platvorm |

Projekti juurde kuuluvad kirjalik dokumentatsioon (soovitatavalt Git-repos) ja esitlus.

## Hindamine

Soovituslik hindamine (kohanda õppekava järgi):

| Osa | Kaal | Arvestatud, kui |
|---|---|---|
| **Laboritööd** | 40% | kõik kohustuslikud osad on tehtud ja vähemalt 80% K-küsimustest on vastatud sisuliselt õigesti |
| **Enesekontroll** | - | iseseisvaks kontrolliks; õpetaja võib kasutada küsimusi kontrolltöös |
| **Proovieksamid** | 20% | vähemalt 70% punktidest kontrollskripti järgi |
| **Lõpuprojekt** | 40% | vt [lõpuprojekti hindamine](lopuprojekt.md) |

### Laboritöö hindamisjuhend

| Tase | Kirjeldus |
|---|---|
| **Suurepärane** | Kõik osad tehtud, ka lisaülesanne; vastused on põhjendatud ja seostavad teooriaga; aruandes on käsud ja väljundid; probleemid on kirjeldatud koos lahendusega |
| **Hea** | Kõik kohustuslikud osad tehtud; vastused õiged, mõni põhjendus pinnapealne |
| **Arvestatud** | Kohustuslikud osad tehtud; ≥ 80% küsimustest vastatud õigesti; masin on töö lõpus nõutud olekus |
| **Mittearvestatud** | Osa kohustuslikest osadest tegemata või vastused kopeeritud ilma arusaamata (õppija ei oska suuliselt selgitada) |

Hea tava: lase õppijal mõne laboritöö lõpus **suuliselt selgitada** ühte tehtud sammu („Miks kasutasid `nofail`-i?“). See näitab arusaamist paremini kui kirjalik vastus ja on hea vastumeede AI-l põhinevale kopeerimisele.

## Lisad

- [Linuxi distributsioonide ülevaade](lisad/distrod.md) - suuremad distrod perekondade kaupa, BSD ja Linuxi erinevused
- [UNIX-i ja Linuxi ajalugu](lisad/ajalugu.md) - UNIX-ist Linuxi ja tänapäevani
- [Sõnastik](lisad/sonastik.md) - mõisted eesti ja inglise keeles
- [Käskude loend](lisad/kasud.md) - olulisemad käsud tähestiku järgi: mida teeb ja millises moodulis õpetatakse
- [Laborikeskkond ja paigaldus](lisad/paigaldus.md) - HKHK Proxmoxi ligipääs, võrguplaan, virtuaalmasinad, distrode paigaldus, WSL-i kiirstart

## Edasised sammud pärast kursust

- **Sertifikaadid:** LPIC-1 või CompTIA Linux+ (distrost sõltumatu), Red Hat RHCSA (praktiline eksam), hiljem RHCE või LPIC-2; Kubernetese puhul KCNA ja CKA.
- **Süvenemine:** „UNIX and Linux System Administration Handbook“ (Nemeth jt), „The Linux Programming Interface“ (M. Kerrisk), Linux From Scratch.
- **Viide:** Arch Wiki - parim Linuxi teatmeteos, ka siis, kui Archi ei kasuta.

<!-- navigatsioon -->
---

[Sisukord](../README.md#sisukord) · [Moodul 1. Linux ja käsurida →](moodul-01-sissejuhatus/index.md)
<!-- /navigatsioon -->
