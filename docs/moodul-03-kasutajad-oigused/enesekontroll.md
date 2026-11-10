<!-- navigatsioon -->
[← Laboritöö 3. Kasutajad, grupid ja jagatud kataloogid](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 4. Tarkvara ja pakihaldus →](../moodul-04-pakihaldus/index.md)
<!-- /navigatsioon -->

# Moodul 3. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Mis on vähima õiguse põhimõte? Too näide.

<details>
<summary>Vastus</summary>

Iga kasutaja ja programm saab ainult need õigused, mida ta oma tööks vajab. Näiteks veebiserver töötab kasutajana `www-data`, mitte juurkasutajana, et ülevõetud veebiserver ei pääseks ligi kogu süsteemile.

</details>

**2.** Milline on juurkasutaja UID? Mis vahe on süsteemikasutajal ja tavakasutajal?

<details>
<summary>Vastus</summary>

Juurkasutaja UID on `0`. Süsteemikasutajad (UID 1–999) on teenuste jaoks ega saa tavaliselt sisse logida. Tavakasutajad (UID 1000+) on inimesed.

</details>

**3.** Miks on paroolid failis `/etc/shadow`, mitte `/etc/passwd`?

<details>
<summary>Vastus</summary>

Faili `/etc/passwd` peavad saama lugeda kõik programmid (nt et näidata failide omanike nimesid). Paroolide räsid on eraldi failis `/etc/shadow`, mida saab lugeda ainult juurkasutaja, et neid ei saaks varastada ja maha murda.

</details>

**4.** Mis vahe on kasutaja põhigrupil ja lisagruppidel?

<details>
<summary>Vastus</summary>

Põhigrupp on määratud failis `/etc/passwd` ja sellele kuuluvad kasutaja loodud failid. Lisagrupid annavad kasutajale nende gruppide õigused.

</details>

**5.** Mis vahe on käskudel `sudo` ja `su`? Kelle parooli kumbki küsib?

<details>
<summary>Vastus</summary>

`sudo` käivitab käsu teise kasutaja (tavaliselt root) õigustes ja küsib **sinu** parooli, eeldusel et sul on vastav reegel. `su` vahetab kasutajat ja küsib **sihtkasutaja** parooli.

</details>

**6.** Miks ei tohi faili `/etc/sudoers` muuta tavalise redaktoriga?

<details>
<summary>Vastus</summary>

Süntaksiviga sudoers-failis võib takistada `sudo` kasutamist ja võtta kõigilt halduriõigused. `visudo` kontrollib süntaksit enne salvestamist.

</details>

**7.** Mis juhtub, kui käivitad `sudo usermod -G tarkvara mari` ilma võtmeta `-a`?

<details>
<summary>Vastus</summary>

Kasutaja kõik senised lisagrupid asendatakse grupiga `tarkvara`. Kui ta kuulus näiteks gruppi `sudo`, kaotab ta halduriõigused.

</details>

**8.** Mida tähendavad õigused `r`, `w` ja `x` kataloogi puhul?

<details>
<summary>Vastus</summary>

`r` - sisu loetlemine, `w` - failide loomine, kustutamine ja ümbernimetamine, `x` - kataloogi sisenemine ja sealsetele failidele ligipääs.

</details>

**9.** Mis on vaja, et kasutaja saaks faili kustutada?

<details>
<summary>Vastus</summary>

Kirjutus- ja sisenemisõigust (`w` ja `x`) **kataloogile**, kus fail asub. Õigus failile endale ei ole oluline (v.a kui kataloogil on sticky bit - siis peab olema faili omanik).

</details>

**10.** Teisenda numbriliseks: `rwxr-x---`, `rw-r--r--`, `rw-------`.

<details>
<summary>Vastus</summary>

`rwxr-x---` = `750`, `rw-r--r--` = `644`, `rw-------` = `600`.

</details>

**11.** Teisenda sümboliliseks: `755`, `640`, `2770`.

<details>
<summary>Vastus</summary>

`755` = `rwxr-xr-x`, `640` = `rw-r-----`, `2770` = `rwxrws---`.

</details>

**12.** Kui umask on `0027`, millised õigused saavad uus fail ja uus kataloog?

<details>
<summary>Vastus</summary>

Fail: `666 − 027` → `640` (`rw-r-----`). Kataloog: `777 − 027` → `750` (`rwxr-x---`).

</details>

**13.** Mida teeb SGID-õigus kataloogil? Miks on see kasulik jagatud kataloogi puhul?

