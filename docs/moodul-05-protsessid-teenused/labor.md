# Laboritöö 5. Protsessid, teenused ja ajastamine

| | |
|---|---|
| **Distro** | AlmaLinux |
| **Kestus** | 2 × 90 minutit |
| **Vajalik** | AlmaLinuxi virtuaalmasin, `sudo` õigusega kasutaja, internetiühendus. Soovitatavalt **kaks SSH-seanssi** korraga |
| **Eesmärk** | Harjutada protsesside jälgimist, signaale, teenuste haldust, oma teenuse loomist, logide lugemist ja ajastamist |

**Aruanne:** vasta küsimustele **K1–K20**.

---

## 1. osa. Protsesside uurimine

**1.1** Kuva protsesside puu ja leia protsess PID 1:

```bash
ps -ef | head -5
pstree -p | head -20
```

Kui `pstree` puudub, paigalda pakett `psmisc`.

**K1.** Mis on protsessi PID 1 nimi? Kes on sinu praeguse kesta (`bash`) vanemprotsess? (Vihje: `ps -ef | grep $$` - muutuja `$$` on praeguse kesta PID.)

**1.2** Leia viis kõige rohkem mälu kasutavat protsessi:

```bash
ps -eo pid,user,%mem,rss,cmd --sort=-%mem | head -6
```

**1.3** Ava `top`. Vajuta **M** (sorteeri mälu järgi), seejärel **P** (protsessori järgi) ja **1** (iga tuum eraldi). Välju klahviga **q**.

**K2.** Mis on süsteemi koormus (*load average*) ja mitu protsessorituuma on masinal (`nproc`)? Kui palju mälu on tegelikult saadaval (`avail Mem`)?

---

## 2. osa. Signaalid ja taustatööd

**2.1** Käivita kolm taustatööd ja vaata neid:

```bash
sleep 1000 &
sleep 2000 &
sleep 3000 &
jobs
```

**2.2** Too teine töö esiplaanile, peata see klahviga **Ctrl+Z** ja saada uuesti taustale:

```bash
fg %2
# vajuta Ctrl+Z
jobs
bg %2
jobs
```

**K3.** Mis olekus oli töö pärast Ctrl+Z vajutamist? Mis muutus pärast `bg` käsku?

**2.3** Lõpeta töö nr 1 käsuga `kill %1`. Lõpeta ülejäänud `sleep` protsessid **ühe käsuga**.

**K4.** Kirjuta käsk, millega lõpetasid kõik `sleep` protsessid.

**2.4** Koorma protsessorit. Käivita ühes SSH-seansis:

```bash
yes > /dev/null
```

Teises seansis leia protsess `top`-iga ja vaata selle nice-väärtust (veerg `NI`).

**2.5** Muuda teises seansis protsessi prioriteeti:

```bash
pgrep yes
renice 19 -p <PID>
top
```

**K5.** Kas protsessori kasutus muutus? Miks ei pruugi see tühjas virtuaalmasinas eriti muutuda? (Vihje: mille suhtes prioriteet kehtib?)

**2.6** Proovi prioriteeti tagasi tõsta tavakasutajana: `renice 0 -p <PID>`.

**K6.** Mis juhtus? Miks?

**2.7** Saada protsessile signaal `SIGTERM`. Kui see ei lõpe, kasuta `SIGKILL`.

---

## 3. osa. Teenuste haldus

**3.1** Vaata SSH teenuse olekut:

```bash
systemctl status sshd
```

**K7.** Kas teenus on lubatud (`enabled`)? Mis on selle põhiprotsessi PID? Millises failis on teenuse kirjeldus?

**3.2** Paigalda veebiserver Apache:

```bash
sudo dnf install httpd
systemctl status httpd
```

**K8.** Kas teenus töötab kohe pärast paigaldamist? Kas see on lubatud? Kuidas erineb see Debianist ja Ubuntust?

**3.3** Käivita teenus ja kontrolli, kas see vastab:

```bash
sudo systemctl start httpd
systemctl is-active httpd
systemctl is-enabled httpd
curl -s http://localhost | head -5
```

**3.4** Taaskäivita virtuaalmasin (`sudo systemctl reboot`), logi uuesti sisse ja kontrolli, kas `httpd` töötab.

**K9.** Kas `httpd` töötas pärast taaskäivitust? Miks? Millise **ühe** käsuga oleksid saanud teenuse korraga käivitada ja lubada?

