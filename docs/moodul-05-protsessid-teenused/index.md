# Moodul 5. Protsessid, teenused ja systemd

**Maht:** 8 tundi · **Laboritöö:** AlmaLinux · **Eeldused:** moodulid 1–4

## Õpiväljundid

Mooduli läbinud õppija:

- selgitab, mis on protsess, PID ja protsessi olek;
- jälgib protsesse käskudega `ps`, `top` ja `htop`;
- saadab protsessidele signaale ja lõpetab neid;
- haldab esi- ja taustatöid ning protsesside prioriteete;
- haldab teenuseid käsuga `systemctl`;
- kirjutab lihtsa systemd teenuse- ja taimerifaili;
- otsib logidest infot käsuga `journalctl`;
- ajastab korduvaid ülesandeid cron'i ja systemd taimeri abil;
- ajastab ühekordse töö käsuga `at`;
- piirab kasutajate (`ulimit`, `limits.conf`) ja teenuste (`MemoryMax=`, `CPUQuota=`) ressursikasutust.

---

## 5.1 Protsessid

**Protsess** on töötav programm. Kui käivitad käsu `ls`, loob kernel protsessi, mis töötab, kuni `ls` on oma töö teinud. Serveris töötavad pidevalt sajad protsessid: teenused, kasutajate kestad, taustatööd.

Igal protsessil on:

| Omadus | Selgitus |
|---|---|
| **PID** | Protsessi unikaalne number (*process ID*) |
| **PPID** | Vanemprotsessi PID - protsess, mis selle käivitas |
| **Omanik** | Kasutaja, kelle õigustes protsess töötab |
| **Olek** | Mida protsess parajasti teeb |
| **Ressursid** | Protsessori- ja mälukasutus |

Kõik protsessid moodustavad puu. Selle juur on protsess **PID 1** - tänapäeva distrodes **systemd**, mis käivitatakse alglaadimisel esimesena ja mis käivitab kõik ülejäänud teenused.

### Protsesside olekud

| Täht | Olek | Selgitus |
|---|---|---|
| `R` | *Running* | Töötab või ootab protsessorit |
| `S` | *Sleeping* | Ootab sündmust (nt sisendit). Enamik protsesse on selles olekus |
| `D` | *Uninterruptible sleep* | Ootab sisend-väljundtoimingut (nt ketast). Ei reageeri signaalidele |
| `T` | *Stopped* | Peatatud (nt Ctrl+Z) |
| `Z` | *Zombie* | Lõpetanud töö, kuid vanemprotsess pole selle tulemust veel kätte saanud |

## 5.2 Protsesside vaatamine

### ps

`ps` näitab protsesside hetkeseisu.

```bash
ps                           # minu protsessid praeguses terminalis
ps aux                       # kõik protsessid (BSD stiil)
ps -ef                       # kõik protsessid (UNIX stiil, näitab PPID-d)
ps aux | grep sshd           # otsi kindlat protsessi
ps -eo pid,user,%cpu,%mem,cmd --sort=-%cpu | head   # enim protsessorit kasutavad
```

`ps aux` väljund:

```text
USER   PID %CPU %MEM    VSZ   RSS TTY   STAT START   TIME COMMAND
root     1  0.0  0.6 108000 12500 ?     Ss   09:00   0:02 /usr/lib/systemd/systemd
mari  2345  0.1  0.2  10200  5200 pts/0 Ss   10:15   0:00 -bash
```

| Veerg | Tähendus |
|---|---|
| `%CPU`, `%MEM` | Protsessori ja mälu kasutus protsentides |
| `RSS` | Tegelikult kasutatav mälu (KB) |
| `TTY` | Terminal. `?` tähendab, et protsess ei ole terminaliga seotud (teenus) |
| `STAT` | Olek, nt `S` - magab, `s` - seansi juht, `+` - esiplaanil |
| `COMMAND` | Käivitatud käsk |

