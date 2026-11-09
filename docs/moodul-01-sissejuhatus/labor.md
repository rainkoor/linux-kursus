# Laboritöö 1. Esimesed sammud käsureal

| | |
|---|---|
| **Distro** | Debian |
| **Kestus** | 2 × 90 minutit |
| **Vajalik** | Debiani virtuaalmasin, millele on ligipääs SSH kaudu tavakasutajana |
| **Eesmärk** | Harjutada ühendumist, liikumist failisüsteemis ja põhitoiminguid failidega |

**Aruanne:** vasta küsimustele **K1–K18** aruandes, mille vorm (paber, Moodle, tekstifail) määrab õpetaja. Iga käsu järel vaata hoolega, mida see väljastas.

> [!NOTE]
> **Iseõppijale:** sobib iga Debiani virtuaalmasin, nt VirtualBoxis. Paigalda Debian ilma graafilise töölauata ja vali paigaldamisel tarkvara hulka „SSH server“. Täpsed paigaldussammud on lisas [Laborikeskkond ja paigaldus](../lisad/paigaldus.md).

---

## 1. osa. Ühendumine

**1.1** Ava oma arvutis terminal (Windowsis nt Windows Terminal või PowerShell) ja ühendu virtuaalmasinaga. Asenda kasutajanimi ja aadress enda omadega:

```bash
ssh kasutaja@aadress
```

Kinnita serveri võti (`yes`) ja sisesta parool.

**K1.** Mis on sinu viip? Mida tähendab selle iga osa?

**1.2** Logi välja käsuga `exit` ja seejärel uuesti sisse.

**K2.** Kas serveri võtit küsiti ka teisel korral? Miks?

---

## 2. osa. Süsteemiga tutvumine

**2.1** Käivita järgmised käsud:

```bash
whoami
hostname
cat /etc/os-release
uname -r
uptime
```

**K3.** Milline Debiani versioon ja koodnimi on masinal? Milline on kerneli versioon?

**K4.** Kui kaua on masin töötanud?

**2.2** Käivita `hostnamectl`.

**K5.** Millist infot näitab `hostnamectl`, mida eelmised käsud ei näidanud? Kas masin teab, et ta on virtuaalmasin?

---

## 3. osa. Abi leidmine

**3.1** Ava käsu `ls` kasutusjuhend:

```bash
man ls
```

Otsi kasutusjuhendist (klahv `/`) võtme `-t` kirjeldus. Välju klahviga `q`.

**K6.** Mida teeb võti `-t`? Mida teeb võti `-r`? Mida teeb käsk `ls -ltr`?

**3.2** Uuri, millised kasutusjuhendid käsitlevad sõna `passwd`:

```bash
man -k passwd
```

**K7.** Mille poolest erinevad `man 1 passwd` ja `man 5 passwd`?

**3.3** Käivita `cp --help`.

**K8.** Millise võtmega küsib `cp` enne olemasoleva faili ülekirjutamist kinnitust?

---

## 4. osa. Failisüsteemis liikumine

**4.1** Liigu järjest järgmistesse kataloogidesse ja vaata iga kataloogi sisu käsuga `ls`:

```bash
cd /
ls
cd /etc
ls
cd /var/log
ls -lh
cd
pwd
```

**K9.** Milline kataloog avanes käsuga `cd` ilma argumendita? Mis on selle absoluutne tee?

**4.2** Ilma `cd` käsku kasutamata vaata, kas kataloogis `/etc` on fail nimega `hostname`, ja kuva selle sisu:

```bash
ls /etc/hostname
cat /etc/hostname
```

**4.3** Liigu kataloogi `/usr/share/doc` ja sealt suhtelise tee abil kataloogi `/usr/bin`:

```bash
cd /usr/share/doc
cd ../../bin
pwd
```

**K10.** Selgita, miks tee `../../bin` viis kataloogi `/usr/bin`.

**4.4** Käivita `ls -l /bin`.

**K11.** Mida näitab väljundis olev nool (`->`)? Kuhu `/bin` tegelikult viitab?

**4.5** Vaata oma kodukataloogi peidetud faile:

```bash
cd
ls -la
```

**K12.** Nimeta kaks peidetud faili. Mille järgi need ära tunned?

