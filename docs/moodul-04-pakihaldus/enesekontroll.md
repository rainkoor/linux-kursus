<!-- navigatsioon -->
[← Laboritöö 4. Pakihaldus kolmel distrol](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 5. Protsessid, teenused ja systemd →](../moodul-05-protsessid-teenused/index.md)
<!-- /navigatsioon -->

# Moodul 4. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Mis on pakett, hoidla ja sõltuvus?

<details>
<summary>Vastus</summary>

**Pakett** on arhiiv, mis sisaldab programmi faile, metaandmeid ja paigaldusskripte. **Hoidla** on server, kus asuvad paketid ja nende loend. **Sõltuvus** on teine pakett, mida programm töötamiseks vajab.

</details>

**2.** Nimeta kolm põhjust, miks paigaldada tarkvara pakihalduriga, mitte tootja kodulehelt alla laaditud failist.

<details>
<summary>Vastus</summary>

Näiteks: paketid on allkirjastatud ja kontrollitud; sõltuvused lahendatakse automaatselt; kogu süsteem uueneb ühe käsuga; eemaldamine on puhas.

</details>

**3.** Mis vahe on käskudel `dpkg` ja `apt` (või `rpm` ja `dnf`)?

<details>
<summary>Vastus</summary>

`dpkg` / `rpm` on madala taseme tööriistad, mis paigaldavad üksiku paketifaili, kuid ei lahenda sõltuvusi ega laadi midagi alla. `apt` / `dnf` laadivad paketid hoidlast ja lahendavad sõltuvused automaatselt.

</details>

**4.** Mida teeb `apt update` ja mida `apt upgrade`?

<details>
<summary>Vastus</summary>

`apt update` värskendab hoidlatest pakettide loendi. `apt upgrade` uuendab paigaldatud paketid uuematele versioonidele.

</details>

**5.** Mis vahe on käskudel `apt remove` ja `apt purge`?

<details>
<summary>Vastus</summary>

`remove` eemaldab paketi, kuid jätab seadistusfailid alles. `purge` eemaldab ka seadistusfailid.

</details>

**6.** Mida teeb `apt autoremove`?

<details>
<summary>Vastus</summary>

Eemaldab paketid, mis paigaldati sõltuvustena, kuid mida ükski paigaldatud pakett enam ei vaja.

</details>

**7.** Kuidas leida, millisesse paketti kuulub fail `/usr/bin/ssh`? Kirjuta käsk mõlema perekonna jaoks.

<details>
<summary>Vastus</summary>

Debian/Ubuntu: `dpkg -S /usr/bin/ssh`. AlmaLinux: `rpm -qf /usr/bin/ssh` (või `dnf provides /usr/bin/ssh`).

</details>

**8.** Mis on EPEL ja miks seda AlmaLinuxis sageli vaja on?

<details>
<summary>Vastus</summary>

EPEL (*Extra Packages for Enterprise Linux*) on Fedora kogukonna lisapakettide hoidla RHEL-i perekonna distrodele. AlmaLinuxi põhihoidlates on teadlikult piiratud valik tarkvara, palju populaarseid tööriistu (nt `htop`, `ncdu`) on ainult EPEL-is.

</details>

**9.** Millised riskid kaasnevad kolmanda osapoole hoidla lisamisega?

<details>
<summary>Vastus</summary>

Hoidla paigaldusskriptid töötavad juurkasutaja õigustes, seega pahatahtlik või häkitud hoidla võib süsteemi üle võtta. Lisaks võivad tekkida pakettide konfliktid ja uuendusprobleemid ning hoidla võib hooldamata jääda.

</details>

**10.** Kus asuvad hoidlate seadistused Debianis/Ubuntus ja AlmaLinuxis?

<details>
<summary>Vastus</summary>

Debian/Ubuntu: `/etc/apt/sources.list.d/` (uuemates `.sources` failid) või `/etc/apt/sources.list`. AlmaLinux: `/etc/yum.repos.d/*.repo`.

</details>

**11.** Mis on Ubuntu hoidla osade `main` ja `universe` erinevus?

<details>
<summary>Vastus</summary>

`main` on Canonicali ametlikult toetatud vaba tarkvara. `universe` on kogukonna hooldatud vaba tarkvara, mille turvauuendusi Canonical ei taga samal määral.

</details>

**12.** Millised on kolm klassikalist sammu programmi kompileerimisel lähtekoodist? Kuhu programm vaikimisi paigaldatakse?

<details>
<summary>Vastus</summary>

`./configure`, `make`, `sudo make install`. Vaikimisi paigaldatakse kataloogi `/usr/local`.

