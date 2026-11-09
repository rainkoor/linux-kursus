# Laboritöö 11. Turvalisus ja logid

Selles moodulis on kaks laboritööd, kumbki oma distrol:

- **10A - AlmaLinux:** SELinux, automaatsed uuendused, audit;
- **10B - Ubuntu:** logid ja logrotate, fail2ban, AppArmor, turvaaudit.

---

# Laboritöö 11A. SELinux, uuendused ja audit (AlmaLinux)

| | |
|---|---|
| **Distro** | AlmaLinux |
| **Kestus** | 2 × 90 minutit |
| **Vajalik** | AlmaLinuxi virtuaalmasin `sudo` õigusega kasutajaga, internetiühendus |
| **Eesmärk** | Mõista SELinuxi toimimist ja lahendada tüüpilised SELinuxi probleemid; seadistada automaatsed turvauuendused ja audit |

**Aruanne:** vasta küsimustele **A1–A14**.

**Stsenaarium:** paigaldad veebiserveri, mille failid peavad asuma kataloogis `/srv/veeb` ja mis peab kuulama lisaks pordile 80 ka porti 8888. SELinux ei lase seda vaikimisi teha - sinu ülesanne on probleemid lahendada **SELinuxit välja lülitamata**.

## 1. osa. SELinuxi olek ja kontekstid

**1.1** Kontrolli SELinuxi olekut:

```bash
getenforce
sestatus
cat /etc/selinux/config | grep -v '^#'
```

**A1.** Mis režiimis SELinux töötab? Mis on poliitika nimi (`Loaded policy name`)?

**1.2** Uuri kontekste:

```bash
id -Z
ls -Z /etc/passwd /etc/shadow
ls -Zd /home/$USER /tmp /var/www /srv
ps -eZ | grep -E "sshd|systemd " | head -5
```

**A2.** Mis tüüp on failidel `/etc/shadow` ja `/etc/passwd`? Mis tüüp on kataloogil `/srv`? Mis kontekstis töötab `sshd`?

**1.3** Paigalda vajalikud tööriistad:

```bash
sudo dnf install httpd policycoreutils-python-utils setroubleshoot-server
```

## 2. osa. Veebiserver mittestandardses kataloogis

**2.1** Käivita veebiserver ja kontrolli vaikelehte:

```bash
sudo systemctl enable --now httpd
curl -sI http://localhost | head -1
ls -Zd /var/www/html
```

**2.2** Loo veebisaidi kataloog ja leht. Loo leht **kodukataloogis** ja teisalda see:

```bash
sudo mkdir -p /srv/veeb
echo "<h1>Tere, SELinux!</h1>" > ~/index.html
sudo mv ~/index.html /srv/veeb/
sudo chmod 644 /srv/veeb/index.html
ls -lZ /srv/veeb/
```

**2.3** Seadista Apache kasutama uut kataloogi:

```bash
sudo nano /etc/httpd/conf.d/labor.conf
```

```apache
<VirtualHost *:80>
    DocumentRoot /srv/veeb
    <Directory /srv/veeb>
        Require all granted
    </Directory>
</VirtualHost>
```

```bash
sudo apachectl configtest
sudo systemctl restart httpd
curl -s http://localhost
```

**A3.** Mida server vastas? Failiõigused on `644` - miks ei saa veebiserver faili lugeda?

**2.4** Diagnoosi:

```bash
sudo ausearch -m AVC -ts recent
sudo ausearch -m AVC -ts recent | audit2why
sudo journalctl -t setroubleshoot --since "10 min ago"
```

**A4.** Kirjuta AVC teatest välja: protsess (`comm`), tegevus (`{ ... }`), allika tüüp (`scontext`) ja sihi tüüp (`tcontext`). Mida soovitab `setroubleshoot`?

**2.5** Kontrolli, et põhjus on tõesti SELinux, ja lülita see kohe tagasi:

```bash
sudo setenforce 0
curl -s http://localhost
sudo setenforce 1
getenforce
```

