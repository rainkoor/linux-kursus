<!-- navigatsioon -->
[← Moodul 2. Failid, tekst ja torud](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 2. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 2. Logide analüüs ja failide haldus

| | |
|---|---|
| **Distro** | Debian |
| **Kestus** | 2 × 90 minutit |
| **Vajalik** | Debiani virtuaalmasin (sama, mis laboritöös 1), ligipääs SSH kaudu |
| **Eesmärk** | Harjutada redaktoreid, ümbersuunamist, torusid, tekstitöötlust, failide otsimist ja arhiveerimist |

> **Aruanne:** vasta küsimustele **K1–K20**. Kus küsitakse käsku, kirjuta üles kogu käsk. Kõik küsimused on koos ka lehe lõpus ([Aruande küsimused](#aruande-küsimused)).

**Stsenaarium:** oled kooli veebiserveri administraator. Õpetaja kahtlustab, et serverit on rünnatud, ja palub sul logi analüüsida, kokkuvõte teha ning logid varundada.

---

## 1. osa. Ettevalmistus ja redaktorid

**1.1** Loo töökataloog ja liigu sinna:

```bash
mkdir -p ~/labor02 && cd ~/labor02
```

Märk `&&` käivitab teise käsu ainult siis, kui esimene õnnestus.

**1.2** Loo näidislogi. Kopeeri kogu plokk ja kleebi terminali:

```bash
cat > juurdepaas.log <<'EOF'
10.0.83.121 - - [03/Nov/2026:08:12:01 +0200] "GET /index.html HTTP/1.1" 200 5120
10.0.83.134 - - [03/Nov/2026:08:12:45 +0200] "GET /tunniplaan.html HTTP/1.1" 200 8340
10.0.0.7 - - [03/Nov/2026:08:13:02 +0200] "GET /admin HTTP/1.1" 403 512
10.0.83.121 - - [03/Nov/2026:08:14:10 +0200] "GET /pildid/logo.png HTTP/1.1" 200 20480
10.0.83.155 - - [03/Nov/2026:08:15:33 +0200] "GET /kontakt.html HTTP/1.1" 200 3072
10.0.0.7 - - [03/Nov/2026:08:16:01 +0200] "GET /wp-login.php HTTP/1.1" 404 256
10.0.0.7 - - [03/Nov/2026:08:16:02 +0200] "GET /phpmyadmin HTTP/1.1" 404 256
10.0.0.7 - - [03/Nov/2026:08:16:03 +0200] "GET /.env HTTP/1.1" 404 256
10.0.83.134 - - [03/Nov/2026:08:20:17 +0200] "GET /index.html HTTP/1.1" 200 5120
10.0.83.188 - - [03/Nov/2026:09:01:44 +0200] "POST /login HTTP/1.1" 302 128
10.0.83.188 - - [03/Nov/2026:09:01:45 +0200] "GET /oppija/hinded HTTP/1.1" 200 9216
10.0.83.121 - - [03/Nov/2026:09:30:00 +0200] "GET /tunniplaan.html HTTP/1.1" 200 8340
172.16.5.2 - - [03/Nov/2026:10:05:12 +0200] "GET /index.html HTTP/1.1" 200 5120
172.16.5.2 - - [03/Nov/2026:10:05:13 +0200] "GET /uudised HTTP/1.1" 500 1024
10.0.83.155 - - [03/Nov/2026:10:44:51 +0200] "GET /tunniplaan.html HTTP/1.1" 200 8340
10.0.0.7 - - [03/Nov/2026:11:00:00 +0200] "GET /admin/config.php HTTP/1.1" 404 256
10.0.83.134 - - [03/Nov/2026:11:15:22 +0200] "GET /pildid/kool.jpg HTTP/1.1" 200 102400
10.0.83.188 - - [03/Nov/2026:12:02:09 +0200] "GET /oppija/tunniplaan HTTP/1.1" 200 7168
172.16.5.2 - - [03/Nov/2026:12:30:41 +0200] "GET /uudised HTTP/1.1" 500 1024
10.0.83.121 - - [03/Nov/2026:13:10:05 +0200] "GET /index.html HTTP/1.1" 200 5120
EOF
```

Konstruktsioon `<<'EOF' ... EOF` (*here document*) suunab kõik read kuni sõnani `EOF` käsu sisendiks.

Iga logirea väljad (tühikuga eraldatult):

```text
10.0.83.121 - - [03/Nov/2026:08:12:01 +0200] "GET /index.html HTTP/1.1" 200 5120
      1       2 3            4           5       6      7          8      9    10
```

Väli 1 on kliendi IP-aadress, 7 küsitud lehekülg, 9 HTTP olekukood ja 10 vastuse suurus baitides.

**1.3** Ava logi redaktoriga `nano` ja otsi (**Ctrl+W**) sõna `admin`. Välju salvestamata (**Ctrl+X**).

**1.4** Loo redaktoriga `vi` fail `markmed.txt`:

1. `vi markmed.txt`
2. vajuta **i** ja kirjuta: `Logi analüüs, alustatud:` ja oma nimi;
3. vajuta **Esc**, kirjuta `:wq` ja vajuta Enter.

Kontrolli käsuga `cat markmed.txt`.

> **K1.** Milles seisneb vi tava- ja sisestusrežiimi erinevus?

---

## 2. osa. Ümbersuunamine

**2.1** Lisa märkmetesse praegune kuupäev ja kellaaeg:

```bash
date >> markmed.txt
cat markmed.txt
```

**2.2** Proovi nüüd sama ühe märgiga `>`:

```bash
date > proov.txt
date > proov.txt
cat proov.txt
```

> **K2.** Mitu rida on failis `proov.txt`? Miks?

**2.3** Käivita käsk, mis annab nii väljundi kui ka veateate:

```bash
ls /etc/hostname /olematu
ls /etc/hostname /olematu > valjund.txt
ls /etc/hostname /olematu > valjund.txt 2> vead.txt
cat valjund.txt
cat vead.txt
```

> **K3.** Miks kuvati teise käsu järel ekraanil ikkagi midagi? Mis jõudis faili `valjund.txt` ja mis faili `vead.txt`?

**2.4** Otsi kogu süsteemist faile nimega `passwd` nii, et veateateid ekraanil ei kuvata.

> **K4.** Kirjuta käsk ja loetle leitud failid.

---

## 3. osa. Logi analüüs

Kasuta selles osas faili `juurdepaas.log`. Ehita ahelaid järk-järgult: lisa üks käsk korraga ja vaata tulemust.

**3.1** Mitu rida on logis?

> **K5.** Kirjuta käsk ja tulemus.

**3.2** Kuva ainult IP-aadressid (1. väli):

```bash
cut -d' ' -f1 juurdepaas.log
```

**3.3** Leia, mitu päringut tegi iga IP-aadress, ja järjesta tulemus suurimast väikseimani.

> **K6.** Kirjuta käsk. Milline IP-aadress tegi kõige rohkem päringuid?

**3.4** Kuva kõik read, kus olekukood on `404` (lehte ei leitud). Vihje: otsi mustrit `" 404 `.

> **K7.** Mitu sellist rida on? Millise IP-aadressi päringud need on ja milliseid lehti küsiti?

> **K8.** Miks on need päringud kahtlased? (Vihje: vaata küsitud lehtede nimesid. Kas koolilehel on WordPress või phpMyAdmin?)

**3.5** Loenda kõik olekukoodid (9. väli). Kasuta `awk`:

```bash
awk '{print $9}' juurdepaas.log | sort | uniq -c | sort -rn
```

> **K9.** Milline olekukood esineb kõige sagedamini? Mitu serveri viga (koodid 5xx) logis on?

**3.6** Leia, millised leheküljed tagastasid serveri vea `500`. Kuva iga lehekülg ainult ühe korra.

> **K10.** Kirjuta käsk ja tulemus.

**3.7** Leia kolm kõige populaarsemat lehekülge (7. väli).

> **K11.** Kirjuta käsk ja tulemus.

**3.8** Kuva päringud, mis tehti vahemikus kell 10:00–10:59. Kasuta `grep` ja regulaaravaldist, mis otsib mustrit `:10:` kellaaja algusest.

> **K12.** Kirjuta käsk. Mitu päringut tehti selles vahemikus?

**3.9** Kuva kõik read, mis **ei** pärine sisevõrgust `10.0.83.`. Vihje: `grep -v`, ja pea meeles, et punkt tähendab regulaaravaldises suvalist märki.

> **K13.** Kirjuta käsk. Miks on oluline punkt varjestada (`\.`)?

**3.10** Kasutades laiendatud regulaaravaldist, kuva read, kus olekukood on `403` või `404`.

> **K14.** Kirjuta käsk.

**3.11** Arvuta, mitu baiti server kokku välja saatis:

```bash
awk '{summa += $10} END {print summa}' juurdepaas.log
```

**3.12** Koosta aruandefail `kokkuvote.txt`, kuhu kirjutad käskude abil (mitte käsitsi!):

1. pealkirja `IP-aadresside statistika`;
2. IP-aadresside päringute arvu (punkt 3.3 ahel);
3. pealkirja `Kahtlased päringud`;
4. kõik `404` read.

Kasuta `echo` ja ümbersuunamisi `>` ning `>>`.

> **K15.** Kirjuta käsud, millega faili koostasid.

---

## 4. osa. Süsteemifailide uurimine

**4.1** Kuva failist `/etc/passwd` ainult kasutajanimed ja nende kestad (väljad 1 ja 7).

**4.2** Leia, millised kasutajad saavad sisse logida, st nende kest lõpeb sõnaga `bash`.

> **K16.** Kirjuta käsk ja loetle kasutajad.

**4.3** Kuva SSH-serveri seadistusfaili `/etc/ssh/sshd_config` sisu ilma kommentaaride ja tühjade ridadeta.

> **K17.** Kirjuta käsk. Mitu rida jäi alles?

---

## 5. osa. Failide otsimine ja viidad

**5.1** Leia kataloogist `/etc` kõik failid, mille nimi lõpeb laiendiga `.conf`, ja loenda need.

**5.2** Leia kataloogist `/usr` kõik failid, mis on suuremad kui 20 MB. Peida veateated.

**5.3** Leia oma kodukataloogist kõik failid, mida on muudetud viimase 60 minuti jooksul (vihje: `-mmin`).

> **K18.** Kirjuta kõigi kolme ülesande käsud ja leitud failide arv või nimed.

**5.4** Loo kodukataloogi sümbolviit `logi`, mis viitab failile `~/labor02/juurdepaas.log`. Kontrolli seda käskudega `ls -l ~/logi` ja `head -3 ~/logi`.

**5.5** Loo failist `markmed.txt` kõvaviit `markmed-koopia.txt`. Võrdle i-sõlmede numbreid:

```bash
ls -li markmed.txt markmed-koopia.txt
```

Kirjuta faili `markmed-koopia.txt` lõppu uus rida ja vaata seejärel faili `markmed.txt` sisu.

> **K19.** Mis juhtus faili `markmed.txt` sisuga? Miks?

---

## 6. osa. Varundamine

**6.1** Loo kataloogist `~/labor02` pakitud arhiiv `~/labor02-varu.tar.gz`.

**6.2** Vaata arhiivi sisu ilma seda lahti pakkimata.

**6.3** Paki arhiiv lahti kataloogi `/tmp/taastamine` (loo kataloog enne). Kontrolli, et fail `juurdepaas.log` on taastatud.

**6.4** Paki näidislogi eraldi `gzip`-iga ja otsi pakitud failist ilma lahti pakkimata kõik `500` read:

```bash
cp ~/labor02/juurdepaas.log /tmp/vana.log
gzip /tmp/vana.log
ls -l /tmp/vana.log*
zgrep '" 500 ' /tmp/vana.log.gz
```

> **K20.** Mis juhtus pärast `gzip` käsku algse failiga `vana.log`? Milleks on vaja käske `zcat` ja `zgrep`?

**6.5** Koristamine: kustuta `/tmp/taastamine` ja `/tmp/vana.log.gz`. Jäta `~/labor02` ja arhiiv alles.

---

## Lisaülesanne (valikuline)

1. Kirjuta üks käsuahel, mis näitab iga IP-aadressi kohta, mitu **404** vastust see sai.
2. Jätka **OverTheWire Banditiga**, tasemed 6–15. Need tasemed nõuavad just selles moodulis õpitud käske (`find`, `grep`, `sort`, `uniq`, `tr`, `tar`, `gzip`).
3. **diff ja xargs:** tee kataloogist `/etc` koopia (`sudo cp -a /etc ~/etc-varu`), muuda ühte faili ja leia muudatus käsuga `sudo diff -r /etc ~/etc-varu`. Leia `find`-i ja `xargs`-iga kõik `.conf` failid kataloogis `/etc`, mis sisaldavad sõna `Listen`, ja loenda need (`xargs grep -l … | wc -l`).

---

<!-- kysimused -->
## Aruande küsimused

Kõik selle laboritöö küsimused ühes kohas. Sulgudes on punkt, mille juures küsimust küsitakse. Kopeeri loend oma aruande alguseks ja kirjuta vastus iga küsimuse alla. Kus küsitakse käsku, kirjuta üles kogu käsk.

- **K1.** *(punkt 1.4)* Milles seisneb vi tava- ja sisestusrežiimi erinevus?
- **K2.** *(punkt 2.2)* Mitu rida on failis `proov.txt`? Miks?
- **K3.** *(punkt 2.3)* Miks kuvati teise käsu järel ekraanil ikkagi midagi? Mis jõudis faili `valjund.txt` ja mis faili `vead.txt`?
- **K4.** *(punkt 2.4)* Kirjuta käsk ja loetle leitud failid.
- **K5.** *(punkt 3.1)* Kirjuta käsk ja tulemus.
- **K6.** *(punkt 3.3)* Kirjuta käsk. Milline IP-aadress tegi kõige rohkem päringuid?
- **K7.** *(punkt 3.4)* Mitu sellist rida on? Millise IP-aadressi päringud need on ja milliseid lehti küsiti?
- **K8.** *(punkt 3.4)* Miks on need päringud kahtlased? (Vihje: vaata küsitud lehtede nimesid. Kas koolilehel on WordPress või phpMyAdmin?)
- **K9.** *(punkt 3.5)* Milline olekukood esineb kõige sagedamini? Mitu serveri viga (koodid 5xx) logis on?
- **K10.** *(punkt 3.6)* Kirjuta käsk ja tulemus.
- **K11.** *(punkt 3.7)* Kirjuta käsk ja tulemus.
- **K12.** *(punkt 3.8)* Kirjuta käsk. Mitu päringut tehti selles vahemikus?
- **K13.** *(punkt 3.9)* Kirjuta käsk. Miks on oluline punkt varjestada (`\.`)?
- **K14.** *(punkt 3.10)* Kirjuta käsk.
- **K15.** *(punkt 3.12)* Kirjuta käsud, millega faili koostasid.
- **K16.** *(punkt 4.2)* Kirjuta käsk ja loetle kasutajad.
- **K17.** *(punkt 4.3)* Kirjuta käsk. Mitu rida jäi alles?
- **K18.** *(punkt 5.3)* Kirjuta kõigi kolme ülesande käsud ja leitud failide arv või nimed.
- **K19.** *(punkt 5.5)* Mis juhtus faili `markmed.txt` sisuga? Miks?
- **K20.** *(punkt 6.4)* Mis juhtus pärast `gzip` käsku algse failiga `vana.log`? Milleks on vaja käske `zcat` ja `zgrep`?
<!-- /kysimused -->

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 2. Failid, tekst ja torud](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 2. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