**3.5** Luba teenus ja kontrolli tulemust. Uuri, mida `enable` tegelikult tegi:

```bash
sudo systemctl enable --now httpd
ls -l /etc/systemd/system/multi-user.target.wants/ | grep httpd
```

**K10.** Mis on `enable` tegelikult loonud?

**3.6** Uuri teenuse faili ja selle asukohta:

```bash
systemctl cat httpd
```

**3.7** Leia kõik töötavad teenused ja kontrolli, kas mõni üksus on kokku jooksnud:

```bash
systemctl list-units --type=service
systemctl --failed
```

---

## 4. osa. Logid

**4.1** Vaata `httpd` logisid:

```bash
sudo journalctl -u httpd
sudo journalctl -u httpd --since "1 hour ago"
```

**4.2** Jälgi SSH logisid reaalajas. Ühes seansis käivita:

```bash
sudo journalctl -u sshd -f
```

Teises seansis (või oma arvutist) proovi ühenduda **vale parooliga** ja seejärel õigega.

**K11.** Kuidas on logis näha ebaõnnestunud ja õnnestunud sisselogimine? Kirjuta mõlema kohta üks logirida (IP-aadressi võid varjata).

**4.3** Leia käesoleva alglaadimise vead ja kontrolli, kas journal on püsiv:

```bash
sudo journalctl -b -p err
journalctl --list-boots
ls -d /var/log/journal /run/log/journal 2>/dev/null
```

**K12.** Mitu alglaadimist on journal'is (punktis 3.4 tegid ühe taaskäivituse)? Kas journal on püsiv või ajutine? Kui ajutine, tee see püsivaks (vt teooria punkt 5.7).

---

## 5. osa. Oma teenus

Lood teenuse, mis kontrollib iga 10 sekundi järel juurfailisüsteemi täituvust ja hoiatab, kui see ületab piiri.

**5.1** Loo skript **otse sihtkataloogis** (mitte kodukataloogis, vt SELinuxi märkus teoorias):

```bash
sudo nano /usr/local/bin/kettakontroll.sh
```

Kirjuta faili (skriptimist õpime moodulis 6, praegu kopeeri):

```bash
#!/bin/bash
PIIR=80
while true; do
    kasutus=$(df --output=pcent / | tail -1 | tr -d ' %')
    if [ "$kasutus" -gt "$PIIR" ]; then
        echo "HOIATUS: juurfailisüsteem on ${kasutus}% täis!"
    else
        echo "OK: juurfailisüsteem on ${kasutus}% täis"
    fi
    sleep 10
done
```

Tee skript käivitatavaks ja testi seda käsitsi (lõpeta Ctrl+C):

```bash
sudo chmod 755 /usr/local/bin/kettakontroll.sh
/usr/local/bin/kettakontroll.sh
```

**5.2** Loo teenuse fail:

```bash
sudo nano /etc/systemd/system/kettakontroll.service
```

```ini
[Unit]
Description=Juurfailisüsteemi täituvuse kontroll

[Service]
Type=simple
ExecStart=/usr/local/bin/kettakontroll.sh
User=nobody
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**5.3** Laadi üksused uuesti, käivita ja luba teenus:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now kettakontroll
systemctl status kettakontroll
```

**K13.** Mille poolest erineb teenuse `kettakontroll` olek teenuse `httpd` omast? Millise kasutajana teenus töötab (`ps -fu nobody`)?

**5.4** Vaata teenuse väljundit:

```bash
journalctl -u kettakontroll -n 10
journalctl -u kettakontroll -f
```

**K14.** Kuhu jõuab skripti `echo` väljund? Miks ei olnud vaja eraldi logifaili?

**5.5** Testi automaatset taaskäivitust. Leia teenuse põhiprotsessi PID (`systemctl status`) ja lõpeta see kõigepealt viisakalt, seejärel jõuga. Iga kord oota 10 sekundit ja vaata olekut:

```bash
sudo kill <PID>
sleep 10; systemctl status kettakontroll
sudo systemctl start kettakontroll       # kui teenus jäi seisma
sudo kill -9 <uus PID>
sleep 10; systemctl status kettakontroll
```

**K15.** Kummal juhul teenus taaskäivitati ja kummal mitte? Selgita seda seadistusega `Restart=on-failure`.

