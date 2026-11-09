# Laboritöö 7. Võrk, SSH ja tulemüür

| | |
|---|---|
| **Distro** | Ubuntu Server (LTS) |
| **Kestus** | 3 × 90 minutit |
| **Vajalik** | Ubuntu virtuaalmasin (põhimasin), teise masinana **Debiani virtuaalmasin** varasematest laboritest (samas võrgus), oma arvuti SSH kliendiga. Ligipääs Ubuntu masina **konsoolile** (nt Proxmoxi veebiliides) |
| **Eesmärk** | Harjutada võrgu diagnostikat ja seadistamist, SSH-võtmeid, SSH karastamist, failide sünkroniseerimist ja tulemüüri |

**Aruanne:** vasta küsimustele **K1–K20**.

> [!WARNING]
> **Turvavõrk:** selles laboris muudad võrgu- ja SSH-seadistust, mis võib katkestada sinu ühenduse. Hoia Ubuntu masina konsool brauseris avatuna. Kui midagi läheb valesti, saad konsooli kaudu parandada.

Laboris kasutatavad tähised - asenda need oma väärtustega:

| Tähis | Tähendus |
|---|---|
| `UBUNTU_IP` | Ubuntu masina IP-aadress |
| `DEBIAN_IP` | Debiani masina IP-aadress |
| `LISA_IP` | Lisa-aadress Ubuntu masinale, mille annab õpetaja (iseõppija: vali oma võrgust vaba aadress) |
| `kasutaja` | Sinu kasutajanimi |

---

## 1. osa. Võrguseadistuse uurimine (Ubuntu)

**1.1** Uuri liideseid, aadresse ja marsruute:

```bash
ip -br address
ip address show
ip route
ip neigh
```

**K1.** Mis on Ubuntu masina võrguliidese nimi, IP-aadress ja võrgumask? Mis on vaikelüüs? Mitu masinat on võrgus `/24` maski korral võimalik aadresseerida?

**1.2** Uuri DNS-i seadistust:

```bash
cat /etc/resolv.conf
resolvectl status
cat /etc/nsswitch.conf | grep hosts
```

**K2.** Miks on failis `/etc/resolv.conf` aadress `127.0.0.53`? Milline on tegelik DNS-server?

**1.3** Vaata, kuidas võrk on seadistatud:

```bash
ls -l /etc/netplan/
sudo cat /etc/netplan/*.yaml
```

**K3.** Kas masin saab aadressi DHCP-st või on see staatiline? Mille järgi see selgus?

---

## 2. osa. Ühenduvuse kontroll ja DNS

**2.1** Kontrolli ühenduvust kihthaaval (teooria punkt 7.5). Kirjuta iga käsu tulemus aruandesse:

```bash
ping -c3 <vaikelüüs>
ping -c3 1.1.1.1
ping -c3 www.debian.org
ping -c3 DEBIAN_IP
tracepath -n 1.1.1.1
```

**K4.** Mitu ruuterit (hüpet) on sinu masina ja aadressi `1.1.1.1` vahel? Milline on keskmine ping-aeg vaikelüüsini ja `1.1.1.1`-ni?

**2.2** Tee DNS-päringuid:

```bash
dig www.hkhk.edu.ee
dig +short www.hkhk.edu.ee
dig @1.1.1.1 +short www.hkhk.edu.ee
dig MX hkhk.edu.ee +short
dig -x 1.1.1.1 +short
```

**K5.** Mis on `www.hkhk.edu.ee` IP-aadress? Milline server vastas esimesele päringule (rida `SERVER`)? Millised on domeeni `hkhk.edu.ee` e-posti serverid?

**2.3** Lisa Debiani masin faili `/etc/hosts`:

```bash
sudo nano /etc/hosts
```

Lisa rida:

```text
DEBIAN_IP   debian1
```

Kontrolli:

```bash
getent hosts debian1
ping -c2 debian1
dig debian1
```

**K6.** Miks `ping debian1` ja `getent hosts` töötavad, kuid `dig debian1` vastust ei leia?

---

## 3. osa. Pordid ja teenused

**3.1** Vaata, millised pordid kuulavad:

```bash
sudo ss -tulpn
```

**K7.** Millised teenused kuulavad? Millised kuulavad kõigil aadressidel ja millised ainult `127.0.0.x` aadressil?

