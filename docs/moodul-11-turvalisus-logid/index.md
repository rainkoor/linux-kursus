# Moodul 11. Turvalisus ja logid

**Maht:** 10 tundi · **Laboritöö:** AlmaLinux (11A) ja Ubuntu (11B) · **Eeldused:** moodulid 1–10

## Õpiväljundid

Mooduli läbinud õppija:

- rakendab serveri turvamise põhimõtteid;
- seadistab automaatsed turvauuendused;
- kaitseb SSH-teenust paroolirünnakute eest (`fail2ban`);
- leiab olulised logid, haldab journal'it ja logide rotatsiooni;
- selgitab kohustusliku juurdepääsukontrolli (MAC) põhimõtet;
- lahendab SELinuxi põhjustatud probleeme AlmaLinuxis;
- haldab AppArmori profiile Ubuntus;
- jälgib olulisi süsteemimuudatusi `auditd` abil;
- hindab serveri turvalisust auditivahendiga;
- selgitab SIEM-i rolli ja paigaldab Wazuhi koos agentidega (valikuline).

---

## 11.1 Turvalisuse põhimõtted

Turvalisus ei ole üks tööriist ega seadistus, vaid **kihiline kaitse** (*defense in depth*): kui üks kiht murtakse, peavad teised ründaja peatama.

| Põhimõte | Tähendus | Kus kursusel |
|---|---|---|
| **Vähim õigus** | Iga kasutaja ja teenus saab ainult vajalikud õigused | Moodul 3 |
| **Vähendatud ründepind** | Paigalda ja käivita ainult vajalik tarkvara, sulge mittevajalikud pordid | Moodulid 4, 5, 7 |
| **Uuendamine** | Paigalda turvauuendused kiiresti | Moodul 4, punkt 11.2 |
| **Tugev autentimine** | SSH-võtmed, keelatud parooliga ja juurkasutaja sisselogimine | Moodul 7 |
| **Võrgu filtreerimine** | Tulemüür lubab ainult vajaliku | Moodul 7 |
| **Isoleerimine** | SELinux/AppArmor piiravad, mida ülevõetud teenus teha saab | Punktid 11.5–11.6 |
| **Jälgimine** | Logid, audit, hoiatused - rünnakut tuleb märgata | Punktid 11.4, 11.7 |
| **Varundus** | Kui kõik muu ebaõnnestub, peab andmed saama taastada | Moodulid 6, 9, 15 |

### Serveri karastamise kontrollnimekiri

1. Uuenda süsteem ja lülita sisse automaatsed turvauuendused.
2. Loo isiklikud kasutajakontod, kasuta `sudo`-t, ära tööta juurkasutajana.
3. SSH: ainult võtmed, `PermitRootLogin no`, vajadusel `AllowGroups`.
4. Tulemüür: keela vaikimisi sissetulev, luba ainult vajalikud teenused.
5. Eemalda või keela mittevajalikud teenused (`ss -tulpn`, `systemctl list-unit-files --state=enabled`).
6. Hoia SELinux/AppArmor sees ja karasta oma teenuseid systemd turvaseadetega (`systemd-analyze security`, vt moodul 10, punkt 10.11).
7. Seadista `fail2ban` avalikult kättesaadavatele teenustele.
8. Veendu, et logid on püsivad ja neid jälgitakse.
9. Seadista varundus ja **testi taastamist**.
10. Dokumenteeri seadistus.

## 11.2 Automaatsed turvauuendused

Enamik edukaid rünnakuid kasutab ära **teadaolevaid** turvaauke, millele on parandus juba olemas. Seepärast on turvauuenduste kiire paigaldamine üks tõhusamaid kaitsemeetmeid.

### Debian ja Ubuntu: unattended-upgrades