### pgrep ja pstree

```bash
pgrep sshd                   # sshd protsesside PID-d
pgrep -a -u mari             # kasutaja mari protsessid koos käsuga
pstree -p                    # protsesside puu koos PID-dega
```

`pstree` kuulub paketti `psmisc`, mida minimaalsel paigaldusel ei pruugi olla.

### top ja htop

`top` näitab protsesse reaalajas.

```bash
top
```

Ülaosas on süsteemi kokkuvõte:

```text
top - 10:30:15 up 2 days,  3:12,  1 user,  load average: 0.15, 0.10, 0.05
Tasks: 112 total,   1 running, 111 sleeping,   0 stopped,   0 zombie
%Cpu(s):  2.0 us,  1.0 sy,  0.0 ni, 96.5 id,  0.5 wa, ...
MiB Mem :   1967.0 total,    812.4 free,    455.1 used,    699.5 buff/cache
```

**Koormus** (*load average*) näitab viimase 1, 5 ja 15 minuti keskmist protsesside arvu, mis töötavad või ootavad protsessorit. Rusikareegel: kui koormus on püsivalt suurem kui protsessorituumade arv (`nproc`), on süsteem ülekoormatud.

Mälu juures tasub vaadata välja `avail Mem`, mitte `free`. Linux kasutab vaba mälu failide vahemäluks (`buff/cache`), mis vabastatakse vajadusel kohe.

Klahvid `top`-is:

| Klahv | Tegevus |
|---|---|
| **P** | Sorteeri protsessori järgi |
| **M** | Sorteeri mälu järgi |
| **k** | Saada protsessile signaal (küsib PID-d) |
| **u** | Näita ühe kasutaja protsesse |
| **1** | Näita iga protsessorituuma eraldi |
| **q** | Välju |

**htop** on mugavam ja värviline `top`-i alternatiiv, mida saab kasutada ka hiirega. Selle peab tavaliselt eraldi paigaldama (AlmaLinuxis EPEL-ist).

## 5.3 Signaalid

**Signaal** on teade, mille kernel või teine protsess protsessile saadab. Protsess võib signaalile reageerida, seda ignoreerida või kasutada vaikekäitumist.

| Nr | Nimi | Vaikekäitumine | Kasutus |
|---|---|---|---|
| 1 | `SIGHUP` | Lõpeta | Paljud teenused loevad seepeale seadistuse uuesti |
| 2 | `SIGINT` | Lõpeta | Ctrl+C |
| 9 | `SIGKILL` | Lõpeta kohe | Sundlõpetamine, protsess ei saa seda ignoreerida |
| 15 | `SIGTERM` | Lõpeta | Viisakas palve lõpetada (vaikimisi signaal) |
| 18 | `SIGCONT` | Jätka | Jätka peatatud protsessi |
| 19 | `SIGSTOP` | Peata | Peatamine, ei saa ignoreerida |
| 20 | `SIGTSTP` | Peata | Ctrl+Z |

```bash
kill 2345                    # saada SIGTERM (viisakas lõpetamine)
kill -9 2345                 # saada SIGKILL (sundlõpetamine)
kill -HUP 2345               # saada SIGHUP
pkill -u mari                # lõpeta kõik kasutaja mari protsessid
killall firefox              # lõpeta kõik protsessid nimega firefox
kill -l                      # kõik signaalid
```

> [!TIP]
> **Hea tava:** proovi alati kõigepealt `kill` (SIGTERM), mis laseb programmil oma töö korrektselt lõpetada: salvestada andmed, sulgeda failid ja ühendused. `kill -9` kasuta alles siis, kui protsess ei reageeri, sest see võib jätta andmed poolikuks.

Tavakasutaja saab signaale saata ainult oma protsessidele, juurkasutaja kõigile.

## 5.4 Esi- ja taustatööd