**3.2** Paigalda veebiserver nginx ja kontrolli seda:

```bash
sudo apt install nginx
sudo ss -tlpn | grep :80
curl -I http://localhost
```

**3.3** Debiani masinast kontrolli, kas Ubuntu veebiserver on kättesaadav:

```bash
curl -I http://UBUNTU_IP
nc -zv UBUNTU_IP 80
nc -zv UBUNTU_IP 3306
```

**K8.** Mida näitasid `nc` käsud kummagi pordi kohta? Miks?

---

## 4. osa. Püsiv võrguseadistus Netplaniga

Lisad Ubuntu masinale teise IP-aadressi, säilitades olemasoleva DHCP-seadistuse.

**4.1** Proovi kõigepealt ajutiselt:

```bash
sudo ip address add LISA_IP/24 dev <liides>
ip -br address
```

Debiani masinast: `ping -c2 LISA_IP`.

**4.2** Taaskäivita Ubuntu masin ja kontrolli, kas lisa-aadress on alles.

**K9.** Kas aadress oli pärast taaskäivitust alles? Miks?

**4.3** Lisa aadress püsivalt. Loo uus Netplani fail (asenda liidese nimi ja aadress):

```bash
sudo nano /etc/netplan/60-lisa-aadress.yaml
```

```yaml
network:
  version: 2
  ethernets:
    ens18:
      addresses:
        - LISA_IP/24
```

```bash
sudo chmod 600 /etc/netplan/60-lisa-aadress.yaml
sudo netplan try
```

Kui ühendus säilis, vajuta Enter, et muudatus kinnitada. Kontrolli tulemust ja taaskäivita masin veel kord.

**K10.** Mida teeb `netplan try`? Miks on see SSH kaudu töötades oluline? Kas aadress püsis pärast taaskäivitust?

**4.4** Tee meelega viga: muuda faili `60-lisa-aadress.yaml` taandeid (nihuta rida `addresses:` paar tühikut vasakule) ja käivita `sudo netplan try`.

**K11.** Mis veateate said? Paranda viga.

---

## 5. osa. SSH-võtmed

**5.1** Loo **oma arvutis** võtmepaar (kui sul seda veel pole):

```bash
ssh-keygen -t ed25519 -C "kasutaja@minu-arvuti"
```

Määra võtmele parool.

**5.2** Kopeeri avalik võti Ubuntu masinasse. Linuxis ja macOS-is:

```bash
ssh-copy-id kasutaja@UBUNTU_IP
```

Windowsis PowerShellis:

```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh kasutaja@UBUNTU_IP "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

**5.3** Logi sisse ja uuri serveris tulemust:

```bash
ssh kasutaja@UBUNTU_IP
ls -la ~/.ssh
cat ~/.ssh/authorized_keys
```

**K12.** Mida küsiti sisselogimisel - serveri kasutaja parooli või võtme parooli? Millised on kataloogi `~/.ssh` ja faili `authorized_keys` õigused?

**5.4** Loo oma arvutis fail `~/.ssh/config` (Windowsis `%USERPROFILE%\.ssh\config`):

```text
Host ubuntusrv
    HostName UBUNTU_IP
    User kasutaja
    IdentityFile ~/.ssh/id_ed25519