Ubuntus on `unattended-upgrades` vaikimisi paigaldatud ja sisse lülitatud (paigaldab turvauuendused). Debianis tuleb see paigaldada:

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades     # lülita sisse
```

Seadistus:

| Fail | Sisu |
|---|---|
| `/etc/apt/apt.conf.d/20auto-upgrades` | Kas automaatne uuendamine on sees |
| `/etc/apt/apt.conf.d/50unattended-upgrades` | Millised uuendused paigaldatakse, kas taaskäivitada automaatselt, e-posti teavitused |

```text
# /etc/apt/apt.conf.d/20auto-upgrades
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
```

Olulised valikud failis `50unattended-upgrades`:

```text
Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-Time "03:30";
Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";
```

Kontroll ja logid:

```bash
sudo unattended-upgrade --dry-run --debug           # näita, mida tehtaks
ls /var/log/unattended-upgrades/
systemctl list-timers 'apt-daily*'
```

### AlmaLinux: dnf-automatic

```bash
sudo dnf install dnf-automatic
sudo nano /etc/dnf/automatic.conf
```

```ini
[commands]
upgrade_type = security
apply_updates = yes
```

```bash
sudo systemctl enable --now dnf-automatic.timer
systemctl list-timers dnf-automatic.timer
```

`upgrade_type = security` paigaldab ainult turvauuendused, `default` kõik uuendused.

Ülevaade turvauuendustest:

```bash
dnf updateinfo list --security          # saadaolevad turvauuendused
dnf updateinfo info <ID>                # ühe teate üksikasjad (CVE-numbrid)
```

> [!NOTE]
> **Automaatne taaskäivitus?** Kerneli ja põhiteekide uuendused rakenduvad alles pärast taaskäivitust. Mõne serveri puhul on automaatne öine taaskäivitus vastuvõetav, teiste puhul (andmebaasid, kriitilised teenused) planeeritakse see käsitsi hooldusaknasse. Igal juhul peab keegi jälgima, et taaskäivitus toimub.

### Turvateated

Distrod avaldavad turvateateid:

- Debian: **DSA** (*Debian Security Advisory*) - security.debian.org;
- Ubuntu: **USN** (*Ubuntu Security Notice*) - ubuntu.com/security/notices;
- AlmaLinux: **ALSA** - errata.almalinux.org.

Turvaaugud tähistatakse rahvusvaheliselt **CVE** numbriga (nt `CVE-2024-3094` - xz tagauks, vt [ajalugu](../lisad/ajalugu.md)).

## 11.3 fail2ban

Avalikult kättesaadavat SSH-serverit proovitakse pidevalt automaatselt paroolidega murda. `fail2ban` jälgib logisid ja **blokeerib tulemüüri abil** IP-aadressid, millelt tuleb liiga palju ebaõnnestunud katseid.

```bash
sudo apt install fail2ban               # Debian, Ubuntu
sudo dnf install epel-release && sudo dnf install fail2ban   # AlmaLinux
```

Seadistus kirjutatakse faili **`/etc/fail2ban/jail.local`** (mitte `jail.conf`, mille uuendus üle kirjutab):

```ini
[DEFAULT]
bantime  = 1h
findtime = 10m
maxretry = 5
ignoreip = 127.0.0.1/8 10.0.83.0/24

