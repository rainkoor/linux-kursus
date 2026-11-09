# Laborikeskkond ja serverite paigaldus

Kursuse laboritööd eeldavad, et sul on olemas **Debiani**, **Ubuntu** ja **AlmaLinuxi** virtuaalmasinad, millele saad SSH kaudu ligi. See lisa kirjeldab, kuidas laborikeskkond planeerida, virtuaalmasinad luua ja kõik kolm distrot serveriks paigaldada.

> [!NOTE]
> **HKHK õppijale: masinad on enamasti juba olemas.** Kooli Proxmoxis on iga laboritöö jaoks vajalikud virtuaalmasinad valmis tehtud mallidest - **ise ei pea midagi paigaldama**. Sinu jaoks on olulised punktid 1 (sisselogimine ja oma võrk), 2 (võrguplaan) ja 7 (esimesed sammud: parool, hostinimi, IP-aadress, uuendused). Punktid 3-6 ja 8 (VM-i loomine, distrode paigaldus, mallid) on vajalikud ainult erijuhtudel: kui laboritöö või projekt seda eraldi nõuab (nt moodul 19 PXE-paigaldus, moodul 23, lõpuprojekt) või kui õpetaja nii ütleb. Iseõppija vajab kõiki punkte.

Juhend on kirjutatud eelkõige **Proxmox VE** jaoks (HKHK labor), kuid lisatud on ka märkused **VirtualBoxi** ja **WSL-i** kasutajatele.

---

## 1. HKHK Proxmoxi labor

> [!TIP]
> See osa on mõeldud **HKHK õppijatele**. Iseõppija võib selle vahele jätta ja kasutada oma Proxmoxi, VirtualBoxi või muud keskkonda - võrguplaan (punkt 2) on hea tava igal pool.

Haapsalu Kutsehariduskeskuses on õppetöö jaoks mitu Proxmox VE klastrit. Igal õppijal on seal oma labor: virtuaalmasinad ja **eraldi IPv4 privaatvõrk**, mis ei kattu teiste sama serveri kasutajate võrkudega. Laboritöö masinad on loodud õpetaja mallidest ja leiad need Proxmoxi veebiliidesest oma kasutaja alt - kui mõni masin on puudu, pöördu õpetaja poole, mitte ära loo seda ise.

### Sisselogimine

1. Ava brauseris klastri aadress (pordiga `8006`), mille annab õpetaja. Brauser hoiatab iseallkirjastatud sertifikaadi eest - see on laboris oodatud.
2. Kasutajanimi ja parool on samad mis kooli **Liivakasti** keskkonnas.
3. Vali rippmenüüst **Realm: `hkhk.edu.ee`** (mitte vaikimisi *Linux PAM standard authentication*).

Uue kasutaja parool on esialgu sama mis tema AD (kooli) kontol. Parooli saab muuta, kui logid SSH-ga Liivakasti serverisse ja käivitad seal käsu `passwd`:

```bash
ssh <kasutajanimi>@liivakast.hkhk.edu.ee
passwd
```

Virtuaalmasinate mallides on eelnevalt loodud kasutajad. Nende nimed ja esialgsed paroolid annab õpetaja - **muuda parool kohe pärast esimest sisselogimist** (`passwd`), sest kõigis mallides on algul sama parool.

<!-- PILT: ../pildid/lisa-hkhk-proxmox-sisselogimine.png | HKHK Proxmoxi sisselogimisaken (realm valik); õppija masinad vasakus puus -->

### Virtuaalmasinate kasutamine

- Käivita masin topeltklõpsuga ja *Start Now* või paremklõps → *Start*. **Käivita ainult selle labori masinad, millega parasjagu töötad** - ressursse jagavad kõik õppijad.
- Masina ekraan avaneb topeltklõpsuga, täisekraan vasakult menüüst *Full Screen*.
- ISO-faili ühendamiseks: masin → *Hardware* → *CD/DVD Drive* → *Use CD/DVD disc image file (iso)*, *Storage*: `local` ja vali fail.

### Oma võrgu leidmine

Vaata oma mõne virtuaalmasina *Hardware* → *Network Device*:

| Võrguseade | Sinu võrk | Vaikelüüs |
|---|---|---|
| `vmbrX` (nt `vmbr208`) | `10.0.X.0/24` (nt `10.0.208.0/24`) | `10.0.X.1` |
| `vnetX` (SDN) | `192.168.X.0/24` | `192.168.X.1` |