**5.6** Muuda teenuse seadistust nii, et see taaskäivitub **alati**, kasutades käsku `systemctl edit` (mitte põhifaili muutmist):

```bash
sudo systemctl edit kettakontroll
```

Lisa avanevasse faili märgitud kohta:

```ini
[Service]
Restart=always
```

**K16.** Millise faili `systemctl edit` lõi? Miks on see parem kui põhifaili muutmine? Kontrolli tulemust käsuga `systemctl cat kettakontroll`.

---

## 6. osa. Ajastamine

### cron

**6.1** Lisa oma crontab'i rida, mis kirjutab iga minuti järel kuupäeva ja koormuse faili:

```bash
crontab -e
```

```text
* * * * * /usr/bin/uptime >> /home/SINU_KASUTAJA/koormus.log 2>&1
```

Asenda `SINU_KASUTAJA` oma kasutajanimega. Oota 2–3 minutit ja kontrolli: `cat ~/koormus.log`.

**K17.** Kirjuta crontab'i read, mis käivitaksid skripti `/usr/local/bin/aruanne.sh`: a) iga päev kell 06:45; b) tööpäeviti iga 30 minuti järel vahemikus 8–17; c) iga pühapäeva keskööl.

**6.2** Eemalda rida crontab'ist (`crontab -e`).

### systemd taimer

**6.3** Loo varundusskript, mis arhiveerib kataloogi `/etc`:

```bash
sudo mkdir -p /srv/varundus
sudo nano /usr/local/bin/varundus.sh
```

```bash
#!/bin/bash
tar -czf /srv/varundus/etc-$(date +%F-%H%M).tar.gz /etc 2>/dev/null
echo "Varundus valmis: $(ls /srv/varundus | wc -l) arhiivi"
```

```bash
sudo chmod 755 /usr/local/bin/varundus.sh
```

**6.4** Loo teenus `/etc/systemd/system/varundus.service`:

```ini
[Unit]
Description=Kataloogi /etc varundus

[Service]
Type=oneshot
ExecStart=/usr/local/bin/varundus.sh
```

ja taimer `/etc/systemd/system/varundus.timer`, mis käivitab teenuse testimiseks **iga 2 minuti järel**:

```ini
[Unit]
Description=Kataloogi /etc varundus iga 2 minuti järel

[Timer]
OnCalendar=*:0/2
Persistent=true

[Install]
WantedBy=timers.target
```

**6.5** Käivita taimer ja jälgi selle tööd:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now varundus.timer
systemctl list-timers varundus.timer
```

Oota 4–5 minutit:

```bash
ls -l /srv/varundus
journalctl -u varundus.service
```

**K18.** Millal käivitub taimer järgmisena? Mitu arhiivi tekkis? Mida näitab teenuse logi?

**6.6** Muuda taimer igapäevaseks kell 02:30 ja kontrolli ajaavaldist:

```bash
systemd-analyze calendar "*-*-* 02:30:00"
```

**K19.** Mida tähendab `Persistent=true`? Miks on see varunduse puhul oluline?

**6.7** Koristamine: peata ja keela teenus `kettakontroll` ning taimer `varundus.timer`. Kustuta varundusarhiivid.

**K20.** Kirjuta koristamise käsud.

---

## Lisaülesanne (valikuline)

1. Paigalda `htop` (EPEL-ist) ja uuri selle võimalusi: puuvaade (**F5**), sorteerimine (**F6**), signaali saatmine (**F9**).
2. Paigalda `tmux`, käivita selles `top`, ühenda seansist lahti (**Ctrl+B**, seejärel **d**), logi välja, logi uuesti sisse ja ühenda tagasi (`tmux attach`). Kas `top` töötas edasi?
3. **at:** ajasta `at`-iga 2 minuti pärast käsk, mis kirjutab kuupäeva faili `/tmp/at-test.txt`. Vaata `atq`-d ja kontrolli tulemust.
4. **Ressursipiirangud:** piira mõne teenuse mälu (`sudo systemctl set-property <teenus> MemoryMax=100M`), vaata `systemctl status <teenus>` rida `Memory:` ja `systemd-cgtop`-i. Käivita `systemd-run --scope -p CPUQuota=20%` abil protsessorit koormav käsk (`sha256sum /dev/zero`) ja vaata `top`-is, mitu protsenti see saab.

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 5. Protsessid, teenused ja systemd](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 5. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