[sshd]
enabled = true
backend = systemd
```

| Seade | Tähendus |
|---|---|
| `bantime` | Kui kauaks blokeeritakse |
| `findtime`, `maxretry` | Blokeeri, kui `findtime` jooksul on `maxretry` ebaõnnestumist |
| `ignoreip` | Aadressid, mida kunagi ei blokeerita (nt sinu kooli võrk) |
| `backend = systemd` | Loe logisid journal'ist (vajalik Debianis, kus tekstilogi `auth.log` vaikimisi puudub) |

```bash
sudo systemctl enable --now fail2ban
sudo fail2ban-client status                       # aktiivsed vanglad (jails)
sudo fail2ban-client status sshd                  # blokeeritud aadressid
sudo fail2ban-client set sshd unbanip 203.0.113.7 # vabasta aadress
```

### Kas fail2ban on vajalik?

Pärast `PasswordAuthentication no` seadmist ei saa SSH-sse parooliga sisse murda, nii et SSH puhul on fail2ban pigem **lisakaitse** kui hädavajalik. Kus see on endiselt kasulik:

| Olukord | Kas fail2ban aitab? |
|---|---|
| SSH ainult võtmetega, server sisevõrgus | vähe - piira SSH tulemüüris lubatud võrkudele |
| SSH internetist kättesaadav | vähendab logide müra ja koormust |
| Paroolipõhine teenus internetis (WordPressi sisselogimine, e-post, FTP, veebiliides) | **jah** - see on fail2ban-i peamine kasutus tänapäeval |
| Hulk servereid, tahetakse jagada teavet ründajatest | vaata **CrowdSec**-i (fail2ban-i tänapäevane järeltulija, jagab blokeerimisloendeid) või Wazuhi automaatset reageerimist (punkt 11.10) |

**OpenSSH 9.8** ja uuemad oskavad ka ise: seade `PerSourcePenalties` paneb liiga palju vigaseid ühendusi tegevale aadressile ajutise keelu ilma lisatarkvarata. Kontrolli, kas sinu versioonis see on olemas ja sees: `ssh -V` ja `sudo sshd -T | grep -i persourcepenalties`. (Ubuntu 24.04 OpenSSH 9.6 seda veel ei toeta.)

Kokkuvõttes: fail2ban ei asenda võtmepõhist autentimist ega tulemüüri, kuid on lihtne ja levinud vahend paroolidega kaitstud teenuste jaoks - seepärast tasub seda osata.
> [!NOTE]
> **Kas fail2ban on vajalik, kui paroolid on keelatud?** Pärast `PasswordAuthentication no` seadmist ei saa parooliga sisse murda. `fail2ban` vähendab siiski logide müra ja koormust ning kaitseb ka teisi teenuseid (veebiserveri sisselogimine, e-post), mille jaoks saab samuti vanglaid seadistada.

## 11.4 Logid

Logid on peamine allikas, et mõista, mis süsteemis toimus - nii vigade kui ka rünnakute puhul.

### Olulisemad logid

| Logi | Debian | Ubuntu | AlmaLinux |
|---|---|---|---|
| Üldine süsteemilogi | journal | `/var/log/syslog` | `/var/log/messages` |
| Autentimine (SSH, sudo, su) | journal | `/var/log/auth.log` | `/var/log/secure` |
| Kerneli teated | `dmesg`, `journalctl -k` | `/var/log/kern.log` | `dmesg`, `journalctl -k` |
| Pakihaldus | `/var/log/apt/` | `/var/log/apt/` | `/var/log/dnf.log` |
| Auditilogi | `/var/log/audit/audit.log` (kui `auditd` on paigaldatud) | sama | `/var/log/audit/audit.log` |
| Veebiserver | `/var/log/nginx/`, `/var/log/apache2/` | sama | `/var/log/nginx/`, `/var/log/httpd/` |
| Sisselogimised | `last`, `lastb` | sama | sama |

Journal'is on kõik need logid olemas kõigis kolmes distros, tekstifailid lisab **rsyslog**, kui see on paigaldatud.

```bash
last -n 10                          # viimased sisselogimised
sudo lastb -n 10                    # ebaõnnestunud sisselogimised
journalctl _COMM=sshd --since today # SSH logid
journalctl _COMM=sudo               # sudo kasutamine
logger -t minuskript "Varundus valmis"   # kirjuta logisse oma teade
journalctl -t minuskript
```

### journald seadistus

journald seadistus on failis `/etc/systemd/journald.conf`. Muudatused kirjutatakse eraldi faili kataloogi `/etc/systemd/journald.conf.d/`:

```ini
# /etc/systemd/journald.conf.d/90-labor.conf
[Journal]
Storage=persistent
SystemMaxUse=500M
MaxRetentionSec=1month
```

```bash
sudo systemctl restart systemd-journald
journalctl --disk-usage
sudo journalctl --vacuum-size=200M      # kustuta vanimad, kuni maht on alla 200 MB
sudo journalctl --vacuum-time=14d       # kustuta vanemad kui 14 päeva
```

### Logide rotatsioon: logrotate

Tekstilogid kasvavad lõputult, kui neid ei piirata. **logrotate** nimetab logid regulaarselt ümber (`syslog` → `syslog.1` → `syslog.2.gz` …), pakib vanad ja kustutab kõige vanemad.

Seadistus: üldine `/etc/logrotate.conf` ja teenuste kaupa `/etc/logrotate.d/`:

```text
# /etc/logrotate.d/minurakendus
/var/log/minurakendus/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root adm
}
```

| Valik | Tähendus |
|---|---|
| `daily` / `weekly` / `monthly` | Kui tihti roteerida |
| `size 100M` | Roteeri, kui fail ületab suuruse |
| `rotate 14` | Hoia alles 14 vana faili |
| `compress`, `delaycompress` | Paki vanad failid (viimast alles järgmisel korral) |
| `missingok`, `notifempty` | Ära anna viga puuduva faili korral, ära roteeri tühja faili |
| `create 0640 root adm` | Loo uus tühi fail nende õigustega |
| `postrotate … endscript` | Käsk pärast roteerimist (nt teenusele uue faili kasutamise märku andmine) |

```bash
sudo logrotate -d /etc/logrotate.d/minurakendus     # proovirežiim
sudo logrotate -f /etc/logrotate.d/minurakendus     # sunni roteerima
```

logrotate'i käivitab igapäevaselt systemd taimer (`logrotate.timer`) või cron.

### Tsentraalne logimine

Ründaja, kes saab juurkasutaja õigused, võib logid kustutada. Seepärast saadetakse olulistes keskkondades logid **logiserverisse**. Lihtsaim viis on rsyslog:

```text
# /etc/rsyslog.d/90-kaug.conf (kliendis)
*.* @@logiserver.lab.example:514
```

`@@` tähendab TCP-d, `@` UDP-d. Suuremates keskkondades kasutatakse logide kogumiseks ja analüüsimiseks lahendusi nagu Graylog, Elasticsearch/OpenSearch või Grafana Loki.

## 11.5 Kohustuslik juurdepääsukontroll

Moodulis 3 õpitud tavalised õigused (`rwx`, omanik, grupp) on **valikuline juurdepääsukontroll** (DAC, *Discretionary Access Control*): faili omanik otsustab ise, kes tohib faili kasutada, ja juurkasutajale need piirangud ei kehti.

**Kohustuslik juurdepääsukontroll** (MAC, *Mandatory Access Control*) lisab süsteemse poliitika, mida ei saa mööda minna isegi juurkasutaja õigustes töötav programm. Näiteks: veebiserver tohib lugeda ainult veebifaile ja kuulata ainult veebiporte - isegi kui ründaja võtab veebiserveri üle, ei saa ta lugeda faili `/etc/shadow` ega avada uut porti.

| | **SELinux** | **AppArmor** |
|---|---|---|
| Distrod | AlmaLinux, RHEL, Fedora | Ubuntu, Debian, SUSE |
| Põhimõte | **Märgised** - igal failil, protsessil ja pordil on turvakontekst | **Teed** - profiil kirjeldab, milliseid faile programm tohib kasutada |
| Ulatus | Kogu süsteem | Programmid, millel on profiil |
| Keerukus | Võimsam, keerulisem | Lihtsam |

> [!WARNING]
> **Ära lülita SELinuxit ega AppArmorit välja!** Internetis soovitavad paljud juhendid probleemi korral SELinuxi lihtsalt välja lülitada. See on sama, mis tulemüüri väljalülitamine, sest port ei avane. Õige lahendus on probleem diagnoosida ja poliitikat kohandada - tavaliselt on see üks käsk.

## 11.6 SELinux (AlmaLinux)

### Režiimid

| Režiim | Tähendus |
|---|---|
| **Enforcing** | Poliitika kehtib, keelatud tegevused blokeeritakse ja logitakse |
| **Permissive** | Poliitika ei blokeeri, kuid rikkumised logitakse (diagnostika jaoks) |
| **Disabled** | Välja lülitatud |

```bash
getenforce                          # praegune režiim
sestatus                            # üksikasjalik olek
sudo setenforce 0                   # permissive (kuni taaskäivituseni)
sudo setenforce 1                   # enforcing
```

Püsiv režiim on failis `/etc/selinux/config` (`SELINUX=enforcing`).

### Kontekstid

Igal failil, protsessil ja pordil on **SELinuxi kontekst** kujul `kasutaja:roll:tüüp:tase`. Praktikas on oluline **tüüp** (lõpeb tavaliselt `_t`-ga).

```bash
ls -Z /var/www/html/                # failide kontekstid
ps -eZ | grep httpd                 # protsesside kontekstid
id -Z                               # sinu kontekst
```

```text
system_u:object_r:httpd_sys_content_t:s0 index.html
system_u:system_r:httpd_t:s0      1234 ?  00:00:00 httpd
```

Poliitika ütleb näiteks: protsess tüübiga `httpd_t` tohib lugeda faile tüübiga `httpd_sys_content_t`. Kui failil on muu tüüp (nt kodukataloogist teisaldatud fail `user_home_t`), keelatakse lugemine - isegi kui failiõigused on `644`.

Uued failid saavad konteksti kataloogi järgi, kus need luuakse. **`mv` säilitab vana konteksti, `cp` annab uue** - see on levinuim SELinuxi probleemide põhjus.

### Kontekstide parandamine

```bash
sudo restorecon -Rv /var/www/html   # taasta poliitika järgi õiged kontekstid
```

Kui kasutad mittestandardset kataloogi (nt veebifailid kataloogis `/srv/veeb`), lisa poliitikasse püsiv reegel ja rakenda see:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/srv/veeb(/.*)?"
sudo restorecon -Rv /srv/veeb
```