**Alguses ei ole võrgus DHCP-serverit**, sest paljudes laborites seadistab õppija selle ise (moodulid 18 ja 19). Seepärast seadista masinate võrk esialgu käsitsi (moodul 7 ja punkt 7 allpool).

Selle kursuse näidetes on õppija võrguks `10.0.83.0/24` - asenda `83` oma võrgu numbriga.

### Probleemid ja lahendused

| Probleem | Lahendus |
|---|---|
| Veebiliides on aeglane, konsooliühendused katkevad | Palju kasutajaid pöördub korraga klastri ühise aadressi poole. Kasuta selle **sõlme (serveri) aadressi**, kus sinu masinad asuvad. |
| Hetktõmmis võtab kaua ja lukustab masina | Lülita masin enne hetktõmmist välja ja **ära salvesta RAM-i sisu** (*Include RAM* maha). |
| Masin ei reageeri peatamisele | Pöördu õpetaja poole. Administraator kasutab `qm unlock <vmid>` ja `qm stop <vmid>`, viimase abinõuna protsessi `kill -9`. |
| `Installed QEMU version … is too old to run machine type …` | Mall on tehtud uuemas Proxmoxis. Muuda masina *Hardware* → *Machine* versioon vanemaks (või õpetaja uuendab sõlme). |

---

## 2. Võrguplaan

Enne virtuaalmasinate loomist tee **võrguplaan**. See hoiab ära IP-aadresside konfliktid ja on hiljem dokumentatsiooni osa.

### Võrgu andmed

| Võrk | Vaikelüüs | Võrgumask | Leviaadress | DHCP vahemik |
|---|---|---|---|---|
| `10.0.83.0/24` | `10.0.83.1` | `255.255.255.0` | `10.0.83.255` | `10.0.83.80`–`10.0.83.99` |

### IP-aadresside plaan

Kursuse laboritööd kasutavad seda plaani. Sama masin teenib mitut laboritööd: nt `debian1` on veebi-, andmebaasi- ja DNS-server (laboritööd 13–15), DHCP-server (19) ja LDAP-server (20).

| Virtuaalmasina nimi | Hostinimi | IP-aadress | Teenused (laboritööd) |
|---|---|---|---|
| `debian1-IT24-MariMaasikas` | `debian1` | `10.0.83.52` | SSH, veeb (13), andmebaasid (14), DNS ja e-post (15), DHCP/PXE (19), LDAP (20) |
| `debian2-IT24-MariMaasikas` | `debian2` | `10.0.83.53` | SSH, Samba, NFS (15), iSCSI (19) |
| `ubuntu-IT24-MariMaasikas` | `ubuntusrv` | `10.0.83.54` | SSH, tulemüür (7, 11), konteinerid (12), seire (17), Pi-hole (15B) |
| `alma-IT24-MariMaasikas` | `alma` | `10.0.83.55` | SSH, SELinux (11), konteinerid ja Ansible'i juhtmasin (12, 16), Apache (13) |
| `dc1-IT24-MariMaasikas` | `dc1` | `10.0.83.56` | Samba AD DC (21) |
| `ubuntuklient-IT24-MariMaasikas` | `ubuntuklient` | DHCP (`10.0.83.98` reserveeritud) | töölaud (22), domeeni liige (20–21) |
| `winklient-IT24-MariMaasikas` | `winklient` | DHCP (`10.0.83.99` reserveeritud) | Windowsi klient (15, 21, 22) |
| `k3s1-IT24-MariMaasikas` … `k3s3-…` | `k3s1`, `k3s2`, `k3s3` | `10.0.83.61`–`10.0.83.63` | Kubernetese klaster (24) |
| `pbs-IT24-MariMaasikas` | `pbs` | `10.0.83.65` | Proxmox Backup Server (23) |
| `fbsd-IT24-MariMaasikas` | `fbsd` | `10.0.83.66` (jail `www`: `10.0.83.67`) | FreeBSD server (25) |
| - | - | `10.0.83.50` | virtuaalne IP (keepalived, 13) |
| - | - | `10.0.83.64` | k3s klastri virtuaalne IP (24, lisaülesanne) |

