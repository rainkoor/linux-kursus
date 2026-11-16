<!-- navigatsioon -->
[← Moodul 19. Faili- ja prindiserverid](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 19. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 19. Kooli väikeserver, IV osa: faili- ja prindiserver, varundus ja dokumentatsioon

| | |
|---|---|
| **Distro** | Debian (laboritööde 15-17 server `debian1`), klient Ubuntu, Windows |
| **Kestus** | 4 × 90 minutit |
| **Vajalik** | Laboritööde 15-17 server ja Ubuntu klient, oma arvuti Windowsi failihalduriga, varunduseks teine Debiani masin `debian2` (lisaülesanne) |
| **Eesmärk** | Lisada serverile failijagamine Linuxile ja Windowsile, seadistada ühiskaust ja varundus ning dokumenteerida valmis server |

> **Aruanne:** vasta küsimustele **K1–K13** ja esita 7. osas koostatud serveri dokumentatsioon. Kõik küsimused on koos ka lehe lõpus ([Aruande küsimused](#aruande-küsimused)).

Tähised on samad mis laboritöös 15 (`SERVER_IP`, `KLIENT_IP`, `VORK`, `lab.example`).

---

## 0. osa. Ettevalmistus

```bash
sudo apt install nfs-kernel-server samba restic acl
```

---

## 1. osa. NFS

**1.1** Seadista serveris NFS-jagamine `/srv/nfs/jagatud` ainult oma laborivõrgule (lugemis- ja kirjutusõigusega). Pane sinna testfail.

```bash
sudo mkdir -p /srv/nfs/jagatud
echo "NFS töötab" | sudo tee /srv/nfs/jagatud/tere.txt
sudo nano /etc/exports
sudo exportfs -ra
sudo exportfs -v
```

**1.2** Haagi jagamine Ubuntu kliendis:

```bash
sudo apt install nfs-common
showmount -e debian1.lab.example
sudo mkdir -p /mnt/nfs
sudo mount -t nfs debian1.lab.example:/srv/nfs/jagatud /mnt/nfs
cat /mnt/nfs/tere.txt
touch /mnt/nfs/klient.txt
sudo touch /mnt/nfs/root.txt
```

> **K1.** Kas tavakasutaja sai faili luua? Mis juhtus juurkasutajana (`sudo touch`)? Miks? (Vihje: `root_squash`.)

**1.3** Muuda serveris jagatud kataloogi õigusi nii, et kõik saavad sinna kirjutada (`sudo chmod 1777 /srv/nfs/jagatud`), ja korda kliendis faili loomist. Vaata serveris failide omanikke (`ls -ln /srv/nfs/jagatud`).

> **K2.** Mis numbriline omanik (UID) on kliendis loodud failidel serveris? Kas see vastab serveris samale kasutajale? Miks võib see olla probleem?

**1.4** Lisa haakimine kliendi faili `/etc/fstab` (vt teooria punkt 19.2) ja kontrolli `sudo mount -a`.


---

## 2. osa. autofs

**2.1** Eemalda Ubuntu kliendis 1. osas lisatud NFS-rida failist `/etc/fstab` (kommenteeri välja) ja haagi jagamine lahti (`sudo umount /mnt/nfs`).

**2.2** Seadista autofs nii, et jagamine haagitakse kataloogi `/mnt/kool/jagatud` alles siis, kui seda kasutatakse, ja haagitakse lahti 60 sekundi tegevusetuse järel (teooria punkt 19.3):

```bash
sudo apt install autofs
echo "/mnt/kool  /etc/auto.kool  --timeout=60" | sudo tee /etc/auto.master.d/kool.autofs
echo "jagatud  -rw,sync  debian1.lab.example:/srv/nfs/jagatud" | sudo tee /etc/auto.kool
sudo systemctl restart autofs
ls /mnt/kool
ls /mnt/kool/jagatud
findmnt /mnt/kool/jagatud
sleep 70; findmnt /mnt/kool/jagatud
```

> **K3.** Mida näitas `ls /mnt/kool` enne jagatud kataloogi avamist? Kas jagamine oli pärast 70 sekundit veel haagitud? Miks on autofs parem kui fstab-rida, kui failiserver võib alglaadimise ajal maas olla?

---

## 3. osa. Samba

**3.1** Loo serveris Samba jagamine `jagatud` grupile `smbkasutajad` (vt teooria punkt 19.4). Lisa oma kasutaja gruppi ja määra Samba parool.

```bash
testparm -s 2>/dev/null | tail -10
sudo systemctl restart smbd
```

**3.2** Testi Ubuntu kliendist:

```bash
sudo apt install smbclient
smbclient -L //debian1.lab.example -U <kasutaja>
smbclient //debian1.lab.example/jagatud -U <kasutaja> -c "put /etc/hostname klient-hostname.txt; ls"
```

**3.3** Ühenda jagamine oma **Windowsi arvutist**: Exploreri aadressiribale `\\SERVER_IP\jagatud`. Loo seal fail ja vaata serveris: `ls -l /srv/samba/jagatud`.

> **K4.** Millised olid Windowsist loodud faili õigused ja grupp serveris? Millised `smb.conf` valikud seda mõjutasid?


---

## 4. osa. Ühiskaust õpetajatele

**4.1** Loo serveris grupid `opetajad` ja `juhtkond` ning kaks testkasutajat (nt `ain` ja `kati`) gruppi `opetajad`. Loo kataloog `/srv/jagatud/opetajad`, mille õigused on seadistatud teooria punkti 19.5 järgi: SGID, grupil `opetajad` täisõigused (ka vaikimisi ACL-iga), grupil `juhtkond` ainult lugemisõigus.

**4.2** Jaga kataloog Sambaga nimega `opetajad` (`valid users = @opetajad @juhtkond`, `inherit acls = yes`, prügikast `vfs objects = recycle`). Määra testkasutajatele Samba paroolid.

**4.3** Testi: Ain loob faili (nt `smbclient //debian1.lab.example/opetajad -U ain -c "put /etc/hostname ain.txt"`), Kati muudab sama faili (laadi see alla, muuda ja laadi üles) ning kustutab selle. Vaata serveris:

```bash
ls -l /srv/jagatud/opetajad
getfacl /srv/jagatud/opetajad/ain.txt
ls -la /srv/jagatud/opetajad/.prugikast/
```

> **K5.** Millised olid Aini loodud faili grupp ja ACL? Kas Kati sai faili muuta? Kuhu sattus kustutatud fail? Mis juhtuks ilma vaikimisi ACL-ita, kui Aini `umask` on `022`?

---

## 5. osa. Prindiserver

Päris printerit laboris ei ole, seepärast kasutame virtuaalset PDF-printerit. Kõik muu (jagamine, kliendid, järjekord) on sama mis päris printeriga (teooria punkt 19.8).

**5.1** Paigalda serverisse CUPS ja PDF-printer, lisa oma kasutaja haldurite gruppi ning luba jagamine:

```bash
sudo apt install cups printer-driver-cups-pdf
sudo usermod -aG lpadmin $USER
sudo cupsctl --share-printers --remote-admin
sudo lpadmin -p PDF -o printer-is-shared=true
lpstat -p -d
sudo ss -tlpn | grep 631
```

Kui tulemüür on sees, luba port 631/tcp oma laborivõrgust.

**5.2** Prindi serveris proovileht ja leia tulemus:

```bash
lp -d PDF /etc/hostname
lpstat -o
ls -l ~/PDF/
```

**5.3** Lisa printer Ubuntu kliendis (`sudo apt install cups-client`, kui käske ei ole) ja prindi sealt:

```bash
sudo lpadmin -p kool-pdf -E -v ipp://debian1.lab.example:631/printers/PDF -m everywhere
lpstat -p
lp -d kool-pdf /etc/os-release
```

> **K6.** Kuhu tekkis kliendist prinditud PDF-fail ja kelle nimel? Mida näitab serveris fail `/var/log/cups/page_log` (või `access_log`)? Miks on see haldurile kasulik?

**5.4** Peata serveris järjekord, prindi kliendist kaks faili, vaata järjekorda, tühista üks töö ja käivita järjekord uuesti:

```bash
sudo cupsdisable PDF
lpstat -o                      # pärast kliendist printimist
cancel <töö-ID>
sudo cupsenable PDF
```

> **K7.** Mida näitas `lpstat -o` peatatud järjekorra ajal? Mis sai tühistamata tööst pärast `cupsenable`-t? Too kolm põhjust, miks kasutada prindiserverit, selle asemel et iga arvuti prindiks otse printerisse.

**5.5** (Kui sul on Windowsi klient) lisa printer Windowsis aadressiga `http://debian1.lab.example:631/printers/PDF` ja prindi proovileht.

---

## 6. osa. Kogu serveri varundus ja taastamine

Kooli väikeserver on nüüd valmis: veebisait (laboritöö 15), andmebaas (16), DNS (17) ja failijagamised. Varunda kõik moodulis 9 õpitud viisil.

**6.1** Loo varundusskript `/usr/local/sbin/varunda-debian1`:

```bash
#!/bin/bash
# debian1 igaöine varundus: andmebaas + seadistus + andmed → restic
set -euo pipefail

export RESTIC_REPOSITORY=/srv/varundus/restic
export RESTIC_PASSWORD_FILE=/root/.restic-parool
DUMPID=/var/backups/mariadb

mkdir -p "$DUMPID"
mariadb-dump --all-databases --single-transaction > "$DUMPID/koik.sql"

restic backup --tag igaoine /etc /var/www /srv/nfs /srv/samba /srv/jagatud /var/lib/samba/private "$DUMPID" /root/ca
restic forget --tag igaoine --keep-daily 7 --keep-weekly 4 --prune
restic check
```

**6.2** Loo parool, hoidla ja tee esimene varundus:

```bash
sudo chmod 700 /usr/local/sbin/varunda-debian1
openssl rand -base64 24 | sudo tee /root/.restic-parool > /dev/null
sudo chmod 600 /root/.restic-parool
sudo mkdir -p /srv/varundus
sudo env RESTIC_REPOSITORY=/srv/varundus/restic RESTIC_PASSWORD_FILE=/root/.restic-parool restic init
sudo /usr/local/sbin/varunda-debian1
```

**6.3** Ajasta varundus systemd taimeriga iga päev kell 02:00 (moodul 9). Kontrolli `systemctl list-timers`.

> **K8.** Miks varundatakse andmebaas `mariadb-dump`-iga, mitte kataloogi `/var/lib/mysql` kopeerides? Miks varundatakse ka `/root/ca`?

**6.4** **Katastroof!** Simuleeri õnnetust:

```bash
sudo mariadb -e "DROP TABLE kool.opilased;"
sudo rm -rf /var/www/kool
curl -k https://kool.lab.example/opilased.php
```

**6.5** Taasta:

```bash
export RESTIC_REPOSITORY=/srv/varundus/restic RESTIC_PASSWORD_FILE=/root/.restic-parool
sudo -E restic snapshots
sudo -E restic ls latest /var/www/kool
sudo -E restic restore latest --target /tmp/taaste --include /var/www/kool --include /var/backups/mariadb
ls -R /tmp/taaste | head -20
sudo cp -a /tmp/taaste/var/www/kool /var/www/
sudo mariadb < /tmp/taaste/var/backups/mariadb/koik.sql
curl https://kool.lab.example/opilased.php
```

> **K9.** Kas kõik taastus? Kui kaua taastamine aega võttis? Mis oleks juhtunud, kui varundus oleks tehtud samale kettale ja ketas oleks riknenud?

> **K10.** Kuidas vastab sinu varundus 3-2-1 reeglile? Mis on puudu ja kuidas seda parandada? (Vihje: restic toetab SFTP-hoidlat - Ubuntu masin võiks olla varuserver.)


---

## 7. osa. Dokumentatsioon

**7.1** Kirjuta serveri dokumentatsioon faili `/root/SERVER.md` Markdownis. Kasuta allolevat malli ja täida kõik osad.

```markdown
# debian1 - kooli väikeserver

## Üldinfo
- Eesmärk:
- Asukoht (Proxmoxi sõlm / VM ID):
- IP-aadress, DNS-nimed:
- OS ja versioon:
- Vastutaja:

## Teenused
| Teenus | Pakett | Port | Seadistus | Märkused |
|---|---|---|---|---|

## Veebisaidid
## DNS-tsoon
## Failijagamised
## Printerid
## Andmebaasid ja kasutajad
## Sertifikaadid (kehtivus!)
## Tulemüür
## Varundus
- Mida, kuhu, millal:
- Kuidas taastada (sammud):
- Viimane taastamistest:

## Muudatuste logi
| Kuupäev | Muudatus | Tegija |
|---|---|---|
```

> **K11.** Millal aeguvad sinu serveri ja CA sertifikaadid? Kuidas tagaksid, et keegi märkab enne aegumist?

> **K12.** Kirjuta loetelu kõigist portidest, mis sinu serveris on avatud, ja millise teenuse jaoks. Millised neist peaksid olema kättesaadavad kogu sisevõrgule ja millised ainult kindlatele masinatele?

> **K13.** Kui server tuleks homme nullist uuesti üles ehitada, millised sammud oleksid kõige aeganõudvamad? Kuidas saaks seda kiirendada? (See on hea sissejuhatus moodulisse 20.)


---

## Lisaülesanne (valikuline)

1. **Tulemüür:** seadista serverisse `nftables` nii, et avatud on ainult SSH, HTTP/HTTPS, DNS, NFS ja Samba ning NFS ja Samba ainult laborivõrgule.
2. **Kaugvarundus:** seadista restic varundama `debian2` masinasse SFTP kaudu (`sftp:varu@debian2:/srv/restic`) eraldi kasutajaga, kellel on ainult SSH-võtmega ligipääs (moodul 9).
3. **TrueNAS:** loo Proxmoxis VM (2 vCPU, 8 GiB RAM, süsteemiketas 16 GiB ja kolm 10 GiB andmeketast), paigalda TrueNAS Community Edition ja:
    - loo andmeketastest RAIDZ1 pool ja selles dataset'id `kool` (SMB) ja `linux` (NFS);
    - loo kasutaja `mari`, jaga `kool` SMB-ga (luba hetktõmmiste näitamine) ja `linux` NFS-iga ainult laborivõrgule;
    - haagi jagamised Windowsis ja Ubuntus nagu 2. ja 3. osas;
    - seadista igatunnine hetktõmmis, kustuta Windowsis fail ja taasta see *Previous Versions* kaudu;
    - eemalda VM-ilt üks andmeketas, vaata pooli olekut (*Degraded*) ja lisa uus ketas asemele.

    Võrdle: mis oli TrueNASis lihtsam ja mis keerulisem kui käsitsi seadistatud Debianis? Mida näitab TrueNASi shellis `zpool status` ja `zfs list -t snapshot`?

4. **Kodukataloogid autofs-iga:** jaga serverist `/srv/kodu` ja seadista kliendis autofs metamärgiga (`* -rw,sync debian1:/srv/kodu/&`), nii et iga kasutaja kodukataloog haagitakse failiserverist.
5. **AlmaLinux ja SELinux:** korda 3. osa Samba jagamine AlmaLinuxis. Mis veateate saad enne `samba_share_t` konteksti lisamist ja kust selle põhjuse leiad (`ausearch -m AVC -ts recent`)?

---

<!-- kysimused -->
## Aruande küsimused

Kõik selle laboritöö küsimused ühes kohas. Sulgudes on punkt, mille juures küsimust küsitakse. Kopeeri loend oma aruande alguseks ja kirjuta vastus iga küsimuse alla. Kus küsitakse käsku, kirjuta üles kogu käsk.

- **K1.** *(punkt 1.2)* Kas tavakasutaja sai faili luua? Mis juhtus juurkasutajana (`sudo touch`)? Miks? (Vihje: `root_squash`.)
- **K2.** *(punkt 1.3)* Mis numbriline omanik (UID) on kliendis loodud failidel serveris? Kas see vastab serveris samale kasutajale? Miks võib see olla probleem?
- **K3.** *(punkt 2.2)* Mida näitas `ls /mnt/kool` enne jagatud kataloogi avamist? Kas jagamine oli pärast 70 sekundit veel haagitud? Miks on autofs parem kui fstab-rida, kui failiserver võib alglaadimise ajal maas olla?
- **K4.** *(punkt 3.3)* Millised olid Windowsist loodud faili õigused ja grupp serveris? Millised `smb.conf` valikud seda mõjutasid?
- **K5.** *(punkt 4.3)* Millised olid Aini loodud faili grupp ja ACL? Kas Kati sai faili muuta? Kuhu sattus kustutatud fail? Mis juhtuks ilma vaikimisi ACL-ita, kui Aini `umask` on `022`?
- **K6.** *(punkt 5.3)* Kuhu tekkis kliendist prinditud PDF-fail ja kelle nimel? Mida näitab serveris fail `/var/log/cups/page_log` (või `access_log`)? Miks on see haldurile kasulik?
- **K7.** *(punkt 5.4)* Mida näitas `lpstat -o` peatatud järjekorra ajal? Mis sai tühistamata tööst pärast `cupsenable`-t? Too kolm põhjust, miks kasutada prindiserverit, selle asemel et iga arvuti prindiks otse printerisse.
- **K8.** *(punkt 6.3)* Miks varundatakse andmebaas `mariadb-dump`-iga, mitte kataloogi `/var/lib/mysql` kopeerides? Miks varundatakse ka `/root/ca`?
- **K9.** *(punkt 6.5)* Kas kõik taastus? Kui kaua taastamine aega võttis? Mis oleks juhtunud, kui varundus oleks tehtud samale kettale ja ketas oleks riknenud?
- **K10.** *(punkt 6.5)* Kuidas vastab sinu varundus 3-2-1 reeglile? Mis on puudu ja kuidas seda parandada? (Vihje: restic toetab SFTP-hoidlat - Ubuntu masin võiks olla varuserver.)
- **K11.** *(punkt 7.1)* Millal aeguvad sinu serveri ja CA sertifikaadid? Kuidas tagaksid, et keegi märkab enne aegumist?
- **K12.** *(punkt 7.1)* Kirjuta loetelu kõigist portidest, mis sinu serveris on avatud, ja millise teenuse jaoks. Millised neist peaksid olema kättesaadavad kogu sisevõrgule ja millised ainult kindlatele masinatele?
- **K13.** *(punkt 7.1)* Kui server tuleks homme nullist uuesti üles ehitada, millised sammud oleksid kõige aeganõudvamad? Kuidas saaks seda kiirendada? (See on hea sissejuhatus moodulisse 20.)
<!-- /kysimused -->

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 19. Faili- ja prindiserverid](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 19. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