```

Kontrolli: `ssh ubuntusrv`.

**5.5** Loo **Ubuntu masinas** veel üks võtmepaar (ilma paroolita, masinatevaheliseks tööks) ja kopeeri see Debiani masinasse:

```bash
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519
ssh-copy-id kasutaja@debian1
ssh debian1 hostname
```

---

## 6. osa. Failide kopeerimine ja sünkroniseerimine

Kõik käsud Ubuntu masinas.

**6.1** Loo testandmed ja kopeeri need `scp`-ga Debiani masinasse:

```bash
mkdir -p ~/sync/{dokumendid,pildid}
for i in 1 2 3; do echo "Dokument $i" > ~/sync/dokumendid/dok$i.txt; done
scp -r ~/sync debian1:~/
ssh debian1 ls -R ~/sync
```

**6.2** Paigalda `rsync` mõlemasse masinasse (kui puudub). Muuda ühte faili, lisa üks ja kustuta üks:

```bash
echo "Muudetud" >> ~/sync/dokumendid/dok1.txt
echo "Uus" > ~/sync/dokumendid/dok4.txt
rm ~/sync/dokumendid/dok2.txt
```

**6.3** Sünkroniseeri - kõigepealt proovirežiimis:

```bash
rsync -avn --delete ~/sync/ debian1:~/sync/
rsync -av --delete ~/sync/ debian1:~/sync/
ssh debian1 ls ~/sync/dokumendid
```

**K13.** Milliseid faile `rsync` üle kandis? Mis juhtus failiga `dok2.txt` Debiani masinas ja miks? Miks on oluline käivitada `--delete` kõigepealt koos võtmega `-n`?

**6.4** Proovi kaldkriipsu erinevust:

```bash
rsync -av ~/sync debian1:~/proov1/
rsync -av ~/sync/ debian1:~/proov2/
ssh debian1 "ls ~/proov1 ~/proov2"
```

**K14.** Selgita tulemust.

---

## 7. osa. SSH-serveri karastamine

> [!NOTE]
> **Hoia kogu selle osa jooksul üks SSH-seanss Ubuntu masinasse avatuna** ja testi muudatusi teises aknas.

**7.1** Uuri olemasolevaid lisafaile ja kehtivaid väärtusi:

```bash
ls /etc/ssh/sshd_config.d/
sudo sshd -T | grep -Ei '^(permitrootlogin|passwordauthentication|pubkeyauthentication)'
```

**7.2** Loo karastamise fail:

```bash
sudo nano /etc/ssh/sshd_config.d/10-karastamine.conf
```

```text
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
MaxAuthTries 3
```

**7.3** Kontrolli süntaksit, rakenda ja kontrolli kehtivaid väärtusi:

```bash
sudo sshd -t
sudo systemctl reload ssh
sudo sshd -T | grep -Ei '^(permitrootlogin|passwordauthentication|maxauthtries)'
```

**7.4** Testi **uues aknas** oma arvutist: `ssh ubuntusrv`. See peab töötama võtmega.

**7.5** Testi paroolipõhist sisselogimist Debiani masinast mõnele teisele Ubuntu kasutajale (nt laboritöö 3 kasutaja, kellel võtit pole) või sundides paroolipõhist autentimist:

```bash
ssh -o PubkeyAuthentication=no kasutaja@UBUNTU_IP
```

**K15.** Mis veateate said? Miks? Miks on oluline, et karastamise fail algaks väikese numbriga (`10-`)?

---

## 8. osa. Tulemüür ufw

**8.1** Kontrolli olekut ja rakenduste profiile:

```bash
sudo ufw status verbose
sudo ufw app list
```

**8.2** Seadista reeglid. **Luba SSH enne tulemüüri sisselülitamist!**

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow from DEBIAN_IP to any port 80 proto tcp
sudo ufw enable
sudo ufw status numbered
```

**8.3** Testi:

- Debiani masinast: `curl -I http://UBUNTU_IP` (peab töötama);
- oma arvuti brauserist: `http://UBUNTU_IP` (ei tohi töötada);
- oma arvutist: `ssh ubuntusrv` (peab töötama).

**K16.** Kirjuta testide tulemused. Miks ei saanud sinu arvuti veebiserveriga ühendust, kuid SSH töötas?

**8.4** Vaata, milliseid madala taseme reegleid ufw lõi:

```bash
sudo nft list ruleset | head -40
```

**8.5** Luba veebiserver kõigile rakenduse profiili abil ja eemalda eraldi reegel:

```bash
sudo ufw allow "Nginx HTTP"
sudo ufw status numbered
sudo ufw delete <Debiani reegli number>
```

**K17.** Kirjuta lõplik `ufw status numbered` väljund aruandesse.

---

## 9. osa. Tõrkeotsing

Õpetaja tekitab sinu masinas (või paarilise masinas) ühe võrguvea. Iseõppija: palu kellelgi teisel valida üks vigadest allolevast loendist või vali ise juhuslikult ja unusta, kumma valisid.

Võimalikud vead:

1. failis `/etc/hosts` on Debiani masinale vale aadress;
2. ufw keelab pordi 80;
3. nginx on peatatud;
4. Netplani failis on vale DNS-server ja `netplan apply` on tehtud;
5. SSH karastamise failis on `AllowUsers` kellegi teise nimega.