Ruuteriks (`.1`) on Proxmoxi sild või moodulis 18 sinu enda OPNsense.

Head tavad:

- **serveritel staatilised aadressid**, klientidel DHCP;
- staatilised aadressid ja DHCP vahemik **ei tohi kattuda**;
- vaikelüüs (ruuter) on tavaliselt võrgu esimene aadress (`.1`);
- virtuaalmasina nimes on rühm ja õppija nimi, et Proxmoxis oleks selge, kellele masin kuulub;
- hostinimi on lühike, väiketähtedega ja kirjeldab rolli.

> [!NOTE]
> Võrguplaani mall sobib ka lõpuprojekti dokumentatsiooni. Täienda seda iga uue masina ja teenuse lisamisel.

---

## 3. Virtuaalmasina loomine Proxmoxis

> [!NOTE]
> **HKHK õppija:** seda punkti (ja punkte 4-6) on vaja ainult siis, kui laboritöö või projekt nõuab uue masina loomist ja paigaldamist. Tavaliselt on masinad olemas - jätka punktist 7.

Proxmoxi veebiliideses: paremklõps sõlmel → **Create VM**.

| Vaheleht | Seade | Soovitus |
|---|---|---|
| General | Name | Võrguplaani järgi, nt `debian1-IT24-MariMaasikas` |
| OS | ISO image | Distro paigaldusmeedia (vt allpool) |
| | Guest OS | Linux, 6.x – 2.6 Kernel |
| System | Graphic card | Default |
| | Machine, BIOS | Vaikimisi (i440fx, SeaBIOS). UEFI (OVMF) ainult siis, kui seda on vaja |
| | SCSI Controller | VirtIO SCSI single |
| | Qemu Agent | ✔ (paigalda masinasse hiljem `qemu-guest-agent`) |
| Disks | Disk size | 20 GiB (FOG-i ja Wazuhi jaoks rohkem) |
| | Discard | ✔, kui salvestus on SSD/ZFS |
| CPU | Cores | 1–2 |
| | Type | **host** (või `x86-64-v3`) - vt AlmaLinuxi märkust |
| Memory | Memory | 2048 MiB |
| Network | Bridge | Õpetaja antud sild või SDN VNet |
| | Model | VirtIO (paravirtualized) |

> [!NOTE]
> **AlmaLinux 10 ja protsessori tüüp.** AlmaLinux 10 (nagu RHEL 10) on vaikimisi kompileeritud protsessoritasemele **x86-64-v3**. Proxmoxi vaikimisi CPU-tüüp `x86-64-v2-AES` seda ei toeta ja paigaldusmeedia jookseb käivitamisel kokku. Lahendused:
>
> - vali CPU tüübiks **host** (kui kõik klastri sõlmed on sarnase protsessoriga) või **x86-64-v3**;
> - või kasuta AlmaLinuxi **x86_64_v2** paigaldusmeediat, mis töötab ka vanematel protsessoritel.

<!-- PILT: ../pildid/lisa-proxmox-loo-vm.png | Proxmoxi *Create VM* aken, vahekaart *Hardware* või kokkuvõte (*Confirm*) -->

### Paigaldusmeedia

| Distro | Paigaldusmeedia | Allalaadimine |
|---|---|---|
| Debian 13 | `debian-13.x.x-amd64-netinst.iso` | debian.org/distrib |
| Ubuntu Server 24.04 LTS | `ubuntu-24.04.x-live-server-amd64.iso` | ubuntu.com/download/server |
| AlmaLinux 10 | `AlmaLinux-10-latest-x86_64-minimal.iso` või `…-x86_64_v2-minimal.iso` | almalinux.org/get-almalinux |

Eestis on kiire peegel **mirrors.xtom.ee**, kust saab alla laadida kõiki kolme. Proxmoxis saab ISO laadida otse URL-ilt: *local* → *ISO Images* → *Download from URL*.

---

## 4. Debian 13 paigaldus

