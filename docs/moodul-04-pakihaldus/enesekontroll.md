# Moodul 4. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Mis on pakett, hoidla ja sõltuvus?
2. Nimeta kolm põhjust, miks paigaldada tarkvara pakihalduriga, mitte tootja kodulehelt alla laaditud failist.
3. Mis vahe on käskudel `dpkg` ja `apt` (või `rpm` ja `dnf`)?
4. Mida teeb `apt update` ja mida `apt upgrade`?
5. Mis vahe on käskudel `apt remove` ja `apt purge`?
6. Mida teeb `apt autoremove`?
7. Kuidas leida, millisesse paketti kuulub fail `/usr/bin/ssh`? Kirjuta käsk mõlema perekonna jaoks.
8. Mis on EPEL ja miks seda AlmaLinuxis sageli vaja on?
9. Millised riskid kaasnevad kolmanda osapoole hoidla lisamisega?
10. Kus asuvad hoidlate seadistused Debianis/Ubuntus ja AlmaLinuxis?
11. Mis on Ubuntu hoidla osade `main` ja `universe` erinevus?
12. Millised on kolm klassikalist sammu programmi kompileerimisel lähtekoodist? Kuhu programm vaikimisi paigaldatakse?
13. Miks ei uuendata lähtekoodist kompileeritud programmi koos süsteemiga?
14. Mis on Snap ja Flatpak? Nimeta üks eelis ja üks puudus.
15. Kuidas AlmaLinuxis viimast pakihalduri toimingut tagasi võtta?
16. Mida tuleb teha enne väljalaske uuendust (nt Debian 12 → 13)? Nimeta vähemalt neli sammu.
17. Milliste tööriistadega uuendatakse väljalaset Ubuntus ja AlmaLinuxis?

## Praktilised miniülesanded

Tee ülesanded Debiani või Ubuntu masinas (A) ja AlmaLinuxi masinas (B).

1. (A ja B) Uuenda süsteem ühe käsurea abil.
2. (A ja B) Leia, mitu faili on paketis `bash`.
3. (A) Leia paketi `curl` paigaldatud ja hoidlas saadaval olev versioon.
4. (B) Leia, milline pakett annab käsu `semanage`.
5. (A ja B) Paigalda ja seejärel eemalda pakett `htop` (AlmaLinuxis on vaja EPEL-i).
6. (A) Leia failist `/var/log/apt/history.log` kõik read, kus midagi paigaldati (`Install:`).

---

## Vastused

1. **Pakett** on arhiiv, mis sisaldab programmi faile, metaandmeid ja paigaldusskripte. **Hoidla** on server, kus asuvad paketid ja nende loend. **Sõltuvus** on teine pakett, mida programm töötamiseks vajab.
2. Näiteks: paketid on allkirjastatud ja kontrollitud; sõltuvused lahendatakse automaatselt; kogu süsteem uueneb ühe käsuga; eemaldamine on puhas.
3. `dpkg` / `rpm` on madala taseme tööriistad, mis paigaldavad üksiku paketifaili, kuid ei lahenda sõltuvusi ega laadi midagi alla. `apt` / `dnf` laadivad paketid hoidlast ja lahendavad sõltuvused automaatselt.
4. `apt update` värskendab hoidlatest pakettide loendi. `apt upgrade` uuendab paigaldatud paketid uuematele versioonidele.
5. `remove` eemaldab paketi, kuid jätab seadistusfailid alles. `purge` eemaldab ka seadistusfailid.
6. Eemaldab paketid, mis paigaldati sõltuvustena, kuid mida ükski paigaldatud pakett enam ei vaja.
7. Debian/Ubuntu: `dpkg -S /usr/bin/ssh`. AlmaLinux: `rpm -qf /usr/bin/ssh` (või `dnf provides /usr/bin/ssh`).
8. EPEL (*Extra Packages for Enterprise Linux*) on Fedora kogukonna lisapakettide hoidla RHEL-i perekonna distrodele. AlmaLinuxi põhihoidlates on teadlikult piiratud valik tarkvara, palju populaarseid tööriistu (nt `htop`, `ncdu`) on ainult EPEL-is.
9. Hoidla paigaldusskriptid töötavad juurkasutaja õigustes, seega pahatahtlik või häkitud hoidla võib süsteemi üle võtta. Lisaks võivad tekkida pakettide konfliktid ja uuendusprobleemid ning hoidla võib hooldamata jääda.
10. Debian/Ubuntu: `/etc/apt/sources.list.d/` (uuemates `.sources` failid) või `/etc/apt/sources.list`. AlmaLinux: `/etc/yum.repos.d/*.repo`.
11. `main` on Canonicali ametlikult toetatud vaba tarkvara. `universe` on kogukonna hooldatud vaba tarkvara, mille turvauuendusi Canonical ei taga samal määral.
12. `./configure`, `make`, `sudo make install`. Vaikimisi paigaldatakse kataloogi `/usr/local`.
13. Pakihaldur ei tea sellest programmist midagi, seega ei saa see programmi uuendada ega eemaldada. Uuendused tuleb ise jälgida ja programm uuesti kompileerida.
14. Distrost sõltumatud paketivormingud, kus programm on koos oma sõltuvustega ja töötab isoleeritult. Eelis: uusim versioon igas distros. Puudus: suurem maht ja aeglasem käivitus (või sõltuvuste turvauuendused sõltuvad paketi koostajast).
15. `dnf history` näitab toimingute numbreid, `sudo dnf history undo <nr>` võtab valitud toimingu tagasi.
16. Loe väljalaskemärkmeid, tee hetktõmmis või varukoopia, uuenda praegune väljalase lõpuni ja taaskäivita, kontrolli vaba kettaruumi, keela kolmandate osapoolte hoidlad, tee uuendust konsoolis või `tmux`-is.
17. Ubuntu: `do-release-upgrade`. AlmaLinux: ELevate projekti `leapp` (`leapp preupgrade`, `leapp upgrade`); RHEL-i perekonnas eelistatakse siiski uut paigaldust.

### Miniülesannete lahendused

```bash
# 1
sudo apt update && sudo apt upgrade -y            # A
sudo dnf upgrade -y                               # B
# 2
dpkg -L bash | wc -l                              # A
rpm -ql bash | wc -l                              # B
# 3
apt policy curl                                   # A
# 4
dnf provides semanage                             # B (pakett policycoreutils-python-utils)
# 5
sudo apt install htop && sudo apt remove htop     # A
sudo dnf install epel-release && sudo dnf install htop && sudo dnf remove htop   # B
# 6
grep '^Install:' /var/log/apt/history.log         # A
```

Võti `-y` vastab kõigile küsimustele automaatselt „jah“. Seda kasutatakse skriptides, kuid käsitsi töötades on parem enne kinnitamist üle vaadata, mida pakihaldur teha kavatseb.