<details>
<summary>Vastus</summary>

Uued failid ja alamkataloogid saavad kataloogi grupi, mitte looja põhigrupi. Nii kuuluvad kõik jagatud kataloogi failid automaatselt meeskonna grupile ja kõik liikmed saavad neile ligi.

</details>

**14.** Miks on kataloogil `/tmp` sticky bit?

<details>
<summary>Vastus</summary>

Kõik kasutajad saavad kataloogi `/tmp` kirjutada, kuid sticky bit tagab, et igaüks saab kustutada ainult oma faile, mitte teiste omi.

</details>

**15.** Miks on `chmod 777` halb lahendus?

<details>
<summary>Vastus</summary>

See annab kõigile süsteemi kasutajatele (ka teenustele ja võimalikele ründajatele) õiguse faili muuta või kustutada. Õige lahendus on määrata sobiv omanik või grupp.

</details>

**16.** Milleks on kataloog `/etc/skel` ja fail `/etc/login.defs`?

<details>
<summary>Vastus</summary>

`/etc/skel` sisu kopeeritakse uue kasutaja kodukataloogi; `login.defs` määrab uute kasutajate UID vahemikud, parooli aegumise vaikeväärtused ja `UMASK`-i.

</details>

**17.** Mis on PAM ja millised on selle nelja moodulitüübi ülesanded?

<details>
<summary>Vastus</summary>

Autentimise raamistik, mille kaudu programmid kasutajaid kontrollivad. `auth` - kes sa oled; `account` - kas tohid sisse logida; `password` - parooli muutmine ja nõuded; `session` - sisselogimisel tehtavad toimingud.

</details>

**18.** Kuidas nõuda vähemalt 12-märgilisi paroole ja lukustada konto 5 vale katse järel?

<details>
<summary>Vastus</summary>

`/etc/security/pwquality.conf`: `minlen = 12` (`pam_pwquality`); `/etc/security/faillock.conf`: `deny = 5` ja `pam_faillock` sisse (AlmaLinuxis `authselect enable-feature with-faillock`).

</details>

**19.** Mis on lokaat ja milleks kasutatakse skriptides `LC_ALL=C`?

<details>
<summary>Vastus</summary>

Lokaat määrab keele, kuupäevade ja arvude vormingu ning järjestuse (nt `et_EE.UTF-8`). `LC_ALL=C` annab ühtse, lokaadist sõltumatu käitumise (järjestus, vead inglise keeles), mistõttu skripti tulemus on igas masinas sama.

</details>

## Praktilised miniülesanded

**1.** Loo grupp `opetajad` ja kasutaja `ain`, kes kuulub sellesse gruppi ja kelle kest on `/bin/bash`.

<details>
<summary>Lahendus</summary>

```bash
sudo groupadd opetajad
sudo useradd -m -s /bin/bash -G opetajad ain
```

</details>

**2.** Loo fail `~/hinded.txt` ja määra sellele õigused nii, et sina saad lugeda ja kirjutada, grupp ainult lugeda ja muud mitte midagi.

<details>
<summary>Lahendus</summary>

```bash
touch ~/hinded.txt && chmod 640 ~/hinded.txt
```

</details>

**3.** Loo kataloog `/srv/opetajad`, kuhu ainult grupi `opetajad` liikmed pääsevad ja kus uued failid kuuluvad automaatselt sellele grupile.

<details>
<summary>Lahendus</summary>

```bash
sudo mkdir /srv/opetajad
sudo chown root:opetajad /srv/opetajad
sudo chmod 2770 /srv/opetajad
```

</details>

**4.** Leia kõik failid kataloogis `/etc`, mille omanik ei ole `root`.

<details>
<summary>Lahendus</summary>

```bash
find /etc ! -user root 2>/dev/null
```

`!` käsus `find` pöörab tingimuse ümber (omanik **ei ole** root).

</details>

**5.** Kontrolli, millised `sudo` õigused on sinu kasutajal.

<details>
<summary>Lahendus</summary>

```bash
sudo -l
```

</details>

**6.** Kustuta kasutaja `ain` koos kodukataloogiga ja grupp `opetajad`.

<details>
<summary>Lahendus</summary>

```bash
sudo userdel -r ain && sudo groupdel opetajad
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 3. Kasutajad, grupid ja jagatud kataloogid](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 4. Tarkvara ja pakihaldus →](../moodul-04-pakihaldus/index.md)
<!-- /navigatsioon -->
