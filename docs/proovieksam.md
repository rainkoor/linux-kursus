<!-- navigatsioon -->
[← Moodul 17. Enesekontroll](moodul-17-seire/enesekontroll.md) · [Sisukord](../README.md#sisukord) · [Lõpuprojekt →](lopuprojekt.md)
<!-- /navigatsioon -->

# Proovieksam: süvendusosa

**Maht:** 4 tundi (eksam 2,5 h + arutelu) · **Distro:** AlmaLinux 10 · **Eeldused:** moodulid 1–17

Proovieksam on RHCSA eksami stiilis praktiline töö: tühjas virtuaalmasinas tuleb piiratud aja jooksul täita hulk haldusülesandeid. Hinnatakse **tulemust** (kas süsteem on õiges olekus, ka pärast taaskäivitust), mitte käskude kirjutamise viisi. Pärast eksamit kontrollib tulemust automaatne skript.

Põhiosa (moodulid 1–8) järel on lühem [proovieksam Debianis](proovieksam-pohiosa.md).

Eksam aitab õppijal näha, milliseid teemasid ta valdab iseseisvalt, ja õpetajal, mida enne lõpuprojekti korrata.

## Reeglid

- Aeg: **2,5 tundi**.
- Lubatud: süsteemi enda dokumentatsioon (`man`, `--help`, `/usr/share/doc`). Keelatud: internet, kursuse materjal, tehisintellekt, kaasõpilased.
- Masin peab pärast eksamit **taaskäivituma** ja kõik seaded peavad olema püsivad. Kontroll tehakse pärast taaskäivitust.
- Kui sa ei saa ülesannet tehtud, jäta see vahele ja tule hiljem tagasi.
- Sooritatud: vähemalt **70%** punktidest.

## Ettevalmistus (õpetaja või iseõppija)

1. Loo AlmaLinux 10 VM (2 vCPU, 2 GiB RAM, süsteemiketas 20 GiB) ja **lisaketas 2 GiB**. Paigalda minimaalne süsteem (vt [paigalduslisa](lisad/paigaldus.md)), loo kasutaja `opilane` sudo-õigusega, seadista võrk (SSH ligipääs).
2. Tee masinast **hetktõmmis** „eksami algus“ - nii saab eksamit korrata.
3. Laadi kontrollskript [kontroll.sh](proovieksam/kontroll.sh) masinasse alles **pärast** eksamit (või hoia seda õpetaja käes).

## Ülesanded

### 1. Süsteem ja võrk (6 p)

1. Sea masina hostinimeks `eksam.lab.example`.
2. Sea ajavööndiks `Europe/Tallinn`.
3. Veendu, et ajasünkroonimise teenus `chronyd` töötab ja käivitub alglaadimisel.

### 2. Kasutajad ja grupid (7 p)

1. Loo grupp `arendajad` GID-ga `3000`.
2. Loo kasutajad `liis` ja `tom`, kes kuuluvad lisagrupina gruppi `arendajad`.
3. Loo kasutaja `robot`, kes ei saa sisse logida (kest `/sbin/nologin`).
4. Grupi `arendajad` liikmed tohivad käivitada `sudo`-ga **ainult** käsu `systemctl restart httpd`. Kasuta faili kataloogis `/etc/sudoers.d/`.
5. Kasutaja `liis` parool peab aeguma iga 90 päeva järel.

### 3. Failid ja õigused (9 p)

1. Loo kataloog `/srv/projekt`, mille omanik on `root` ja grupp `arendajad`. Grupi liikmed saavad seal faile luua ja muuta, teised ei näe sisu. Kataloogis loodud failid kuuluvad automaatselt grupile `arendajad`.
2. Kasutaja `robot` peab saama `/srv/projekt` sisu lugeda (ACL), kuid mitte muuta.
3. Tee kataloogist `/etc` gzip-iga pakitud tar-arhiiv `/root/etc-varu.tar.gz`.
4. Leia kõik kataloogi `/usr` all olevad tavalised failid, mis on suuremad kui 50 MiB, ja kirjuta nende täisteed (üks rida kohta) faili `/root/suured.txt`.

### 4. Tarkvara ja teenused (7 p)

1. Paigalda veebiserver `httpd`.
2. Veebiserver peab töötama ja käivituma alglaadimisel.
3. Veebiserveri avaleht `http://localhost/` peab sisaldama sõna `Eksam`.
4. Luba tulemüüris püsivalt teenus `http`.

### 5. Kettad ja LVM (10 p)

Kasuta lisaketast (nt `/dev/sdb` või `/dev/vdb`).

1. Loo köitegrupp `vg_eksam`.
2. Loo selles köide `lv_andmed` suurusega **500 MiB**.
3. Loo köitele XFS-failisüsteem ja haagi see kataloogi `/mnt/andmed`.
4. Haakimine peab olema püsiv; kasuta fstab-is **UUID**-d.
5. Loo samale kettale 256 MiB lisasaaleala (köide või partitsioon), mis aktiveeritakse püsivalt alglaadimisel.

### 6. Turvalisus (11 p)

1. SSH: keela juurkasutaja sisselogimine.
2. SSH peab kuulama **pordil 2222** (lisaks võib jääda port 22). Luba port tulemüüris ja SELinuxis (`semanage port`).
3. SELinux peab olema režiimis *enforcing*.
4. Loo kataloog `/srv/veeb` ja seadista sellele püsivalt SELinuxi tüüp `httpd_sys_content_t` (ka alamkataloogidele).
5. Muuda süsteemilogi (journal) püsivaks, et logid säiliksid taaskäivitusel.

### 7. Ajastamine ja kernel (5 p)

1. Loo systemd teenus `varunda-etc.service` ja taimer `varunda-etc.timer`, mis käivitab iga päev kell 01:30 käsu `tar -czf /var/tmp/etc-$(date +%F).tar.gz /etc` (vihje: teenuses kasuta `/bin/bash -c '…'`). Taimer peab olema lubatud ja aktiivne.
2. Sea kerneli parameeter `vm.swappiness` väärtusele `10` püsivalt (fail kataloogis `/etc/sysctl.d/`).

### 8. Konteiner (3 p)

1. Käivita Podmaniga juurkasutaja konteiner pildist `docker.io/library/nginx` nimega `eksamiveeb`, mis on kättesaadav hosti pordil `8080`. Konteiner peab olema systemd teenus `eksamiveeb.service` (Quadlet) ja käivituma alglaadimisel.

**Kokku: 58 punkti.**

## Kontroll

Pärast eksamit taaskäivita masin ja käivita:

```bash
sudo bash kontroll.sh
```

Skript näitab iga kontrolli kohta `OK` või `VIGA`, punktisumma ja tulemuse. Kui midagi jäi tegemata, arutage koos: mis oli põhjus - kas ei teadnud, kuidas, ei leidnud dokumentatsioonist või unustas püsivuse (`enable`, `--permanent`, fstab)?

## Pärast eksamit

- Taasta hetktõmmis „eksami algus“ ja tee eksam uuesti - eesmärk on jõuda **90%+** ilma abita.
- Tee sama eksam Debianis: mis on erinev (`apt`, `ufw`, AppArmor, `/etc/apt/`, `adm`/`sudo` grupid)? Skript on kirjutatud AlmaLinuxi jaoks - Debianis tuleb osa kontrolle kohandada.

> [!NOTE]
> **Õpetajale:** skript kontrollib ainult olekut. Ülesannete sõnastus on täpne (nimed, numbrid), et kontroll oleks automaatne. Lisaülesandeid saab hõlpsasti lisada funktsiooniga `kontroll PUNKTID "kirjeldus" käsk`. Skripti süntaks on kontrollitud (`bash -n`), kuid päris AlmaLinuxis ei ole seda testitud - tee eksam enne õppijatega kasutamist üks kord ise läbi. Näidislahendus ja sagedased vead on õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 17. Enesekontroll](moodul-17-seire/enesekontroll.md) · [Sisukord](../README.md#sisukord) · [Lõpuprojekt →](lopuprojekt.md)
<!-- /navigatsioon -->