Käsk `chcon -t tüüp fail` muudab konteksti otse, kuid see muudatus kaob järgmise `restorecon`-i või täieliku ümbermärgistamise korral. Kasuta püsivaks muutmiseks `semanage fcontext`.

### Pordid

Teenus tohib kuulata ainult porte, mis on poliitikas tema tüübile lubatud:

```bash
sudo semanage port -l | grep http_port_t
sudo semanage port -a -t http_port_t -p tcp 8888   # luba veebiserverile port 8888
```

### Tõeväärtused (booleans)

Poliitika osi saab sisse ja välja lülitada tõeväärtustega:

```bash
getsebool -a | grep httpd
sudo setsebool -P httpd_can_network_connect on     # veebiserver tohib luua võrguühendusi (nt pöördpuhvri jaoks)
sudo setsebool -P httpd_enable_homedirs on         # veebiserver tohib lugeda kodukataloogide veebifaile
```

`-P` muudab seade püsivaks.

### Probleemide diagnoosimine

SELinuxi keelud logitakse auditilogisse **AVC** teadetena:

```bash
sudo ausearch -m AVC -ts recent                    # viimased keelud
sudo ausearch -m AVC -ts recent | audit2why        # selgitus
sudo journalctl -t setroubleshoot                  # inimloetav selgitus (pakett setroubleshoot-server)
```

