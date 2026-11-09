<!-- navigatsioon -->
[← Moodul 18. BSD praktikas: OPNsense tulemüür](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 18. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 18. OPNsense laborivõrgu tulemüürina

| | |
|---|---|
| **Süsteem** | OPNsense (FreeBSD); kliendid Debian, AlmaLinux ja Ubuntu |
| **Kestus** | 3 × 90 minutit |
| **Vajalik** | Proxmoxis isoleeritud sild või SDN VNet (küsi õpetajalt), OPNsense'i ISO, varasemate laboritööde Debiani, AlmaLinuxi ja Ubuntu masinad |
| **Eesmärk** | Ehitada isoleeritud laborivõrk, mida kaitseb OPNsense, ja seadistada selle teenused |

**Aruanne:** vasta küsimustele **K1–K16** ja lisa oma võrguplaan (vt [paigalduslisa](../lisad/paigaldus.md), punkt 2).

**Tulemus:** pärast seda laborit on sinu masinad isoleeritud võrgus OPNsense'i taga. Seda võrku kasutavad ka moodulid 19–21.

Tähised: `WAN_IP` - OPNsense'i WAN-aadress (saad kooli DHCP-st), `LAN_VORK` - sinu laborivõrk võrguplaanist (nt `10.0.83.0/24`, ruuter `10.0.83.1`).

---

## 1. osa. Võrguplaan ja virtuaalmasin

**1.1** Koosta võrguplaan: sinu laborivõrk, ruuteri aadress (`.1`), DHCP vahemik ja kõigi masinate aadressid (vt paigalduslisa punkt 1).

**1.2** Loo Proxmoxis OPNsense'i virtuaalmasin (teooria punkt 18.3): kaks VirtIO võrguliidest - `net0` kooli silda (WAN), `net1` isoleeritud silda/VNet-i (LAN).

**K1.** Kirjuta aruandesse virtuaalmasina riistvara seaded ja selgita, miks vajab tulemüür kahte võrguliidest.

## 2. osa. Paigaldus

**2.1** Paigalda OPNsense (teooria punkt 18.3): liidesed käsitsi (WAN `vtnet0`, LAN `vtnet1`), sisselogimine `installer`/`opnsense`, UFS või ZFS, uus juurkasutaja parool.

**2.2** Pärast taaskäivitust ja paigaldusmeedia eemaldamist logi konsoolis sisse kasutajaga `root`.

**2.3** Muuda konsoolimenüü punktis **2** LAN-i aadress oma võrguplaani järgi (`LAN_VORK`-i esimene aadress, mask 24). Luba LAN-il DHCP ja anna vahemik võrguplaani järgi. Veebiliidese protokolliks jäta HTTPS.

**K2.** Millise WAN-aadressi sai OPNsense? Milline liides on WAN ja milline LAN (konsooli kokkuvõte)?

## 3. osa. Kliendid laborivõrku

**3.1** Muuda **Ubuntu** masina võrguliides Proxmoxis isoleeritud silda/VNet-i (*Hardware* → *Network Device* → *Bridge*). Masin peab saama aadressi OPNsense'ilt:

```bash
sudo netplan apply          # või taaskäivita
ip -br a
ip r
resolvectl status | grep -A2 "DNS Servers"
ping -c2 10.0.83.1
ping -c2 1.1.1.1
ping -c2 debian.org
```

**K3.** Millise aadressi, vaikelüüsi ja DNS-serveri Ubuntu sai? Kas internet töötas? Mille kaudu (vt `tracepath -n 1.1.1.1`)?

**3.2** Tõsta isoleeritud võrku ka Debiani ja AlmaLinuxi masinad ning anna neile võrguplaani järgi **staatilised** aadressid (moodul 7, punkt 7.2). Vaikelüüs ja DNS on OPNsense'i LAN-aadress.

**3.3** OPNsense'i veebiliides on vaikimisi kättesaadav ainult **LAN-ist**, kuid sinu arvuti on kooli võrgus (WAN-i pool). Vali üks viis:

- **A (soovitatav):** laborivõrgus on töölauaga klient (nt Ubuntu Desktop või Windows), mida kasutad Proxmoxi konsooli kaudu, ja avad veebiliidese selle brauseris;
- **B:** luba veebiliides ajutiselt WAN-ist **ainult oma arvuti aadressilt**. OPNsense'i konsoolis (punkt **8**, kest) lülita tulemüür ajutiselt välja käsuga `pfctl -d`, ava oma arvutist `https://WAN_IP`, eemalda kõigepealt *Interfaces* → *WAN* valik *Block private networks* (sinu arvuti aadress on privaatvõrgust), seejärel lisa WAN-i liidesele reegel *Pass*, TCP, allikas = sinu arvuti IP, sihtkoht = *This Firewall*, port 443, ja vajuta *Apply* - see lülitab tulemüüri jälle sisse. Kontrolli konsoolis `pfctl -s info | head -1` (peab olema `Status: Enabled`).

> [!NOTE]
> **Õpetajale:** variant A on turvalisem ja lihtsam. Kui kasutad varianti B, veendu, et õppijad ei jätaks tulemüüri välja lülitatuks ega avaks haldusliidest kogu kooli võrgule.

## 4. osa. Veebiliides ja seadistusviisard

**4.1** Ava veebiliides `https://10.0.83.1` (sinu LAN-aadress), aktsepteeri iseallkirjastatud sertifikaat ja logi sisse kasutajaga `root`.

**4.2** Läbi seadistusviisard (teooria punkt 18.3): hostinimi `fw`, domeen `lab.example`, ajavöönd `Europe/Tallinn`, WAN DHCP, **lülita välja „Block private networks from entering via WAN“**.

**K4.** Miks lülitasime laboris välja „Block private networks from entering via WAN“? Miks ei tohi seda teha päris interneti ühenduse korral?

**4.3** Paigalda pistikprogramm `os-qemu-guest-agent` (*System* → *Firmware* → *Plugins*) ja kontrolli Proxmoxis, et OPNsense'i IP-aadressid on *Summary* lehel näha.

## 5. osa. DHCP ja DNS

**5.1** Ava DHCP-teenuse seaded (vaikimisi *Services* → *Dnsmasq DNS & DHCP*) ja kontrolli vahemikku. Leia antud rendid.

**5.2** Lisa **staatiline vastendus**: Ubuntu kliendi MAC-aadress (Ubuntus `ip link`) → võrguplaanis reserveeritud aadress (nt `10.0.83.98`), hostinimi `ubuntuklient`. Ubuntus uuenda renti:

```bash
sudo networkctl renew <liides>    # või taaskäivita
ip -br a
```

**K5.** Kas Ubuntu sai reserveeritud aadressi? Miks kasutatakse serveritel siiski pigem staatilist aadressi kui DHCP reserveeringut?

**5.3** Lisa Unboundi käsitsi kirjed (*Services* → *Unbound DNS* → *Overrides*): `debian1.lab.example`, `alma.lab.example`, `www.lab.example → alma`. Testi Ubuntust:

```bash
dig debian1.lab.example +short
dig www.lab.example +short
ping -c1 ubuntuklient
```

**K6.** Kas DHCP-kliendi nimi (`ubuntuklient`) lahenes? Kes vastas DNS-päringutele?

## 6. osa. Tulemüür, aliased ja pordisuunamine

**6.1** Loo aliased (*Firewall* → *Aliases*):

| Nimi | Tüüp | Sisu |
|---|---|---|
| `serverid` | Host(s) | Debiani ja AlmaLinuxi aadressid |
| `veebipordid` | Port(s) | 80, 443 |

**6.2** Paigalda AlmaLinuxi masinasse veebiserver (moodul 5 laboritöö) või kasuta olemasolevat. Kontrolli, et see on laborivõrgust kättesaadav: Ubuntust `curl -I http://alma.lab.example`.

**6.3** Tee pordisuunamine: WAN, TCP, port **8080** → `alma` port **80**, logimine sees, kirjeldus. Rakenda.

Testi **oma arvutist** (kooli võrgust): `http://WAN_IP:8080`.

**K7.** Kas leht avanes? Millise WAN-i reegli OPNsense automaatselt lõi (*Firewall* → *Rules* → *WAN*)? Mida näitas *Live View* logi ühendumise ajal?

**6.4** Keela Ubuntu kliendil serveritele SSH: lisa LAN-i liidesele **vaikimisi lubava reegli kohale** reegel:

| Väli | Väärtus |
|---|---|
| Action | Reject |
| Interface | LAN |
| Protocol | TCP |
| Source | `ubuntuklient` aadress |
| Destination | alias `serverid` |
| Destination port | 22 |
| Log | ✔ |
| Description | Klient ei tohi serveritesse SSH-ga |

Testi Ubuntust: `ssh kasutaja@debian1.lab.example` ja `curl -I http://alma.lab.example`.

**K8.** Kas SSH keelati ja veeb töötas? Mis vahe on *Block* ja *Reject* vahel (proovi mõlemat ja vaata, kuidas `ssh` käitub)?

**6.5** Liiguta oma reegel vaikimisi lubava reegli **alla** ja testi uuesti.

**K9.** Mis juhtus? Selgita, kuidas reeglite järjekord mõjutab tulemust.

Taasta õige järjekord.

## 7. osa. FreeBSD käsurida

**7.1** Ava konsoolis kest (punkt **8**) või luba SSH (*System* → *Settings* → *Administration* → *Secure Shell*, ainult LAN!) ja uuri süsteemi:

```sh
freebsd-version
opnsense-version
uname -a
ifconfig vtnet1
netstat -rn
sockstat -4l
pfctl -sr | head -30
pfctl -sn
pfctl -ss | head
pkg info | wc -l
service -e
gpart show
df -h
top
```

**K10.** Täida tabel: milline FreeBSD käsk vastab Linuxi käsule `ip a`, `ip r`, `ss -tulpn`, `nft list ruleset`, `systemctl list-units`, `lsblk`? Mis on FreeBSD versioon?

**K11.** Leia `pfctl -sr` väljundist oma osa 6.4 reegel. Kuidas see erineb veebiliideses nähtust?

**7.2** Püüa pakette LAN-i liideselt, kui Ubuntu teeb `ping`-i:

```sh
tcpdump -ni vtnet1 icmp
```

## 8. osa. Varundus ja taastamine

**8.1** Laadi alla seadistuse varukoopia (*System* → *Configuration* → *Backups*). Ava fail tekstiredaktoriga ja leia sealt oma alias `serverid`.

**K12.** Mis vormingus on seadistusfail? Miks peab seda hoidma turvaliselt (vihje: mis seal veel on)?

**8.2** Muuda midagi (nt kustuta alias `veebipordid`) ja taasta eelmine versioon lehelt *System* → *Configuration* → *History*.

**8.3** Tee OPNsense'i virtuaalmasinast Proxmoxis hetktõmmis.

**K13.** Mis vahe on OPNsense'i seadistuse varukoopial ja virtuaalmasina hetktõmmisel? Millal kumbagi kasutada?

## 9. osa. Kokkuvõte

**K14.** Joonista oma laborivõrgu skeem: OPNsense (WAN- ja LAN-aadress), kõik masinad koos aadressidega, pordisuunamine.

**K15.** Too kolm näidet, kus OPNsense'i ja Linuxi serveri (moodul 7 - `ufw`, `firewalld`, `nftables`) tulemüüri ülesanded erinevad.

**K16.** Mida tuleks teha, enne kui sellist OPNsense'i kasutatakse päris ettevõtte internetiühenduse ees?

---

## Lisaülesanne (valikuline)

1. **WireGuard VPN:** seadista OPNsense'is WireGuardi server (*VPN* → *WireGuard*) ja ühenda oma arvuti laborivõrku turvaliselt ilma pordisuunamisteta.
2. **IDS/IPS:** lülita sisse *Services* → *Intrusion Detection*, laadi ET Open reeglid ja vaata, milliseid hoiatusi tekib, kui Ubuntust skannid oma võrku `nmap`-iga (ainult oma laborivõrk!).
3. **pfSense:** paigalda pfSense CE teise virtuaalmasinasse ja võrdle veebiliidest ning seadistuse loogikat.
4. **FreeBSD:** paigalda tavaline FreeBSD virtuaalmasinasse (moodul 1 laboritöö FreeBSD-s): `pkg install nginx`, `sysrc nginx_enable=YES`, `service nginx start`. Võrdle Linuxiga.

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 18. BSD praktikas: OPNsense tulemüür](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 18. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