1. **Paigaldusviis:** *Graphical install* või *Install* - funktsionaalselt sama. Kui sa ei vali kiiresti, käivitub viimane valik (kõnesüntees).
2. **Keel, asukoht, klaviatuur:** Eesti. Keel määrab ka süsteemi vaikekeele.
3. **Võrk:** kui võrgus on DHCP, seadistatakse võrk automaatselt. Staatilise aadressi jaoks vajuta automaatseadistuse ajal *Cancel* ja vali *Configure network manually* - sisesta IP, mask, vaikelüüs ja DNS võrguplaani järgi.
4. **Hostinimi:** võrguplaani järgi (nt `debian1`). **Domeen:** võib jääda tühjaks.
5. **Juurkasutaja parool: jäta tühjaks.** Siis paigaldatakse `sudo` ja esimene kasutaja lisatakse gruppi `sudo` - nagu Ubuntus.
6. **Kasutaja:** sinu nimi ja kasutajanimi, tugev parool.
7. **Partitsioneerimine:**
   - *Juhitud – kasuta tervet ketast* ja skeem *Eraldi /var ja /srv partitsioonid* - kiiresti kasvavad logid või andmed ei täida juurfailisüsteemi;
   - või *Juhitud – kasuta tervet ketast ja seadista LVM* - partitsioonide suurust on hiljem lihtsam muuta (vt moodul 8).
8. **Pakihaldur:** peegel Eestist (`deb.debian.org` valib ise kiireima, `mirrors.xtom.ee` on Eestis). Puhverserver tühi, populaarsuse uuringust võib keelduda.
9. **Tarkvara:** ainult **SSH server** ja **standard system utilities**. **Mitte töölauakeskkonda** - server ei vaja seda ja see suurendab ründepinda ning uuendamist vajavate pakettide hulka.
10. **GRUB:** paigalda põhikettale (`/dev/sda`).
11. **Taaskäivitus** - eemalda paigaldusmeedia (Proxmoxis *Hardware* → *CD/DVD* → *Do not use any media*).

<!-- PILT: ../pildid/lisa-debian-tarkvara-valik.png | Debiani paigaldaja tarkvara valik: ainult *SSH server* ja *standard system utilities* -->

## 5. Ubuntu Server 24.04 LTS paigaldus

1. **Keel:** English (eesti keelt paigaldaja ei paku). **Klaviatuur:** Estonian.
2. **Paigalduse tüüp:** *Ubuntu Server* (mitte *Minimized* - sealt puuduvad paljud haldustööriistad). Kolmanda osapoole draivereid pole vaja.
3. **Võrk:** DHCP või staatiline aadress (*Edit IPv4* → *Manual*).
4. **Puhverserver:** tühi. **Peegel:** `http://archive.ubuntu.com/ubuntu` või Eestis `https://mirrors.xtom.ee/ubuntu`.
5. **Salvestus:** vaikimisi *Use an entire disk* ja *Set up this disk as an LVM group*.

   > **Tähelepanu:** suure ketta korral jätab paigaldaja osa köitegrupist kasutamata. Kontrolli ekraanil, et `ubuntu-lv` suurus vastab ootustele, või suurenda seda pärast paigaldust (vt moodul 8).

6. **Kasutaja:** nimi, serveri nimi (hostinimi), kasutajanimi, parool. Esimene kasutaja saab `sudo` õiguse, juurkasutaja on lukus.
7. **Ubuntu Pro:** *Skip for now* (saab hiljem tasuta kuni viiele masinale aktiveerida).
8. **SSH:** ✔ *Install OpenSSH server*. Soovi korral saab importida avaliku võtme GitHubist.
9. **Featured server snaps:** ära vali midagi.
10. **Taaskäivitus** - eemalda paigaldusmeedia.

<!-- PILT: ../pildid/lisa-ubuntu-openssh.png | Ubuntu paigaldaja *SSH configuration* (Install OpenSSH server märgitud) -->

## 6. AlmaLinux 10 paigaldus

1. **Paigaldusmeedia:** vt protsessori märkust punktis 2. Vali käivitusmenüüst *Install AlmaLinux 10*.
2. **Keel ja klaviatuur:** Eesti.
3. Avaneb **kokkuvõtlik menüü** - punasega märgitud punktid tuleb läbi vaadata.
4. **Network & Host Name:** kontrolli, et võrguliides on **sisse lülitatud (ON)**, ja määra hostinimi. Staatilise aadressi jaoks *Configure* → *IPv4 Settings* → *Manual*.
5. **Installation Destination:** vali ketas ja jäta automaatne partitsioneerimine (LVM, XFS). Soovi korral saab ketta krüpteerida (*Encrypt my data*).
6. **Root Account:** jäta keelatuks (*Disable root account*).
7. **User Creation:** loo kasutaja ja märgi **Make this user administrator** - kasutaja lisatakse gruppi `wheel` ja saab kasutada `sudo`-t.
8. **Software Selection:** *Minimal Install* (vaikimisi minimaalse meedia korral).
9. **Begin Installation**, lõpus **Reboot System**.