```text
type=AVC msg=audit(...): avc:  denied  { read } for  pid=1234 comm="httpd"
name="index.html" scontext=system_u:system_r:httpd_t:s0
tcontext=unconfined_u:object_r:user_home_t:s0 tclass=file permissive=0
```

Loe nii: protsess `httpd` (`httpd_t`) tahtis **lugeda** faili `index.html`, mille tüüp on `user_home_t` - keelatud.

**Diagnoosimise töövoog:**

1. Kas probleem kaob, kui `setenforce 0`? Kui jah, on põhjus SELinuxis (lülita kohe tagasi: `setenforce 1`).
2. Vaata AVC teadet: milline protsess, mis tegevus, millise tüübiga objekt.
3. Lahenda: vale faili tüüp → `restorecon` või `semanage fcontext`; mittestandardne port → `semanage port`; vajalik funktsioon → `setsebool -P`.

`semanage` on paketis `policycoreutils-python-utils`.

## 11.7 AppArmor (Ubuntu)

AppArmor piirab programme **profiilide** abil. Profiil on tekstifail kataloogis `/etc/apparmor.d/`, mis loetleb failid ja võimalused, mida programm tohib kasutada.

```bash
sudo aa-status                      # laaditud profiilid ja nende režiimid
```

Profiilil on kaks režiimi:

| Režiim | Tähendus |
|---|---|
| **enforce** | Keelatud tegevused blokeeritakse ja logitakse |
| **complain** | Keelatud tegevused ainult logitakse (profiili koostamiseks ja diagnostikaks) |

```bash
sudo apt install apparmor-utils
sudo aa-complain /usr/bin/tcpdump        # profiil complain-režiimi
sudo aa-enforce /usr/bin/tcpdump         # tagasi enforce-režiimi
sudo apparmor_parser -r /etc/apparmor.d/usr.bin.tcpdump   # laadi muudetud profiil uuesti
```

### Profiili näide

```text
# /etc/apparmor.d/usr.local.bin.loe-faili
abi <abi/3.0>,
include <tunables/global>

/usr/local/bin/loe-faili {
  include <abstractions/base>
  include <abstractions/bash>

  /usr/bin/bash ix,
  /usr/bin/cat ix,
  /usr/local/bin/loe-faili r,
  /etc/hostname r,
}
```

Profiil lubab skriptil `loe-faili` käivitada `bash`-i ja `cat`-i ning lugeda faili `/etc/hostname`. Kõik muu - näiteks `/etc/passwd` lugemine - on keelatud.