**2.6** Lahenda probleem õigesti - lisa poliitikasse kataloogi reegel ja taasta kontekstid:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/srv/veeb(/.*)?"
sudo semanage fcontext -l | grep /srv/veeb
sudo restorecon -Rv /srv/veeb
ls -lZ /srv/veeb/
curl -s http://localhost
```

**A5.** Mis muutus faili kontekstis? Miks oli `index.html` kontekst algselt just selline (vihje: kus fail loodi)? Mis vahe on `semanage fcontext` ja `chcon` vahel?

**2.7** Loo uus fail otse kataloogis ja võrdle konteksti:

```bash
echo "<p>Teine leht</p>" | sudo tee /srv/veeb/teine.html
ls -Z /srv/veeb/
curl -s http://localhost/teine.html
```

**A6.** Millise konteksti sai uus fail ja miks ei olnud seekord `restorecon`-i vaja?

## 3. osa. Mittestandardne port

**3.1** Lisa Apache'ile port 8888:

```bash
echo "Listen 8888" | sudo tee /etc/httpd/conf.d/port8888.conf
sudo systemctl restart httpd
```

**A7.** Mis juhtus? Leia põhjus käskudega `systemctl status httpd`, `journalctl -u httpd -n 20` ja `ausearch -m AVC -ts recent`.

**3.2** Uuri, millised pordid on veebiserverile lubatud, ja lisa port:

```bash
sudo semanage port -l | grep -w http_port_t
sudo semanage port -a -t http_port_t -p tcp 8888
sudo semanage port -l | grep -w http_port_t
sudo systemctl restart httpd
curl -s http://localhost:8888
```

Kui `semanage port -a` teatab, et port on juba mõnele teisele tüübile määratud, kasuta `-a` asemel `-m`.

**A8.** Millised pordid olid algselt `http_port_t` loendis? Miks piirab SELinux ka porte?

**3.3** Ava tulemüüris port 8888 ja testi teisest masinast (või oma arvuti brauserist):

```bash
sudo firewall-cmd --add-port=8888/tcp --permanent
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --reload
```

## 4. osa. Tõeväärtused

**4.1** Uuri veebiserveri tõeväärtusi:

```bash
getsebool -a | grep httpd | head -20
getsebool httpd_can_network_connect httpd_enable_homedirs
```

**4.2** Seadista Apache pöördpuhverserverina, mis suunab aadressi `/vana` päringud teisele veebiserverile (nt laboritöö 7 Ubuntu nginx-ile):

```bash
sudo nano /etc/httpd/conf.d/proxy.conf
```

```apache
ProxyPass        /vana http://UBUNTU_IP/
ProxyPassReverse /vana http://UBUNTU_IP/
```

```bash
sudo systemctl restart httpd
curl -sI http://localhost/vana | head -1
```

**A9.** Mis vastuse said? Mida näitab `ausearch -m AVC -ts recent`?

**4.3** Luba veebiserveril luua võrguühendusi:

```bash
sudo setsebool -P httpd_can_network_connect on
curl -sI http://localhost/vana | head -1
```

**A10.** Mida tähendab võti `-P`? Miks on see tõeväärtus vaikimisi väljas? (Mõtle, mida saaks ründaja teha ülevõetud veebiserveriga, mis tohib igale poole ühenduda.)

## 5. osa. Automaatsed turvauuendused

**5.1** Vaata saadaolevaid turvauuendusi:

```bash
dnf updateinfo summary
dnf updateinfo list --security
```

**5.2** Seadista `dnf-automatic` paigaldama automaatselt ainult turvauuendusi:

```bash
sudo dnf install dnf-automatic
sudo nano /etc/dnf/automatic.conf          # upgrade_type = security, apply_updates = yes
sudo systemctl enable --now dnf-automatic.timer
systemctl list-timers dnf-automatic.timer
```

**A11.** Millal käivitub `dnf-automatic` järgmisena? Leia ühe turvauuenduse kohta CVE number (`dnf updateinfo info <ID>`). Kui uuendusi pole, leia mõni CVE AlmaLinuxi turvateadete lehelt (errata.almalinux.org).

## 6. osa. Audit

**6.1** Lisa auditireeglid oluliste failide jälgimiseks:

```bash
sudo auditctl -w /etc/passwd -p wa -k kasutajad
sudo auditctl -w /etc/sudoers -p wa -k sudoers
sudo auditctl -w /etc/sudoers.d/ -p wa -k sudoers
sudo auditctl -l
```

**6.2** Tekita sündmusi ja otsi neid:

```bash
sudo useradd auditikatse
sudo userdel auditikatse
sudo ausearch -k kasutajad -i | tail -20
sudo aureport --summary
```

**A12.** Millised programmid muutsid faili `/etc/passwd`? Mis on sündmuste juures välja `auid` väärtus ja miks on see oluline, kuigi käsud käivitati `sudo`-ga?

**6.3** Muuda reeglid püsivaks:

```bash
sudo tee /etc/audit/rules.d/90-labor.rules <<'EOF'
-w /etc/passwd -p wa -k kasutajad
-w /etc/sudoers -p wa -k sudoers
-w /etc/sudoers.d/ -p wa -k sudoers
EOF
sudo augenrules --load
sudo auditctl -l
```

**A13.** Kus asub auditilogi fail? Miks võib olla hea saata auditilogid teise serverisse?

## 7. osa. Kokkuvõte

**A14.** Täida tabel: SELinuxi probleem → tunnus → lahendus.

| Probleem | Tunnus | Lahendus (käsk) |
|---|---|---|
| Fail on vale kontekstiga (nt teisaldati `mv`-ga) | | |
| Teenus kasutab mittestandardset kataloogi | | |
| Teenus kasutab mittestandardset porti | | |
| Teenus vajab lisavõimalust (nt võrguühendused) | | |

---

# Laboritöö 11B. Logid, fail2ban, AppArmor ja audit (Ubuntu)

| | |
|---|---|
| **Distro** | Ubuntu Server (LTS) |
| **Kestus** | 2 × 90 minutit |
| **Vajalik** | Laboritöö 7 Ubuntu masin (SSH karastatud, ufw sees) ja teise masinana Debiani virtuaalmasin |
| **Eesmärk** | Hallata logisid, kaitsta SSH-d fail2ban-iga, mõista AppArmori toimimist ja auditeerida serveri turvalisust |

**Aruanne:** vasta küsimustele **B1–B14**.

## 1. osa. Logid

**1.1** Uuri logikataloogi ja autentimislogi:

```bash
ls -lh /var/log/
sudo tail -20 /var/log/auth.log
last -n 10
sudo lastb -n 10
```

**B1.** Millised on kataloogi `/var/log` suurimad failid? Kes ja millal viimati sisse logis? Kas on ebaõnnestunud sisselogimisi?

**1.2** Otsi journal'ist `sudo` kasutamine ja SSH sündmused:

```bash
journalctl _COMM=sudo --since today | tail -10
journalctl -u ssh --since today | tail -10
```

**1.3** Kirjuta logisse oma teade ja leia see:

```bash
logger -t labor10 -p user.warning "Testteade laboritööst"
journalctl -t labor10
grep labor10 /var/log/syslog
```

**B2.** Kas teade jõudis nii journal'isse kui ka faili `/var/log/syslog`? Miks?

**1.4** Piira journal'i mahtu:

```bash
journalctl --disk-usage
sudo mkdir -p /etc/systemd/journald.conf.d
sudo tee /etc/systemd/journald.conf.d/90-labor.conf <<'EOF'
[Journal]
Storage=persistent
SystemMaxUse=300M
MaxRetentionSec=1month
EOF
sudo systemctl restart systemd-journald
journalctl --disk-usage
```

### logrotate

**1.5** Loo väljamõeldud rakenduse logi ja selle rotatsioonireegel:

```bash
sudo mkdir -p /var/log/minurakendus
for i in $(seq 1 5000); do echo "$(date '+%F %T') rida $i"; done | sudo tee /var/log/minurakendus/rakendus.log > /dev/null
ls -lh /var/log/minurakendus/
```

```bash
sudo tee /etc/logrotate.d/minurakendus <<'EOF'
/var/log/minurakendus/*.log {
    daily
    rotate 3
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root adm
}
EOF
```

**1.6** Testi ja sunni rotatsiooni mitu korda:

```bash
sudo logrotate -d /etc/logrotate.d/minurakendus
for i in 1 2 3 4 5; do
    echo "uus rida $i" | sudo tee -a /var/log/minurakendus/rakendus.log > /dev/null
    sudo logrotate -f /etc/logrotate.d/minurakendus
    ls /var/log/minurakendus/
done
```

**B3.** Mitu faili jäi lõpuks alles ja millised neist on pakitud? Mida tegid valikud `rotate 3` ja `delaycompress`?

## 2. osa. Automaatsed uuendused

**2.1** Kontrolli `unattended-upgrades` seadistust:

```bash
cat /etc/apt/apt.conf.d/20auto-upgrades
grep -v '^\s*//' /etc/apt/apt.conf.d/50unattended-upgrades | grep -v '^\s*$' | head -30
systemctl list-timers 'apt-daily*'
sudo unattended-upgrade --dry-run --debug 2>&1 | tail -15
ls /var/log/unattended-upgrades/
```

**B4.** Kas automaatsed uuendused on sisse lülitatud? Milliseid hoidlaid (`Allowed-Origins`) need hõlmavad? Kas masin taaskäivitatakse automaatselt (`Automatic-Reboot`)?

## 3. osa. fail2ban

**3.1** Paigalda ja seadista fail2ban:

```bash
sudo apt install fail2ban
sudo tee /etc/fail2ban/jail.local <<'EOF'
[DEFAULT]
bantime  = 10m
findtime = 10m
maxretry = 3