---

## 5. osa. Failid ja kataloogid

Selles osas ehitad väljamõeldud veebiprojekti kataloogistruktuuri.

**5.1** Loo kodukataloogi järgmine struktuur **ühe käsuga**:

```text
labor01/
├── veebileht/
│   ├── html/
│   ├── pildid/
│   └── logid/
└── varukoopiad/
```

Vihje: `mkdir -p` ja loogelised sulud. Kontrolli tulemust:

```bash
ls -R ~/labor01
```

**K13.** Millise käsuga struktuuri lõid?

**5.2** Loo failid ja kontrolli tulemust:

```bash
cd ~/labor01/veebileht
touch html/index.html html/kontakt.html html/meist.html
touch pildid/logo.png pildid/taust.jpg pildid/foto1.jpg pildid/foto2.jpg
touch logid/juurdepaas.log logid/vead.log
ls -R
```

**5.3** Kasutades metamärke:

1. kopeeri kõik `.jpg` failid kataloogi `~/labor01/varukoopiad`;
2. loetle kataloogis `pildid` ainult need failid, mille nimi algab sõnaga `foto`;
3. kopeeri kõik `.html` failid kataloogi `~/labor01/varukoopiad`.

**K14.** Kirjuta üles kõik kolm käsku.

**5.4** Nimeta fail `html/meist.html` ümber failiks `html/tutvustus.html`. Teisalda kataloog `logid` kataloogi `~/labor01` (st ühe taseme võrra kõrgemale).

**5.5** Kopeeri kogu kataloog `veebileht` koos sisuga nimega `~/labor01/varukoopiad/veebileht-varu`.

**5.6** Kirjuta faili sisu ja kuva see:

```bash
echo "<h1>Tere tulemast!</h1>" > ~/labor01/veebileht/html/index.html
cat ~/labor01/veebileht/html/index.html
file ~/labor01/veebileht/html/index.html
file ~/labor01/veebileht/pildid/logo.png
```

**K15.** Mida väitis käsk `file` faili `logo.png` kohta? Miks ei pidanud ta seda pildiks?

**5.7** Kontrolli kogu struktuuri käsuga `ls -R ~/labor01`.

---

## 6. osa. Kustutamine ja ajalugu

**6.1** Kustuta kataloogist `varukoopiad` kõik `.jpg` failid nii, et iga faili puhul küsitakse kinnitust.

**6.2** Proovi kustutada kataloogi `~/labor01/logid` käsuga `rmdir`.

**K16.** Mis juhtus ja miks? Millise käsuga saab kataloogi koos sisuga kustutada?

**6.3** Vaata oma käsuajalugu:

```bash
history
```

Proovi klahvikombinatsiooni **Ctrl+R** ja kirjuta `mkdir` - kest leiab sinu viimase `mkdir` käsu.

**6.4** Kui õpetaja ei ole teisiti öelnud, jäta kataloog `~/labor01` alles - see on sooritatud töö tõend.

---

## 7. osa. Harjutusmäng: OverTheWire Bandit

**OverTheWire Bandit** on tasuta harjutuskeskkond, kus iga taseme lahendusest saad järgmise taseme parooli. Ülesanded nõuavad just neid oskusi, mida selles moodulis õppisid.

**7.1** Ühendu (oma arvutist või laborimasinast - kui laborivõrgust välja ei pääse, tee see osa kodus):

```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220
```

Parool on `bandit0`. Juhised: overthewire.org/wargames/bandit. Läbi vähemalt tasemed **0 → 5**.

**K17.** Mitu taset läbisid? Kirjuta iga taseme kohta üks rida: mis oli ülesanne ja millise käsuga selle lahendasid (**ära kirjuta paroole aruandesse**).

**K18.** Tase 2 ja 3 (failinimed kriipsu või tühikuga, peidetud failid) - miks olid need keerulised ja kuidas neid failinimesid käsureal käsitleda (vt teooria punkt 1.9)?

---

## Lisaülesanne (valikuline)

Jätka Banditiga tasemetel 6–15 - need kasutavad mooduli 2 teemasid (`find`, `grep`, `sort`, `uniq`, torud).

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 1. Linux ja käsurida](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 1. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