| Õigus | Tähendus |
|---|---|
| `r`, `w` | Lugemine, kirjutamine |
| `ix` | Käivita programm sama profiiliga |
| `px` | Käivita programm tema enda profiiliga |
| `include <abstractions/...>` | Lisa valmis reeglite kogum (nt põhiteegid) |

Profiili saab koostada ka interaktiivselt: `aa-genprof programm` jälgib programmi tööd ja pakub reegleid, `aa-logprof` täiendab profiili logide põhjal.

### Diagnoosimine

AppArmori keelud on kerneli logis:

```bash
sudo journalctl -k | grep -i apparmor
sudo dmesg | grep DENIED
```

```text
audit: type=1400 audit(...): apparmor="DENIED" operation="open"
profile="/usr/local/bin/loe-faili" name="/etc/passwd" pid=2345 comm="cat"
requested_mask="r" denied_mask="r"
```

## 11.8 Auditeerimine: auditd

**auditd** salvestab kerneli tasemel üksikasjalikult, kes mida süsteemis tegi. Sellega saab näiteks jälgida oluliste failide muutmist. AlmaLinuxis on `auditd` vaikimisi paigaldatud, Debianis ja Ubuntus tuleb paigaldada pakett `auditd`.

```bash
sudo auditctl -w /etc/passwd -p wa -k kasutajad       # jälgi kirjutamist ja atribuutide muutmist
sudo auditctl -w /etc/sudoers -p wa -k sudoers
sudo auditctl -l                                      # aktiivsed reeglid
sudo ausearch -k kasutajad -i                         # sündmused võtme järgi (-i: loetav kuju)
sudo aureport --summary                               # kokkuvõte
```

| Õigus | Tähendus |
|---|---|
| `r` | Lugemine |
| `w` | Kirjutamine |
| `x` | Käivitamine |
| `a` | Atribuutide (õigused, omanik) muutmine |

`auditctl` reeglid kaovad taaskäivitusel. Püsivad reeglid kirjutatakse faili `/etc/audit/rules.d/*.rules` (sama süntaks ilma `auditctl`-ita) ja laaditakse käsuga `sudo augenrules --load`.

Auditilogi näitab ka **algset kasutajat** (`auid`), isegi kui tegevus tehti `sudo` abil juurkasutajana - nii on näha, kes muudatuse tegelikult tegi.

## 11.9 Turvaaudit

**Lynis** kontrollib süsteemi sadade turvanõuete vastu ja annab soovitusi:

```bash
sudo apt install lynis                     # Ubuntu, Debian
sudo dnf install lynis                     # AlmaLinux (EPEL)
sudo lynis audit system
```

Tulemuse lõpus on **karastamise indeks** (*hardening index*) ja soovituste loend. Täielik aruanne on failis `/var/log/lynis-report.dat`. Kõiki soovitusi ei pea järgima - mõtle iga puhul, kas see on sinu serveri jaoks oluline.

Muud kasulikud tööriistad:

| Tööriist | Kasutus |
|---|---|
| `nmap` | Pordiskanner - vaata oma serverit nii, nagu ründaja seda näeb (ainult oma masinaid!) |
| `rkhunter`, `chkrootkit` | Juurkomplektide (*rootkit*) otsimine |
| `aide` | Failide terviklikkuse kontroll: märkab, kui süsteemifaile on muudetud |
| CIS Benchmarks | Rahvusvaheliselt tunnustatud karastamise juhendid iga distro jaoks |

> [!WARNING]
> **Ainult oma süsteemid!** Pordiskannimine ja turvatestimine võõraste süsteemide vastu ilma loata on ebaseaduslik. Kooli laboris tee neid ainult oma virtuaalmasinate vastu või õpetaja loal.

## 11.10 Turvasündmuste haldus: Wazuh

Kui servereid on palju, ei jõua keegi iga masina logisid käsitsi lugeda. **SIEM** (*Security Information and Event Management*) kogub logid ja sündmused kõigist masinatest kokku, analüüsib neid reeglite järgi ja annab märku kahtlastest tegevustest.

**Wazuh** on vaba SIEM- ja XDR-platvorm, mida kasutatakse ka koolides ja väiksemates ettevõtetes. Sellel on kolm osa:

