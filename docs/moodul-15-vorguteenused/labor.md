# Laboritöö 15. Kooli väikeserver, III osa: DNS, failid, e-post ja varundus

| | |
|---|---|
| **Distro** | Debian (laboritööde 13 ja 14 server `debian1`), klient Ubuntu |
| **Kestus** | 3 × 90 minutit |
| **Vajalik** | Laboritööde 13 ja 14 server ja Ubuntu klient, oma arvuti Windowsi failihalduriga |
| **Eesmärk** | Lisada serverile sisevõrgu DNS, failijagamine Linuxile ja Windowsile, e-posti teavitused ja varundus ning dokumenteerida server |

**Aruanne:** vasta küsimustele **K1–K13** ja esita 6. osas koostatud serveri dokumentatsioon.

Tähised on samad mis laboritöös 13 (`SERVER_IP`, `KLIENT_IP`, `VORK`, `lab.example`).

---

## 0. osa. Ettevalmistus

```bash
sudo apt install bind9 bind9-dnsutils nfs-kernel-server samba restic
```

Eemalda pärast 1. osa Ubuntu kliendi `/etc/hosts` failist laboritöös 13 lisatud rida - nüüd lahendab nimed sinu DNS-server.

---

## 1. osa. DNS-server

**1.1** Loo tsoon `lab.example` (vt teooria punkt 15.1). Lisa kirjed:

| Nimi | Tüüp | Väärtus |
|---|---|---|
| `ns1` | A | `SERVER_IP` |
| `debian1` | A | `SERVER_IP` |
| `kool` | A | `SERVER_IP` |
| `info` | CNAME | `kool` |
| `www` | CNAME | `kool` |
| `klient` | A | `KLIENT_IP` |

**1.2** Kontrolli ja rakenda:

```bash
sudo named-checkconf
sudo named-checkzone lab.example /etc/bind/db.lab.example
sudo systemctl reload named
dig @localhost kool.lab.example +short
dig @localhost info.lab.example
dig @localhost www.debian.org +short
```

**K1.** Mida näitab `dig` väljundis `info.lab.example` kohta (sektsioon `ANSWER`)? Kas server lahendab ka internetinimesid? Miks?

**1.3** Seadista **Ubuntu klient** kasutama sinu DNS-serverit (ajutiselt, kuni taaskäivituseni):

```bash
sudo resolvectl dns <liides> SERVER_IP
sudo resolvectl domain <liides> lab.example
resolvectl status <liides>
dig kool.lab.example +short
ping -c2 kool
curl http://info.lab.example
```

**1.4** Lisa tsooni uus kirje `test IN A 192.0.2.10`, **suurenda seerianumbrit**, kontrolli ja laadi uuesti. Kontrolli Ubuntust: `dig test.lab.example +short`.

**K2.** Mis juhtub, kui muudad tsoonifaili, kuid seerianumbrit ei suurenda? (Ühe serveriga laboris töötab see sageli ikkagi - miks on seerianumber siiski oluline?)


---

## 2. osa. NFS

**2.1** Seadista serveris NFS-jagamine `/srv/nfs/jagatud` ainult oma laborivõrgule (lugemis- ja kirjutusõigusega). Pane sinna testfail.

```bash
sudo mkdir -p /srv/nfs/jagatud
echo "NFS töötab" | sudo tee /srv/nfs/jagatud/tere.txt
sudo nano /etc/exports
sudo exportfs -ra
sudo exportfs -v
```

**2.2** Haagi jagamine Ubuntu kliendis:

```bash
sudo apt install nfs-common
showmount -e debian1.lab.example
sudo mkdir -p /mnt/nfs
sudo mount -t nfs debian1.lab.example:/srv/nfs/jagatud /mnt/nfs
cat /mnt/nfs/tere.txt
touch /mnt/nfs/klient.txt
sudo touch /mnt/nfs/root.txt
```

**K3.** Kas tavakasutaja sai faili luua? Mis juhtus juurkasutajana (`sudo touch`)? Miks? (Vihje: `root_squash`.)

**2.3** Muuda serveris jagatud kataloogi õigusi nii, et kõik saavad sinna kirjutada (`sudo chmod 1777 /srv/nfs/jagatud`), ja korda kliendis faili loomist. Vaata serveris failide omanikke (`ls -ln /srv/nfs/jagatud`).

