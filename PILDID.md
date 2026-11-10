# Ekraanipiltide plaan

Materjalis on peidetud kohatäited kujul `<!-- PILT: ../pildid/FAIL.png | kirjeldus -->`. Need ei ole veebilehel nähtavad. Kui pilt on tehtud, salvesta see kausta `docs/pildid/` täpselt allolevas tabelis toodud nimega - seejärel asendatakse kohatäide pildiga (`![kirjeldus](../pildid/FAIL.png)`).

## Nõuded piltidele

- vorming **PNG**, laius 1200-1600 px; lõika välja ainult vajalik aken (mitte kogu ekraan);
- hele teema, suurendus 100%; tekst peab olema loetav ka telefonis;
- **ära jäta pildile**: paroole, võtmeid, tokeneid, kooli avalikke IP-aadresse, päris õpilaste nimesid - kasuta laboriaadresse (`10.0.83.x`) ja näidisnimesid (`mari`, `IT24-MariMaasikas`);
- failinimes ainult väiketähed, numbrid ja sidekriipsud (täpitähti ei kasutata);
- kui menüü nimi pildil erineb tekstist (uuem versioon), anna teada - tekst tuleb siis samuti üle vaadata.

## Pildid

| Fail | Mida pildistada | Kus materjalis |
|---|---|---|
| `lisa-hkhk-proxmox-sisselogimine.png` | HKHK Proxmoxi sisselogimisaken (realm valik); õppija masinad vasakus puus | `docs/lisad/paigaldus.md`, Sisselogimine |
| `lisa-proxmox-loo-vm.png` | Proxmoxi *Create VM* aken, vahekaart *Hardware* või kokkuvõte (*Confirm*) | `docs/lisad/paigaldus.md`, 3. Virtuaalmasina loomine Proxmoxis |
| `lisa-debian-tarkvara-valik.png` | Debiani paigaldaja tarkvara valik: ainult *SSH server* ja *standard system utilities* | `docs/lisad/paigaldus.md`, 4. Debian 13 paigaldus |
| `lisa-ubuntu-openssh.png` | Ubuntu paigaldaja *SSH configuration* (Install OpenSSH server märgitud) | `docs/lisad/paigaldus.md`, 5. Ubuntu Server 24.04 LTS paigaldus |
| `lisa-alma-paigalduse-kokkuvote.png` | AlmaLinuxi paigaldaja *Installation Summary* (Minimal Install, ketas, kasutaja) | `docs/lisad/paigaldus.md`, 6. AlmaLinux 10 paigaldus |
| `m01-esimene-ssh-uhendus.png` | Windows Terminal: esimene `ssh` ühendus koos sõrmejälje küsimusega | `docs/moodul-01-sissejuhatus/index.md`, 1.4 Ühendumine serveriga SSH kaudu |
| `m12-wazuh-armatuurlaud.png` | Wazuhi veebiliidese ülevaade (agentide olek, turvasündmused) | `docs/moodul-12-turvalisus-logid/index.md`, 12.11 Turvasündmuste haldus: Wazuh |
| `m15-brauseri-hoiatus.png` | Brauseri hoiatus isesigneeritud sertifikaadi korral | `docs/moodul-15-veebiserverid/index.md`, Labor ja päris maailm |
| `m15-sertifikaadi-ahel.png` | Brauseri sertifikaadivaade: labori CA → serveri sertifikaat (pärast CA usaldamist) | `docs/moodul-15-veebiserverid/index.md`, Oma CA (sisevõrk ja labor) |
| `m20-grafana-node-exporter.png` | Grafana töölaud *Node Exporter Full* (CPU, mälu, ketas) | `docs/moodul-20-seire/index.md`, Grafana |
| `m20-uptime-kuma.png` | Uptime Kuma jälgitavate teenuste nimekiri | `docs/moodul-20-seire/index.md`, 20.6 Kättesaadavus: Uptime Kuma |
| `m21-konsoolimenuu.png` | OPNsense'i konsoolimenüü (liidesed ja aadressid, valikud 0-13) | `docs/moodul-21-opnsense/index.md`, Konsoolimenüü |
| `m21-armatuurlaud.png` | OPNsense'i veebiliidese armatuurlaud (*Lobby → Dashboard*) | `docs/moodul-21-opnsense/index.md`, Veebiliides |
| `m21-tulemuurireeglid.png` | *Firewall → Rules → LAN* reeglite loend | `docs/moodul-21-opnsense/index.md`, Reegli osad |
| `m21-pordisuunamine.png` | *Firewall → NAT → Port Forward* reegli vorm | `docs/moodul-21-opnsense/index.md`, NAT ja pordisuunamine |
| `m22-netbootxyz-menuu.png` | netboot.xyz menüü võrgust alglaadimisel | `docs/moodul-22-dhcp-pxe-iscsi/index.md`, Automaatne paigaldus: kickstart, preseed ja autoinstall |
| `m24-lam-kasutajad.png` | LAM-i kasutajate loend (`ou=kasutajad`) | `docs/moodul-24-openldap/index.md`, 24.4 LDIF ja kirjete haldus |
| `m25-aduc.png` | *Active Directory Users and Computers* Samba domeeniga | `docs/moodul-25-samba-ad/index.md`, RSAT - haldus Windowsist |
| `m25-gpo-haldus.png` | *Group Policy Management* - lingitud rühmapoliitika | `docs/moodul-25-samba-ad/index.md`, Rühmapoliitika näide |
| `m26-gnome-toolaud.png` | Ubuntu GNOME töölaud (*Activities* vaade) | `docs/moodul-26-toolaud-wsl/index.md`, 26.3 Graafiline süsteem |
| `m26-wsl-terminal.png` | Windows Terminal: PowerShell `wsl -l -v` ja Ubuntu vahekaart | `docs/moodul-26-toolaud-wsl/index.md`, Paigaldus ja põhikäsud (PowerShell) |
| `m27-proxmox-ulevaade.png` | Proxmoxi veebiliides: sõlm, VM-id ja konteinerid, *Summary* | `docs/moodul-27-virtualiseerimine/index.md`, Virtuaalmasinad |
| `m27-proxmox-varunduse-too.png` | *Datacenter → Backup* ajastatud varunduse töö | `docs/moodul-27-virtualiseerimine/index.md`, Varundus, mallid ja kloonid |
| `m27-pbs-andmehoidla.png` | PBS-i andmehoidla *Summary* koos deduplitseerimisteguriga | `docs/moodul-27-virtualiseerimine/index.md`, Proxmox Backup Server |
| `m27-cloud-init.png` | VM-i vahekaart *Cloud-Init* (kasutaja, SSH-võti, IP) | `docs/moodul-27-virtualiseerimine/index.md`, Cloud-init mall |
| `m27-xen-orchestra.png` | Xen Orchestra VM-ide loend | `docs/moodul-27-virtualiseerimine/index.md`, Xen Orchestra |
| `m29-bsdinstall-zfs.png` | bsdinstall *ZFS Configuration* aken | `docs/moodul-29-freebsd/index.md`, 29.2 Paigaldus |
| `m29-alglaadija-be.png` | FreeBSD alglaadija menüü, *Boot Environments* valik | `docs/moodul-29-freebsd/index.md`, 29.9 ZFS ja alglaadimiskeskkonnad |

Kokku 28 pilti. Kõige suurem mõju on OPNsense'i (moodul 21), Proxmoxi ja PBS-i (moodul 27) ning paigalduslisa piltidel - neid samme tehakse veebiliideses ja tekst üksi on algajale raske.

## Logod ja maskotid (README ja avaleht)

Salvesta kausta `docs/pildid/logod/`. Ära muuda logode värve ega proportsioone (ainult suurus).

| Fail | Mis | Kust |
|---|---|---|
| `tux.svg` | Tux (Larry Ewing), SVG | Wikimedia Commons „Tux.svg“ |
| `bsd-daemon.svg` | BSD deemon (M. K. McKusick), SVG | mckusick.com/beastie/ (ametlikud pildid) või freebsd.org → *Logo* |
| `debian.svg` | Debian Open Use Logo koos nimega (`openlogo.svg`) | debian.org/logos/ |
| `ubuntu.svg` | Ubuntu logo | design.ubuntu.com → *Brand* või ubuntu.com → *Logos* |
| `almalinux.svg` | AlmaLinuxi logo (horisontaalne) | almalinux.org/branding/ |