Tavaliselt töötab käsk **esiplaanil**: kest ootab, kuni see lõpetab. Pikaajalise käsu saab käivitada ka **taustal**, et terminal jääks vabaks.

```bash
sleep 300 &                  # käivita taustal (& lõpus)
jobs                         # selle kesta tööd
fg %1                        # too töö nr 1 esiplaanile
```

Juba töötava käsu saab tausta saata:

1. vajuta **Ctrl+Z** - käsk peatatakse;
2. kirjuta `bg` - käsk jätkab taustal.

| Käsk | Tegevus |
|---|---|
| `käsk &` | Käivita taustal |
| **Ctrl+Z** | Peata esiplaanil olev töö |
| `jobs` | Näita töid |
| `bg %n` | Jätka tööd taustal |
| `fg %n` | Too töö esiplaanile |
| `kill %n` | Lõpeta töö |

### Seansist sõltumatud protsessid

Kui logid välja, saavad sinu kesta tööd signaali `SIGHUP` ja lõpetavad. Et pikk töö jätkuks ka pärast väljalogimist:

```bash
nohup ./pikk-skript.sh > valjund.log 2>&1 &
```

Mugavam lahendus on terminali multiplekser **tmux** (või vanem **screen**): sellega saab seansist lahti ühenduda ja hiljem uuesti tagasi tulla, nii et kõik töötab edasi. Püsivalt töötavad programmid tuleb aga muuta **teenusteks** (vt punkt 5.6).

## 5.5 Prioriteedid

Protsessori jagamist mõjutab protsessi **nice-väärtus** vahemikus **−20** (kõrgeim prioriteet) kuni **19** (madalaim). Vaikimisi on see 0. Mida „kenam“ (*nicer*) protsess on, seda rohkem annab ta teistele protsessorit.

```bash
nice -n 10 ./varundus.sh     # käivita madalama prioriteediga
renice 15 -p 2345            # muuda töötava protsessi prioriteeti
sudo renice -5 -p 2345       # kõrgemat prioriteeti saab anda ainult juurkasutaja
```

Prioriteeti tasub alandada näiteks varundus- ja arhiveerimistöödel, et need ei aeglustaks teenuseid.

## 5.6 systemd ja teenused

**Teenus** (*service*, UNIX-is ka *daemon*) on taustal pidevalt töötav programm, näiteks SSH-server, veebiserver või andmebaas. Tänapäeva distrodes haldab teenuseid **systemd**.

systemd haldab **üksusi** (*units*). Olulisemad tüübid:

| Tüüp | Laiend | Mida kirjeldab |
|---|---|---|
| Teenus | `.service` | Taustaprogramm |
| Taimer | `.timer` | Ajastatud käivitus |
| Pesa | `.socket` | Võrgu- või kohalik pesa, mille kaudu teenus käivitub |
| Eesmärk | `.target` | Üksuste rühm (süsteemi olek, nt `multi-user.target`) |
| Haakepunkt | `.mount` | Failisüsteemi haakimine |

### systemctl

```bash
systemctl status sshd                 # teenuse olek ja viimased logiread
sudo systemctl start httpd            # käivita
sudo systemctl stop httpd             # peata
sudo systemctl restart httpd          # taaskäivita
sudo systemctl reload httpd           # loe seadistus uuesti (ilma katkestuseta)
sudo systemctl enable httpd           # käivita automaatselt alglaadimisel
sudo systemctl disable httpd          # ära käivita automaatselt
sudo systemctl enable --now httpd     # luba ja käivita kohe
systemctl is-active httpd             # kas töötab
systemctl is-enabled httpd            # kas on lubatud
```

> [!WARNING]
> **start ja enable on eri asjad!** `start` käivitab teenuse **praegu**, `enable` määrab, et teenus käivitub **järgmisel alglaadimisel**. Uue teenuse puhul on tavaliselt vaja mõlemat: `enable --now`.

`systemctl status` väljund:

