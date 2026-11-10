<!-- navigatsioon -->
[← Moodul 9. Varundus ja taastamine](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 9. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 9. Varundus ja taastamine

| | |
|---|---|
| **Distro** | Debian (varundatav masin), Ubuntu (varuserver) |
| **Kestus** | 3 × 90 minutit |
| **Vajalik** | Debiani ja Ubuntu virtuaalmasin samas võrgus (laboritöö 7), SSH-võtmed Debianist Ubuntusse, laboritöö 6 skript `varunda` |
| **Eesmärk** | Varundada ja taastada `tar`-i, `rsync`-i ja restic'uga, automatiseerida varundus ning teha taastamistest |

> **Aruanne:** vasta küsimustele **K1–K12** ja lisa 7. osas koostatud varundusplaan. Kõik küsimused on koos ka lehe lõpus ([Aruande küsimused](#aruande-küsimused)).

Laboris kasutatavad tähised:

| Tähis | Tähendus |
|---|---|
| `UBUNTU_IP` | Ubuntu masina (varuserveri) aadress |
| `kasutaja` | Sinu kasutajanimi |

---

## 0. osa. Ettevalmistus

**0.1** Loo Debianis „asutuse andmed“, mida hakkad varundama:

```bash
sudo mkdir -p /srv/andmed/{raamatupidamine,opetajad,pildid}
for i in $(seq 1 50); do echo "Dokument $i, loodud $(date)" | sudo tee /srv/andmed/opetajad/dok$i.txt > /dev/null; done
sudo dd if=/dev/urandom of=/srv/andmed/pildid/suur.bin bs=1M count=50 status=none
echo "Eelarve 2027: 12 345 eurot" | sudo tee /srv/andmed/raamatupidamine/eelarve.txt
sudo chmod 750 /srv/andmed/raamatupidamine
du -sh /srv/andmed
```

**0.2** Loo Ubuntus varunduse jaoks kasutaja ja kataloog ning luba Debiani juurkasutajal SSH-võtmega sisse logida (varundus töötab juurkasutajana, et lugeda kõiki faile):

```bash
# Ubuntu
sudo adduser --disabled-password --gecos "" varu
sudo mkdir -p /varu && sudo chown varu:varu /varu
```

```bash
# Debian
sudo ssh-keygen -t ed25519 -N "" -f /root/.ssh/varu_ed25519
sudo cat /root/.ssh/varu_ed25519.pub        # kopeeri see Ubuntu faili /home/varu/.ssh/authorized_keys
```

```bash
# Ubuntu: lisa võti
sudo -u varu mkdir -p -m 700 /home/varu/.ssh
sudo -u varu nano /home/varu/.ssh/authorized_keys       # kleebi võti
sudo chmod 600 /home/varu/.ssh/authorized_keys
```

```bash
# Debian: kontrolli
sudo ssh -i /root/.ssh/varu_ed25519 varu@UBUNTU_IP hostname
sudo apt install restic acl
```

Lisa Debianis faili `/root/.ssh/config` plokk, et edaspidi piisaks nimest `varuserver`:

```text
Host varuserver
    HostName UBUNTU_IP
    User varu
    IdentityFile /root/.ssh/varu_ed25519
```

---

## 1. osa. tar: täisvarundus ja üksiku faili taastamine

**1.1** Lisa ühele failile ACL (moodul 3) ja tee täisvarundus (teooria punkt 9.6):

```bash
sudo setfacl -m u:kasutaja:r /srv/andmed/raamatupidamine/eelarve.txt
sudo mkdir -p /varu
sudo tar --acls --xattrs -czpf /varu/andmed-$(date +%F).tar.gz /srv/andmed
ls -lh /varu
sudo tar -tzvf /varu/andmed-*.tar.gz | head
```

> **K1.** Kui suur on arhiiv võrreldes `du -sh /srv/andmed` tulemusega? Miks pakkis `suur.bin` nii halvasti (vihje: juhuslikud andmed)? Kuidas on arhiivis failiteed kirjutatud ja miks pole alguses `/`-i?

**1.2** „Kustuta kogemata“ fail ja taasta ainult see üks fail:

```bash
sudo rm /srv/andmed/raamatupidamine/eelarve.txt
sudo mkdir -p /tmp/taaste
sudo tar --acls --xattrs -xzpf /varu/andmed-*.tar.gz -C /tmp/taaste srv/andmed/raamatupidamine/eelarve.txt
getfacl /tmp/taaste/srv/andmed/raamatupidamine/eelarve.txt
sudo cp -a /tmp/taaste/srv/andmed/raamatupidamine/eelarve.txt /srv/andmed/raamatupidamine/
```

> **K2.** Kas taastatud failil olid alles omanik, õigused ja ACL? Mis juhtunuks, kui oleksid arhiivi lahti pakkinud otse kataloogi `/` (ilma `-C`-ta)?

---

## 2. osa. Juurdekasvuga varundus

**2.1** Tee tar-iga juurdekasvu ahel (teooria punkt 9.6):

```bash
sudo tar --listed-incremental=/varu/andmed.snar -czpf /varu/inc-0.tar.gz /srv/andmed
echo "Uus dokument" | sudo tee /srv/andmed/opetajad/uus.txt
sudo tar --listed-incremental=/varu/andmed.snar -czpf /varu/inc-1.tar.gz /srv/andmed
sudo rm /srv/andmed/opetajad/dok1.txt
sudo tar --listed-incremental=/varu/andmed.snar -czpf /varu/inc-2.tar.gz /srv/andmed
ls -lh /varu/inc-*
sudo tar -tzvf /varu/inc-1.tar.gz
```

> **K3.** Kui suured on `inc-0`, `inc-1` ja `inc-2`? Mida sisaldab `inc-1`? Milliseid arhiive on vaja seisu taastamiseks pärast 2. sammu ja mis juhtub, kui `inc-1` on rikutud?

---

## 3. osa. rsync teise masinasse

**3.1** Kopeeri andmed varuserverisse (teooria punkt 9.7):

```bash
sudo rsync -aAXv --delete /srv/andmed/ varuserver:/varu/debian1-peegel/
sudo rsync -aAXv --delete /srv/andmed/ varuserver:/varu/debian1-peegel/     # teine kord - mida kopeeris?
```

**3.2** Simuleeri lunavara: „krüpteeri“ Debianis üks kaust ja käivita peegeldus uuesti:

```bash
for f in /srv/andmed/opetajad/dok*.txt; do sudo sh -c "rev '$f' > '$f.lukus' && rm '$f'"; done
ls /srv/andmed/opetajad | head
sudo rsync -aAXv --delete /srv/andmed/ varuserver:/varu/debian1-peegel/
sudo ssh varuserver ls /varu/debian1-peegel/opetajad | head
```

> **K4.** Mis juhtus varuserveris olevate failidega? Miks ei ole `rsync --delete` peegel varukoopia? Taasta `opetajad` kaust 1. osa tar-arhiivist.

**3.3** Tee ajalised koopiad `--link-dest`-iga. Kuna laboris ei saa päevi oodata, kasuta kuupäeva asemel numbrit:

```bash
sudo rsync -aAX --delete /srv/andmed/ varuserver:/varu/aeg/1/
echo "muudatus" | sudo tee /srv/andmed/opetajad/muudetud.txt
sudo rsync -aAX --delete --link-dest=/varu/aeg/1 /srv/andmed/ varuserver:/varu/aeg/2/
```

```bash
# Ubuntu
sudo du -sh /varu/aeg/1 /varu/aeg/2      # du loeb kõvaviiteid üks kord
sudo du -sh /varu/aeg/2
ls -li /varu/aeg/1/pildid/suur.bin /varu/aeg/2/pildid/suur.bin
```

> **K5.** Kui palju ruumi võttis teine koopia? Mida näitab `ls -li` (i-sõlme number ja viidete arv) faili `suur.bin` kohta ja miks? Kas koopiast `2` saab taastada kõik failid, kuigi see võttis vähe ruumi?

---

## 4. osa. Varundusskript ja taimer

**4.1** Loo skript `/usr/local/sbin/varunda-andmed` teooria punkti 9.8 eeskujul: varundab `/etc`, `/home` ja `/srv/andmed` kataloogi `/varu/igaoine`, kontrollib arhiivi, kustutab üle 7 päeva vanad koopiad ja logib `logger -t varundus` abil. Lisa skripti lõppu koopia saatmine varuserverisse:

```bash
rsync -a "$SIHT/$NIMI.tar.gz" varuserver:/varu/igaoine/
```

Võid kasutada ja täiendada laboritöö 6 skripti `varunda`.

```bash
sudo chmod 700 /usr/local/sbin/varunda-andmed
sudo /usr/local/sbin/varunda-andmed
journalctl -t varundus -n 5
```

**4.2** Loo veateate üksus, mis kirjutab logisse ja faili `/var/log/varundus-VIGA` (päris süsteemis saadaks see e-kirja, moodul 20):

```ini
# /etc/systemd/system/varundus-viga.service
[Unit]
Description=Teata varunduse veast

[Service]
Type=oneshot
ExecStart=/bin/sh -c 'logger -t varundus -p user.crit "VARUNDUS EBAÕNNESTUS"; date >> /var/log/varundus-VIGA'
```

**4.3** Loo teooria punkti 9.8 järgi `varundus.service` (koos `OnFailure=varundus-viga.service`) ja `varundus.timer` (iga päev 02:30, `Persistent=true`). Luba taimer ja käivita teenus kohe:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now varundus.timer
sudo systemctl start varundus.service
systemctl status varundus.service --no-pager
systemctl list-timers varundus.timer
```

> **K6.** Millal käivitub varundus järgmine kord? Mis juhtub, kui masin on kell 02:30 välja lülitatud? Mida teevad `Nice=` ja `IOSchedulingClass=idle`?

**4.4** Riku skript meelega (nt muuda sihtkataloog `/varu` kohta, kuhu ei saa kirjutada, või lisa rida `false`), käivita teenus ja vaata tulemust:

```bash
sudo systemctl start varundus.service
systemctl status varundus.service varundus-viga.service --no-pager
journalctl -t varundus -p crit
cat /var/log/varundus-VIGA
```

> **K7.** Kas veateade jõudis logisse ja faili? Miks on `set -euo pipefail` varundusskriptis eriti oluline? Paranda skript.

---

## 5. osa. restic

**5.1** Loo kohalik restic'u hoidla ja tee kaks varundust (teooria punkt 9.9):

```bash
openssl rand -base64 24 | sudo tee /root/.restic-parool > /dev/null
sudo chmod 600 /root/.restic-parool
export RESTIC_REPOSITORY=/varu/restic RESTIC_PASSWORD_FILE=/root/.restic-parool
sudo -E restic init
sudo -E restic backup /etc /srv/andmed
echo "teine versioon" | sudo tee -a /srv/andmed/raamatupidamine/eelarve.txt
sudo -E restic backup /etc /srv/andmed
sudo -E restic snapshots
sudo -E restic diff ID1 ID2          # ID-d võta snapshots väljundist (vanem, uuem)
du -sh /varu/restic
```

> **K8.** Kui palju ruumi võttis teine varundus (võrdle `du` enne ja pärast või vaata `backup` väljundi rida `Added to the repository`)? Mida näitas `restic diff`? Miks ei saa restic'u hoidlat ilma paroolita lugeda ja mida see tähendab parooli hoidmise jaoks?

**5.2** Tee teine hoidla varuserverisse SFTP kaudu ja varunda sinna:

```bash
export RESTIC_REPOSITORY=sftp:varuserver:/varu/restic-debian1
sudo -E restic init
sudo -E restic backup /etc /srv/andmed
sudo -E restic forget --keep-last 3 --keep-daily 7 --prune
sudo -E restic check
```

> **K9.** Kuidas vastab sinu varundus nüüd 3-2-1 reeglile (loe kokku koopiad, andmekandjad ja asukohad)? Mis on veel puudu?

---

## 6. osa. Katastroof ja taastamistest

**6.1** Märgi üles kellaaeg. Simuleeri katastroofi Debianis:

```bash
date
sudo rm -rf /srv/andmed
```

**6.2** Taasta kõik andmed **varuserveri** restic'u hoidlast (mitte kohalikust - kujutle, et kohalik ketas on läinud):

```bash
export RESTIC_REPOSITORY=sftp:varuserver:/varu/restic-debian1 RESTIC_PASSWORD_FILE=/root/.restic-parool
sudo -E restic snapshots
sudo -E restic restore latest --target /tmp/taaste2 --include /srv/andmed
sudo ls -la /tmp/taaste2/srv/andmed
sudo cp -a /tmp/taaste2/srv/andmed /srv/
getfacl /srv/andmed/raamatupidamine/eelarve.txt
cat /srv/andmed/raamatupidamine/eelarve.txt
date
```

> **K10.** Kui kaua taastamine aega võttis (alates kustutamisest)? Kas kõik failid, õigused ja ACL taastusid? Milline versioon failist `eelarve.txt` taastus ja miks?

> **K11.** Mis oleks juhtunud, kui `/root/.restic-parool` oleks olnud ainult Debianis ja kogu Debiani masin oleks hävinud? Kus peaks varunduse parooli hoidma?

---

## 7. osa. Varundusplaan

**7.1** Kirjuta oma Debiani masina varundusplaan (Markdown, 1 lk):

- mida varundatakse ja mida mitte;
- RPO ja RTO (kujutle, et `/srv/andmed` on kooli õpetajate ühiskaust);
- kuidas, kuhu ja millal varundatakse (tööriist, ajastus, säilitamine);
- kuidas jälgitakse, et varundus töötab;
- taastamise sammud (nii, et klassivend saaks neid järgida);
- millal ja kuidas tehakse taastamistest.

> **K12.** Milline sinu plaani RPO ja RTO on ning kas 6. osa taastamistest neid täitis? Mis oleks plaani kõige nõrgem koht lunavara rünnaku korral?

---

## Koristamine

Kui õpetaja ei ole teisiti öelnud, jäta varundus alles - seda kasutatakse süvendusosas edasi. Kustuta ajutised taastekataloogid (`sudo rm -rf /tmp/taaste /tmp/taaste2`).

---

## Lisaülesanne (valikuline)

1. **Piiratud SSH-võti:** piira varuserveris võtme õigusi nii, et sellega saab ainult `rsync`-iga kirjutada kataloogi `/varu` (faili `authorized_keys` võtme ette `command="rrsync /varu",restrict`; `rrsync` on paketis `rsync`). Mis juhtub, kui proovid sama võtmega `ssh varuserver bash`?
2. **Varundus teisest suunast (*pull*):** seadista varuserver ise andmeid Debianist tõmbama (`rsync` Ubuntust Debiani lugemisõigusega kasutajana). Miks on see lunavara vastu turvalisem?
3. **LVM hetktõmmis varunduseks:** kui sul on laboritööst 8 LVM-köide, tee sellest hetktõmmis, haagi see ainult lugemiseks, varunda hetktõmmis tar-iga ja kustuta hetktõmmis. Miks on see parem kui töötava kataloogi otse varundamine?
4. **borg:** korda 5. osa BorgBackupiga (`borg init`, `borg create`, `borg list`, `borg extract`) ja võrdle restic'uga.

---

<!-- kysimused -->
## Aruande küsimused

Kõik selle laboritöö küsimused ühes kohas. Sulgudes on punkt, mille juures küsimust küsitakse. Kopeeri loend oma aruande alguseks ja kirjuta vastus iga küsimuse alla. Kus küsitakse käsku, kirjuta üles kogu käsk.

- **K1.** *(punkt 1.1)* Kui suur on arhiiv võrreldes `du -sh /srv/andmed` tulemusega? Miks pakkis `suur.bin` nii halvasti (vihje: juhuslikud andmed)? Kuidas on arhiivis failiteed kirjutatud ja miks pole alguses `/`-i?
- **K2.** *(punkt 1.2)* Kas taastatud failil olid alles omanik, õigused ja ACL? Mis juhtunuks, kui oleksid arhiivi lahti pakkinud otse kataloogi `/` (ilma `-C`-ta)?
- **K3.** *(punkt 2.1)* Kui suured on `inc-0`, `inc-1` ja `inc-2`? Mida sisaldab `inc-1`? Milliseid arhiive on vaja seisu taastamiseks pärast 2. sammu ja mis juhtub, kui `inc-1` on rikutud?
- **K4.** *(punkt 3.2)* Mis juhtus varuserveris olevate failidega? Miks ei ole `rsync --delete` peegel varukoopia? Taasta `opetajad` kaust 1. osa tar-arhiivist.
- **K5.** *(punkt 3.3)* Kui palju ruumi võttis teine koopia? Mida näitab `ls -li` (i-sõlme number ja viidete arv) faili `suur.bin` kohta ja miks? Kas koopiast `2` saab taastada kõik failid, kuigi see võttis vähe ruumi?
- **K6.** *(punkt 4.3)* Millal käivitub varundus järgmine kord? Mis juhtub, kui masin on kell 02:30 välja lülitatud? Mida teevad `Nice=` ja `IOSchedulingClass=idle`?
- **K7.** *(punkt 4.4)* Kas veateade jõudis logisse ja faili? Miks on `set -euo pipefail` varundusskriptis eriti oluline? Paranda skript.
- **K8.** *(punkt 5.1)* Kui palju ruumi võttis teine varundus (võrdle `du` enne ja pärast või vaata `backup` väljundi rida `Added to the repository`)? Mida näitas `restic diff`? Miks ei saa restic'u hoidlat ilma paroolita lugeda ja mida see tähendab parooli hoidmise jaoks?
- **K9.** *(punkt 5.2)* Kuidas vastab sinu varundus nüüd 3-2-1 reeglile (loe kokku koopiad, andmekandjad ja asukohad)? Mis on veel puudu?
- **K10.** *(punkt 6.2)* Kui kaua taastamine aega võttis (alates kustutamisest)? Kas kõik failid, õigused ja ACL taastusid? Milline versioon failist `eelarve.txt` taastus ja miks?
- **K11.** *(punkt 6.2)* Mis oleks juhtunud, kui `/root/.restic-parool` oleks olnud ainult Debianis ja kogu Debiani masin oleks hävinud? Kus peaks varunduse parooli hoidma?
- **K12.** *(punkt 7.1)* Milline sinu plaani RPO ja RTO on ning kas 6. osa taastamistest neid täitis? Mis oleks plaani kõige nõrgem koht lunavara rünnaku korral?
<!-- /kysimused -->

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 9. Varundus ja taastamine](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 9. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