**K4.** Mis numbriline omanik (UID) on kliendis loodud failidel serveris? Kas see vastab serveris samale kasutajale? Miks võib see olla probleem?

**2.4** Lisa haakimine kliendi faili `/etc/fstab` (vt teooria punkt 15.2) ja kontrolli `sudo mount -a`.


---

## 3. osa. Samba

**3.1** Loo serveris Samba jagamine `jagatud` grupile `smbkasutajad` (vt teooria punkt 15.2). Lisa oma kasutaja gruppi ja määra Samba parool.

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

**K5.** Millised olid Windowsist loodud faili õigused ja grupp serveris? Millised `smb.conf` valikud seda mõjutasid?


---

## 4. osa. E-posti teavitused (Postfix)

**4.1** Paigalda Postfix kohaliku kohaletoimetamisega (*Local only*; kui õpetaja annab SMTP-relee andmed, vali *Satellite system* ja seadista relee teooria punkti 15.3 järgi):

```bash
sudo apt install postfix mailutils
sudo postconf myhostname inet_interfaces
sudo ss -tlpn | grep :25
```

**4.2** Saada kiri ja loe seda:

```bash
echo "Varundus õnnestus" | mail -s "debian1 test" $USER
mail                        # q - välju
sudo journalctl -u postfix -n 20 --no-pager
```

**4.3** Suuna juurkasutaja kirjad oma kasutajale (`/etc/aliases`: `root: <kasutaja>`, siis `sudo newaliases`) ja testi: `echo test | sudo mail -s "root-ile" root`.

**K6.** Millisel aadressil Postfix kuulab (`inet_interfaces`) ja miks ei tohi server võtta kirju vastu kogu võrgust?

**K7.** Milliseid serveri teateid tasuks e-postiga saada? Kuidas saaksid 5. osa varundusskripti vea korral teavituse (vihje: systemd `OnFailure=` või skriptis `|| mail ...`)?

---

## 5. osa. Varundus ja taastamine

**5.1** Loo varundusskript `/usr/local/sbin/varunda-debian1`:

```bash
#!/bin/bash
# debian1 igaöine varundus: andmebaas + seadistus + andmed → restic
set -euo pipefail

export RESTIC_REPOSITORY=/srv/varundus/restic
export RESTIC_PASSWORD_FILE=/root/.restic-parool
DUMPID=/var/backups/mariadb

mkdir -p "$DUMPID"
mariadb-dump --all-databases --single-transaction > "$DUMPID/koik.sql"

restic backup --tag igaoine /etc /var/www /srv/nfs /srv/samba "$DUMPID" /root/ca
restic forget --tag igaoine --keep-daily 7 --keep-weekly 4 --prune
restic check
```

**5.2** Loo parool, hoidla ja tee esimene varundus:

```bash
sudo chmod 700 /usr/local/sbin/varunda-debian1
openssl rand -base64 24 | sudo tee /root/.restic-parool > /dev/null
sudo chmod 600 /root/.restic-parool
sudo mkdir -p /srv/varundus
sudo env RESTIC_REPOSITORY=/srv/varundus/restic RESTIC_PASSWORD_FILE=/root/.restic-parool restic init
sudo /usr/local/sbin/varunda-debian1
```

**5.3** Ajasta varundus systemd taimeriga iga päev kell 02:00 (vt moodul 5). Kontrolli `systemctl list-timers`.

**K8.** Miks varundatakse andmebaas `mariadb-dump`-iga, mitte kataloogi `/var/lib/mysql` kopeerides? Miks varundatakse ka `/root/ca`?

**5.4** **Katastroof!** Simuleeri õnnetust:

```bash
sudo mariadb -e "DROP TABLE kool.opilased;"
sudo rm -rf /var/www/kool
curl -k https://kool.lab.example/opilased.php
```

**5.5** Taasta:

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

**K9.** Kas kõik taastus? Kui kaua taastamine aega võttis? Mis oleks juhtunud, kui varundus oleks tehtud samale kettale ja ketas oleks riknenud?

**K10.** Kuidas vastab sinu varundus 3-2-1 reeglile? Mis on puudu ja kuidas seda parandada? (Vihje: restic toetab SFTP-hoidlat - Ubuntu masin võiks olla varuserver.)


---

## 6. osa. Dokumentatsioon

**6.1** Kirjuta serveri dokumentatsioon faili `/root/SERVER.md` Markdownis. Kasuta allolevat malli ja täida kõik osad.

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