**K18.** Kirjelda, millised diagnostikakäsud sa järjest käivitasid, mida iga käsk näitas, mis oli viga ja kuidas selle parandasid.

---

## 10. osa. Kellaaeg ja NTP

**10.1** Uuri Ubuntu masina kellaaega ja ajasünkroonimist (teooria punkt 7.9):

```bash
timedatectl
timedatectl timesync-status
systemctl status systemd-timesyncd
```

**K19.** Milline ajavöönd on seadistatud? Millise serveriga kell sünkroniseeritakse ja kui suur on nihe (*Offset*)? Kas riistvara kell on UTC-s?

**10.2** Kui ajavöönd ei ole `Europe/Tallinn`, muuda see. Seadista Ubuntu küsima aega Eesti kogumist (`NTP=ee.pool.ntp.org` failis `/etc/systemd/timesyncd.conf`) ja taaskäivita `systemd-timesyncd`.

**10.3** Tee Debiani masinast laborivõrgu ajaserver: paigalda `chrony`, lisa seadistusse `allow` oma laborivõrgu jaoks ja ava tulemüüris port 123/udp. Seadista Ubuntu küsima aega Debianilt (`NTP=debian1`) ja kontrolli:

```bash
# Ubuntus
timedatectl timesync-status
# Debianis
sudo chronyc clients
chronyc tracking
```

**10.4** Riku Ubuntu kell ja vaata, kuidas see paraneb:

```bash
sudo timedatectl set-ntp false
sudo date -s "2020-01-01 12:00"
date
curl -sI https://www.debian.org | head -1
sudo timedatectl set-ntp true
sleep 10; date
```

**K20.** Mis juhtus `curl`-i HTTPS-päringuga vale kellaajaga ja miks? Kas Debian näitas `chronyc clients` väljundis Ubuntut?

---

## Koristamine

Kui õpetaja ei ole teisiti öelnud, jäta seadistus alles. Iseõppija võib soovi korral eemaldada lisa-aadressi faili (`/etc/netplan/60-lisa-aadress.yaml`, seejärel `sudo netplan apply`) ja lülitada tulemüüri välja (`sudo ufw disable`). SSH karastamise jäta alles - see on hea tava.

---

## Lisaülesanne (valikuline)

1. Loo SSH tunnel, mis teeb sinu arvutis aadressil `http://localhost:8080` kättesaadavaks Ubuntu nginx-i, kuigi ufw lubab ainult SSH-d. (Eemalda ajutiselt reegel "Nginx HTTP".)
2. Debiani masinas: seadista `nftables` nii, et sissetulev on lubatud ainult SSH ja ICMP. Kontrolli Ubuntust, et `ping` töötab, kuid `nc -zv debian1 80` mitte.
3. Paigalda `fail2ban` Ubuntu masinasse ja uuri, kuidas see SSH paroolirünnakuid blokeerib (`sudo fail2ban-client status sshd`). (Pärast punkti 7 on paroolirünnakud niikuinii võimatud - miks on `fail2ban` ikkagi kasulik?)
4. **Lokaat:** sea Ubuntus süsteemi keeleks inglise keel, kuid kuupäevade vorminguks eesti oma (`LC_TIME=et_EE.UTF-8`), ja konsooli klaviatuur eesti paigutusele. Kontrolli `date` ja `localectl` väljundit.
5. **WireGuard:** tee Ubuntust VPN-server ja Debianist klient (võrk `10.99.0.0/24`, teooria punkt 7.11). Kontrolli `wg show` ja `ping`-iga. Mis juhtub, kui kliendi `AllowedIPs` ei sisalda serveri aadressi?
6. **ProxyJump:** seadista `~/.ssh/config`-is Debiani masinale ligipääs läbi Ubuntu masina (`ProxyJump`) ja kontrolli `ssh -v` väljundist, et ühendus läks läbi hüppeserveri.
7. **Bond:** lisa Proxmoxis Ubuntu masinale teine võrguliides, loo Netplaniga `bond0` (`active-backup`), võta Proxmoxis üks liides lahti (*Disconnect*) ja kontrolli `ping`-iga, et ühendus jätkub (`cat /proc/net/bonding/bond0`).
8. **IPv6:** leia oma masinate link-local aadressid (`ip -6 a`) ja pingi naabrit: `ping -6 fe80::…%ens18`. Miks on vaja liidese nime (`%ens18`)?

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).