[sshd]
enabled = true
EOF
sudo systemctl enable --now fail2ban
sudo systemctl restart fail2ban
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

**3.2** Simuleeri rünnakut **Debiani masinast**: proovi 4–5 korda sisse logida olematu kasutajanimega:

```bash
for i in 1 2 3 4 5; do ssh -o ConnectTimeout=5 olematu$i@UBUNTU_IP exit; done
```

(Kuna paroolid on laboritöös 7 keelatud, keeldub server kohe. Logisse jääb siiski kirje `Invalid user ...`.)

**3.3** Ubuntu masinas:

```bash
sudo fail2ban-client status sshd
sudo grep "Invalid user" /var/log/auth.log | tail -5
sudo nft list ruleset | grep -A3 f2b
```

**B5.** Kas Debiani IP-aadress blokeeriti? Mitu katset kulus? Kuidas oli blokeering tulemüüris näha?

**3.4** Proovi Debiani masinast ühenduda (ka õige kasutajaga): `ssh kasutaja@UBUNTU_IP`. Seejärel vabasta aadress:

```bash
sudo fail2ban-client set sshd unbanip DEBIAN_IP
```

**B6.** Mis juhtus ühenduskatsega blokeeringu ajal? Miks on oluline seada `ignoreip` oma administraatorivõrgule?