| Komponent | Roll |
|---|---|
| **Wazuh server** (manager) | võtab agentidelt sündmused vastu ja analüüsib neid reeglite järgi |
| **Wazuh indexer** | OpenSearchil põhinev andmebaas sündmuste salvestamiseks ja otsimiseks |
| **Wazuh dashboard** | veebiliides (HTTPS) |
| **Wazuh agent** | jälgitavas masinas: saadab logid, kontrollib failide terviklikkust, otsib haavatavusi |

Wazuh oskab näiteks:

- koguda ja analüüsida logisid (SSH sisselogimiskatsed, `sudo` kasutamine, veebiserveri vead);
- jälgida failide muutumist (*File Integrity Monitoring*, sarnane `aide`-ga);
- leida paigaldatud pakettide teadaolevaid haavatavusi (CVE);
- kontrollida seadistust CIS Benchmarki järgi (*Security Configuration Assessment*);
- reageerida automaatselt (nt blokeerida IP-aadress, sarnane fail2ban-iga).

<!-- PILT: ../pildid/m11-wazuh-armatuurlaud.png | Wazuhi veebiliidese ülevaade (agentide olek, turvasündmused) -->

### Paigaldus Dockeriga (üks sõlm)

Laboris on lihtsaim käivitada kõik komponendid konteineritena Dockeri masinas (nt `ubuntusrv`, moodul 12). Wazuh vajab vähemalt **4 GiB mälu** (soovitatavalt 8 GiB) ja 2 protsessorituuma.

```bash
# OpenSearch vajab suuremat mälukaartide arvu
echo "vm.max_map_count=262144" | sudo tee /etc/sysctl.d/90-wazuh.conf
sudo sysctl --system

git clone https://github.com/wazuh/wazuh-docker.git -b v4.x.x    # asenda uusima stabiilse väljalaske sildiga
cd wazuh-docker/single-node
sudo docker compose -f generate-indexer-certs.yml run --rm generator   # komponentidevahelised TLS-sertifikaadid
sudo docker compose up -d
sudo docker compose ps
```

Väljalaskesildid (*tags*) leiad hoidla lehelt GitHubis või käsuga `git ls-remote --tags https://github.com/wazuh/wazuh-docker.git`. Veebiliides avaneb aadressil `https://<masina-IP>`; vaikimisi kasutajanimi ja parool on kirjas hoidla failis `docker-compose.yml` ja dokumentatsioonis - **muuda need kohe** (juhend: Wazuh docs → *Wazuh Docker deployment* → *Change the default password*).

### Agentide lisamine

Kõige lihtsam on kasutada veebiliidese nuppu *Deploy new agent*: vali operatsioonisüsteem ja arhitektuur, sisesta serveri aadress ning liides genereerib käsud. Need näevad välja umbes nii:

```bash
# Debian / Ubuntu
wget https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_<versioon>_amd64.deb
sudo WAZUH_MANAGER='10.0.83.54' WAZUH_AGENT_NAME='debian1' dpkg -i ./wazuh-agent_<versioon>_amd64.deb

# AlmaLinux
sudo WAZUH_MANAGER='10.0.83.54' WAZUH_AGENT_NAME='alma' rpm -ihv https://packages.wazuh.com/4.x/yum/wazuh-agent-<versioon>.x86_64.rpm

sudo systemctl daemon-reload
sudo systemctl enable --now wazuh-agent
```

