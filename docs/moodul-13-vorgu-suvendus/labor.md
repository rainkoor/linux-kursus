<!-- navigatsioon -->
[← Moodul 13. Võrgu süvendus: IPv6, sild, VLAN, bond ja VPN](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 13. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 13. Võrgu süvendus

| | |
|---|---|
| **Distro** | Ubuntu (`ubuntusrv`), AlmaLinux (`alma`), Debian (`debian1`) |
| **Kestus** | 3 × 90 minutit |
| **Vajalik** | Kolm laborimasinat samas võrgus; Ubuntu masinal **kaks lisavõrgukaarti** (`ens19`, `ens20`) ja AlmaLinuxil **üks** (`ens19`), kõik samal Proxmoxi sillal; ligipääs mõlema masina **konsoolile** |
| **Eesmärk** | Harjutada IPv6-t, VLAN-i, silda, NAT-i, bond'i ja WireGuardi ning analüüsida liiklust `tcpdump`-iga |

> **Aruanne:** vasta küsimustele **K1–K16**. Kõik küsimused on koos ka lehe lõpus ([Aruande küsimused](#aruande-küsimused)).

> [!WARNING]
> **Turvavõrk:** selles laboris muudad võrguseadistust. Tee kõik muudatused **lisakaartidel** (`ens19`, `ens20`), mitte liidesel, mille kaudu oled SSH-ga ühendatud, ja hoia konsool brauseris avatuna.

Laboris kasutatavad aadressid (asenda `83` oma võrgu numbriga):

| Masin | ens18 (põhivõrk) | IPv6 (ULA) | VLAN 20 | Bond-võrk | WireGuard |
|---|---|---|---|---|---|
| `debian1` | `10.0.83.52` | - | - | - | `10.99.0.2` |
| `ubuntusrv` | `10.0.83.54` | `fd83::54` | `10.20.0.54` | `10.30.0.54` | `10.99.0.1` |
| `alma` | `10.0.83.55` | `fd83::55` | `10.20.0.55` | `10.30.0.55` | - |

---

## 0. osa. Ettevalmistus

**0.1** Lisa Proxmoxis (*Hardware* → *Add* → *Network Device*, sama sild mis `net0`, mudel VirtIO) Ubuntu masinale kaks ja AlmaLinuxile üks võrgukaart. Kooli Proxmoxis võib selle teha õpetaja.

**0.2** Kontrolli mõlemas masinas, et uued liidesed on olemas, kuid ilma aadressita:

```bash
ip -br link
ip -br address
```

Ubuntus paigalda vajalikud tööriistad:

```bash
sudo apt install tcpdump wireguard-tools
```

---

## 1. osa. IPv6

**1.1** Vaata mõlemas masinas IPv6-aadresse ja leia **link-local** aadress (`fe80::…`):

```bash
ip -6 -br address
ip -6 route
```

**1.2** Pingi Ubuntust AlmaLinuxi link-local aadressi. Proovi kõigepealt ilma liidese nimeta, siis koos sellega:

```bash
ping -6 -c2 fe80::XXXX:XXXX:XXXX:XXXX
ping -6 -c2 fe80::XXXX:XXXX:XXXX:XXXX%ens18
ip -6 neigh
```

> **K1.** Miks ei töötanud ping ilma liidese nimeta? Mis on IPv4-s käsu `ip -6 neigh` vaste?

**1.3** Lisa mõlemale masinale püsiv ULA-aadress (teooria punkt 13.1): Ubuntule Netplaniga `fd83::54/64`, AlmaLinuxile `nmcli`-ga `fd83::55/64`. Ubuntus kasuta `sudo netplan try`.

```bash
ip -6 -br address
ping -6 -c2 fd83::55
ssh kasutaja@fd83::55 hostname
```

**1.4** Kontrolli Ubuntus, kas teenused kuulavad ka IPv6-l ja kas tulemüür kaitseb neid:

```bash
sudo ss -6 -tlpn
sudo ufw status verbose
grep IPV6 /etc/default/ufw
```

> **K2.** Millised teenused kuulavad IPv6-l (aadress `[::]` või `*`)? Kas ufw reeglid kehtivad ka IPv6-le? Mille järgi seda näed?

**1.5** Püüa Ubuntus `tcpdump`-iga IPv6 kontrollsõnumeid ja pingi samal ajal AlmaLinuxist Ubuntut:

```bash
sudo tcpdump -i ens18 -n icmp6
```

> **K3.** Milliseid ICMPv6 sõnumeid nägid peale `echo request`/`echo reply` (vihje: *neighbor solicitation*, *neighbor advertisement*)? Mis juhtuks, kui tulemüür blokeeriks kogu ICMPv6?

> **K4.** Kirjuta aadress `2001:0db8:0000:0000:0083:0000:0000:0052` lühikujul. Miks ei saa `::` kasutada aadressis kaks korda?

---

## 2. osa. VLAN

**2.1** Loo AlmaLinuxis liidese `ens19` peale VLAN 20 (teooria punkt 13.3):

```bash
sudo nmcli connection add type vlan con-name vlan20 dev ens19 id 20 \
    ipv4.method manual ipv4.addresses 10.20.0.55/24
sudo nmcli connection up vlan20
ip -d link show ens19.20
```

**2.2** Loo Ubuntus sama VLAN Netplaniga (fail `/etc/netplan/70-vlan.yaml`, liides `ens19`, VLAN `20`, aadress `10.20.0.54/24`) ja pingi:

```bash
sudo netplan try
ping -c3 10.20.0.55
```

**2.3** Käivita Ubuntus `tcpdump` füüsilisel liidesel, kuva Etherneti päis ja pingi AlmaLinuxist uuesti:

```bash
sudo tcpdump -i ens19 -n -e
```

> **K5.** Mida näitab `tcpdump` iga kaadri juures VLAN-i kohta (otsi `vlan 20` ja `ethertype 802.1Q`)? Mida näed, kui käivitad `tcpdump -i ens19.20 -n -e`? Miks erineb?

**2.4** Muuda Ubuntus VLAN-i number 30-ks (aadress jääb samaks) ja proovi uuesti pingida.

> **K6.** Miks ping enam ei tööta, kuigi mõlemad masinad on samas füüsilises võrgus ja samas IP-alamvõrgus? Kuidas saaksid VLAN-ide 20 ja 30 masinad omavahel suhelda?

**2.5** Eemalda VLAN-id (Ubuntus kustuta `/etc/netplan/70-vlan.yaml` ja `sudo netplan apply`; AlmaLinuxis `sudo nmcli connection delete vlan20`).

---

## 3. osa. Sild, nimeruum ja NAT: kuidas konteiner võrku saab

Selles osas ehitad Ubuntus käsitsi selle, mida Podman ja Docker teevad iga konteineri käivitamisel: silla, veth-paari ja eraldi **võrgunimeruumi**, ning teed Ubuntust nimeruumile ruuteri.

**3.1** Loo sild ilma füüsilise liideseta ja anna sellele aadress (see on „konteinerivõrgu“ lüüs):

```bash
sudo ip link add br0 type bridge
sudo ip address add 10.50.0.1/24 dev br0
sudo ip link set br0 up
```

**3.2** Loo võrgunimeruum `kast` (eraldatud võrgukeskkond - konteineri võrk) ja veth-paar, mille üks ots on nimeruumis ja teine sillas:

```bash
sudo ip netns add kast
sudo ip link add veth-host type veth peer name veth-kast
sudo ip link set veth-kast netns kast
sudo ip link set veth-host master br0
sudo ip link set veth-host up
sudo ip netns exec kast ip address add 10.50.0.2/24 dev veth-kast
sudo ip netns exec kast ip link set veth-kast up
sudo ip netns exec kast ip link set lo up
sudo ip netns exec kast ip route add default via 10.50.0.1
bridge link
```

```bash
sudo ip netns exec kast ip -br address     # mida nimeruum näeb?
sudo ip netns exec kast ping -c2 10.50.0.1
sudo ip netns exec kast ping -c2 1.1.1.1
```

> **K7.** Milliseid liideseid nimeruum `kast` näeb? Miks töötab ping sillale `10.50.0.1`, kuid mitte aadressile `1.1.1.1`?

**3.3** Tee Ubuntust ruuter: luba edastamine ja lisa NAT (teooria punkt 13.5). Kasuta nftables'i eraldi tabelit, et mitte segada ufw reegleid:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo nft add table ip labnat
sudo nft add chain ip labnat post '{ type nat hook postrouting priority srcnat; }'
sudo nft add rule ip labnat post ip saddr 10.50.0.0/24 oifname ens18 masquerade
sudo ufw route allow in on br0 out on ens18
sudo ip netns exec kast ping -c2 1.1.1.1
```

**3.4** Käivita nimeruumis veebiserver ja suuna Ubuntu port 8080 sinna (DNAT):

```bash
sudo ip netns exec kast python3 -m http.server 80 --directory /etc &
sudo nft add chain ip labnat pre '{ type nat hook prerouting priority dstnat; }'
sudo nft add rule ip labnat pre iifname ens18 tcp dport 8080 dnat to 10.50.0.2:80
sudo ufw allow 8080/tcp
sudo ufw route allow in on ens18 out on br0 to 10.50.0.2 port 80 proto tcp
```

Ava Debianist või AlmaLinuxist `curl -s http://10.0.83.54:8080/ | head` ja vaata nimeruumi veebiserveri logi.

> **K8.** Millise lähteaadressiga päringuid nimeruumi veebiserver logis nägi? Millise aadressiga nägi `1.1.1.1` punktis 3.3 nimeruumi ping-päringuid? Selgita masquerade ja DNAT erinevust.

> **K9.** Võrdle seda osa Podmaniga: käivita `sudo podman run -d --name v -p 8081:80 docker.io/library/nginx:alpine` ja vaata `ip -br link`, `bridge link`, `sudo nft list ruleset | grep -i dnat`. Mida Podman lõi? (Kui Podmanit pole, paigalda see või kirjelda moodulis 14 õpitu põhjal.)

**3.5** Koristamine: `sudo kill %1`, `sudo ip netns del kast`, `sudo ip link del br0`, `sudo nft delete table ip labnat`, eemalda ufw reeglid (`sudo ufw status numbered`, `sudo ufw delete N`), Podmani konteiner `sudo podman rm -f v`.

---

## 4. osa. Bond

**4.1** Loo Ubuntus Netplaniga `bond0` liidestest `ens19` ja `ens20` (režiim `active-backup`, aadress `10.30.0.54/24`, teooria punkt 13.4). Anna AlmaLinuxi `ens19`-le aadress `10.30.0.55/24` (`nmcli connection add type ethernet ifname ens19 con-name bondtest ipv4.method manual ipv4.addresses 10.30.0.55/24`).

```bash
sudo netplan try
cat /proc/net/bonding/bond0
ping -c3 10.30.0.55
```

**4.2** Käivita AlmaLinuxist pidev ping `ping 10.30.0.54`. Vaata Ubuntus, milline liides on aktiivne (`Currently Active Slave`), ja ühenda see Proxmoxis lahti (*Hardware* → võrgukaart → *Edit* → *Disconnect*).

```bash
cat /proc/net/bonding/bond0
sudo journalctl -k --since "5 min ago" | grep -i bond
```

> **K10.** Mitu ping-paketti kadus ümberlülitusel? Milline liides on nüüd aktiivne ja mida näitab `Link Failure Count`?

**4.3** Ühenda kaart tagasi. Kas aktiivne liides vahetus tagasi?

> **K11.** Millist bond'i režiimi kasutaksid füüsilises serveris, mis on ühendatud kahe eri kommutaatoriga, mis LACP-d ei toeta? Miks ei kahekordista bond ühe faili kopeerimise kiirust?

**4.4** Eemalda bond (kustuta Netplani fail ja `sudo netplan apply`; AlmaLinuxis `sudo nmcli connection delete bondtest`).

---

## 5. osa. WireGuard VPN

**5.1** Tee Ubuntust VPN-server ja Debianist klient (võrk `10.99.0.0/24`, teooria punkt 13.6). Loo mõlemas võtmepaar, seadista `wg0.conf` ja ava Ubuntu tulemüüris port `51820/udp`. Kliendi `AllowedIPs = 10.99.0.0/24`.

```bash
sudo systemctl enable --now wg-quick@wg0
sudo wg show
ping -c3 10.99.0.1               # Debianist
```

> **K12.** Mida näitab `wg show` väljund (`latest handshake`, `transfer`)? Mis juhtub, kui serveri `[Peer]` plokis on kliendi avalik võti vale?

**5.2** Laienda kliendi `AllowedIPs` nii, et ka AlmaLinuxi VLAN-võrk või muu sisevõrk läheks tunneli kaudu (laboris lisa AlmaLinuxile ajutiselt `ens19`-le aadress `10.40.0.55/24` ja Ubuntule `10.40.0.54/24` - see on „labori sisevõrk“, mida Debian otse ei näe). Lisa serverisse edastamine ja masquerade (teooria punkt 13.6, `PostUp`) - väljuvaks liideseks on siin `ens19` - ning luba ufw-s edastamine: `sudo ufw route allow in on wg0 out on ens19`. Kliendis: `AllowedIPs = 10.99.0.0/24, 10.40.0.0/24`.

```bash
sudo wg-quick down wg0 && sudo wg-quick up wg0     # mõlemas pärast muudatust
ip route                                           # Debianis: kuhu läheb 10.40.0.0/24?
ping -c3 10.40.0.55                                # Debianist
```

> **K13.** Millise marsruudi lisas `wg-quick` Debianisse? Millise lähteaadressiga jõudsid Debiani ping-paketid AlmaLinuxisse (kontrolli AlmaLinuxis `sudo tcpdump -i ens19 -n icmp`)? Miks?

> **K14.** Kuidas tuleks seadistada `AllowedIPs` kliendis, kui tahaksid kogu interneti liikluse suunata läbi VPN-i? Millal on see kasulik?

---

## 6. osa. Mida näeb pealtkuulaja?

**6.1** Käivita Ubuntus kaks `tcpdump`-i (kaks terminali) ja pingi Debianist `10.99.0.1`:

```bash
sudo tcpdump -i ens18 -n udp port 51820      # 1. terminal: väljaspool tunnelit
sudo tcpdump -i wg0 -n                       # 2. terminal: tunneli sees
```

> **K15.** Mida nägid kummaski aknas? Mida näeb ründaja, kes kuulab võrku tunneli ja füüsilise liidese vahel?

> **K16.** Kokkuvõte: kool tahab ühes füüsilises serveris (kaks võrgukaarti) pidada Proxmoxi virtuaalmasinaid kolmes eraldi võrgus (õpetajad, õpilased, serverid) ning lubada administraatoritele kodust ligipääsu. Milliseid selle mooduli tehnikaid kasutaksid ja kuidas need omavahel seotud on? (Vihje: bond → VLAN → sild → VM; WireGuard OPNsense'is või Linuxi ruuteris.)

---

## Koristamine

Eemalda WireGuard mõlemast masinast (`sudo systemctl disable --now wg-quick@wg0`) ja ajutised aadressid. IPv6 ULA-aadressid võid alles jätta. Lisakaardid võid Proxmoxis eemaldada, kui õpetaja ei ole öelnud teisiti.

---

## Lisaülesanne (valikuline)

1. **IPv6 tunnelis:** lisa WireGuardi tunnelile ka IPv6-võrk (`fd99::1/64`, `fd99::2/64`) ja pingi `ping -6 fd99::1`.
2. **Sild püsivalt:** tee AlmaLinuxis `ens19`-st sild `br0` (`nmcli`), nagu Proxmox teeb `vmbr0`-ga. Kontrolli `bridge link`.
3. **Site-to-site:** ühenda WireGuardiga kaks „asukohta“: Ubuntu taga on võrk `10.40.0.0/24`, Debiani taga võrgunimeruumis (3. osa järgi) `10.60.0.0/24`. Seadista mõlemas `AllowedIPs` teise poole võrguga ja marsruudid nii, et NAT-i pole vaja.
4. **firewalld:** korda 3. osa NAT ja pordi edasisuunamine AlmaLinuxis firewalld-iga (`--add-masquerade`, `--add-forward-port`).
5. **Wireshark:** salvesta 2. osa VLAN-liiklus faili (`tcpdump -i ens19 -w vlan.pcap`), kopeeri see oma arvutisse ja ava Wiresharkis. Leia kaadri päisest 802.1Q väli.

---

<!-- kysimused -->
## Aruande küsimused

Kõik selle laboritöö küsimused ühes kohas. Sulgudes on punkt, mille juures küsimust küsitakse. Kopeeri loend oma aruande alguseks ja kirjuta vastus iga küsimuse alla. Kus küsitakse käsku, kirjuta üles kogu käsk.

- **K1.** *(punkt 1.2)* Miks ei töötanud ping ilma liidese nimeta? Mis on IPv4-s käsu `ip -6 neigh` vaste?
- **K2.** *(punkt 1.4)* Millised teenused kuulavad IPv6-l (aadress `[::]` või `*`)? Kas ufw reeglid kehtivad ka IPv6-le? Mille järgi seda näed?
- **K3.** *(punkt 1.5)* Milliseid ICMPv6 sõnumeid nägid peale `echo request`/`echo reply` (vihje: *neighbor solicitation*, *neighbor advertisement*)? Mis juhtuks, kui tulemüür blokeeriks kogu ICMPv6?
- **K4.** *(punkt 1.5)* Kirjuta aadress `2001:0db8:0000:0000:0083:0000:0000:0052` lühikujul. Miks ei saa `::` kasutada aadressis kaks korda?
- **K5.** *(punkt 2.3)* Mida näitab `tcpdump` iga kaadri juures VLAN-i kohta (otsi `vlan 20` ja `ethertype 802.1Q`)? Mida näed, kui käivitad `tcpdump -i ens19.20 -n -e`? Miks erineb?
- **K6.** *(punkt 2.4)* Miks ping enam ei tööta, kuigi mõlemad masinad on samas füüsilises võrgus ja samas IP-alamvõrgus? Kuidas saaksid VLAN-ide 20 ja 30 masinad omavahel suhelda?
- **K7.** *(punkt 3.2)* Milliseid liideseid nimeruum `kast` näeb? Miks töötab ping sillale `10.50.0.1`, kuid mitte aadressile `1.1.1.1`?
- **K8.** *(punkt 3.4)* Millise lähteaadressiga päringuid nimeruumi veebiserver logis nägi? Millise aadressiga nägi `1.1.1.1` punktis 3.3 nimeruumi ping-päringuid? Selgita masquerade ja DNAT erinevust.
- **K9.** *(punkt 3.4)* Võrdle seda osa Podmaniga: käivita `sudo podman run -d --name v -p 8081:80 docker.io/library/nginx:alpine` ja vaata `ip -br link`, `bridge link`, `sudo nft list ruleset | grep -i dnat`. Mida Podman lõi? (Kui Podmanit pole, paigalda see või kirjelda moodulis 14 õpitu põhjal.)
- **K10.** *(punkt 4.2)* Mitu ping-paketti kadus ümberlülitusel? Milline liides on nüüd aktiivne ja mida näitab `Link Failure Count`?
- **K11.** *(punkt 4.3)* Millist bond'i režiimi kasutaksid füüsilises serveris, mis on ühendatud kahe eri kommutaatoriga, mis LACP-d ei toeta? Miks ei kahekordista bond ühe faili kopeerimise kiirust?
- **K12.** *(punkt 5.1)* Mida näitab `wg show` väljund (`latest handshake`, `transfer`)? Mis juhtub, kui serveri `[Peer]` plokis on kliendi avalik võti vale?
- **K13.** *(punkt 5.2)* Millise marsruudi lisas `wg-quick` Debianisse? Millise lähteaadressiga jõudsid Debiani ping-paketid AlmaLinuxisse (kontrolli AlmaLinuxis `sudo tcpdump -i ens19 -n icmp`)? Miks?
- **K14.** *(punkt 5.2)* Kuidas tuleks seadistada `AllowedIPs` kliendis, kui tahaksid kogu interneti liikluse suunata läbi VPN-i? Millal on see kasulik?
- **K15.** *(punkt 6.1)* Mida nägid kummaski aknas? Mida näeb ründaja, kes kuulab võrku tunneli ja füüsilise liidese vahel?
- **K16.** *(punkt 6.1)* Kokkuvõte: kool tahab ühes füüsilises serveris (kaks võrgukaarti) pidada Proxmoxi virtuaalmasinaid kolmes eraldi võrgus (õpetajad, õpilased, serverid) ning lubada administraatoritele kodust ligipääsu. Milliseid selle mooduli tehnikaid kasutaksid ja kuidas need omavahel seotud on? (Vihje: bond → VLAN → sild → VM; WireGuard OPNsense'is või Linuxi ruuteris.)
<!-- /kysimused -->

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 13. Võrgu süvendus: IPv6, sild, VLAN, bond ja VPN](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 13. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
