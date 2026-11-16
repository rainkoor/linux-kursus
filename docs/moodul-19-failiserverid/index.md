<!-- navigatsioon -->
[← Moodul 18. Enesekontroll](../moodul-18-dhcp/enesekontroll.md) · [Sisukord](../../README.md#sisukord) · [Laboritöö 19. Kooli väikeserver, IV osa: faili- ja prindiserver, varundus ja dokumentatsioon →](labor.md)
<!-- /navigatsioon -->

# Moodul 19. Faili- ja prindiserverid

**Maht:** 8 tundi · **Laboritöö:** Debian, Ubuntu, Windows · **Eeldused:** moodulid 1–17 (eriti 3, 9 ja 10)

Failiserver on üks vanimaid ja levinumaid serveriülesandeid: ühised kaustad õpetajatele, kodukataloogid kesksel serveril, tarkvara paigaldusfailid, varukoopiate hoidla. Selles moodulis jagame faile Linuxile (NFS) ja Windowsile (Samba), haagime neid automaatselt, seadistame ühiskaustade õigused ja varunduse ning võrdleme isehallatavat serverit valmis NAS-lahendusega. Mooduli lõpus on kooli väikeserver valmis ja dokumenteerime selle.

## Õpiväljundid

Mooduli läbinud õppija:

- valib olukorrale sobiva failijagamise viisi (NFS, SMB, SFTP, iSCSI);
- jagab faile NFS-iga ja selgitab ekspordi valikuid ning kasutajate vastendamist (`root_squash`, UID);
- haagib võrgukettad vajadusel automaatselt (autofs, `x-systemd.automount`);
- jagab faile Samba abil Windowsi ja Linuxi klientidele ning seadistab jagamise õigused;
- seadistab ühiskausta õigused SGID-i ja ACL-idega nii, et grupi liikmed saavad kõik faile muuta;
- seadistab prindiserveri (CUPS), jagab printeri võrku ja haldab prinditööde järjekorda;
- varundab failiserveri ja võrdleb isehallatavat failiserverit NAS-lahendustega (TrueNAS);
- dokumenteerib serveri seadistuse ning koostab käsiraamatu (*runbook*) ja otsuste logi.

> [!NOTE]
> **Kuidas seda lehte lugeda:** iga teema algab kastiga **Lühidalt** - seal on kõige tähtsam paari lausega. Käsud ja näited on alati näha. Pikemad selgitused ja taust on peidetud plokkidesse **Loe lähemalt** - ava need, kui tahad teemast rohkem teada või kui laboritöös midagi ei õnnestu.

---

## 19.1 Failide jagamise viisid

> [!TIP]
> **Lühidalt:** Linuxile jagatakse faile **NFS**-iga, Windowsile **Samba** (SMB) abil, üksikutele kasutajatele **SFTP**-ga. iSCSI jagab terve ketta, mida kasutab üks klient korraga.

| Viis | Protokoll | Kellele | Tüüpiline kasutus |
|---|---|---|---|
| **NFS** | NFSv4, TCP 2049 | Linux, Unix, hüperviisorid | Linuxi serverite ühised kataloogid, kodukataloogid, Proxmoxi salvestus |
| **SMB** (Samba) | SMB3, TCP 445 | Windows, macOS, Linux | Kontori ühiskaustad, Windowsi kodukataloogid |
| **SFTP** | SSH, TCP 22 | kõik | Turvaline failiedastus üksikutele kasutajatele (moodul 7) |
| **WebDAV**, Nextcloud | HTTPS | brauser, telefon | Pilvelaadne failijagamine, ka väljastpoolt asutust |
| **iSCSI** | TCP 3260 | serverid | Võrgu**plokk**seade - klient teeb sellele ise failisüsteemi (valikmoodul 23) |

NFS ja SMB on **failitasandi** jagamised: server haldab failisüsteemi ja mitu klienti saavad sama kausta korraga kasutada. iSCSI jagab **plokkseadet** nagu võrgu kaudu ühendatud ketast - sama ketast tohib üldjuhul kasutada ainult üks klient korraga.

## 19.2 NFS: failide jagamine Linuxile

> [!TIP]
> **Lühidalt:** NFS: serveris kirjuta jagamine faili `/etc/exports` ja rakenda `exportfs -ra`, kliendis `mount -t nfs server:/kataloog /mnt/…`. Kasutajad tuvastatakse UID-numbri järgi.

**NFS** (*Network File System*) võimaldab haakida teise Linuxi masina kataloogi üle võrgu nagu kohaliku ketta.

**Server:**

```bash
sudo apt install nfs-kernel-server
sudo mkdir -p /srv/nfs/jagatud
```

`/etc/exports`:

```text
/srv/nfs/jagatud  10.0.83.0/24(rw,sync,no_subtree_check)
```

```bash
sudo exportfs -ra              # rakenda
sudo exportfs -v               # vaata jagamisi
```

**Klient:**

```bash
sudo apt install nfs-common
showmount -e 10.0.83.152
sudo mkdir -p /mnt/nfs
sudo mount -t nfs 10.0.83.152:/srv/nfs/jagatud /mnt/nfs
```

Püsivalt (`/etc/fstab`):

```text
10.0.83.152:/srv/nfs/jagatud  /mnt/nfs  nfs  defaults,_netdev,nofail  0  0
```

`_netdev` ütleb, et failisüsteem vajab võrku.

> [!NOTE]
> **NFS ja kasutajad:** lihtsas NFS-is tuvastatakse kasutajad **UID-numbri järgi**. Kui kasutaja `mari` on serveris UID 1001 ja kliendis 1002, ei klapi failide omanikud. Suuremates keskkondades kasutatakse kesksest kataloogist (LDAP, Active Directory - valikmoodulid 25 ja 26) pärit kasutajaid ja Kerberost. Lisaks muudetakse kliendi juurkasutaja serveris vaikimisi õigusteta kasutajaks `nobody` (**root_squash**), et kliendi juurkasutaja ei saaks serveris kõike teha.

### Ekspordi valikud

| Valik | Tähendus |
|---|---|
| `rw` / `ro` | Lugemis- ja kirjutusõigus / ainult lugemine |
| `sync` | Server kinnitab kirjutamise alles siis, kui andmed on kettal (turvalisem; `async` on kiirem, kuid elektrikatkestusel võib andmeid kaduda) |
| `root_squash` | Kliendi `root` muudetakse serveris kasutajaks `nobody` (vaikimisi) |
| `no_root_squash` | Kliendi `root` on serveris samuti `root` - ainult usaldusväärsetele masinatele (nt varundusserver) |
| `all_squash`, `anonuid=1500`, `anongid=1500` | Kõik kliendi kasutajad muudetakse ühe kindla kasutajana - avalikud jagamised |
| `no_subtree_check` | Lülitab välja aeglase alamkataloogi kontrolli (soovitatav) |

Mitu klienti eri õigustega: `/srv/nfs/jagatud  10.0.83.0/24(ro,sync) 10.0.83.153(rw,sync,no_root_squash)`. Tühikud on olulised: `10.0.83.0/24 (rw)` (tühikuga) annaks `rw` **kõigile**!

**Tulemüür:** NFSv4 vajab ainult porti **2049/tcp** (`sudo ufw allow from 10.0.83.0/24 to any port nfs`, `sudo firewall-cmd --permanent --add-service=nfs`). Vana NFSv3 ja `showmount` kasutavad lisaks `rpcbind`-i ja muutuvaid porte (`--add-service=rpc-bind --add-service=mountd`).

## 19.3 autofs: haakimine vajadusel

> [!TIP]
> **Lühidalt:** autofs haagib võrgukataloogi alles siis, kui seda kasutatakse, ja haagib tegevusetuse järel lahti. Nii ei takista kättesaamatu server alglaadimist.

`/etc/fstab`-is olev NFS-jagamine haagitakse alglaadimisel. Kui server ei ole sel hetkel kättesaadav, aeglustab see alglaadimist ja haakimine jääb tegemata. **autofs** haagib jagamise alles siis, kui keegi kataloogi poole pöördub, ja haagib selle tegevusetuse järel lahti.

```bash
sudo apt install autofs                     # AlmaLinux: sudo dnf install autofs
```

`/etc/auto.master` (või fail `/etc/auto.master.d/kool.autofs`):

```text
/mnt/kool   /etc/auto.kool   --timeout=300
```

`/etc/auto.kool`:

```text
jagatud   -rw,sync   debian1.lab.example:/srv/nfs/jagatud
```

```bash
sudo systemctl enable --now autofs
ls /mnt/kool              # tühi
ls /mnt/kool/jagatud      # nüüd haagitakse
findmnt /mnt/kool/jagatud
```

Kodukataloogide jaoks kasutatakse metamärki: `* -rw,sync server:/srv/kodu/&` (`&` asendatakse kataloogi nimega) - nii saab iga LDAP/AD kasutaja (moodulid 25–26) oma kodukataloogi failiserverist.

Lihtsam systemd alternatiiv: fstab-is valik `x-systemd.automount` (nt `debian1:/srv/nfs/jagatud /mnt/nfs nfs defaults,_netdev,x-systemd.automount 0 0`).

## 19.4 Samba: failide jagamine Windowsile

> [!TIP]
> **Lühidalt:** Samba jagamine kirjeldatakse failis `/etc/samba/smb.conf`. Kasutajal peab olema Samba parool (`smbpasswd -a`). Kontrolli seadistust `testparm` ja ühendust `smbclient -L`.

**Samba** rakendab Windowsi failijagamise protokolli **SMB**. Sellega saab Linuxi server jagada kaustu Windowsi arvutitele (ja vastupidi). Samba võib olla ka Active Directory domeenikontroller (valikmoodul 26).

```bash
sudo apt install samba
sudo mkdir -p /srv/samba/jagatud
sudo groupadd smbkasutajad
sudo chown root:smbkasutajad /srv/samba/jagatud
sudo chmod 2770 /srv/samba/jagatud
```

Jagamine faili `/etc/samba/smb.conf` lõppu:

```ini
[jagatud]
   comment = Ühine kaust
   path = /srv/samba/jagatud
   valid users = @smbkasutajad
   read only = no
   create mask = 0660
   directory mask = 2770
```

Samba kasutab **oma paroolide andmebaasi** - Linuxi kasutaja peab olema olemas, kuid Samba parool määratakse eraldi:

```bash
sudo usermod -aG smbkasutajad mari
sudo smbpasswd -a mari
testparm                              # kontrolli seadistust
sudo systemctl restart smbd
```

Ühendamine:

- **Windows:** Exploreris `\\10.0.83.152\jagatud`;
- **Linux:** `smbclient //10.0.83.152/jagatud -U mari` või haakimine `mount -t cifs` (pakett `cifs-utils`).

## 19.5 Ühiskausta õigused: SGID ja ACL

> [!TIP]
> **Lühidalt:** Ühiskaustas peavad kõik saama muuta teiste faile: kataloogile **SGID** (`chmod 2770`) ja **vaike-ACL** (`setfacl -d -m g:grupp:rwx`).

Ühiskaustas peavad kõik grupi liikmed saama muuta ka **teiste** loodud faile. Moodulis 3 õpitud vahenditest on siin vaja kahte:

1. **SGID kataloogil** (`chmod 2770`) - uued failid kuuluvad kataloogi grupile, mitte looja põhigrupile;
2. **vaikimisi ACL** (`setfacl -d`) - uutel failidel on grupil kirjutusõigus, sõltumata looja `umask`-ist (tavaline `umask 022` annaks grupile ainult lugemisõiguse).

```bash
sudo groupadd opetajad
sudo mkdir -p /srv/jagatud/opetajad
sudo chown root:opetajad /srv/jagatud/opetajad
sudo chmod 2770 /srv/jagatud/opetajad
sudo setfacl -m g:opetajad:rwx /srv/jagatud/opetajad
sudo setfacl -d -m g:opetajad:rwx /srv/jagatud/opetajad      # uutele failidele ja kataloogidele
sudo setfacl -m g:juhtkond:rx /srv/jagatud/opetajad          # teine grupp ainult lugemiseks
sudo setfacl -d -m g:juhtkond:rx /srv/jagatud/opetajad
getfacl /srv/jagatud/opetajad
```

Samba jaoks lisa jagamisele `inherit acls = yes` (või `create mask`/`force group`); NFS kasutab serveri failiõigusi otse. Kui sama kausta jagatakse nii NFS-i kui ka Samba kaudu, on õigused ühed - seadista need **failisüsteemis**, mitte ainult jagamise seadetes.

> [!TIP]
> **Õiguste kujundamise rusikareegel:** õigused antakse **gruppidele**, mitte üksikutele kasutajatele. Kui Mari liigub teise rolli, muudetakse tema grupid, mitte kümnete kaustade õigusi. Suurtes asutustes tulevad grupid kataloogiteenusest (valikmoodulid 25-26).

## 19.6 Samba ja SELinux, kasutajad ja prügikast

> [!TIP]
> **Lühidalt:** AlmaLinuxis vajab Samba kataloog SELinuxi konteksti `samba_share_t`. Samba prügikast (`vfs objects = recycle`) aitab kogemata kustutatud faile taastada.

**AlmaLinuxis** lubab SELinux Sambale ligipääsu ainult õige kontekstiga kataloogidele:

```bash
sudo semanage fcontext -a -t samba_share_t "/srv/samba(/.*)?"
sudo restorecon -Rv /srv/samba
sudo setsebool -P samba_enable_home_dirs on      # kui jagad kodukatalooge
sudo firewall-cmd --permanent --add-service=samba && sudo firewall-cmd --reload
```

Kasulikud Samba lisavõimalused:

```ini
[homes]
   comment = Kodukataloog
   browseable = no                 # iga kasutaja näeb ja haagib ainult oma kodukataloogi
   read only = no

[jagatud]
   path = /srv/samba/jagatud
   valid users = @smbkasutajad
   read only = no
   inherit acls = yes
   vfs objects = recycle           # kustutatud failid prügikasti, mitte kohe kaduma
   recycle:repository = .prugikast/%U
   recycle:keeptree = yes
```

```bash
sudo pdbedit -L                  # Samba kasutajad
sudo smbstatus                   # kes on ühendatud, millised failid lukus
```

## 19.7 Valmis NAS-lahendused: TrueNAS

> [!TIP]
> **Lühidalt:** TrueNAS on valmis NAS-süsteem ZFS-iga: jagamised, hetktõmmised ja replikatsioon on veebiliideses. See sobib, kui on vaja ainult failiserverit, mitte üldotstarbelist serverit.

Eespool seadistasid failiserveri käsitsi: Debian, `/etc/exports`, `smb.conf`, kasutajad ja õigused. Paljudes asutustes ja kodudes kasutatakse selle asemel **NAS-i** (*Network Attached Storage*) - seadet või distrot, mis on loodud ainult failide hoidmiseks ja jagamiseks ning mida hallatakse veebiliidesest.

| | Oma server (Debian + Samba/NFS) | **TrueNAS** Community Edition | OpenMediaVault | Synology, QNAP |
|---|---|---|---|---|
| Alus | mis tahes distro | Debian + **ZFS** (vanem TrueNAS CORE: FreeBSD) | Debian | tootja Linux (Btrfs/ext4) |
| Haldus | käsurida, seadistusfailid | veebiliides, API | veebiliides, pistikprogrammid | veebiliides, rakendused |
| Failisüsteem | ext4, XFS, LVM, ZFS - vali ise | ainult ZFS | ext4/XFS + mdadm, ZFS pistikprogrammiga | Btrfs, ext4 |
| Paindlikkus | täielik | piiratud (süsteem on „seade“) | keskmine | piiratud |
| Hind | tasuta | tasuta (Enterprise tasuline) | tasuta | riistvara koos tarkvaraga |
| Kellele | õppimine, eri teenused ühes masinas | tõsine salvestus, palju kettaid, hetktõmmised ja replikatsioon | väike kodu-NAS, vana riistvara | kes ei taha ise hallata |

**TrueNAS** ühendab mooduli 10 ZFS-i ja selle mooduli failijagamise. Veebiliideses vastavad mõisted käsurea tööriistadele:

| TrueNASi veebiliides | Mida see tegelikult teeb |
|---|---|
| *Storage* → *Create Pool* | `zpool create` (vdev-ide tüüp: mirror, RAIDZ1/2/3) |
| *Datasets* | `zfs create`, pakkimine, kvoodid, õigused (ACL) |
| *Shares* → *SMB* | Samba jagamine (`smb.conf`) |
| *Shares* → *NFS* | NFS-i eksport (`/etc/exports`) |
| *Credentials* → *Local Users* / *Directory Services* | kasutajad ja grupid; liitumine AD-ga (valikmoodul 26) või LDAP-iga (valikmoodul 25) |
| *Data Protection* → *Periodic Snapshot Tasks* | ajastatud `zfs snapshot` |
| *Data Protection* → *Replication Tasks* | `zfs send \| ssh … zfs receive` teise masinasse |
| *Data Protection* → *Scrub Tasks*, *S.M.A.R.T. Tests* | `zpool scrub`, `smartctl` |
| *Apps* | konteinerid (Docker) |

SMB-jagamisel saab lubada **hetktõmmiste näitamise Windowsis**: ZFS-i hetktõmmised ilmuvad Windowsi failiomaduste vahekaardile *Previous Versions* ja kasutaja saab kustutatud või üle kirjutatud faili ise taastada.

Mida TrueNASi puhul arvestada:

- **TrueNAS on seade, mitte üldotstarbeline distro.** Süsteemi paketihaldus on keelatud ja käsitsi muudatused võivad uuendusel kaduda. Kõik seadistused tehakse veebiliidese või API kaudu.
- **ZFS tahab näha päris kettaid.** Proxmoxis tootmiskasutuseks suunatakse TrueNASi VM-ile terve kettakontroller (HBA, PCIe läbisuunamine) või vähemalt kettad otse (`qm set <vmid> -scsi1 /dev/disk/by-id/…`). Virtuaalkettad Proxmoxi enda ZFS-i peal tähendavad „ZFS-i ZFS-i peal“: topelt vahemälu ja ZFS ei näe ketaste tervist. Laboris harjutamiseks sobivad virtuaalkettad.
- **Süsteemiketas** on eraldi väike SSD; andmekettad lähevad poolidesse.
- **Mälu:** soovitatav vähemalt 8 GiB, sest ARC kasutab vaba mälu vahemäluna.
- **RAID ja hetktõmmised ei ole varukoopia** - andmed peavad olema ka teises masinas või asukohas (replikatsioon, 3-2-1 reegel, moodul 9).

## 19.8 Prindiserver: CUPS

> [!TIP]
> **Lühidalt:** Linuxi printimissüsteem on **CUPS**. Prindiserver hoiab printerite järjekordi ja jagab neid võrku protokolliga IPP (port 631). Printereid haldab `lpadmin` või veebiliides `https://server:631`, järjekorda näitab `lpstat`, prindib `lp`.

Prindiserver on masin, mille kaudu kõik kasutajad prindivad: printer ja selle draiver seadistatakse **ühes kohas**, kliendid näevad valmis järjekorda ning haldur näeb, kes mida printis, ja saab kinni jäänud töö tühistada. Väikeses kontoris on see sageli sama masin mis failiserver.

```bash
sudo apt install cups                    # AlmaLinux: sudo dnf install cups
sudo usermod -aG lpadmin mari            # kes tohib printereid hallata (AlmaLinux: grupp sys või wheel)
sudo cupsctl --share-printers --remote-admin     # luba jagamine ja haldus võrgust
sudo ufw allow 631/tcp                   # AlmaLinux: firewall-cmd --permanent --add-service=ipp && firewall-cmd --reload
systemctl status cups
```

Veebiliides on aadressil `https://server:631` (logi sisse `lpadmin` grupi kasutajana). Sama saab teha käsurealt:

```bash
# Lisa võrguprinter (tänapäevased printerid töötavad ilma draiverita: -m everywhere)
sudo lpadmin -p kontor -E -v ipp://10.0.83.120/ipp/print -m everywhere -D "Kontori printer" -L "2. korrus"
sudo lpadmin -p kontor -o printer-is-shared=true      # jaga võrku
sudo lpadmin -d kontor                                 # vaikeprinter

lpstat -p -d                 # printerid ja vaikeprinter
lpstat -o                    # ootel tööd
lp -d kontor /etc/hostname   # prindi fail
cancel kontor-12             # tühista töö
sudo cupsdisable kontor; sudo cupsenable kontor       # peata ja jätka järjekorda
```

Laboris päris printerit ei ole. Selle asemel sobib **virtuaalne PDF-printer** (`sudo apt install printer-driver-cups-pdf`): see loob järjekorra `PDF` ja salvestab prinditu PDF-failina printija kodukataloogi `~/PDF/`.

**Kliendid:**

| Klient | Kuidas printer lisada |
|---|---|
| Linux | `sudo lpadmin -p kontor -E -v ipp://debian1.lab.example:631/printers/kontor -m everywhere` või töölaual *Settings* → *Printers* |
| Windows | *Printers & scanners* → *Add device* → *Add manually* → jagatud printer nime järgi: `http://debian1.lab.example:631/printers/kontor` |
| macOS, telefonid | leiavad jagatud printeri enamasti ise (mDNS/Bonjour, AirPrint) |

**Tõrkeotsing:** logid on kataloogis `/var/log/cups/` (`error_log`, `access_log`, `page_log` - kes, millal ja mitu lehte). Kui klient printerit ei näe, kontrolli tulemüüri (631/tcp), kas printer on jagatud (`lpstat -v`, `printer-is-shared`) ja kas `cupsd` kuulab võrguliidesel (`sudo ss -tlpn | grep 631`). Kinni jäänud järjekorra puhul vaata `lpstat -p` (kas printer on peatatud) ja käivita `cupsenable`.

> [!NOTE]
> **Samba ja printerid.** Windowsi domeenis jagatakse printereid sageli Samba kaudu (`[printers]` jagamine, draiverite levitamine klientidele). Tänapäevaste draiverita printeritega on IPP lihtsam ja töötab kõigi klientidega ühtemoodi. Varunda `/etc/cups/` (printerite seadistus on failis `printers.conf`).

## 19.9 Failiserveri varundus

> [!TIP]
> **Lühidalt:** Failiserveri andmed on kõige väärtuslikumad. Varunda need teise masinasse (restic, `zfs send`) ja hoia mitu ajalist koopiat lunavara ja kogemata kustutamise vastu.

Failiserveri andmed on sageli asutuse kõige väärtuslikum osa ja just neid kustutatakse kogemata või krüpteerib lunavara. Moodulis 9 õpitud põhimõtted kehtivad siin täies ulatuses:

| Kiht | Mida annab | Mida ei asenda |
|---|---|---|
| **RAID / ZFS mirror** (moodul 10) | Ketta rike ei too katkestust | Varukoopiat - kustutamine ja lunavara jõuavad kõigile ketastele |
| **Hetktõmmised** (ZFS, LVM, Samba *Previous Versions*) | Kasutaja taastab kustutatud faili ise minutitega | Varukoopiat - asuvad samas masinas |
| **Prügikast** (Samba `recycle`) | Kogemata kustutatud faili taastamine | Varukoopiat |
| **Varukoopia teises masinas** (restic, ZFS replikatsioon) | Taastamine masina, ruumi või lunavara korral | - |

```bash
# failiserveri jagamised restic'uga teise serverisse (moodul 9)
export RESTIC_REPOSITORY=sftp:varu@debian2:/srv/restic/failiserver
export RESTIC_PASSWORD_FILE=/root/.restic-parool
sudo -E restic backup /srv/nfs /srv/samba /srv/jagatud --exclude '.prugikast'
sudo -E restic forget --keep-daily 14 --keep-weekly 8 --keep-monthly 12 --prune
```

Varunda koos andmetega ka **õigused ja ACL-id** (restic ja `tar --acls` teevad seda) ning seadistus (`/etc/exports`, `/etc/samba/smb.conf`, Samba kasutajate andmebaas `/var/lib/samba/private/`). Ilma õigusteta taastatud ühiskaust tähendab tunde käsitsi parandamist.

## 19.10 Serveri dokumenteerimine

> [!TIP]
> **Lühidalt:** Dokumenteeri, **mis** on seadistatud, **miks** ja **kuidas** see taastada. Hoia dokumentatsioon Gitis koos seadistusfailidega.

Hästi seadistatud, kuid dokumenteerimata server on ohtlik: keegi (ka sina ise poole aasta pärast) ei tea, miks miski on seadistatud nii, nagu on. Serveri dokumentatsioon peaks sisaldama:

- serveri eesmärk, asukoht (nt Proxmoxi sõlm), IP-aadressid ja DNS-nimed;
- operatsioonisüsteem ja versioon;
- paigaldatud teenused, nende pordid ja olulised seadistusfailid;
- kasutajad ja kes vastutab;
- tulemüüri reeglid;
- varundus: mida, kuhu, kui tihti ja **kuidas taastada**;
- muudatuste logi: kuupäev, mida muudeti ja miks.

Dokumentatsioon kirjutatakse sageli Markdownis ja hoitakse Git-repos koos seadistusfailidega (vt moodul 6).

Suuremate süsteemide juurde kuuluvad veel kaks dokumenti:

**Käsiraamat** (*runbook*) - sammhaaval juhised tüüpilisteks toiminguteks ja riketeks, mida saab järgida ka see, kes süsteemi ei ehitanud (näiteks öösel valves olev kolleeg). Iga juhis on lühike ja konkreetne:

```markdown
## Veebisait ei vasta
1. Kontrolli: `curl -I https://kool.lab.example` - mis koodi saad?
2. `systemctl status nginx php8.4-fpm` - kas teenused töötavad?
3. `journalctl -u nginx --since "30 min ago"` - vead?
4. `df -h /var` - kas ketas on täis?
5. Kui andmebaas ei vasta: vt „MariaDB ei käivitu“.
6. Kui 15 minutiga ei lahene: teavita (kontakt) ja kirjuta intsident üles.
```

**Otsuste logi** (*decision log*, ka ADR - *Architecture Decision Record*) - lühike kirje iga olulise valiku kohta: mis oli probleem, millised olid variandid, mida valiti ja **miks**. Näiteks „Valisime PostgreSQL-i asemel MariaDB, sest rakendus toetab ametlikult ainult MariaDB-d ja meeskond tunneb seda“. Aasta pärast ei pea keegi arvama, miks asjad nii on.

---

## Distrode erinevused

| | **Debian** | **Ubuntu** | **AlmaLinux** |
|---|---|---|---|
| NFS server | `nfs-kernel-server` | `nfs-kernel-server` | `nfs-utils`, teenus `nfs-server` |
| NFS klient | `nfs-common` | `nfs-common` | `nfs-utils` |
| Samba | `samba`, teenus `smbd` | sama | `samba`, teenus `smb`, SELinux `samba_share_t` |
| autofs | `autofs` | `autofs` | `autofs` |
| Teenus käivitub paigaldamisel | Jah | Jah | Ei (`enable --now`), avada ka `firewall-cmd --add-service=nfs/samba` |

AlmaLinuxis tuleb lisaks arvestada SELinuxiga (moodul 12): Samba jagamised (`samba_share_t`) ja NFS-i kodukataloogid (`use_nfs_home_dirs`) vajavad õigeid kontekste või tõeväärtusi.

---

## Kokkuvõte

| Teenus | Paigaldus | Seadistus | Kontroll |
|---|---|---|---|
| NFS | `apt install nfs-kernel-server` | `/etc/exports` | `exportfs -v`, `showmount -e`, `findmnt` |
| autofs | `apt install autofs` | `/etc/auto.master`, `/etc/auto.*` | `ls` haakepunktis, `findmnt` |
| Samba | `apt install samba` | `/etc/samba/smb.conf`, `smbpasswd -a` | `testparm`, `smbclient`, `smbstatus` |
| Prindiserver | `apt install cups` | `lpadmin`, `cupsctl --share-printers`, `https://server:631` | `lpstat -p -o`, `lp`, `/var/log/cups/` |
| Ühiskaust | - | `chmod 2770`, `setfacl -d -m g:grupp:rwx` | `getfacl` |
| TrueNAS | ISO, eraldi masin/VM | veebiliides: *Storage*, *Datasets*, *Shares*, *Data Protection* | `zpool status`, Windowsi *Previous Versions* |
| Varundus | `apt install restic` | `RESTIC_REPOSITORY`, taimer | `restic snapshots`, taastamistest |

**Järgmised sammud:** tee [laboritöö](labor.md) ja kontrolli oma teadmisi [enesekontrolli](enesekontroll.md) abil.

## Lisamaterjal

- Samba Wiki (wiki.samba.org)
- Ubuntu Server dokumentatsioon - NFS, Samba (documentation.ubuntu.com)
- `man 5 exports`, `man 5 auto.master`, `man 5 smb.conf`
- TrueNAS dokumentatsioon (www.truenas.com/docs)

<!-- navigatsioon -->
---

[← Moodul 18. Enesekontroll](../moodul-18-dhcp/enesekontroll.md) · [Sisukord](../../README.md#sisukord) · [Laboritöö 19. Kooli väikeserver, IV osa: faili- ja prindiserver, varundus ja dokumentatsioon →](labor.md)
<!-- /navigatsioon -->