```text
● sshd.service - OpenSSH server daemon
     Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; preset: enabled)
     Active: active (running) since Mon 2026-11-02 09:00:12 EET; 2 days ago
   Main PID: 812 (sshd)
     CGroup: /system.slice/sshd.service
             └─812 "sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups"
```

| Rida | Tähendus |
|---|---|
| `Loaded` | Üksuse fail ja kas teenus on lubatud (`enabled`/`disabled`) |
| `Active` | Kas töötab (`active (running)`), on peatatud (`inactive`) või kokku jooksnud (`failed`) |
| `Main PID` | Teenuse põhiprotsess |

Ülevaade kõigist teenustest:

```bash
systemctl list-units --type=service           # töötavad teenused
systemctl list-units --type=service --all     # kõik laaditud teenused
systemctl --failed                            # kokku jooksnud üksused
systemctl list-unit-files --type=service      # kõik teenused ja nende lubamise olek
```

Teenuse saab ka täielikult blokeerida, nii et seda ei saa käivitada isegi käsitsi: `systemctl mask teenus` (tagasi: `unmask`).

### Üksuse failid

| Asukoht | Kasutus |
|---|---|
| `/usr/lib/systemd/system/` | Pakettidega paigaldatud üksused. **Ära muuda neid** - uuendus kirjutab need üle |
| `/etc/systemd/system/` | Administraatori üksused ja muudatused. Siinsed failid on eelistatud |

```bash
systemctl cat sshd                    # näita üksuse faili
sudo systemctl edit httpd             # loo muudatusfail (drop-in) olemasolevale üksusele
sudo systemctl daemon-reload          # loe üksuste failid pärast käsitsi muutmist uuesti
```

`systemctl edit` loob faili `/etc/systemd/system/httpd.service.d/override.conf`, kuhu kirjutad ainult muudetavad read. Nii jääb paketi originaalfail puutumata.

### Oma teenuse loomine

Teenuse fail `/etc/systemd/system/minuteenus.service`:

```ini
[Unit]
Description=Minu näidisteenus
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/minuteenus.sh
User=nobody
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

| Jaotis ja võti | Tähendus |
|---|---|
| `[Unit] Description` | Kirjeldus, mida näitab `systemctl status` |
| `[Unit] After` | Käivita pärast neid üksusi |
| `[Service] ExecStart` | Käivitatav programm (**täielik tee!**) |
| `[Service] User` | Kasutaja, kelle õigustes teenus töötab |
| `[Service] Restart` | Millal teenus automaatselt taaskäivitada (`on-failure`, `always`, `no`) |
| `[Install] WantedBy` | Millise eesmärgiga koos teenus `enable` korral käivitub |

Seejärel:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now minuteenus
systemctl status minuteenus
```

`Restart=on-failure` taaskäivitab teenuse, kui see lõpetab veakoodiga või sunnitakse lõpetama (nt `SIGKILL`). Viisaka lõpetamise (`SIGTERM`) või `systemctl stop` järel taaskäivitust ei toimu.

> [!NOTE]
> **Programmi väljund läheb logisse.** Kõik, mida teenus kirjutab standardväljundisse või veaväljundisse, salvestab systemd journal'isse. Eraldi logifaili pole vaja.