## 4. osa. AppArmor

**4.1** Uuri AppArmori olekut:

```bash
sudo aa-status
ls /etc/apparmor.d/
```

**B7.** Mitu profiili on laaditud? Mitu on enforce- ja mitu complain-režiimis? Nimeta kolm programmi, millel on profiil.

**4.2** Loo skript, mis loeb faili, mille nimi antakse argumendina:

```bash
sudo tee /usr/local/bin/loe-faili <<'EOF'
#!/bin/bash
cat "$1"
EOF
sudo chmod 755 /usr/local/bin/loe-faili
loe-faili /etc/hostname
loe-faili /etc/passwd | head -3
```

**4.3** Loo skriptile AppArmori profiil, mis lubab lugeda ainult faili `/etc/hostname`:

```bash
sudo tee /etc/apparmor.d/usr.local.bin.loe-faili <<'EOF'
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
EOF
sudo apparmor_parser -r /etc/apparmor.d/usr.local.bin.loe-faili
sudo aa-status | grep loe-faili
```

**4.4** Testi:

```bash
loe-faili /etc/hostname
loe-faili /etc/passwd
sudo loe-faili /etc/shadow
sudo journalctl -k --since "5 min ago" | grep -i apparmor
```

**B8.** Milliseid faile skript sai lugeda ja milliseid mitte? Kas `sudo` aitas faili `/etc/shadow` lugeda? Miks? Kirjuta üks `DENIED` logirida aruandesse.

**4.5** Lülita profiil complain-režiimi ja korda testi:

```bash
sudo apt install apparmor-utils
sudo aa-complain /usr/local/bin/loe-faili
loe-faili /etc/passwd | head -3
sudo journalctl -k --since "2 min ago" | grep -i apparmor | tail -3
sudo aa-enforce /usr/local/bin/loe-faili
```

**B9.** Mis vahe oli complain- ja enforce-režiimil? Milleks on complain-režiim kasulik?

## 5. osa. Turvaaudit

**5.1** Käivita turvaaudit:

```bash
sudo apt install lynis
sudo lynis audit system 2>&1 | tee ~/lynis.txt | tail -40
```

**B10.** Mis on karastamise indeks (*hardening index*)? Nimeta kolm hoiatust (*warnings*) või soovitust (*suggestions*), mis tunduvad sinu serveri jaoks olulised.

**5.2** Vali kolm Lynise soovitust, rakenda need ja käivita audit uuesti.

**B11.** Milliseid soovitusi rakendasid ja kuidas? Kas indeks muutus?

**5.3** Vaata oma serverit „ründaja pilgu läbi“ - **Debiani masinast** (ainult oma laborimasina vastu!):

```bash
sudo apt install nmap
nmap UBUNTU_IP
sudo nmap -sV UBUNTU_IP
```

**B12.** Millised pordid ja teenused on väljast nähtavad? Kas `nmap` tuvastas tarkvara versioonid? Kas midagi on avatud, mis ei peaks olema?

## 6. osa. Kokkuvõte

**B13.** Loetle kõik turvameetmed, mis on sinu Ubuntu serveris laboritööde 3, 7 ja 11 järel rakendatud, ja seosta need punktis 11.1 toodud põhimõtetega.

**B14.** Võrdle SELinuxit (laboritöö 11A) ja AppArmorit: mis on nende põhimõtteline erinevus? Kumba oli sinu arvates lihtsam kasutada?

---

## Lisaülesanne (valikuline): Wazuh SIEM

Vajalik: Dockeriga Ubuntu masin (moodul 12) vähemalt 4 GiB (soovitatavalt 8 GiB) mäluga ja vähemalt 2 jälgitavat masinat (nt `debian1` ja `alma`).

1. Paigalda Wazuh ühe sõlmena Dockeriga (teooria punkt 11.10). Muuda vaikeparool.
2. Lisa veebiliidese viisardiga agendid masinatele `debian1` ja `alma`. Kontrolli, et agendid ühenduvad serveri pordile 1514/tcp ja 1515/tcp. (Docker lisab avaldatud portide reeglid ise ja need ei läbi `ufw` reegleid - mõtle, mida see turvalisuse mõttes tähendab.)
3. Tekita sündmusi: proovi mõnest masinast `ssh vale@debian1` mitu korda vale parooliga, käivita `sudo` vale parooliga, muuda faili `/etc/passwd` (nt `sudo useradd wazuhtest`).
4. Leia sündmused veebiliidesest (*Threat Hunting* / *Security events*).
5. Seadista automaatne reageerimine (teooria punkt 11.10, reegel 5763 ja `firewall-drop`) ning korda SSH jõurünnet mõnest kolmandast masinast. Kontrolli agendis `/var/ossec/logs/active-responses.log` ja `sudo nft list ruleset`.

**W1.** Milliste reeglite (reegli ID ja tase) alla sinu tekitatud sündmused liigitati?

**W2.** Milliseid haavatavusi (*Vulnerability Detection*) leiti agentidega masinates? Milliseid CIS-i soovitusi (*Configuration Assessment*) Debiani masin ei täitnud?

**W3.** Võrdle Wazuhi fail2ban-i ja `auditd`-ga, mida kasutasid selles laboris: mida pakub tsentraalne süsteem, mida üksikud tööriistad ei paku?

**W4.** Kas ründav aadress blokeeriti ja kui kauaks? Mille poolest erineb Wazuhi reageerimine fail2ban-ist (kus otsus tehakse, kus blokeeritakse)?

---

## Õpetajale: kontrollvastused

### 11A