</details>

**13.** Miks ei uuendata lähtekoodist kompileeritud programmi koos süsteemiga?

<details>
<summary>Vastus</summary>

Pakihaldur ei tea sellest programmist midagi, seega ei saa see programmi uuendada ega eemaldada. Uuendused tuleb ise jälgida ja programm uuesti kompileerida.

</details>

**14.** Mis on Snap ja Flatpak? Nimeta üks eelis ja üks puudus.

<details>
<summary>Vastus</summary>

Distrost sõltumatud paketivormingud, kus programm on koos oma sõltuvustega ja töötab isoleeritult. Eelis: uusim versioon igas distros. Puudus: suurem maht ja aeglasem käivitus (või sõltuvuste turvauuendused sõltuvad paketi koostajast).

</details>

**15.** Kuidas AlmaLinuxis viimast pakihalduri toimingut tagasi võtta?

<details>
<summary>Vastus</summary>

`dnf history` näitab toimingute numbreid, `sudo dnf history undo <nr>` võtab valitud toimingu tagasi.

</details>

**16.** Mida tuleb teha enne väljalaske uuendust (nt Debian 12 → 13)? Nimeta vähemalt neli sammu.

<details>
<summary>Vastus</summary>

Loe väljalaskemärkmeid, tee hetktõmmis või varukoopia, uuenda praegune väljalase lõpuni ja taaskäivita, kontrolli vaba kettaruumi, keela kolmandate osapoolte hoidlad, tee uuendust konsoolis või `tmux`-is.

</details>

**17.** Milliste tööriistadega uuendatakse väljalaset Ubuntus ja AlmaLinuxis?

<details>
<summary>Vastus</summary>

Ubuntu: `do-release-upgrade`. AlmaLinux: ELevate projekti `leapp` (`leapp preupgrade`, `leapp upgrade`); RHEL-i perekonnas eelistatakse siiski uut paigaldust.

</details>

**18.** Mis on jagatud teek? Programm annab vea `error while loading shared libraries: libxyz.so.1`. Kuidas leiad põhjuse ja parandad selle, kui teek on kataloogis `/usr/local/lib`?

<details>
<summary>Vastus</summary>

Jagatud teek (`*.so`) on kood, mida kasutavad korraga paljud programmid ja mis laaditakse programmi käivitamisel. `ldd /tee/programm` näitab, milline teek on puudu (`not found`). Lisa kataloog `/usr/local/lib` faili `/etc/ld.so.conf.d/kohalik.conf` ja käivita `sudo ldconfig`; kontrolli `ldconfig -p | grep libxyz`.

</details>

## Praktilised miniülesanded

**1.** (A ja B) Uuenda süsteem ühe käsurea abil.

<details>
<summary>Lahendus</summary>

```bash
sudo apt update && sudo apt upgrade -y            # A
sudo dnf upgrade -y                               # B
```

Võti `-y` vastab kõigile küsimustele automaatselt „jah“. Seda kasutatakse skriptides, kuid käsitsi töötades on parem enne kinnitamist üle vaadata, mida pakihaldur teha kavatseb.

</details>

**2.** (A ja B) Leia, mitu faili on paketis `bash`.

<details>
<summary>Lahendus</summary>

```bash
dpkg -L bash | wc -l                              # A
rpm -ql bash | wc -l                              # B
```

</details>

**3.** (A) Leia paketi `curl` paigaldatud ja hoidlas saadaval olev versioon.

<details>
<summary>Lahendus</summary>

```bash
apt policy curl                                   # A
```

</details>

**4.** (B) Leia, milline pakett annab käsu `semanage`.

<details>
<summary>Lahendus</summary>

```bash
dnf provides semanage                             # B (pakett policycoreutils-python-utils)
```

</details>

**5.** (A ja B) Paigalda ja seejärel eemalda pakett `htop` (AlmaLinuxis on vaja EPEL-i).

<details>
<summary>Lahendus</summary>

```bash
sudo apt install htop && sudo apt remove htop     # A
sudo dnf install epel-release && sudo dnf install htop && sudo dnf remove htop   # B
```

</details>

**6.** (A) Leia failist `/var/log/apt/history.log` kõik read, kus midagi paigaldati (`Install:`).

<details>
<summary>Lahendus</summary>

```bash
grep '^Install:' /var/log/apt/history.log         # A
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 4. Pakihaldus kolmel distrol](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 5. Protsessid, teenused ja systemd →](../moodul-05-protsessid-teenused/index.md)
<!-- /navigatsioon -->
