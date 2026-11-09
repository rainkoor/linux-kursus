# Moodul 3. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Mis on vähima õiguse põhimõte? Too näide.
2. Milline on juurkasutaja UID? Mis vahe on süsteemikasutajal ja tavakasutajal?
3. Miks on paroolid failis `/etc/shadow`, mitte `/etc/passwd`?
4. Mis vahe on kasutaja põhigrupil ja lisagruppidel?
5. Mis vahe on käskudel `sudo` ja `su`? Kelle parooli kumbki küsib?
6. Miks ei tohi faili `/etc/sudoers` muuta tavalise redaktoriga?
7. Mis juhtub, kui käivitad `sudo usermod -G tarkvara mari` ilma võtmeta `-a`?
8. Mida tähendavad õigused `r`, `w` ja `x` kataloogi puhul?
9. Mis on vaja, et kasutaja saaks faili kustutada?
10. Teisenda numbriliseks: `rwxr-x---`, `rw-r--r--`, `rw-------`.
11. Teisenda sümboliliseks: `755`, `640`, `2770`.
12. Kui umask on `0027`, millised õigused saavad uus fail ja uus kataloog?
13. Mida teeb SGID-õigus kataloogil? Miks on see kasulik jagatud kataloogi puhul?
14. Miks on kataloogil `/tmp` sticky bit?
15. Miks on `chmod 777` halb lahendus?
16. Milleks on kataloog `/etc/skel` ja fail `/etc/login.defs`?
17. Mis on PAM ja millised on selle nelja moodulitüübi ülesanded?
18. Kuidas nõuda vähemalt 12-märgilisi paroole ja lukustada konto 5 vale katse järel?

## Praktilised miniülesanded

Tee need ülesanded laborimasinas, kus sul on `sudo` õigus.

1. Loo grupp `opetajad` ja kasutaja `ain`, kes kuulub sellesse gruppi ja kelle kest on `/bin/bash`.
2. Loo fail `~/hinded.txt` ja määra sellele õigused nii, et sina saad lugeda ja kirjutada, grupp ainult lugeda ja muud mitte midagi.
3. Loo kataloog `/srv/opetajad`, kuhu ainult grupi `opetajad` liikmed pääsevad ja kus uued failid kuuluvad automaatselt sellele grupile.
4. Leia kõik failid kataloogis `/etc`, mille omanik ei ole `root`.
5. Kontrolli, millised `sudo` õigused on sinu kasutajal.
6. Kustuta kasutaja `ain` koos kodukataloogiga ja grupp `opetajad`.

---

## Vastused

1. Iga kasutaja ja programm saab ainult need õigused, mida ta oma tööks vajab. Näiteks veebiserver töötab kasutajana `www-data`, mitte juurkasutajana, et ülevõetud veebiserver ei pääseks ligi kogu süsteemile.
2. Juurkasutaja UID on `0`. Süsteemikasutajad (UID 1–999) on teenuste jaoks ega saa tavaliselt sisse logida. Tavakasutajad (UID 1000+) on inimesed.
3. Faili `/etc/passwd` peavad saama lugeda kõik programmid (nt et näidata failide omanike nimesid). Paroolide räsid on eraldi failis `/etc/shadow`, mida saab lugeda ainult juurkasutaja, et neid ei saaks varastada ja maha murda.
4. Põhigrupp on määratud failis `/etc/passwd` ja sellele kuuluvad kasutaja loodud failid. Lisagrupid annavad kasutajale nende gruppide õigused.
5. `sudo` käivitab käsu teise kasutaja (tavaliselt root) õigustes ja küsib **sinu** parooli, eeldusel et sul on vastav reegel. `su` vahetab kasutajat ja küsib **sihtkasutaja** parooli.
6. Süntaksiviga sudoers-failis võib takistada `sudo` kasutamist ja võtta kõigilt halduriõigused. `visudo` kontrollib süntaksit enne salvestamist.
7. Kasutaja kõik senised lisagrupid asendatakse grupiga `tarkvara`. Kui ta kuulus näiteks gruppi `sudo`, kaotab ta halduriõigused.
8. `r` - sisu loetlemine, `w` - failide loomine, kustutamine ja ümbernimetamine, `x` - kataloogi sisenemine ja sealsetele failidele ligipääs.
9. Kirjutus- ja sisenemisõigust (`w` ja `x`) **kataloogile**, kus fail asub. Õigus failile endale ei ole oluline (v.a kui kataloogil on sticky bit - siis peab olema faili omanik).
10. `rwxr-x---` = `750`, `rw-r--r--` = `644`, `rw-------` = `600`.
11. `755` = `rwxr-xr-x`, `640` = `rw-r-----`, `2770` = `rwxrws---`.
12. Fail: `666 − 027` → `640` (`rw-r-----`). Kataloog: `777 − 027` → `750` (`rwxr-x---`).
13. Uued failid ja alamkataloogid saavad kataloogi grupi, mitte looja põhigrupi. Nii kuuluvad kõik jagatud kataloogi failid automaatselt meeskonna grupile ja kõik liikmed saavad neile ligi.
14. Kõik kasutajad saavad kataloogi `/tmp` kirjutada, kuid sticky bit tagab, et igaüks saab kustutada ainult oma faile, mitte teiste omi.
15. See annab kõigile süsteemi kasutajatele (ka teenustele ja võimalikele ründajatele) õiguse faili muuta või kustutada. Õige lahendus on määrata sobiv omanik või grupp.
16. `/etc/skel` sisu kopeeritakse uue kasutaja kodukataloogi; `login.defs` määrab uute kasutajate UID vahemikud, parooli aegumise vaikeväärtused ja `UMASK`-i.
17. Autentimise raamistik, mille kaudu programmid kasutajaid kontrollivad. `auth` - kes sa oled; `account` - kas tohid sisse logida; `password` - parooli muutmine ja nõuded; `session` - sisselogimisel tehtavad toimingud.
18. `/etc/security/pwquality.conf`: `minlen = 12` (`pam_pwquality`); `/etc/security/faillock.conf`: `deny = 5` ja `pam_faillock` sisse (AlmaLinuxis `authselect enable-feature with-faillock`).

### Miniülesannete lahendused

```bash
sudo groupadd opetajad
sudo useradd -m -s /bin/bash -G opetajad ain
touch ~/hinded.txt && chmod 640 ~/hinded.txt
sudo mkdir /srv/opetajad
sudo chown root:opetajad /srv/opetajad
sudo chmod 2770 /srv/opetajad
find /etc ! -user root 2>/dev/null
sudo -l
sudo userdel -r ain && sudo groupdel opetajad
```

`!` käsus `find` pöörab tingimuse ümber (omanik **ei ole** root).

<!-- navigatsioon -->
---

[← Laboritöö 3. Kasutajad, grupid ja jagatud kataloogid](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 4. Tarkvara ja pakihaldus →](../moodul-04-pakihaldus/index.md)
<!-- /navigatsioon -->
