<!-- navigatsioon -->
[← Moodul 25. FreeBSD server](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 25. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 25. FreeBSD server

| | |
|---|---|
| **Distro** | FreeBSD 15 (viimane *RELEASE*) |
| **Kestus** | 4 × 90 minutit |
| **Vajalik** | FreeBSD VM `fbsd` (2 vCPU, 2 GiB RAM, 20 GiB ketas, VirtIO võrk), aadressid `10.0.83.66` (host) ja `10.0.83.67` (jail). Linuxi klient testimiseks (nt `ubuntuklient`) |
| **Eesmärk** | Paigaldada ja hallata FreeBSD serverit: paketid ja uuendused, teenused, kasutajad, võrk, ZFS-i alglaadimiskeskkonnad, pf ja jail |

> **Aruanne:** vasta küsimustele **K1–K12**. Kõik küsimused on koos ka lehe lõpus ([Aruande küsimused](#aruande-küsimused)).

> [!NOTE]
> **HKHK laboris** võib õpetaja anda valmis FreeBSD malli - siis alusta 2. osast. Iseõppijale sobib ka VirtualBox (võrguliides on siis `em0`, mitte `vtnet0`).

---

## 1. osa. Paigaldus

**1.1** Loo Proxmoxis VM (tüüp *Other*, VirtIO SCSI ketas, VirtIO võrk) ja paigalda FreeBSD teooria punkti 25.2 järgi: hostinimi `fbsd.lab.example`, **Auto (ZFS)**, DHCP, ajavöönd Estonia, teenused `sshd` ja `ntpd`, tavakasutaja lisagrupiga `wheel`.

**1.2** Pärast taaskäivitust ühendu SSH-ga tavakasutajana ja saa juurkasutajaks:

```sh
ssh kasutaja@<fbsd-aadress>
su -
```

> **K1.** Mitu sammu oli paigaldajas võrreldes Debiani paigaldajaga? Mis juhtub, kui proovid `su -` kasutajaga, kes ei ole grupis `wheel`?

---

## 2. osa. Süsteemiga tutvumine

**2.1**

```sh
freebsd-version -kru
uname -a
sysctl hw.model hw.ncpu hw.physmem
geom disk list
gpart show
zpool status
zfs list
echo $SHELL
```

**2.2** Proovi GNU ja BSD tööriistade erinevust:

```sh
ls --color          # mis juhtub?
ls -G
printf 'tere\n' > /tmp/proov.txt
sed -i 's/tere/head aega/' /tmp/proov.txt   # mis juhtub?
sed -i '' 's/tere/head aega/' /tmp/proov.txt
cat /tmp/proov.txt
man sed             # otsi -i kirjeldus
```

> **K2.** Milline on FreeBSD ja kerneli versioon? Millised ZFS-i andmekogumid paigaldaja lõi? Miks ebaõnnestus `sed -i` ilma tühja argumendita ja mida see sulle skriptide kirjutamise kohta ütleb?

---

## 3. osa. Paketid ja uuendused

**3.1** Uuenda baassüsteem ja paigalda paketid:

```sh
freebsd-update fetch
freebsd-update install
pkg bootstrap -y
pkg update
pkg install -y bash doas tmux nginx
pkg info | wc -l
pkg info -l nginx | head
pkg which /usr/local/sbin/nginx
pkg audit -F
which bash
```

> **K3.** Kas `freebsd-update` leidis uuendusi? Kus asuvad `bash` ja nginx-i seadistusfail? Miks just seal, mitte `/bin` ja `/etc` all? Kas `pkg audit` leidis haavatavusi?

---

## 4. osa. Kasutajad ja halduriõigused

**4.1** Loo grupp ja kasutajad:

```sh
pw groupadd opetajad -g 4000
pw useradd anna -m -s /bin/sh -G opetajad -c "Anna Kask"
pw useradd peeter -m -s /usr/local/bin/bash -c "Peeter Puu"
passwd anna
passwd peeter
pw groupmod opetajad -m peeter
id anna; id peeter
```

**4.2** Seadista `doas` grupile `wheel` ja lisa sinna `anna`:

```sh
echo 'permit persist :wheel' > /usr/local/etc/doas.conf
pw groupmod wheel -m anna
```

Logi teises terminalis sisse kasutajana `anna` ja proovi `doas pkg info nginx` ning `su -`.

> **K4.** Mis vahe on `pw usermod anna -G grupp` ja `pw groupmod grupp -m anna` vahel? Kus on FreeBSD-s parooliräsid (võrdle Linuxi `/etc/shadow`-ga)? Miks on `peeter`-i kest `/usr/local/bin/bash`, mitte `/bin/bash`?

---

## 5. osa. Teenused ja logid

**5.1** Käivita nginx ja muuda avaleht:

```sh
sysrc nginx_enable=YES
service nginx start
service nginx status
sockstat -4l | grep nginx
echo '<h1>FreeBSD jail-ita</h1>' > /usr/local/www/nginx/index.html
fetch -qo - http://localhost/
service -e
```

**5.2** Uuri logisid ja periodic aruandeid:

```sh
tail -20 /var/log/messages
tail /var/log/auth.log
ls /etc/periodic/daily | head
periodic daily
less /var/mail/root
```

> **K5.** Millises failis on nginx-i lubamise seade ja mis rida `sysrc` sinna kirjutas? Mida sisaldas igapäevane `periodic` aruanne? Kuidas teeksid sama Linuxis (systemd)?

---

## 6. osa. Staatiline aadress

**6.1** **Proxmoxi konsoolis** (mitte SSH-s):

```sh
sysrc ifconfig_vtnet0="inet 10.0.83.66/24"
sysrc defaultrouter="10.0.83.1"
echo "nameserver 10.0.83.1" > /etc/resolv.conf
service netif restart && service routing restart
ifconfig vtnet0
netstat -rn
host www.freebsd.org
```

Ühendu uue aadressiga SSH-ga.

> **K6.** Võrdle FreeBSD võrguseadistust Debiani (`/etc/network/interfaces`), Ubuntu (Netplan) ja AlmaLinuxi (`nmcli`) omaga (moodul 7). Mis on lihtsam, mis on keerulisem?

---

## 7. osa. ZFS ja alglaadimiskeskkonnad

**7.1** Hetktõmmis ja taastamine:

```sh
zfs snapshot zroot/usr/home@enne
rm -rf /home/anna/*                       # „kogemata“ kustutamine
ls -a /home/anna
ls /home/anna/.zfs/snapshot/enne/          # hetktõmmise sisu on näha
zfs rollback zroot/usr/home@enne
ls -a /home/anna
```

**7.2** Alglaadimiskeskkond:

```sh
bectl list
bectl create enne-katset
echo "katse" > /etc/katse-fail
pkg delete -y tmux                         # „vigane muudatus“
bectl activate enne-katset
shutdown -r now
```

Pärast taaskäivitust:

```sh
bectl list
ls /etc/katse-fail
which tmux
ls /home/anna
```

Vaata Proxmoxi konsoolis ka alglaadija menüüd (*Boot Environments*). Lõpuks aktiveeri soovi korral jälle `default` ja kustuta katsekeskkond (`bectl destroy`).

> **K7.** Mis juhtus failiga `/etc/katse-fail` ja paketiga `tmux` pärast vana keskkonna aktiveerimist? Miks ei mõjutanud see kodukataloogi? Kuidas aitab see põhiversiooni uuendamisel?

---

## 8. osa. Tulemüür pf

**8.1** Kirjuta `/etc/pf.conf` teooria punkti 25.10 näite järgi (haldusvõrk `10.0.83.0/24`). **Proxmoxi konsoolis:**

```sh
pfctl -nf /etc/pf.conf
sysrc pf_enable=YES pflog_enable=YES
service pf start
service pflog start
pfctl -sr
pfctl -si
```

**8.2** Testi Linuxi kliendist:

```sh
ssh kasutaja@10.0.83.66                    # peab töötama
curl -I http://10.0.83.66                  # peab töötama
for i in $(seq 1 8); do ssh -o ConnectTimeout=3 -o BatchMode=yes kasutaja@10.0.83.66 true; done
ssh kasutaja@10.0.83.66                    # kas töötab veel?
```

FreeBSD-s:

```sh
pfctl -t ryndajad -T show
tcpdump -n -e -ttt -i pflog0 &             # blokeeritud paketid (Ctrl+C / kill %1)
pfctl -t ryndajad -T delete <kliendi-IP>
```

> **K8.** Kas klient sattus tabelisse `<ryndajad>`? Pärast mitut ühendust? Mida tähendab pf-i reeglite juures „viimane sobiv reegel kehtib“ ja milleks on `quick`? Võrdle seda lahendust fail2ban-iga (moodul 11).

---

## 9. osa. Jail

**9.1** Hosti nginx kuulab praegu kõigil aadressidel, ka jailile antaval. Lase sel kuulata ainult hosti aadressil:

```sh
sed -i '' 's/listen[[:space:]]*80;/listen 10.0.83.66:80;/' /usr/local/etc/nginx/nginx.conf
nginx -t && service nginx restart
sockstat -4l | grep nginx
```

**9.2** Loo jail `www` teooria punkti 25.11 järgi (aadress `10.0.83.67`), käivita see ja paigalda sinna nginx (kui `pkg` küsib jailis enda paigaldamist, vasta `y`):

```sh
zfs create -o mountpoint=/usr/local/jails zroot/jails
zfs create zroot/jails/www
fetch https://download.freebsd.org/releases/amd64/$(freebsd-version -u | cut -d- -f1-2)/base.txz -o /tmp/base.txz
tar -xf /tmp/base.txz -C /usr/local/jails/www
cp /etc/resolv.conf /etc/localtime /usr/local/jails/www/etc/
# kirjuta /etc/jail.conf
sysrc jail_enable=YES jail_list="www"
service jail start www
jls
pkg -j www install -y nginx
sysrc -j www nginx_enable=YES
echo '<h1>Tere jailist</h1>' > /usr/local/jails/www/usr/local/www/nginx/index.html
service -j www nginx start
```

**9.3** Võrdle hosti ja jaili vaadet:

```sh
jexec www sh -c 'hostname; ps aux; ifconfig; id'
ps aux | grep nginx                        # hostis
sockstat -4l | grep nginx
zfs snapshot zroot/jails/www@puhas
```

Linuxi kliendist: `curl http://10.0.83.67` ja `curl http://10.0.83.66`. Lisa vajadusel pf-i reeglisse jaili aadress (reegel `to port { http, https }` kehtib kõigile hosti aadressidele).

> **K9.** Milliseid protsesse ja võrguliideseid nägi jail ja milliseid host? Mis on jaili ja Podmani konteineri (moodul 12) sarnasused ja erinevused?

> **K10.** Mitu megabaiti võttis jail (`zfs list zroot/jails/www`)? Kuidas saaksid hetktõmmisest kiiresti luua teise samasuguse jaili (vihje: `zfs clone`)?

---

## 10. osa. Kokkuvõte

> **K11.** Täida tabel kümne toimingu kohta: kuidas seda tehakse Debianis ja kuidas FreeBSD-s (paketid, uuendus, teenus, kasutaja gruppi, staatiline IP, kuulavad pordid, tulemüür, logid, isoleeritud teenus, tagasivõtt pärast uuendust).

> **K12.** Millises olukorras valiksid serverile FreeBSD ja millises Linuxi? Too vähemalt kaks argumenti mõlema kohta.

---

## Koristamine

`service jail stop www`, vajadusel `zfs destroy -r zroot/jails`. Kui VM-i enam ei vaja, kustuta see või tee hetktõmmis ja lülita välja.

---

## Lisaülesanne (valikuline)

1. **Bastille:** paigalda `bastille` (`pkg install bastille`), loo sellega jail ja paigalda sinna mõni teenus (nt `bastille create`, `bastille pkg`, `bastille service`). Võrdle käsitsi tehtud jailiga.
2. **Põhiversiooni uuendus:** kui on uuem *RELEASE*, uuenda `freebsd-update upgrade -r`-iga. Kontrolli enne ja pärast `bectl list`.
3. **Pordid:** paigalda mõni väike programm pordist (`git clone https://git.FreeBSD.org/ports.git /usr/ports`, `cd /usr/ports/sysutils/tree && make install clean`). Mida küsis `make config`?
4. **pkgbase:** paigalda teine FreeBSD VM, vali paigaldajas baassüsteem pakettidena ja võrdle uuendamist (`pkg upgrade`) traditsioonilisega.
5. **Ansible ja FreeBSD:** halda FreeBSD-d mooduli 16 Ansible'iga (`ansible_python_interpreter=/usr/local/bin/python3`, moodulid `community.general.pkgng` ja `community.general.sysrc`).

---

<!-- kysimused -->
## Aruande küsimused

Kõik selle laboritöö küsimused ühes kohas. Sulgudes on punkt, mille juures küsimust küsitakse. Kopeeri loend oma aruande alguseks ja kirjuta vastus iga küsimuse alla. Kus küsitakse käsku, kirjuta üles kogu käsk.

- **K1.** *(punkt 1.2)* Mitu sammu oli paigaldajas võrreldes Debiani paigaldajaga? Mis juhtub, kui proovid `su -` kasutajaga, kes ei ole grupis `wheel`?
- **K2.** *(punkt 2.2)* Milline on FreeBSD ja kerneli versioon? Millised ZFS-i andmekogumid paigaldaja lõi? Miks ebaõnnestus `sed -i` ilma tühja argumendita ja mida see sulle skriptide kirjutamise kohta ütleb?
- **K3.** *(punkt 3.1)* Kas `freebsd-update` leidis uuendusi? Kus asuvad `bash` ja nginx-i seadistusfail? Miks just seal, mitte `/bin` ja `/etc` all? Kas `pkg audit` leidis haavatavusi?
- **K4.** *(punkt 4.2)* Mis vahe on `pw usermod anna -G grupp` ja `pw groupmod grupp -m anna` vahel? Kus on FreeBSD-s parooliräsid (võrdle Linuxi `/etc/shadow`-ga)? Miks on `peeter`-i kest `/usr/local/bin/bash`, mitte `/bin/bash`?
- **K5.** *(punkt 5.2)* Millises failis on nginx-i lubamise seade ja mis rida `sysrc` sinna kirjutas? Mida sisaldas igapäevane `periodic` aruanne? Kuidas teeksid sama Linuxis (systemd)?
- **K6.** *(punkt 6.1)* Võrdle FreeBSD võrguseadistust Debiani (`/etc/network/interfaces`), Ubuntu (Netplan) ja AlmaLinuxi (`nmcli`) omaga (moodul 7). Mis on lihtsam, mis on keerulisem?
- **K7.** *(punkt 7.2)* Mis juhtus failiga `/etc/katse-fail` ja paketiga `tmux` pärast vana keskkonna aktiveerimist? Miks ei mõjutanud see kodukataloogi? Kuidas aitab see põhiversiooni uuendamisel?
- **K8.** *(punkt 8.2)* Kas klient sattus tabelisse `<ryndajad>`? Pärast mitut ühendust? Mida tähendab pf-i reeglite juures „viimane sobiv reegel kehtib“ ja milleks on `quick`? Võrdle seda lahendust fail2ban-iga (moodul 11).
- **K9.** *(punkt 9.3)* Milliseid protsesse ja võrguliideseid nägi jail ja milliseid host? Mis on jaili ja Podmani konteineri (moodul 12) sarnasused ja erinevused?
- **K10.** *(punkt 9.3)* Mitu megabaiti võttis jail (`zfs list zroot/jails/www`)? Kuidas saaksid hetktõmmisest kiiresti luua teise samasuguse jaili (vihje: `zfs clone`)?
- **K11.** *(10. osa)* Täida tabel kümne toimingu kohta: kuidas seda tehakse Debianis ja kuidas FreeBSD-s (paketid, uuendus, teenus, kasutaja gruppi, staatiline IP, kuulavad pordid, tulemüür, logid, isoleeritud teenus, tagasivõtt pärast uuendust).
- **K12.** *(10. osa)* Millises olukorras valiksid serverile FreeBSD ja millises Linuxi? Too vähemalt kaks argumenti mõlema kohta.
<!-- /kysimused -->

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 25. FreeBSD server](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 25. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