**K11.** Millal aeguvad sinu serveri ja CA sertifikaadid? Kuidas tagaksid, et keegi märkab enne aegumist?

**K12.** Kirjuta loetelu kõigist portidest, mis sinu serveris on avatud, ja millise teenuse jaoks. Millised neist peaksid olema kättesaadavad kogu sisevõrgule ja millised ainult kindlatele masinatele?

**K13.** Kui server tuleks homme nullist uuesti üles ehitada, millised sammud oleksid kõige aeganõudvamad? Kuidas saaks seda kiirendada? (See on hea sissejuhatus moodulisse 16.)


---

## Lisaülesanne (valikuline)

1. **Tulemüür:** seadista serverisse `nftables` nii, et avatud on ainult SSH, HTTP/HTTPS, DNS, NFS ja Samba ning NFS ja Samba ainult laborivõrgule.
2. **Kaugvarundus:** seadista restic varundama Ubuntu masinasse SFTP kaudu (`sftp:varu@KLIENT_IP:/srv/restic`) eraldi kasutajaga, kellel on ainult SSH-võtmega ligipääs.
3. **TrueNAS:** loo Proxmoxis VM (2 vCPU, 8 GiB RAM, süsteemiketas 16 GiB ja kolm 10 GiB andmeketast), paigalda TrueNAS Community Edition ja:
    - loo andmeketastest RAIDZ1 pool ja selles dataset'id `kool` (SMB) ja `linux` (NFS);
    - loo kasutaja `mari`, jaga `kool` SMB-ga (luba hetktõmmiste näitamine) ja `linux` NFS-iga ainult laborivõrgule;
    - haagi jagamised Windowsis ja Ubuntus nagu 2. ja 3. osas;
    - seadista igatunnine hetktõmmis, kustuta Windowsis fail ja taasta see *Previous Versions* kaudu;
    - eemalda VM-ilt üks andmeketas, vaata pooli olekut (*Degraded*) ja lisa uus ketas asemele.

    Võrdle: mis oli TrueNASis lihtsam ja mis keerulisem kui käsitsi seadistatud Debianis? Mida näitab TrueNASi shellis `zpool status` ja `zfs list -t snapshot`?

4. **Päris relee:** seadista Postfix saatma kirju päris SMTP-serveri kaudu (nt kooli või oma e-posti pakkuja rakenduse parooliga) ja saada varundusskripti tulemus oma postkasti.
5. **autofs:** asenda Ubuntu kliendis 2. osa fstab-i NFS-rida autofs-iga (teooria punkt 15.2) ja kontrolli, et jagamine haagitakse alles kataloogi avamisel ning haagitakse lahti pärast `--timeout` aega.

---

# Laboritöö 15B. Teised DNS-serverid: Pi-hole ja CoreDNS (Ubuntu)

| | |
|---|---|
| **Distro** | Ubuntu |
| **Kestus** | 2 × 90 minutit |
| **Vajalik** | Laboritöö 15 Debiani server BIND9-ga, laboritöö 7 Ubuntu masin (või eraldi Ubuntu VM, nt `ubuntusrv` Dockeriga), 2. osa jaoks Docker või Podman |
| **Eesmärk** | Paigaldada filtreeriv DNS-server ja kasutada sama tsooni CoreDNS-iga |

**Aruanne:** vasta küsimustele **D1–D10**.

## 1. osa. Pi-hole

**1.1** Kontrolli, mis Ubuntus pordil 53 juba kuulab:

```bash
sudo ss -tulpn | grep ':53 '
resolvectl status | head -20
```

**D1.** Milline protsess kuulab pordil 53 ja millisel aadressil? Miks see võib Pi-hole'iga konflikti minna?

**1.2** Lülita `systemd-resolved` kohalik kuulaja välja (teooria punkt 15.1, dnsmasq-i märkus) ja seadista masin ise kasutama ajutiselt välist DNS-i:

```bash
sudo mkdir -p /etc/systemd/resolved.conf.d
printf '[Resolve]\nDNSStubListener=no\n' | sudo tee /etc/systemd/resolved.conf.d/pihole.conf
sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf
sudo systemctl restart systemd-resolved
sudo ss -tulpn | grep ':53 '
```

**1.3** Laadi alla Pi-hole'i paigaldusskript, **loe see läbi** ja käivita. Vali ülemiseks DNS-iks nt Quad9, liides `ens18` (või sinu liides), luba veebiliides ja päringute logi. Määra veebiliidese parool:

```bash
curl -sSL https://install.pi-hole.net -o basic-install.sh
less basic-install.sh
sudo bash basic-install.sh
sudo pihole setpassword
sudo ufw allow from VORK to any port 53
sudo ufw allow from VORK to any port 80 proto tcp
```

**D2.** Mida skript tegi (paketid, teenused, failid)? Miks on parem skript enne käivitamist läbi lugeda kui kasutada `curl ... | sudo bash`?

**1.4** Testi teisest masinast (nt Debianist):

```bash
dig @PIHOLE_IP www.debian.org +short
dig @PIHOLE_IP doubleclick.net +short
dig @PIHOLE_IP ads.google.com +short
```

**D3.** Mida vastas Pi-hole blokeeritud domeenidele? Mitu domeeni on blokeerimisloendis (veebiliides → *Dashboard* või `pihole status`)?

**1.5** Ava veebiliides `http://PIHOLE_IP/admin`. Lisa:

- kohalik DNS-kirje `pihole.lab.example → PIHOLE_IP` (*Local DNS*);
- oma blokeeritav domeen (nt `example.org`) ja kontrolli `dig`-iga;
- lubatud domeen (*allowlist*) mõnele blokeeritud domeenile ja kontrolli uuesti;
- suunamine: domeeni `lab.example` päringud saadetakse laboritöö 15 BIND9 serverile (Pi-hole'i v6 seadetes *Conditional forwarding* või *All settings* → `misc.dnsmasq_lines` reaga `server=/lab.example/SERVER_IP`).

```bash
dig @PIHOLE_IP kool.lab.example +short
pihole -q example.org
```

**D4.** Kas `kool.lab.example` lahenes Pi-hole'i kaudu? Kirjelda päringu teekonda: klient → ? → ?

**1.6** Seadista Debiani server kasutama DNS-ina Pi-hole'i ja ava Debianis mõni veebileht `curl`-iga. Vaata veebiliidese *Query Log*-i.

**D5.** Milliseid päringuid Debian tegi? Mis on Pi-hole'i eelised ja puudused võrreldes brauseri reklaamiblokeerijaga? Milline privaatsusküsimus kaasneb päringute logiga?

## 2. osa. CoreDNS konteineris

Kasuta moodulis 12 õpitud Compose'i. Pi-hole'i ja CoreDNS-i korraga samal pordil käivitada ei saa - kasuta teist VM-i või peata Pi-hole (`sudo systemctl stop pihole-FTL`).

**2.1** Loo kataloog ja kopeeri sinna laboritöö 15 BIND9 tsoonifail:

```bash
mkdir -p ~/coredns/zones && cd ~/coredns
scp kasutaja@SERVER_IP:/etc/bind/db.lab.example zones/
```

**2.2** Loo `Corefile` (teooria punkt 15.1): tsoon `lab.example` failist ja kõik muu edasi `1.1.1.1`-le. Loo `compose.yaml` ja käivita:

```bash
docker compose up -d          # või: podman compose up -d
docker compose logs -f
dig @localhost kool.lab.example +short
dig @localhost www.debian.org +short
```

**D6.** Kas CoreDNS vastas mõlemale päringule? Millised read tekkisid logis (`log` pistikprogramm)?

**2.3** Lisa tsoonifaili uus kirje `test IN A 10.0.83.60`, **suurenda seerianumbrit** ja oota ~1 minut ilma konteinerit taaskäivitamata:

```bash
dig @localhost test.lab.example +short
```

**D7.** Kas uus kirje ilmus ilma taaskäivituseta? Mis juhtub, kui seerianumbrit ei suurenda?

**2.4** Pane `Corefile`, `compose.yaml` ja `zones/` Giti hoidlasse. Kirjuta skript `uuenda.sh`, mis teeb `git pull` ja mille käivitab systemd taimer (moodul 5) iga 5 minuti järel. Muuda kirjet teises masinas, `push`-i ja kontrolli, et CoreDNS-i vastus muutus.

**D8.** Kuidas tagab selline lahendus, et kaks DNS-serverit annavad sama vastuse? Mis on selle eelis ja puudus võrreldes BIND9 primaar-sekundaar tsooniülekandega (AXFR)?

## 3. osa. Kokkuvõte

**D9.** Täida tabel: BIND9, dnsmasq, CoreDNS, Pi-hole - kas autoriteetne, kas rekursiivne/edastav, seadistuse vorm, kus sa seda kasutaksid?

**D10.** Kool tahab laborivõrgule sisevõrgu nimesid ja reklaamide blokeerimist. Kirjelda arhitektuur, kasutades selle laboritöö teenuseid.

---

## Õpetajale: kontrollvastused

### 15

| Küsimus | Vastus |
|---|---|
| K1 | CNAME `info → kool.lab.example.` ja seejärel A-kirje; rekursioon on Debiani vaikimisi lubatud kohalikule võrgule |
| K2 | Teised (sekundaarsed) serverid ja vahemälud ei saa muudatusest teada; seerianumber on tsooni versioon |
| K3 | Tavakasutaja jah (kui õigused lubavad); `sudo touch` ebaõnnestus (`Permission denied`), sest kliendi root muudetakse serveris kasutajaks `nobody` |
| K4 | Kliendi kasutaja UID (nt 1000); serveris võib see olla teine kasutaja - UID-d peavad klappima (LDAP/AD) |
| K5 | Õigused `create mask = 0660`, grupp kataloogi SGID-i tõttu `smbkasutajad` |
| K6 | `loopback-only` (127.0.0.1:25); avatud relee'd kasutatakse rämpsposti saatmiseks ja server satub mustadesse nimekirjadesse |
| K7 | Varunduse tulemus, kettaruumi ja SMART-i hoiatused, turvauuendused, cron'i vead, sertifikaatide aegumine; `OnFailure=teavitus@%n.service` või `varunda-debian1 || mail -s ...` |
| K8 | Töötava andmebaasi failid võivad olla ebajärjepidevad; CA võti on vajalik uute sertifikaatide väljaandmiseks |
| K9 | Varukoopia samal kettal kaob koos kettaga |
| K10 | 3 koopiat? Ei - originaal ja üks varukoopia samal masinal. Vaja on koopiat teises masinas/asukohas |
| K11 | `openssl x509 -enddate -noout -in kool.crt`; jälgimissüsteem (nt Zabbix, Uptime Kuma) või skript taimeriga, mis hoiatab 30 päeva enne |
| K13 | Seadistuste käsitsi taastamine; kiirendamine: seadistus Gitis ja automatiseeritud (Ansible), konteinerid |

### 15B

| Küsimus | Vastus |
|---|---|
| D1 | `systemd-resolved` aadressil `127.0.0.53` (ja `127.0.0.54`); Pi-hole tahab kuulata pordil 53 kõigil liidestel |
| D2 | Paigaldab `pihole-FTL` (dnsmasq-il põhinev DNS + veebiserver), seadistuse `/etc/pihole/`, blokeerimisloendid (gravity), teenuse ja `pihole` käsu; skript töötab juurkasutajana, seega peab teadma, mida see teeb |
| D3 | `0.0.0.0` (või `::`) - blokeeritud; loendis tavaliselt sadu tuhandeid domeene |
| D4 | klient → Pi-hole → BIND9 (`lab.example`); muud päringud Pi-hole → ülemine DNS |
| D5 | Kogu võrgu kaitse, ka seadmetel ilma blokeerijata; ei näe URL-i ega sisu (YouTube'i reklaamid), DoH möödub; logist näeb, milliseid saite iga masin külastab - juurdepääs logile tuleb piirata |
| D6 | Jah; logiridadel päringu tüüp, nimi, vastuskood (`NOERROR`) ja kestus |
| D7 | Jah, `file` pistikprogramm loeb faili uuesti, kui seerianumber suurenes; muidu muudatust ei rakendata |
| D8 | Mõlemad tõmbavad sama Giti versiooni; eelis: ajalugu, ülevaatus, lihtne; puudus: viivitus kuni taimeri intervall, sõltub Giti serveri kättesaadavusest, pole DNS-i standardset NOTIFY-mehhanismi |
| D10 | Nt Pi-hole (või kaks) klientidele DNS-iks, mis suunab `lab.example` päringud CoreDNS-ile/BIND9-le; DHCP jagab Pi-hole'i aadressi; tsoonid Gitis |

> **Märkus õpetajale:** teenuste seadistused põhinevad Debiani standardpakettidel; kontrolli BIND9 versiooni (`type primary` vajab BIND 9.16+, vanemates `type master`). Postfixi, Pi-hole'i (v6) veebiliidese menüüde nimesid ja CoreDNS-i osa ei ole testitud.