<!-- PILT: ../pildid/lisa-alma-paigalduse-kokkuvote.png | AlmaLinuxi paigaldaja *Installation Summary* (Minimal Install, ketas, kasutaja) -->

---

## 7. Esimesed sammud pärast paigaldust

Tee need sammud igas uues serveris - ka HKHK mallist tehtud masinas (eriti parooli muutmine, hostinimi ja IP-aadress). Täpsemad selgitused on viidatud moodulites.

### 7.1 Uuendused ja põhitööriistad

```bash
# Debian, Ubuntu
sudo apt update && sudo apt full-upgrade
sudo apt install qemu-guest-agent vim curl

# AlmaLinux
sudo dnf upgrade
sudo dnf install qemu-guest-agent vim curl
```

**QEMU külalisagent** laseb Proxmoxil näha masina IP-aadressi, masinat korrektselt välja lülitada ja teha järjepidevaid varukoopiaid. Käivita see (`sudo systemctl enable --now qemu-guest-agent`) ja kontrolli, et Proxmoxi masina *Summary* lehel on näha IP-aadress. Agent peab olema Proxmoxis *Options* → *QEMU Guest Agent* lubatud.

### 7.2 Hostinimi ja staatiline IP-aadress

```bash
sudo hostnamectl set-hostname debian1
```

Staatilise aadressi seadistamine on igas distros erinev - vt moodul 7 (Debian: `/etc/network/interfaces`, Ubuntu: Netplan, AlmaLinux: `nmcli`).

### 7.3 SSH-võtmed

Loo oma arvutis võtmepaar ja kopeeri avalik võti serverisse (vt moodul 7):

```bash
ssh-keygen -t ed25519
ssh-copy-id kasutaja@10.0.83.52
```

Windowsis PowerShellis:

```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh kasutaja@10.0.83.52 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

Kui võtmega sisselogimine töötab, keela paroolid (vt moodul 7, punkt 7.7). **Ubuntus** pane tähele faili `/etc/ssh/sshd_config.d/50-cloud-init.conf` - kui see on olemas ja sisaldab rida `PasswordAuthentication yes`, kehtib see sinu `sshd_config`-i muudatuse asemel.

### 7.4 Tulemüür

| Distro | Tulemüür | Esmane seadistus |
|---|---|---|
| Debian | `ufw` (lihtsam) või `nftables` | `sudo apt install ufw`, siis nagu Ubuntus |
| Ubuntu | `ufw` | `sudo ufw default deny incoming && sudo ufw allow ssh && sudo ufw enable` |
| AlmaLinux | `firewalld` | Juba sees, SSH lubatud: `sudo firewall-cmd --list-all` |

Täpsemalt moodulis 7. Avalikult kättesaadavatele serveritele lisa `fail2ban` (moodul 11).

### 7.5 Hetktõmmis

Kui masin on paigaldatud ja põhiseadistus tehtud, **tee hetktõmmis** (Proxmoxis *Snapshots* → *Take Snapshot*, nimi nt `puhas-paigaldus`). Laboritöödes saad alati sellesse olekusse tagasi minna.

---

## 8. Masinate kloonimine ja mallid

Kui vajad mitut ühesugust masinat, ei pea igaüht paigaldama. Proxmoxis saab masina kloonida (*Clone*) või teha sellest **malli** (*Convert to template*), millest kloonid luuakse.

**Enne malliks muutmist tuleb masin „üldistada“**, muidu on kõigil kloonidel sama masina-ID ja samad SSH hostivõtmed:

```bash
# masina-ID tühjaks - luuakse järgmisel käivitusel uus
sudo truncate -s 0 /etc/machine-id
sudo rm -f /var/lib/dbus/machine-id
sudo ln -s /etc/machine-id /var/lib/dbus/machine-id

# SSH hostivõtmed kustutada
sudo rm -f /etc/ssh/ssh_host_*