Agent peab olema **sama või vanem versioon** kui server. Agent ühendub serveriga pordil **1514/tcp** (sündmused) ja registreerub pordil **1515/tcp** - need peavad olema serveris kättesaadavad. (Docker avaldab konteineri pordid ise iptables/nftables reeglitega, mis ei läbi `ufw`-d - piira ligipääsu vajadusel OPNsense'is või Dockeri reeglitega.) Windowsi agent paigaldatakse MSI-paketiga samast veebiliidese viisardist.

Agendi seadistus on failis `/var/ossec/etc/ossec.conf`, logi `/var/ossec/logs/ossec.log`.

### Automaatne reageerimine (active response)

Wazuh võib sündmusele ka ise reageerida - näiteks blokeerida SSH-d murda prooviva aadressi kõigis agentides, sarnaselt fail2ban-iga, kuid tsentraalselt. Reageerimine seadistatakse **serveri** seadistusfailis (Dockeri paigalduses `single-node/config/wazuh_cluster/wazuh_manager.conf`), `<ossec_config>` ploki sisse:

```xml
<active-response>
  <command>firewall-drop</command>   <!-- valmis käsk: lisab tulemüürireegli -->
  <location>local</location>         <!-- käivita agendis, kus sündmus tekkis -->
  <rules_id>5763</rules_id>          <!-- reegel: SSH jõurünne (brute force) -->
  <timeout>600</timeout>             <!-- eemalda blokeering 10 minuti pärast -->
</active-response>
```

Pärast muudatust taaskäivita server (`sudo docker compose restart wazuh.manager`). Agendi poolel näeb reageerimise logi failis `/var/ossec/logs/active-responses.log`. Reegli numbri leiad veebiliidesest (*Server management* → *Rules*) sündmuse juurest.

> [!WARNING]
> **Ettevaatust:** automaatne blokeerimine võib lukustada välja ka sinu enda (nt kui proovid mitu korda vale võtmega). Lisa oma haldusvõrk erandiks (`<white_list>` ploki `<global>` all) ja testi enne, kui lülitad selle sisse tootmises.

> [!NOTE]
> **Märkus:** Wazuh on suur süsteem ja selle seadistamine on omaette eriala. Selles kursuses on eesmärk näha, kuidas tsentraalne turvaseire töötab, ja seostada seda logide, fail2ban-i ja auditiga, mida tegid käsitsi.

---

## Distrode erinevused

| | **Debian** | **Ubuntu** | **AlmaLinux** |
|---|---|---|---|
| MAC | AppArmor | AppArmor | SELinux |
| Automaatsed uuendused | `unattended-upgrades` (tuleb paigaldada) | `unattended-upgrades` (vaikimisi sees) | `dnf-automatic` |
| Autentimislogi | journal | `/var/log/auth.log` | `/var/log/secure` |
| Üldine logi | journal | `/var/log/syslog` | `/var/log/messages` |
| auditd | Tuleb paigaldada | Tuleb paigaldada | Vaikimisi paigaldatud |
| fail2ban | Põhihoidla, `backend = systemd` | Põhihoidla | EPEL |
| Turvateated | DSA | USN | ALSA |

---

## Kokkuvõte

| Käsk või fail | Tegevus |
|---|---|
| `unattended-upgrades`, `dnf-automatic` | Automaatsed turvauuendused |
| `/etc/fail2ban/jail.local`, `fail2ban-client` | Rünnakute blokeerimine |
| `journalctl`, `last`, `lastb`, `logger` | Logide lugemine ja kirjutamine |
| `journald.conf.d/`, `journalctl --vacuum-size` | journal'i haldus |
| `/etc/logrotate.d/`, `logrotate -d` | Logide rotatsioon |
| `getenforce`, `setenforce`, `sestatus` | SELinuxi režiim |
| `ls -Z`, `restorecon`, `semanage fcontext` | SELinuxi kontekstid |
| `semanage port`, `setsebool -P` | SELinuxi pordid ja tõeväärtused |
| `ausearch -m AVC`, `audit2why` | SELinuxi diagnostika |
| `aa-status`, `aa-complain`, `aa-enforce` | AppArmor |
| `auditctl -w`, `ausearch -k` | Audit |
| `lynis audit system` | Turvaaudit |
| `docker compose up -d` (wazuh-docker), `wazuh-agent` | Tsentraalne turvaseire (SIEM) |

**Järgmised sammud:** tee [laboritööd](labor.md) ja kontrolli oma teadmisi [enesekontrolli](enesekontroll.md) abil.

## Lisamaterjal

- Red Hat Enterprise Linux dokumentatsioon - „Using SELinux“ (docs.redhat.com)
- Dan Walsh - „SELinux Coloring Book“ - SELinuxi põhimõtted piltidena
- Ubuntu Server dokumentatsioon - Security, AppArmor (documentation.ubuntu.com)
- CIS Benchmarks (cisecurity.org) - karastamise juhendid
- Debian Securing Manual (debian.org/doc)

<!-- navigatsioon -->
---

[← Moodul 10. Enesekontroll](../moodul-10-alglaadimine-kernel/enesekontroll.md) · [Sisukord](../../README.md#sisukord) · [Laboritöö 11. Turvalisus ja logid →](labor.md)
<!-- /navigatsioon -->