Sõltuvused, teenuse tüübid, mallid, pesa- ja teeüksused, kasutajateenused ning teenuste karastamine on põhjalikumalt [moodulis 10, punkt 10.11](../moodul-10-alglaadimine-kernel/index.md#1011-systemd-suvitsi).

## 5.7 Logid: journalctl

systemd kogub kõigi teenuste ja kerneli logid ühte kohta - **journal'isse**. Seda loetakse käsuga `journalctl`.

```bash
journalctl                            # kõik logid (vanimad eespool)
journalctl -e                         # hüppa lõppu
journalctl -f                         # jälgi uusi kirjeid reaalajas (Ctrl+C lõpetab)
journalctl -u sshd                    # ühe teenuse logid
journalctl -u sshd -n 50              # viimased 50 rida
journalctl -b                         # praeguse alglaadimise logid
journalctl -b -1                      # eelmise alglaadimise logid
journalctl -p err                     # ainult vead ja raskemad
journalctl --since "1 hour ago"       # viimase tunni logid
journalctl --since "2026-11-01 08:00" --until "2026-11-01 12:00"
journalctl -k                         # kerneli teated
journalctl --disk-usage               # kui palju logid ruumi võtavad
```

Võtmeid saab kombineerida: `journalctl -u httpd -p warning --since today`.

Tavakasutaja näeb ainult oma logisid. Kõigi logide nägemiseks on vaja `sudo` õigust või kuulumist gruppi `adm` (Debian, Ubuntu) või `wheel`/`systemd-journal`.

### Püsivad logid

Journal võib olla **püsiv** (salvestatakse kataloogi `/var/log/journal`) või **ajutine** (kataloogis `/run/log/journal`, kaob taaskäivitusel). Kui `journalctl --list-boots` näitab ainult üht alglaadimist, kuigi süsteemi on taaskäivitatud, on journal ajutine. Püsivaks muutmiseks:

```bash
sudo mkdir -p /var/log/journal
sudo systemctl restart systemd-journald
```

Lisaks journal'ile kirjutab mõnes distros **rsyslog** logisid ka tavalistesse tekstifailidesse (`/var/log/messages`, `/var/log/syslog`). Logide haldusest räägime täpsemalt moodulis 11.

## 5.8 Ülesannete ajastamine

### cron

**cron** on klassikaline ajastaja, mis käivitab käske kindlatel aegadel. Iga kasutaja ajakava on tema **crontab**'is:

```bash
crontab -e                   # muuda oma ajakava
crontab -l                   # näita oma ajakava
sudo crontab -u mari -l      # näita teise kasutaja ajakava
```

Crontab'i rea vorming:

```text
┌───────── minut (0–59)
│ ┌─────── tund (0–23)
│ │ ┌───── kuupäev (1–31)
│ │ │ ┌─── kuu (1–12)
│ │ │ │ ┌─ nädalapäev (0–7, 0 ja 7 = pühapäev)
│ │ │ │ │
* * * * *  käsk
```

| Näide | Tähendus |
|---|---|
| `30 2 * * * /usr/local/bin/varundus.sh` | Iga päev kell 02:30 |
| `*/15 * * * * /usr/local/bin/kontroll.sh` | Iga 15 minuti järel |
| `0 8 * * 1-5 /usr/local/bin/aruanne.sh` | Tööpäeviti kell 08:00 |
| `0 0 1 * * /usr/local/bin/kuuaruanne.sh` | Iga kuu esimesel päeval keskööl |
| `@reboot /usr/local/bin/start.sh` | Iga alglaadimise järel |

> [!WARNING]
> **Levinud viga:** cron käivitab käsud väga minimaalse keskkonnaga (`PATH` on lühike). Kasuta crontab'is alati **täielikke teid** ja suuna väljund faili, et vigu näha: `... >> /var/log/varundus.log 2>&1`.

Süsteemi ajastatud tööd on failis `/etc/crontab` ja kataloogides `/etc/cron.d/`, `/etc/cron.daily/`, `/etc/cron.weekly/` ja `/etc/cron.monthly/`.

### systemd taimerid

Taimer on cron'i tänapäevane alternatiiv. Taimeri jaoks on vaja kahte faili: teenus, mis tööd teeb, ja taimer, mis selle käivitab.

`/etc/systemd/system/varundus.service`:

```ini
[Unit]
Description=Seadistuste varundus

[Service]
Type=oneshot
ExecStart=/usr/local/bin/varundus.sh
```

`/etc/systemd/system/varundus.timer`:

```ini
[Unit]
Description=Seadistuste varundus iga päev

[Timer]
OnCalendar=*-*-* 02:30:00
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now varundus.timer
systemctl list-timers                         # kõik taimerid ja järgmised käivitused
systemd-analyze calendar "*-*-* 02:30:00"     # kontrolli ajaavaldist
```

`OnCalendar` näited: `daily`, `weekly`, `Mon..Fri 08:00`, `*:0/15` (iga 15 minuti järel). `Persistent=true` tähendab, et kui masin oli ettenähtud ajal väljas, käivitatakse töö pärast alglaadimist.

| | **cron** | **systemd taimer** |
|---|---|---|
| Seadistus | Üks rida | Kaks faili |
| Logid | Tuleb ise suunata | Automaatselt journal'is |
| Vahelejäänud käivitused | Jäävad vahele (v.a anacron) | `Persistent=true` |
| Olek ja järgmine käivitus | Ei näe | `systemctl list-timers` |
| Levik | Kõikjal, ka vanades süsteemides | Kõik systemd-ga distrod |

## 5.9 Ühekordne ajastamine: at

cron ja systemd taimerid on korduvate tööde jaoks. **Ühekordse** töö (nt „taaskäivita teenus täna kell 22“) jaoks on `at`:

```bash
sudo apt install at                 # AlmaLinux: sudo dnf install at
sudo systemctl enable --now atd
echo "systemctl restart nginx" | sudo at 22:00
echo "/usr/local/bin/varunda" | at now + 30 minutes
at -f skript.sh tomorrow 03:00
atq                                 # ootel tööd
at -c 3                             # töö nr 3 sisu
atrm 3                              # kustuta
```

Väljund saadetakse kasutajale e-postiga (moodul 15). systemd alternatiiv: `sudo systemd-run --on-active=30min systemctl restart nginx`.

## 5.10 Ressursipiirangud: ulimit ja systemd

Üks vigane programm või kasutaja võib võtta kogu mälu või protsessori. Linux võimaldab piirata ressursse kahel tasemel.

### ulimit ja limits.conf (kasutajad ja seansid)

```bash
ulimit -a                 # praeguse kesta piirangud
ulimit -n                 # avatud failide arv
ulimit -u 200             # max 200 protsessi selles kestas (ainult vähendada saab)
```

Püsivad piirangud kasutajatele ja gruppidele (rakendab `pam_limits` sisselogimisel), failis `/etc/security/limits.conf` või `/etc/security/limits.d/*.conf`:

```text
# kes          tüüp   ressurss   väärtus
@opilased      hard   nproc      300      # „fork-pommi“ kaitse
mari           soft   nofile     4096
*              hard   core       0        # ära salvesta mälutõmmiseid
```

`soft` on vaikimisi piir, mida kasutaja saab tõsta kuni `hard`-piirini.

### systemd ja cgroups (teenused)

**Teenustele `limits.conf` ei kehti** - systemd käivitab teenused ise. Teenuste ressursse piiratakse **cgroups**-i abil üksuse seadetes:

```ini
# sudo systemctl edit nginx   →   /etc/systemd/system/nginx.service.d/override.conf
[Service]
MemoryMax=500M            # rohkem mälu ei saa (üle selle tapab kernel)
CPUQuota=50%              # kuni pool ühest tuumast
TasksMax=200              # protsesside/lõimede arv
LimitNOFILE=65536         # avatud failide arv (ulimit -n teenusele)
```

```bash
sudo systemctl daemon-reload && sudo systemctl restart nginx
sudo systemctl set-property nginx.service MemoryMax=500M     # sama ilma failita
systemctl show nginx -p MemoryMax -p CPUQuotaPerSecUSec
systemd-cgtop                                                # ressursikasutus cgroup'ide kaupa
sudo systemd-run --scope -p MemoryMax=200M -p CPUQuota=20% stress-ng --vm 1 --vm-bytes 500M   # piiratud ühekordne käsk
```

Kasutajate seansid on systemd-s **lõikudes** (`user-1000.slice`) - piiranguid saab seada ka neile (`systemctl set-property user-1000.slice MemoryMax=2G`). Samal mehhanismil põhinevad konteinerite piirangud (moodul 12).

---

## Distrode erinevused

| | **Debian** | **Ubuntu** | **AlmaLinux** |
|---|---|---|---|
| SSH teenuse nimi | `ssh` (ka `sshd` alias) | `ssh` | `sshd` |
| Veebiserveri teenus | `apache2` | `apache2` | `httpd` |
| cron'i teenus | `cron` | `cron` | `crond` (pakett `cronie`) |
| Teenus käivitub paigaldamisel | Jah, enamasti kohe | Jah, enamasti kohe | Ei, tuleb ise `enable --now` |
| Tekstilogid lisaks journal'ile | Vaikimisi ei (Debian 12-st) | `/var/log/syslog` | `/var/log/messages` |
| Logide lugemise grupp | `adm`, `systemd-journal` | `adm`, `systemd-journal` | `wheel`, `systemd-journal` |
| SELinux mõjutab teenuseid | Ei (AppArmor) | Ei (AppArmor) | **Jah** - vt märkust allpool |

> [!NOTE]
> **AlmaLinux ja SELinux:** SELinux märgistab iga faili. Kui teenus peab käivitama skripti, mis on loodud kodukataloogis ja seejärel käsuga `mv` kausta `/usr/local/bin` teisaldatud, jääb sellele kodukataloogi märgis ja SELinux keelab käivitamise. Lahendus: loo fail otse sihtkataloogis või taasta õige märgis käsuga `sudo restorecon -v /usr/local/bin/skript.sh`. SELinuxit käsitleme lähemalt moodulis 11.

---

## Kokkuvõte

| Käsk | Tegevus |
|---|---|
| `ps aux`, `ps -ef` | Kõik protsessid |
| `pgrep`, `pstree` | Otsi protsesse, näita puud |
| `top`, `htop` | Protsessid reaalajas |
| `kill`, `kill -9`, `pkill`, `killall` | Saada signaale |
| `käsk &`, Ctrl+Z, `jobs`, `bg`, `fg` | Taustatööd |
| `nohup`, `tmux` | Seansist sõltumatu töö |
| `nice`, `renice` | Prioriteet |
| `systemctl start/stop/restart/reload` | Teenuse haldus praegu |
| `systemctl enable/disable` | Automaatne käivitus |
| `systemctl status`, `--failed` | Teenuste olek |
| `systemctl edit`, `daemon-reload` | Üksuste muutmine |
| `journalctl -u teenus -f` | Teenuse logid |
| `crontab -e` | Ajasta käsk |
| `systemctl list-timers` | Taimerid |
| `at`, `atq`, `atrm` | Ühekordne ajastamine |
| `ulimit`, `/etc/security/limits.conf` | Kasutajate ressursipiirangud |
| `systemctl set-property`, `MemoryMax=`, `CPUQuota=`, `systemd-cgtop` | Teenuste ressursipiirangud |

**Järgmised sammud:** tee [laboritöö](labor.md) ja kontrolli oma teadmisi [enesekontrolli](enesekontroll.md) abil.

## Lisamaterjal

- Brian Ward, „How Linux Works“ - protsesside ja systemd peatükid
- Arch Wiki - systemd, systemd/Timers, systemd/Journal (wiki.archlinux.org)
- `man systemd.service`, `man systemd.timer`, `man 5 crontab`

<!-- navigatsioon -->
---

[← Moodul 4. Enesekontroll](../moodul-04-pakihaldus/enesekontroll.md) · [Sisukord](../../README.md#sisukord) · [Laboritöö 5. Protsessid, teenused ja ajastamine →](labor.md)
<!-- /navigatsioon -->
