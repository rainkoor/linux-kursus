<!-- navigatsioon -->
[← Sõnastik](sonastik.md) · [Sisukord](../../README.md#sisukord)
<!-- /navigatsioon -->

# Käskude loend

Kursusel kasutatud olulisemad käsud tähestikulises järjekorras: mida käsk teeb ja millises moodulis selle kasutamist õpetatakse. Loend on mõeldud kiireks meeldetuletuseks - täpsed võtmed ja näited leiad moodulist ning käsu kasutusjuhendist (`man käsk`, `käsk --help`).

Moodulite kokkuvõtetes on samad käsud teemade kaupa. Mõisteid selgitab [sõnastik](sonastik.md).

| Moodul | Teema |
|---|---|
| 1 | [Linux ja käsurida](../moodul-01-sissejuhatus/index.md) |
| 2 | [Failid, tekst ja torud](../moodul-02-failid-tekst-torud/index.md) |
| 3 | [Kasutajad, grupid ja õigused](../moodul-03-kasutajad-oigused/index.md) |
| 4 | [Tarkvara ja pakihaldus](../moodul-04-pakihaldus/index.md) |
| 5 | [Protsessid, teenused ja systemd](../moodul-05-protsessid-teenused/index.md) |
| 6 | [Bashi skriptimine ja Git](../moodul-06-bash/index.md) |
| 7 | [Võrk ja SSH](../moodul-07-vork-ssh/index.md) |
| 8 | [Kettad, failisüsteemid ja LVM](../moodul-08-kettad-lvm/index.md) |
| 9 | [Varundus ja taastamine](../moodul-09-varundus/index.md) |
| 10 | [Salvestus: RAID, ZFS, jõudlus ja taastamine](../moodul-10-salvestus/index.md) |
| 11 | [Kuidas Linux töötab: alglaadimine ja kernel](../moodul-11-alglaadimine-kernel/index.md) |
| 12 | [Turvalisus ja logid](../moodul-12-turvalisus-logid/index.md) |
| 13 | [Võrgu süvendus: IPv6, sild, VLAN, bond ja VPN](../moodul-13-vorgu-suvendus/index.md) |
| 14 | [Konteinerid](../moodul-14-konteinerid/index.md) |
| 15 | [Veebiserverid](../moodul-15-veebiserverid/index.md) |
| 16 | [Andmebaasid](../moodul-16-andmebaasid/index.md) |
| 17 | [DNS ja nimelahendus](../moodul-17-dns/index.md) |
| 18 | [Failiserverid](../moodul-18-failiserverid/index.md) |
| 19 | [Automatiseerimine: Ansible, Vagrant ja infrastruktuur koodina](../moodul-19-automatiseerimine/index.md) |
| 20 | [Seire ja jõudlus](../moodul-20-seire/index.md) |
| 21 | [BSD praktikas: OPNsense tulemüür](../moodul-21-opnsense/index.md) |
| 22 | [Võrgu infrastruktuur: DHCP, PXE ja iSCSI](../moodul-22-dhcp-pxe-iscsi/index.md) |
| 23 | [E-posti server](../moodul-23-e-post/index.md) |
| 24 | [Kataloogiteenused: OpenLDAP](../moodul-24-openldap/index.md) |
| 25 | [Active Directory Linuxis: Samba AD DC](../moodul-25-samba-ad/index.md) |
| 26 | [Linux töölaual ja WSL](../moodul-26-toolaud-wsl/index.md) |
| 27 | [Virtualiseerimine: KVM, Proxmox VE ja XCP-ng](../moodul-27-virtualiseerimine/index.md) |
| 28 | [Kubernetes: k3s](../moodul-28-kubernetes/index.md) |
| 29 | [FreeBSD server](../moodul-29-freebsd/index.md) |

## A

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `a2ensite` | Lubab Apache'i saidi (Debian, Ubuntu; ka `a2enmod`) | [15](../moodul-15-veebiserverid/index.md) |
| `aa-complain` | Lülitab AppArmori profiili complain-režiimi (ainult logib) | [12](../moodul-12-turvalisus-logid/index.md) |
| `aa-enforce` | Lülitab AppArmori profiili enforce-režiimi (keelab) | [12](../moodul-12-turvalisus-logid/index.md) |
| `aa-status` | AppArmori profiilid ja režiimid | [12](../moodul-12-turvalisus-logid/index.md) |
| `ab` | Apache Bench koormustest | [15](../moodul-15-veebiserverid/index.md) |
| `alias` | Lühinimi käsule | [6](../moodul-06-bash/index.md) |
| `ansible` | Ansible'i ad-hoc käsud | [19](../moodul-19-automatiseerimine/index.md) |
| `ansible-galaxy` | Rollid ja kollektsioonid | [19](../moodul-19-automatiseerimine/index.md) |
| `ansible-lint` | Ansible'i koodi kontroll | [19](../moodul-19-automatiseerimine/index.md) |
| `ansible-playbook` | Mänguraamatu käivitamine (`--check`, `--diff`) | [19](../moodul-19-automatiseerimine/index.md) |
| `ansible-vault` | Saladuste krüpteerimine | [19](../moodul-19-automatiseerimine/index.md) |
| `apache2ctl` | Apache'i juhtimine ja `configtest` | [15](../moodul-15-veebiserverid/index.md) |
| `apt` | Debiani ja Ubuntu pakihaldur (`update`, `upgrade`, `install`, `remove`, `search`) | [4](../moodul-04-pakihaldus/index.md) |
| `apt-mark` | Lukustab paketi versiooni (`hold`, `unhold`, `showhold`) | [4](../moodul-04-pakihaldus/index.md) |
| `arping` | Saadab ARP-päringu; `-D` kontrollib, kas IP-aadress on võrgus juba kasutusel | [7](../moodul-07-vork-ssh/index.md) |
| `at` | Käivitab käsu üks kord kindlal ajal | [5](../moodul-05-protsessid-teenused/index.md) |
| `atq` | Ootel `at`-tööd | [5](../moodul-05-protsessid-teenused/index.md) |
| `atrm` | Eemaldab `at`-töö | [5](../moodul-05-protsessid-teenused/index.md) |
| `audit2why` | Selgitab SELinuxi keeldu | [12](../moodul-12-turvalisus-logid/index.md) |
| `auditctl` | auditd reeglid | [12](../moodul-12-turvalisus-logid/index.md) |
| `ausearch` | Otsib auditilogist | [12](../moodul-12-turvalisus-logid/index.md) |
| `awk` | Väljapõhine tekstitöötlus ja aruanded | [2](../moodul-02-failid-tekst-torud/index.md) |

## B

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `bash` | Bashi kest; `bash -n` süntaksikontroll, `bash -x` silumine | [6](../moodul-06-bash/index.md) |
| `bectl` | ZFS-i alglaadimiskeskkondade haldus (FreeBSD) | [29](../moodul-29-freebsd/index.md) |
| `bg` | Jätkab peatatud tööd taustal | [5](../moodul-05-protsessid-teenused/index.md) |
| `blkid` | Failisüsteemide tüübid ja UUID-d | [8](../moodul-08-kettad-lvm/index.md) |
| `bridge` | Silla liidesed ja MAC-tabel (`bridge link`, `bridge fdb`) | [13](../moodul-13-vorgu-suvendus/index.md) |

## C

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `caddy` | Caddy veebiserver; `caddy validate`, `caddy fmt` | [15](../moodul-15-veebiserverid/index.md) |
| `cat` | Väljastab faili sisu | [1](../moodul-01-sissejuhatus/index.md) |
| `cd` | Kataloogi vahetamine | [1](../moodul-01-sissejuhatus/index.md) |
| `certbot` | Let's Encrypti sertifikaatide hankimine ja uuendamine | [15](../moodul-15-veebiserverid/index.md) |
| `chage` | Parooli aegumise seaded | [3](../moodul-03-kasutajad-oigused/index.md) |
| `chgrp` | Muudab faili gruppi | [3](../moodul-03-kasutajad-oigused/index.md) |
| `chmod` | Muudab faili õigusi | [3](../moodul-03-kasutajad-oigused/index.md) |
| `chown` | Muudab faili omanikku ja gruppi | [3](../moodul-03-kasutajad-oigused/index.md) |
| `chronyc` | chrony ajasünkroonimise olek (`sources`, `tracking`) | [7](../moodul-07-vork-ssh/index.md) |
| `chroot` | Käivitab käsud teise juurkataloogi sees (süsteemi parandamine) | [11](../moodul-11-alglaadimine-kernel/index.md), [14](../moodul-14-konteinerid/index.md) |
| `chsh` | Muudab kasutaja sisselogimiskesta (`-s /usr/bin/zsh`) | [6](../moodul-06-bash/index.md) |
| `cloud-init` | VM-i esmase seadistuse olek (`status --long`) | [19](../moodul-19-automatiseerimine/index.md) |
| `conntrack` | Aktiivsed ühendused ja NAT-kirjed | [13](../moodul-13-vorgu-suvendus/index.md) |
| `cp` | Kopeerib faile ja katalooge (`-r` rekursiivselt) | [1](../moodul-01-sissejuhatus/index.md) |
| `crictl` | Konteinerikäituri (containerd) konteinerid sõlmes | [28](../moodul-28-kubernetes/index.md) |
| `crontab` | Kasutaja ajastatud tööde muutmine (`-e`, `-l`) | [5](../moodul-05-protsessid-teenused/index.md) |
| `cryptsetup` | LUKS-krüpteeritud ketaste haldus | [8](../moodul-08-kettad-lvm/index.md) |
| `curl` | HTTP(S) päringud käsurealt | [7](../moodul-07-vork-ssh/index.md) |
| `cut` | Eraldab ridadest välju või märke | [2](../moodul-02-failid-tekst-torud/index.md) |

## D

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `dd` | Plokikaupa kopeerimine; lihtne kiirustest | [10](../moodul-10-salvestus/index.md) |
| `ddrescue` | Riknenud ketta kopeerimine tõmmiseks | [10](../moodul-10-salvestus/index.md) |
| `debootstrap` | Paigaldab minimaalse Debiani või Ubuntu süsteemi kataloogi (nt `chroot`-i jaoks) | [14](../moodul-14-konteinerid/index.md) |
| `df` | Failisüsteemide vaba ruum (`-h`) | [8](../moodul-08-kettad-lvm/index.md) |
| `diff` | Näitab failide erinevusi (`-u` paiga kujul) | [2](../moodul-02-failid-tekst-torud/index.md) |
| `dig` | DNS-päringud | [7](../moodul-07-vork-ssh/index.md) |
| `dmesg` | Kerneli teated | [11](../moodul-11-alglaadimine-kernel/index.md) |
| `dnf` | AlmaLinuxi pakihaldur (`install`, `upgrade`, `history`, `provides`) | [4](../moodul-04-pakihaldus/index.md) |
| `do-release-upgrade` | Ubuntu väljalaske uuendamine | [4](../moodul-04-pakihaldus/index.md) |
| `doas` | Lihtne `sudo` alternatiiv (OpenBSD, FreeBSD) | [29](../moodul-29-freebsd/index.md) |
| `docker` | Docker konteinerite haldus | [14](../moodul-14-konteinerid/index.md) |
| `doveadm` | Dovecoti haldus (kasutajad, postkastid, logid) | [23](../moodul-23-e-post/index.md) |
| `doveconf` | Dovecoti aktiivne seadistus (`-n`) | [23](../moodul-23-e-post/index.md) |
| `dpkg` | Debiani madala taseme pakihaldus (`-l`, `-L`, `-S`) | [4](../moodul-04-pakihaldus/index.md) |
| `dracut` | Loob initramfs-i uuesti (AlmaLinux) | [11](../moodul-11-alglaadimine-kernel/index.md) |
| `du` | Kataloogide ja failide maht | [8](../moodul-08-kettad-lvm/index.md) |
| `dumpe2fs` | ext-failisüsteemi andmed (`-h` ülevaade) | [8](../moodul-08-kettad-lvm/index.md) |

## E

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `echo` | Väljastab teksti | [2](../moodul-02-failid-tekst-torud/index.md) |
| `ethtool` | Võrguliidese kiirus, duplex ja draiveri info | [20](../moodul-20-seire/index.md) |
| `exit` | Lõpetab skripti antud väljumiskoodiga | [6](../moodul-06-bash/index.md) |
| `exportfs` | NFS-i jagatud kataloogid | [18](../moodul-18-failiserverid/index.md) |

## F

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `fail2ban-client` | fail2ban-i vanglate olek ja blokeeringud | [12](../moodul-12-turvalisus-logid/index.md) |
| `faillock` | Näitab või tühistab valede sisselogimiskatsete lukustuse | [3](../moodul-03-kasutajad-oigused/index.md) |
| `fdisk` | Partitsioonide haldus (MBR ja GPT) | [8](../moodul-08-kettad-lvm/index.md) |
| `fg` | Toob töö esiplaanile | [5](../moodul-05-protsessid-teenused/index.md) |
| `file` | Tuvastab faili tüübi sisu järgi | [1](../moodul-01-sissejuhatus/index.md) |
| `find` | Otsib faile nime, tüübi, suuruse, aja ja õiguste järgi | [2](../moodul-02-failid-tekst-torud/index.md) |
| `findmnt` | Haagitud failisüsteemid; `--verify` kontrollib fstab-i | [8](../moodul-08-kettad-lvm/index.md) |
| `fio` | Ketta jõudluse põhjalik mõõtmine | [10](../moodul-10-salvestus/index.md) |
| `firewall-cmd` | firewalld tulemüür (AlmaLinux) | [7](../moodul-07-vork-ssh/index.md) |
| `flatpak` | Flatpak-rakenduste haldus | [4](../moodul-04-pakihaldus/index.md) |
| `free` | Mälu kasutus (`-h`) | [20](../moodul-20-seire/index.md) |
| `freebsd-update` | FreeBSD baassüsteemi ja kerneli uuendamine | [29](../moodul-29-freebsd/index.md) |
| `freebsd-version` | FreeBSD kerneli ja kasutajaruumi versioon (`-kru`) | [29](../moodul-29-freebsd/index.md) |
| `fwupdmgr` | Püsivara uuendused | [26](../moodul-26-toolaud-wsl/index.md) |

## G

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `geom` | FreeBSD kettaseadmed (`geom disk list`) | [29](../moodul-29-freebsd/index.md) |
| `getenforce` | SELinuxi režiim | [12](../moodul-12-turvalisus-logid/index.md) |
| `getent` | Kasutaja- ja grupikirjed (ka LDAP-ist/AD-st) | [3](../moodul-03-kasutajad-oigused/index.md) |
| `getfacl` | Näitab ACL-i õigusi | [3](../moodul-03-kasutajad-oigused/index.md) |
| `git` | Versioonihaldus (`init`, `add`, `commit`, `log`, `branch`, `push`) | [6](../moodul-06-bash/index.md) |
| `gpart` | FreeBSD partitsioonide haldus (`gpart show`) | [29](../moodul-29-freebsd/index.md) |
| `gpasswd` | Lisab või eemaldab grupi liikmeid | [3](../moodul-03-kasutajad-oigused/index.md) |
| `gpg` | GnuPG: võtmed, allkirjad ja krüpteerimine | [12](../moodul-12-turvalisus-logid/index.md) |
| `grep` | Otsib mustrile vastavaid ridu (`-r`, `-i`, `-v`, `-E`) | [2](../moodul-02-failid-tekst-torud/index.md) |
| `groupadd` | Loob grupi | [3](../moodul-03-kasutajad-oigused/index.md) |
| `groupdel` | Kustutab grupi | [3](../moodul-03-kasutajad-oigused/index.md) |
| `groups` | Kasutaja grupid | [3](../moodul-03-kasutajad-oigused/index.md) |
| `growpart` | Suurendab partitsiooni ketta lõpuni | [8](../moodul-08-kettad-lvm/index.md) |
| `grub-install` | Paigaldab alglaadija | [11](../moodul-11-alglaadimine-kernel/index.md) |
| `grub-reboot` | Valib kerneli ainult järgmiseks alglaadimiseks | [11](../moodul-11-alglaadimine-kernel/index.md) |
| `grub-set-default` | Valib vaikimisi kerneli | [11](../moodul-11-alglaadimine-kernel/index.md) |
| `grubby` | Kernelite ja alglaadimise parameetrite haldus (AlmaLinux) | [11](../moodul-11-alglaadimine-kernel/index.md) |
| `gzip` | Pakib faili (`gunzip` pakib lahti) | [2](../moodul-02-failid-tekst-torud/index.md) |

## H

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `haproxy` | Koormusejaotur; `haproxy -c -f` seadistuse kontroll | [15](../moodul-15-veebiserverid/index.md) |
| `head` | Faili esimesed read | [1](../moodul-01-sissejuhatus/index.md) |
| `helm` | Kubernetese pakihaldur | [28](../moodul-28-kubernetes/index.md) |
| `history` | Varem sisestatud käskude ajalugu | [1](../moodul-01-sissejuhatus/index.md) |
| `host` | Lihtne DNS-päring | [7](../moodul-07-vork-ssh/index.md) |
| `hostnamectl` | Masina nimi ja süsteemi info; nime muutmine | [1](../moodul-01-sissejuhatus/index.md) |
| `htop` | Mugavam `top` | [5](../moodul-05-protsessid-teenused/index.md) |

## I

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `id` | Kasutaja UID, GID ja grupid | [3](../moodul-03-kasutajad-oigused/index.md) |
| `ifreload` | Debiani ifupdown2 seadistuse uuesti laadimine (Proxmox) | [27](../moodul-27-virtualiseerimine/index.md) |
| `iostat` | Ketaste koormus ja ooteajad | [10](../moodul-10-salvestus/index.md) |
| `ip` | Võrguliidesed, aadressid ja marsruudid (`ip a`, `ip r`) | [7](../moodul-07-vork-ssh/index.md) |
| `iperf3` | Mõõdab võrgu läbilaskevõimet kahe masina vahel | [20](../moodul-20-seire/index.md) |
| `iscsiadm` | iSCSI initsiaator: avastamine ja sisselogimine | [22](../moodul-22-dhcp-pxe-iscsi/index.md) |

## J

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `jexec` | Käivitab käsu FreeBSD jailis | [29](../moodul-29-freebsd/index.md) |
| `jls` | Töötavad FreeBSD jailid | [29](../moodul-29-freebsd/index.md) |
| `jobs` | Kesta taustatööd | [5](../moodul-05-protsessid-teenused/index.md) |
| `journalctl` | systemd logide vaatamine (`-u`, `-f`, `-b`, `-p`) | [5](../moodul-05-protsessid-teenused/index.md) |

## K

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `k3s` | k3s binaarfail (`k3s kubectl`, `k3s etcd-snapshot`) | [28](../moodul-28-kubernetes/index.md) |
| `kea-dhcp4` | Kea DHCP-server; `-t` seadistuse kontroll | [22](../moodul-22-dhcp-pxe-iscsi/index.md) |
| `keepalived` | Virtuaalne IP-aadress VRRP-ga | [15](../moodul-15-veebiserverid/index.md) |
| `kill` | Saadab protsessile signaali (vaikimisi TERM) | [5](../moodul-05-protsessid-teenused/index.md) |
| `killall` | Lõpetab kõik sama nimega protsessid | [5](../moodul-05-protsessid-teenused/index.md) |
| `kinit` | Kerberose pileti hankimine | [25](../moodul-25-samba-ad/index.md) |
| `klist` | Kerberose piletid | [25](../moodul-25-samba-ad/index.md) |
| `ksvalidator` | Kickstarti faili kontroll | [22](../moodul-22-dhcp-pxe-iscsi/index.md) |
| `kubectl` | Kubernetese klastri haldus | [28](../moodul-28-kubernetes/index.md) |

## L

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `last` | Viimased sisselogimised | [3](../moodul-03-kasutajad-oigused/index.md) |
| `ldapadd` | Lisab kirjeid LDIF-failist | [24](../moodul-24-openldap/index.md) |
| `ldapdelete` | Kustutab kirje | [24](../moodul-24-openldap/index.md) |
| `ldapmodify` | Muudab kirjeid | [24](../moodul-24-openldap/index.md) |
| `ldappasswd` | Muudab LDAP-i kasutaja parooli | [24](../moodul-24-openldap/index.md) |
| `ldapsearch` | LDAP-i otsing | [24](../moodul-24-openldap/index.md) |
| `ldapwhoami` | Kontrollib LDAP-i autentimist | [24](../moodul-24-openldap/index.md) |
| `ldconfig` | Uuendab jagatud teekide vahemälu (`-p` näitab teadaolevaid teeke) | [4](../moodul-04-pakihaldus/index.md) |
| `ldd` | Näitab, milliseid jagatud teeke programm vajab | [4](../moodul-04-pakihaldus/index.md) |
| `leapp` | AlmaLinuxi põhiversiooni uuendus (ELevate) | [4](../moodul-04-pakihaldus/index.md) |
| `less` | Pikema faili lehitsemine | [1](../moodul-01-sissejuhatus/index.md) |
| `ln` | Loob viida (`-s` sümboolne) | [2](../moodul-02-failid-tekst-torud/index.md) |
| `localectl` | Keel, lokaat ja klaviatuur | [3](../moodul-03-kasutajad-oigused/index.md) |
| `locate` | Kiire failiotsing andmebaasist | [2](../moodul-02-failid-tekst-torud/index.md) |
| `logger` | Kirjutab teate süsteemilogisse | [12](../moodul-12-turvalisus-logid/index.md) |
| `loginctl` | Sisselogimisseansid; `enable-linger` kasutajateenustele | [14](../moodul-14-konteinerid/index.md) |
| `logrotate` | Logide rotatsioon; `-d` proovirežiim | [12](../moodul-12-turvalisus-logid/index.md) |
| `lpstat` | Printerid ja trükijärjekord | [26](../moodul-26-toolaud-wsl/index.md) |
| `ls` | Kataloogi sisu loetelu (`-l` üksikasjad, `-a` peidetud failid) | [1](../moodul-01-sissejuhatus/index.md) |
| `lsblk` | Plokkseadmed ja partitsioonid puuna | [8](../moodul-08-kettad-lvm/index.md) |
| `lscpu` | Protsessori info | [11](../moodul-11-alglaadimine-kernel/index.md) |
| `lsmod` | Laaditud kerneli moodulid | [11](../moodul-11-alglaadimine-kernel/index.md) |
| `lsof` | Avatud failid ja ühendused protsesside kaupa | [20](../moodul-20-seire/index.md) |
| `lspci` | PCI-seadmed ja kasutatavad draiverid | [11](../moodul-11-alglaadimine-kernel/index.md) |
| `lsusb` | USB-seadmed | [11](../moodul-11-alglaadimine-kernel/index.md) |
| `lvcreate` | Loob loogilise köite (ka hetktõmmise) | [8](../moodul-08-kettad-lvm/index.md) |
| `lvextend` | Suurendab köidet (`-r` koos failisüsteemiga) | [8](../moodul-08-kettad-lvm/index.md) |
| `lvreduce` | Vähendab köidet (ext4; XFS-i vähendada ei saa) | [8](../moodul-08-kettad-lvm/index.md) |
| `lynis` | Süsteemi turvaaudit | [12](../moodul-12-turvalisus-logid/index.md) |

## M

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `mail` | E-kirja saatmine käsurealt | [20](../moodul-20-seire/index.md), [23](../moodul-23-e-post/index.md) |
| `mailq` | Postfixi saatmisjärjekord | [20](../moodul-20-seire/index.md), [23](../moodul-23-e-post/index.md) |
| `make` | Kompileerib tarkvara lähtekoodist `Makefile`-i järgi | [4](../moodul-04-pakihaldus/index.md) |
| `man` | Käsu kasutusjuhend | [1](../moodul-01-sissejuhatus/index.md) |
| `mariadb` | MariaDB klient | [16](../moodul-16-andmebaasid/index.md) |
| `mariadb-dump` | MariaDB andmebaasi varundus SQL-failina | [16](../moodul-16-andmebaasid/index.md) |
| `mdadm` | Tarkvaraline RAID | [10](../moodul-10-salvestus/index.md) |
| `mkdir` | Loob kataloogi (`-p` koos vahekataloogidega) | [1](../moodul-01-sissejuhatus/index.md) |
| `mkfs.ext4` | Loob ext4 failisüsteemi | [8](../moodul-08-kettad-lvm/index.md) |
| `mkfs.vfat` | Loob FAT32-failisüsteemi (`-F 32`) | [8](../moodul-08-kettad-lvm/index.md) |
| `mkfs.xfs` | Loob XFS failisüsteemi | [8](../moodul-08-kettad-lvm/index.md) |
| `mkswap` | Valmistab saaleala ette | [8](../moodul-08-kettad-lvm/index.md) |
| `mktemp` | Loob turvalise ajutise faili või kataloogi | [6](../moodul-06-bash/index.md) |
| `modinfo` | Kerneli mooduli info | [11](../moodul-11-alglaadimine-kernel/index.md) |
| `modprobe` | Laadib või eemaldab kerneli mooduli | [11](../moodul-11-alglaadimine-kernel/index.md) |
| `molecule` | Ansible'i rollide testimine | [19](../moodul-19-automatiseerimine/index.md) |
| `mount` | Haagib failisüsteemi | [8](../moodul-08-kettad-lvm/index.md) |
| `mpstat` | Protsessori koormus tuumade kaupa | [20](../moodul-20-seire/index.md) |
| `mtr` | Pidev teekonna ja kadude mõõtmine | [7](../moodul-07-vork-ssh/index.md) |
| `mv` | Teisaldab või nimetab ümber | [1](../moodul-01-sissejuhatus/index.md) |

## N

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `named-checkconf` | BIND-i seadistuse kontroll | [17](../moodul-17-dns/index.md) |
| `named-checkzone` | DNS-tsoonifaili kontroll | [17](../moodul-17-dns/index.md) |
| `nano` | Lihtne tekstiredaktor | [2](../moodul-02-failid-tekst-torud/index.md) |
| `nc` | Netcat: TCP/UDP pordi testimine | [7](../moodul-07-vork-ssh/index.md) |
| `ncdu` | Interaktiivne kettakasutuse vaade | [8](../moodul-08-kettad-lvm/index.md) |
| `needrestart` | Näitab teenuseid, mis vajavad pärast teegi uuendust taaskäivitust (Debian, Ubuntu) | [4](../moodul-04-pakihaldus/index.md) |
| `netplan` | Ubuntu võrguseadistuse rakendamine (`try`, `apply`) | [7](../moodul-07-vork-ssh/index.md) |
| `nft` | nftables tulemüüri reeglid | [7](../moodul-07-vork-ssh/index.md) |
| `nginx` | Veebiserver; `nginx -t` seadistuse kontroll | [15](../moodul-15-veebiserverid/index.md) |
| `nice` | Käivitab protsessi muudetud prioriteediga | [5](../moodul-05-protsessid-teenused/index.md) |
| `nmap` | Võrgu ja avatud portide skaneerimine | [12](../moodul-12-turvalisus-logid/index.md) |
| `nmcli` | NetworkManageri käsurida (AlmaLinux) | [7](../moodul-07-vork-ssh/index.md) |
| `nohup` | Käivitab käsu, mis ei lõpe seansi sulgemisel | [5](../moodul-05-protsessid-teenused/index.md) |

## O

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `opendkim-genkey` | Loob DKIM-võtmepaari ja DNS-kirje | [23](../moodul-23-e-post/index.md) |
| `opendkim-testkey` | Kontrollib DKIM-võtme DNS-kirjet | [23](../moodul-23-e-post/index.md) |
| `openssl` | Võtmed, sertifikaadid, CA ja TLS-i testimine (`s_client`) | [15](../moodul-15-veebiserverid/index.md) |

## P

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `parted` | Partitsioonide haldus, ka skriptides | [8](../moodul-08-kettad-lvm/index.md) |
| `partprobe` | Teatab kernelile partitsioonitabeli muudatusest | [8](../moodul-08-kettad-lvm/index.md) |
| `passwd` | Muudab parooli; lukustab kontot | [3](../moodul-03-kasutajad-oigused/index.md) |
| `patch` | Rakendab `diff`-iga tehtud paiga | [2](../moodul-02-failid-tekst-torud/index.md) |
| `pct` | Proxmoxi LXC konteinerite haldus | [27](../moodul-27-virtualiseerimine/index.md) |
| `pdbedit` | Samba kasutajate andmebaas (`-L`) | [18](../moodul-18-failiserverid/index.md) |
| `pfctl` | FreeBSD/OPNsense pf tulemüüri olek | [21](../moodul-21-opnsense/index.md) |
| `pg_dump` | PostgreSQL-i andmebaasi varundus | [16](../moodul-16-andmebaasid/index.md) |
| `pg_restore` | PostgreSQL-i varukoopia taastamine | [16](../moodul-16-andmebaasid/index.md) |
| `pgrep` | Leiab protsessi PID-i nime järgi | [5](../moodul-05-protsessid-teenused/index.md) |
| `photorec` | Kustutatud failide taastamine sisu järgi | [10](../moodul-10-salvestus/index.md) |
| `pidstat` | Protsesside ressursikasutus ajas | [20](../moodul-20-seire/index.md) |
| `ping` | Kontrollib ühendust ICMP-ga | [7](../moodul-07-vork-ssh/index.md) |
| `pkg` | FreeBSD pakihaldur (`install`, `upgrade`, `audit`) | [29](../moodul-29-freebsd/index.md) |
| `pkill` | Saadab signaali protsessidele nime järgi | [5](../moodul-05-protsessid-teenused/index.md) |
| `podman` | Konteinerite käivitamine ja haldus (juurkasutajata) | [14](../moodul-14-konteinerid/index.md) |
| `podman-compose` | Mitme konteineri rakendus `compose.yaml` järgi | [14](../moodul-14-konteinerid/index.md) |
| `postfix` | Postfixi juhtimine (`check`, `reload`) | [20](../moodul-20-seire/index.md), [23](../moodul-23-e-post/index.md) |
| `postsuper` | Postfixi järjekorra haldus (kirjade kustutamine) | [23](../moodul-23-e-post/index.md) |
| `proxmox-backup-client` | Varundab Linuxi masina katalooge Proxmox Backup Serverisse | [27](../moodul-27-virtualiseerimine/index.md) |
| `proxmox-backup-manager` | Proxmox Backup Serveri haldus (andmehoidlad, kasutajad, õigused) | [27](../moodul-27-virtualiseerimine/index.md) |
| `ps` | Protsesside loetelu (`aux`, `-ef`) | [5](../moodul-05-protsessid-teenused/index.md) |
| `psql` | PostgreSQL-i klient | [16](../moodul-16-andmebaasid/index.md) |
| `pstree` | Protsesside puu | [5](../moodul-05-protsessid-teenused/index.md) |
| `pvcreate` | Loob LVM-i füüsilise köite | [8](../moodul-08-kettad-lvm/index.md) |
| `pvecm` | Proxmoxi klastri haldus | [27](../moodul-27-virtualiseerimine/index.md) |
| `pvesh` | Proxmoxi API käsurealt | [27](../moodul-27-virtualiseerimine/index.md) |
| `pvesm` | Proxmoxi salvestuse haldus | [27](../moodul-27-virtualiseerimine/index.md) |
| `pveversion` | Proxmoxi versioon | [27](../moodul-27-virtualiseerimine/index.md) |
| `pvs` | Füüsiliste köidete ülevaade (ka `vgs`, `lvs`) | [8](../moodul-08-kettad-lvm/index.md) |
| `pw` | FreeBSD kasutajate ja gruppide haldus | [29](../moodul-29-freebsd/index.md) |
| `pwd` | Näitab praegust kataloogi | [1](../moodul-01-sissejuhatus/index.md) |

## Q

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `qm` | Proxmoxi virtuaalmasinate haldus | [27](../moodul-27-virtualiseerimine/index.md) |
| `qmrestore` | VM-i taastamine varukoopiast | [27](../moodul-27-virtualiseerimine/index.md) |

## R

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `read` | Loeb kasutaja sisendit või faili rida muutujasse | [6](../moodul-06-bash/index.md) |
| `realm` | Masina liitmine domeeniga (`discover`, `join`, `permit`) | [25](../moodul-25-samba-ad/index.md) |
| `renice` | Muudab töötava protsessi prioriteeti | [5](../moodul-05-protsessid-teenused/index.md) |
| `resize2fs` | Muudab ext4 failisüsteemi suurust | [8](../moodul-08-kettad-lvm/index.md) |
| `resolvectl` | systemd-resolved olek ja DNS-serverid | [7](../moodul-07-vork-ssh/index.md) |
| `restic` | Krüpteeritud ja dedubleeritud varundus | [9](../moodul-09-varundus/index.md) |
| `restorecon` | Taastab failide SELinuxi kontekstid | [12](../moodul-12-turvalisus-logid/index.md) |
| `rm` | Kustutab faile (`-r` katalooge); prügikasti ei ole | [1](../moodul-01-sissejuhatus/index.md) |
| `rndc` | BIND9 haldus (`reload`, `flush`, `status`) | [17](../moodul-17-dns/index.md) |
| `rpm` | RPM-pakettide päring (`-qa`, `-ql`, `-qf`) | [4](../moodul-04-pakihaldus/index.md) |
| `rsync` | Failide sünkroniseerimine (ainult muudatused) | [7](../moodul-07-vork-ssh/index.md) |

## S

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `samba-tool` | Samba AD domeeni haldus (kasutajad, grupid, DNS, varundus) | [25](../moodul-25-samba-ad/index.md) |
| `sar` | Jõudlusandmete ajalugu | [20](../moodul-20-seire/index.md) |
| `scp` | Failide kopeerimine SSH kaudu | [7](../moodul-07-vork-ssh/index.md) |
| `sed` | Voogredaktor: teksti asendamine failides ja torudes | [2](../moodul-02-failid-tekst-torud/index.md) |
| `semanage` | SELinuxi püsivad kontekstid, pordid ja kasutajad | [12](../moodul-12-turvalisus-logid/index.md) |
| `sestatus` | SELinuxi üksikasjalik olek | [12](../moodul-12-turvalisus-logid/index.md) |
| `set` | Kesta valikud (`set -euo pipefail`) | [6](../moodul-06-bash/index.md) |
| `setenforce` | Muudab SELinuxi režiimi ajutiselt | [12](../moodul-12-turvalisus-logid/index.md) |
| `setfacl` | Seab ACL-i õigusi | [3](../moodul-03-kasutajad-oigused/index.md) |
| `setsebool` | SELinuxi tõeväärtused (`-P` püsivalt) | [12](../moodul-12-turvalisus-logid/index.md) |
| `sha256sum` | Arvutab ja kontrollib (`-c`) SHA-256 kontrollsummasid | [12](../moodul-12-turvalisus-logid/index.md) |
| `shellcheck` | Leiab Bashi skriptidest vigu ja halbu tavasid | [6](../moodul-06-bash/index.md) |
| `showmount` | NFS-serveri jagatud kataloogid kliendi poolelt | [18](../moodul-18-failiserverid/index.md) |
| `slapadd` | LDIF-i import andmebaasi (taastamine) | [24](../moodul-24-openldap/index.md) |
| `slapcat` | LDAP-i andmebaasi eksport LDIF-iks (varundus) | [24](../moodul-24-openldap/index.md) |
| `slappasswd` | Loob LDAP-i parooliräsi | [24](../moodul-24-openldap/index.md) |
| `smartctl` | Ketta tervis (SMART) | [10](../moodul-10-salvestus/index.md) |
| `smbclient` | Samba/Windowsi jagatud kaustade klient | [18](../moodul-18-failiserverid/index.md) |
| `smbpasswd` | Samba kasutaja parool | [18](../moodul-18-failiserverid/index.md) |
| `smbstatus` | Samba ühendused ja lukustatud failid | [18](../moodul-18-failiserverid/index.md) |
| `snap` | Snap-pakettide haldus | [4](../moodul-04-pakihaldus/index.md) |
| `sockstat` | FreeBSD kuulavad pordid (nagu `ss`) | [21](../moodul-21-opnsense/index.md) |
| `sort` | Sorteerib ridu | [2](../moodul-02-failid-tekst-torud/index.md) |
| `sqlite3` | SQLite andmebaasi klient | [16](../moodul-16-andmebaasid/index.md) |
| `ss` | Kuulavad pordid ja ühendused (`-tulpn`) | [7](../moodul-07-vork-ssh/index.md) |
| `ssh` | Turvaline kaugühendus serverisse | [1](../moodul-01-sissejuhatus/index.md) |
| `ssh-agent` | Hoiab lahtikrüpteeritud võtmeid mälus | [7](../moodul-07-vork-ssh/index.md) |
| `ssh-copy-id` | Kopeerib avaliku võtme serverisse | [7](../moodul-07-vork-ssh/index.md) |
| `ssh-keygen` | Loob SSH-võtmepaari | [7](../moodul-07-vork-ssh/index.md) |
| `sshd` | SSH-server; `sshd -t` seadistuse kontroll, `sshd -T` tegelikud seaded | [7](../moodul-07-vork-ssh/index.md) |
| `strace` | Protsessi süsteemikutsete jälgimine | [20](../moodul-20-seire/index.md) |
| `su` | Vahetab kasutajat | [3](../moodul-03-kasutajad-oigused/index.md) |
| `sudo` | Käivitab käsu teise kasutajana (vaikimisi juurkasutajana) | [3](../moodul-03-kasutajad-oigused/index.md) |
| `swaks` | SMTP-serveri testimine (ka TLS ja autentimine) | [23](../moodul-23-e-post/index.md) |
| `swapon` | Aktiveerib saaleala; `--show` näitab olekut | [8](../moodul-08-kettad-lvm/index.md) |
| `sysctl` | Kerneli parameetrid (`-a`, `-w`, `--system`) | [11](../moodul-11-alglaadimine-kernel/index.md) |
| `sysrc` | Muudab FreeBSD `rc.conf`-i seadeid | [29](../moodul-29-freebsd/index.md) |
| `systemctl` | systemd teenuste ja üksuste haldus (`start`, `enable`, `status`) | [5](../moodul-05-protsessid-teenused/index.md) |
| `systemd-analyze` | Alglaadimise aeg ja aeglased üksused | [11](../moodul-11-alglaadimine-kernel/index.md) |
| `systemd-cgtop` | Ressursikasutus cgroup'ide kaupa | [5](../moodul-05-protsessid-teenused/index.md) |
| `systemd-delta` | Näitab, millised paketi üksused ja seadistusfailid on üle kirjutatud | [11](../moodul-11-alglaadimine-kernel/index.md) |
| `systemd-run` | Käivitab käsu ajutise systemd üksusena (ka piirangutega) | [5](../moodul-05-protsessid-teenused/index.md) |

## T

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `tail` | Faili viimased read (`-f` jälgib jooksvalt) | [1](../moodul-01-sissejuhatus/index.md) |
| `tar` | Arhiveerib ja pakib (`-czf` loo, `-xzf` paki lahti, `-tzf` vaata) | [2](../moodul-02-failid-tekst-torud/index.md) |
| `targetcli` | iSCSI sihtmärgi seadistus (LIO) | [22](../moodul-22-dhcp-pxe-iscsi/index.md) |
| `tcpdump` | Võrguliikluse pealtkuulamine ja analüüs | [7](../moodul-07-vork-ssh/index.md) |
| `tee` | Kirjutab sisendi nii ekraanile kui ka faili | [2](../moodul-02-failid-tekst-torud/index.md) |
| `test` | Tingimuse kontroll (`[ ]`) | [6](../moodul-06-bash/index.md) |
| `testdisk` | Kadunud partitsioonide taastamine | [10](../moodul-10-salvestus/index.md) |
| `testparm` | Samba seadistuse kontroll | [18](../moodul-18-failiserverid/index.md) |
| `tftp` | TFTP klient testimiseks | [22](../moodul-22-dhcp-pxe-iscsi/index.md) |
| `timedatectl` | Kellaaeg, ajavöönd ja NTP olek | [7](../moodul-07-vork-ssh/index.md) |
| `tmux` | Terminali multiplekser: seansid jäävad alles ka pärast lahtiühendamist | [5](../moodul-05-protsessid-teenused/index.md) |
| `tofu` | OpenTofu: infrastruktuur koodina (`plan`, `apply`) | [19](../moodul-19-automatiseerimine/index.md) |
| `top` | Protsesside ja koormuse reaalajas vaade | [5](../moodul-05-protsessid-teenused/index.md) |
| `touch` | Loob tühja faili või uuendab muutmisaega | [1](../moodul-01-sissejuhatus/index.md) |
| `tr` | Asendab või kustutab märke | [2](../moodul-02-failid-tekst-torud/index.md) |
| `tracepath` | Näitab teekonda sihtmärgini | [7](../moodul-07-vork-ssh/index.md) |
| `trap` | Käivitab käsu signaali või skripti lõpu korral | [6](../moodul-06-bash/index.md) |
| `tune2fs` | Muudab ext-failisüsteemi seadeid (silt, reserveeritud ruum) | [8](../moodul-08-kettad-lvm/index.md) |
| `tuned-adm` | Jõudlusprofiilide valik | [20](../moodul-20-seire/index.md) |
| `type` | Näitab, kas käsk on programm, sisekäsk või alias | [2](../moodul-02-failid-tekst-torud/index.md) |

## U

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `udevadm` | udev: seadme info (`info`), sündmused (`monitor`), reeglite rakendamine | [11](../moodul-11-alglaadimine-kernel/index.md) |
| `ufw` | Ubuntu lihtne tulemüür | [7](../moodul-07-vork-ssh/index.md) |
| `ulimit` | Kesta ja protsesside ressursipiirangud | [5](../moodul-05-protsessid-teenused/index.md) |
| `umask` | Uute failide vaikimisi õigused | [3](../moodul-03-kasutajad-oigused/index.md) |
| `umount` | Lahutab failisüsteemi | [8](../moodul-08-kettad-lvm/index.md) |
| `uname` | Kerneli ja arhitektuuri info | [1](../moodul-01-sissejuhatus/index.md) |
| `uniq` | Eemaldab või loendab järjestikused korduvad read (`-c`) | [2](../moodul-02-failid-tekst-torud/index.md) |
| `update-grub` | Genereerib GRUB-i menüü (Debian, Ubuntu) | [11](../moodul-11-alglaadimine-kernel/index.md) |
| `update-initramfs` | Loob initramfs-i uuesti (Debian, Ubuntu) | [11](../moodul-11-alglaadimine-kernel/index.md) |
| `uptime` | Kui kaua süsteem on töötanud ja keskmine koormus | [1](../moodul-01-sissejuhatus/index.md) |
| `useradd` | Loob kasutaja | [3](../moodul-03-kasutajad-oigused/index.md) |
| `userdel` | Kustutab kasutaja (`-r` koos kodukataloogiga) | [3](../moodul-03-kasutajad-oigused/index.md) |
| `usermod` | Muudab kasutajat (nt `-aG` lisagrupp) | [3](../moodul-03-kasutajad-oigused/index.md) |

## V

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `vagrant` | Laborimasinad Vagrantfile'i järgi | [19](../moodul-19-automatiseerimine/index.md) |
| `valkey-cli` | Valkey/Redise klient | [16](../moodul-16-andmebaasid/index.md) |
| `vgcreate` | Loob köitegrupi | [8](../moodul-08-kettad-lvm/index.md) |
| `vgextend` | Lisab köitegrupile ketta | [8](../moodul-08-kettad-lvm/index.md) |
| `vim` | Võimas režiimidega tekstiredaktor | [2](../moodul-02-failid-tekst-torud/index.md) |
| `vipw` | Kasutajafaili turvaline muutmine (FreeBSD `master.passwd`) | [29](../moodul-29-freebsd/index.md) |
| `virsh` | libvirt-i virtuaalmasinate haldus | [27](../moodul-27-virtualiseerimine/index.md) |
| `virt-install` | Loob virtuaalmasina käsurealt | [27](../moodul-27-virtualiseerimine/index.md) |
| `visudo` | Muudab sudoers-faili süntaksikontrolliga | [3](../moodul-03-kasutajad-oigused/index.md) |
| `vmstat` | Mälu, protsessori ja I/O ülevaade ajas | [20](../moodul-20-seire/index.md) |
| `vzdump` | Proxmoxi varukoopia | [27](../moodul-27-virtualiseerimine/index.md) |

## W

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `wc` | Loendab ridu, sõnu ja märke | [2](../moodul-02-failid-tekst-torud/index.md) |
| `wg` | WireGuard VPN-i olek ja võtmed | [13](../moodul-13-vorgu-suvendus/index.md) |
| `wg-quick` | Tõstab WireGuardi liidese üles failist `/etc/wireguard/wg0.conf` | [13](../moodul-13-vorgu-suvendus/index.md) |
| `whereis` | Programmi, lähtekoodi ja kasutusjuhendi asukohad | [1](../moodul-01-sissejuhatus/index.md) |
| `which` | Näitab, millisest kataloogist käsk käivitatakse | [2](../moodul-02-failid-tekst-torud/index.md) |
| `who` | Hetkel sisse loginud kasutajad | [3](../moodul-03-kasutajad-oigused/index.md) |
| `whoami` | Näitab praegust kasutajat | [1](../moodul-01-sissejuhatus/index.md) |
| `wrk` | Kestusepõhine HTTP koormustest | [15](../moodul-15-veebiserverid/index.md) |
| `wsl` | WSL-i haldus Windowsis (`--install`, `-l -v`, `--shutdown`) | [26](../moodul-26-toolaud-wsl/index.md) |

## X

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `xargs` | Teeb sisendi ridadest teise käsu argumendid | [2](../moodul-02-failid-tekst-torud/index.md) |
| `xe` | XCP-ng käsurida | [27](../moodul-27-virtualiseerimine/index.md) |
| `xfs_admin` | Muudab XFS-i seadeid (nt silt `-L`) | [8](../moodul-08-kettad-lvm/index.md) |
| `xfs_growfs` | Suurendab XFS failisüsteemi | [8](../moodul-08-kettad-lvm/index.md) |

## Z

| Käsk | Mida teeb | Moodul |
|---|---|---|
| `zcat` | Näitab pakitud faili sisu lahti pakkimata | [2](../moodul-02-failid-tekst-torud/index.md) |
| `zfs` | ZFS-i andmekogumid, hetktõmmised ja `send`/`receive` | [10](../moodul-10-salvestus/index.md) |
| `zpool` | ZFS-i kogumite haldus (`create`, `status`, `scrub`) | [10](../moodul-10-salvestus/index.md) |
| `zypper` | SUSE pakihaldur | [4](../moodul-04-pakihaldus/index.md) |

<!-- navigatsioon -->
---

[← Sõnastik](sonastik.md) · [Sisukord](../../README.md#sisukord)
<!-- /navigatsioon -->