# ajalugu ja logid
history -c
sudo poweroff
```

Pärast kloonimist ja esimest käivitust:

```bash
sudo ssh-keygen -A                       # loo uued SSH hostivõtmed
sudo systemctl restart ssh               # AlmaLinuxis: sshd
sudo hostnamectl set-hostname uusnimi
```

Kui masina-ID on sama, saavad kloonid DHCP-serverilt (mis kasutab masina-ID-st tuletatud tunnust) **sama IP-aadressi** - see on klassikaline laboriprobleem.

Suuremas mahus kasutatakse **cloud-init**-i (Proxmoxis *Cloud-Init* vaheleht), mis seadistab kloonile esimesel käivitusel nime, kasutaja, SSH-võtme ja IP-aadressi automaatselt, ning **Vagrantit** või **Ansible'it** (moodul 16).

---

## 9. VirtualBoxi kasutajale

Kursuse laboreid saab teha ka oma arvutis VirtualBoxiga.

- Uue masina loomisel **ära märgi** *Proceed with Unattended Installation* (*Skip Unattended Installation*) - muidu paigaldab VirtualBox ise töölauaga süsteemi.
- 2048 MB mälu, 1–2 protsessorituuma ja 20–25 GB ketast on piisav.
- Vaikimisi on masin **NAT**-võrgus: masin pääseb internetti, kuid sina ei pääse masinale ligi. Vali *Settings* → *Network* → **Bridged Adapter** (masin saab aadressi samast võrgust, kus sinu arvuti) või loo NAT-i pordisuunamine SSH jaoks.
- Mitme masina labori jaoks (nt DHCP-server ja klient) kasuta tüüpi **Internal Network** - see on isoleeritud võrk, mis ei sega kodu- ega koolivõrku.
- Võrguliides on VirtualBoxis tavaliselt `enp0s3`, Proxmoxis `ens18`.

---

## 10. WSL - kiirstart iseõppijale

Kui sul ei ole veel virtuaalmasinat, saad **moodulitega 1–4 ja 6 alustada kümne minutiga** Windowsi arvutis. **WSL** (*Windows Subsystem for Linux*) käivitab Linuxi otse Windowsis, kasutades kerget virtuaalmasinat päris Linuxi kerneliga.

**Alusta siit:**

1. Ava **PowerShell administraatorina** (Start → kirjuta `PowerShell` → *Run as administrator*).
2. Paigalda Debian (sama distro, mida kasutab moodul 1):

    ```powershell
    wsl --install -d Debian
    ```

3. Taaskäivita arvuti, kui seda palutakse. Seejärel avaneb Debiani aken - vali **Linuxi kasutajanimi ja parool** (need ei ole seotud Windowsi omadega; parooli sisestamisel ei kuvata midagi).
4. Uuenda süsteem ja paigalda mõned kursusel vajalikud tööriistad:

    ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y man-db less nano tree curl git
    ```

5. Ava edaspidi Linux menüüst *Start* → *Debian* või **Windows Terminalis** uue vahelehe valikust. Alusta [moodulist 1](../moodul-01-sissejuhatus/index.md).

Kasulikud käsud PowerShellis:

```powershell
wsl --list --online              # saadaolevad distrod
wsl --list --verbose             # paigaldatud distrod ja WSL-i versioon
wsl -d Debian                    # käivita distro
wsl --shutdown                   # peata kõik
```

Windowsi kettad on Linuxis kataloogis `/mnt/c`, Linuxi failid Windowsis aadressil `\\wsl.localhost\Debian`. Täpsemalt (seadistus, systemd, failid, varundus) vt valikmoodul 22, punkt 22.9.

**Piirangud:** WSL ei sobi serverilaboriteks (moodulid 5, 7–15, 17–23), sest võrk on vaikimisi NAT-i taga ning alglaadimine, GRUB, kettahaldus ja tulemüür erinevad päris süsteemist. Kui jõuad moodulini 5, loo virtuaalmasinad (punktid 3–7) - VirtualBoxis (punkt 9) või oma Proxmoxis.

<!-- navigatsioon -->
---

[← Moodul 25. Enesekontroll](../moodul-25-freebsd/enesekontroll.md) · [Sisukord](../../README.md#sisukord) · [Linuxi distributsioonide ülevaade →](distrod.md)
<!-- /navigatsioon -->