| Küsimus | Vastus |
|---|---|
| A1 | `Enforcing`, poliitika `targeted` |
| A2 | `/etc/shadow` → `shadow_t`, `/etc/passwd` → `passwd_file_t`, `/srv` → `var_t`; `sshd` → `sshd_t` |
| A3 | `403 Forbidden`; failil on vale SELinuxi tüüp (`user_home_t`), mida `httpd_t` ei tohi lugeda |
| A4 | `comm="httpd"`, `{ read }` (või `{ getattr }`), `httpd_t` → `user_home_t` |
| A5 | `user_home_t` → `httpd_sys_content_t`; fail loodi kodukataloogis ja `mv` säilitas konteksti. `semanage fcontext` muudab poliitikat püsivalt, `chcon` ainult faili praegust märgist |
| A6 | `httpd_sys_content_t` - uus fail sai konteksti kataloogi järgi, kus see loodi |
| A7 | `httpd` ei käivitu: `Permission denied: make_sock: could not bind to address ...:8888`; AVC `name_bind` |
| A8 | Muu hulgas 80, 81, 443, 488, 8008, 8009, 8443, 9000. Ülevõetud teenus ei saa avada suvalist porti (nt tagaukse jaoks) |
| A9 | `503 Service Unavailable`; AVC `name_connect` `httpd_t` → `http_port_t` |
| A10 | Püsiv (säilib taaskäivitusel). Ülevõetud veebiserver saaks muidu rünnata sisevõrgu teisi masinaid |
| A12 | `useradd`, `userdel`; `auid` näitab algset sisselogitud kasutajat, mitte `root`-i |
| A13 | `/var/log/audit/audit.log`; ründaja võib kohalikud logid kustutada |

A14:

| Probleem | Tunnus | Lahendus |
|---|---|---|
| Vale kontekst | AVC, `tcontext` on nt `user_home_t` | `restorecon -Rv tee` |
| Mittestandardne kataloog | AVC, `tcontext` on nt `var_t` | `semanage fcontext -a -t ... "tee(/.*)?"` + `restorecon` |
| Mittestandardne port | Teenus ei käivitu, AVC `name_bind` | `semanage port -a -t ... -p tcp PORT` |
| Lisavõimalus | AVC, nt `name_connect` | `setsebool -P tõeväärtus on` |

### 11B

| Küsimus | Vastus |
|---|---|
| B2 | Jah: journald edastab teated rsyslog'ile, mis kirjutab need faili `/var/log/syslog` |
| B3 | `rakendus.log`, `rakendus.log.1` (pakkimata, `delaycompress`), `.2.gz`, `.3.gz`; vanemad kustutati |
| B4 | Tavaliselt sees; `${distro_id}:${distro_codename}-security` jt; `Automatic-Reboot` vaikimisi `false` |
| B5 | Jah, pärast `maxretry` (3) katset; reegel nftables'i tabelis (`f2b-sshd`) |
| B6 | Ühendus aegus või keelduti; muidu võib administraator ennast kogemata välja lukustada |
| B8 | Ainult `/etc/hostname`; `sudo` ei aidanud - AppArmor kehtib ka juurkasutajale |
| B9 | Complain logib, kuid ei keela; sobib profiili koostamiseks ja testimiseks |
| B14 | SELinux - märgised kõigil objektidel (kogu süsteem); AppArmor - teed, ainult profiiliga programmid |
| W1 | sshd reeglid 57xx (autentimise ebaõnnestumine tase 5, korduvad katsed kõrgema tasemega), `sudo` reeglid 54xx, PAM 55xx, uus kasutaja 59xx; täpsed ID-d ja tasemed sõltuvad versioonist |
| W2 | Sõltub pakettidest; CIS-i kontrollist tavaliselt nt eraldi partitsioonid `/tmp`-le, auditi reeglid, paroolipoliitika |
| W3 | Kõigi masinate sündmused ühes kohas, korrelatsioon, ajalugu ka siis, kui ründaja kustutab kohalikud logid, häired, haavatavuste ja seadistuse kontroll |
| W4 | Jah, `timeout` sekunditeks (600 s); reegel on agendi tulemüüris. fail2ban otsustab ja blokeerib samas masinas oma logide põhjal; Wazuhis otsustab server kõigi agentide sündmuste põhjal ja käsib agendil blokeerida (saab blokeerida ka kõigis agentides korraga, `location` = `all`) |

> **Märkus õpetajale:** laboritööd ei saanud testida päris AlmaLinuxi ja Ubuntu masinas. SELinuxi osa (kontekst, port, tõeväärtus) on standardne RHEL-i stsenaarium. AppArmori skriptiprofiil (4. osa) põhineb Ubuntu AppArmor 3/4 süntaksil - kui profiil ei rakendu (`aa-status` ei näita seda või skript loeb kõike), kontrolli `sudo apparmor_parser -r` veateadet ja teid (`which bash cat`). Pordi 8888 puhul kontrolli enne tundi, et see ei ole poliitikas mõnele muule tüübile määratud (`semanage port -l | grep 8888`).
