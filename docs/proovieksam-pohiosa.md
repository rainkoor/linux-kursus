<!-- navigatsioon -->
[← Moodul 8. Enesekontroll](moodul-08-kettad-lvm/enesekontroll.md) · [Sisukord](../README.md#sisukord) · [Moodul 9. Salvestus: RAID, ZFS, jõudlus ja taastamine →](moodul-09-salvestus/index.md)
<!-- /navigatsioon -->

# Proovieksam: põhiosa

**Maht:** 2 tundi (eksam 1,5 h + arutelu) · **Distro:** Debian 13 · **Eeldused:** moodulid 1–8

See proovieksam kontrollib **põhiosa** oskusi: käsurida, failid ja tekst, kasutajad ja õigused, pakihaldus, teenused ja ajastamine, lihtne skript, võrk ja SSH ning kettad ja LVM. Tühjas virtuaalmasinas tuleb piiratud aja jooksul täita haldusülesanded. Hinnatakse **tulemust** - süsteemi olekut pärast taaskäivitust -, mitte käskude kirjutamise viisi. Tulemust kontrollib automaatne skript.

Eksam sobib tegemiseks pärast moodulit 8 ja enne [lõpuprojekti algtaset](lopuprojekt.md). Süvendusosa järel on [teine proovieksam](proovieksam.md) AlmaLinuxis.

## Reeglid

- Aeg: **1,5 tundi**.
- Lubatud: süsteemi enda dokumentatsioon (`man`, `--help`, `/usr/share/doc`). Keelatud: internet, kursuse materjal, tehisintellekt, kaasõpilased.
- Masin peab pärast eksamit **taaskäivituma** ja kõik seaded peavad olema püsivad. Kontroll tehakse pärast taaskäivitust.
- Kui sa ei saa ülesannet tehtud, jäta see vahele ja tule hiljem tagasi.
- Sooritatud: vähemalt **70%** punktidest.

## Ettevalmistus (õpetaja või iseõppija)

1. Loo Debian 13 VM (2 vCPU, 2 GiB RAM, süsteemiketas 20 GiB) ja **lisaketas 2 GiB**. Paigalda minimaalne süsteem koos SSH-serveriga (vt [paigalduslisa](lisad/paigaldus.md)), loo tavakasutaja `opilane` ja anna talle `sudo` õigus. HKHK laboris annab masina õpetaja.
2. Tee masinast **hetktõmmis** „eksami algus“ - nii saab eksamit korrata.
3. Laadi kontrollskript [kontroll-pohiosa.sh](proovieksam/kontroll-pohiosa.sh) masinasse alles **pärast** eksamit (või hoia seda õpetaja käes).

## Ülesanded

Tee ülesanded juurkasutaja õigustes (`sudo`). Nimed, numbrid ja failiteed peavad olema **täpselt** sellised, nagu kirjas.

### 1. Süsteem (4 p)

1. Sea masina hostinimeks `pohi.lab.example`.
2. Sea ajavööndiks `Europe/Tallinn`.

### 2. Kasutajad ja grupid (8 p)

1. Loo grupp `opetajad` GID-ga `4000`.
2. Loo kasutajad `anna` ja `peeter` kodukataloogi ja kestaga `/bin/bash`. Mõlemad kuuluvad lisagrupina gruppi `opetajad`.
3. Kasutaja `anna` peab saama kasutada `sudo`-t.
4. Loo kasutaja `varundus`, kes ei saa sisse logida (kest `/usr/sbin/nologin`).
5. Kasutaja `peeter` parool peab aeguma iga 60 päeva järel.

### 3. Failid, õigused ja tekst (13 p)

1. Loo kataloog `/srv/opetajad`, mille omanik on `root` ja grupp `opetajad`. Grupi liikmed saavad seal faile luua ja muuta, teised ei näe sisu. Uued failid kuuluvad automaatselt grupile `opetajad`.
2. Loo kataloog `/srv/avalik`, kuhu kõik saavad faile kirjutada, kuid teiste faile kustutada ei saa.
3. Loo sümbolviit `/root/hosts-viit`, mis viitab failile `/etc/hosts`.
4. Tee kataloogist `/etc/ssh` gzip-iga pakitud tar-arhiiv `/root/ssh-varu.tar.gz`.
5. **Pärast ülesande 2 tegemist** kirjuta faili `/root/bash-kasutajad.txt` kõigi nende kasutajate nimed, kelle kest on `/bin/bash`, iga nimi eraldi real ja tähestiku järjekorras. Kasuta käske, mitte käsitsi kirjutamist.
6. Kirjuta faili `/root/tcp-arv.txt` ainult üks arv: mitu rida failis `/etc/services` sisaldab teksti `/tcp`.

### 4. Tarkvara, teenused ja ajastamine (10 p)

1. Paigalda paketid `tree` ja `htop`.
2. Paigalda veebiserver `nginx`. See peab töötama ja käivituma alglaadimisel.
3. Veebiserveri avaleht (`http://localhost/`) peab sisaldama sõna `Põhiosa`.
4. Loo systemd teenus `kettaaruanne.service`, mis kirjutab käsu `df -h` väljundi faili `/var/tmp/kettad.txt` (vihje: `/bin/bash -c '…'`), ja taimer `kettaaruanne.timer`, mis käivitab teenuse **iga päev kell 06:00**. Taimer peab olema lubatud ja aktiivne.

### 5. Võrk, SSH ja tulemüür (6 p)

1. SSH: keela juurkasutaja sisselogimine.
2. Paigalda ja lülita sisse tulemüür `ufw`, mis lubab ainult SSH (22) ja HTTP (80). **Luba SSH enne tulemüüri sisselülitamist!**

### 6. Kettad ja LVM (10 p)

Kasuta lisaketast (nt `/dev/sdb` või `/dev/vdb`).

1. Loo köitegrupp `vg_pohi`.
2. Loo selles köide `lv_kodu` suurusega **400 MiB** ja sellele ext4 failisüsteem.
3. Haagi köide kataloogi `/mnt/kodu` püsivalt; kasuta fstab-is **UUID**-d.
4. Suurenda seejärel köide **600 MiB**-ni nii, et ka failisüsteem suureneb.

### 7. Skript (5 p)

Kirjuta skript `/usr/local/bin/tervitus`, mis:

- väljastab argumendiga käivitades tervituse kujul `Tere, Mari!` (käsk `tervitus Mari`);
- ilma argumendita kirjutab kasutusjuhise **standardveaväljundisse** ja lõpetab väljumiskoodiga `1`.

Skript peab olema käivitatav kõigile.

**Kokku: 56 punkti.**

## Kontroll

Pärast eksamit taaskäivita masin ja käivita:

```bash
sudo bash kontroll-pohiosa.sh
```

Skript näitab iga kontrolli kohta `OK` või `VIGA`, punktisumma ja tulemuse. Arutage koos tegemata jäänud ülesandeid: kas ei teadnud, kuidas, ei leidnud dokumentatsioonist või unustas püsivuse (`enable`, fstab, `ufw enable`)?

## Pärast eksamit

- Taasta hetktõmmis „eksami algus“ ja tee eksam uuesti - eesmärk on jõuda **90%+** ilma abita.
- Kõige sagedasemad vead: kasutajal puudub `-a` (`usermod -G` kustutas teised grupid), fstab-is seadme nimi UUID asemel, unustatud `systemctl enable`, failisüsteem jäi köite suurendamisel samaks (`lvextend` ilma `-r`-ita).

> [!NOTE]
> **Õpetajale:** skript kontrollib ainult olekut. Selle süntaks ja abifunktsioonid on kontrollitud, kuid päris Debianis ei ole kogu eksamit läbi tehtud - tee see enne õppijatega kasutamist üks kord ise läbi.

<!-- navigatsioon -->
---

[← Moodul 8. Enesekontroll](moodul-08-kettad-lvm/enesekontroll.md) · [Sisukord](../README.md#sisukord) · [Moodul 9. Salvestus: RAID, ZFS, jõudlus ja taastamine →](moodul-09-salvestus/index.md)
<!-- /navigatsioon -->
