<!-- navigatsioon -->
[← Laboritöö 13. Võrgu süvendus](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 14. Konteinerid →](../moodul-14-konteinerid/index.md)
<!-- /navigatsioon -->

# Moodul 13. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Mis on WireGuardis `AllowedIPs` kahekordne roll?

<details>
<summary>Vastus</summary>

See on marsruutimistabel (millised aadressid saadetakse sellele partnerile tunnelisse) ja juurdepääsukontroll (millise lähteaadressiga pakette sellelt partnerilt vastu võetakse).

</details>

**2.** Mis on IPv6 link-local aadress ja miks on IPv6 puhul tulemüür eriti oluline?

<details>
<summary>Vastus</summary>

`fe80::`-ga algav aadress, mis on igal liidesel automaatselt ja töötab ainult samas võrgulõigus. IPv6-s NAT-i tavaliselt pole, masinad on otse adresseeritavad - ainult tulemüür kaitseb neid.

</details>

**3.** Mis vahe on sillal, VLAN-il ja bond-liidesel?

<details>
<summary>Vastus</summary>

Sild ühendab mitu liidest/VM-i üheks võrgulõiguks (tarkvaraline kommutaator); VLAN jagab ühe füüsilise võrgu mitmeks loogiliseks (märgistusega); bond koondab mitu füüsilist liidest üheks töökindluse või läbilaskevõime jaoks.

</details>

**4.** Kirjuta aadress `fd83:0000:0000:0000:0000:0000:0000:0055` lühikujul. Mis liiki aadress see on?

<details>
<summary>Vastus</summary>

`fd83::155`. See on ULA (*Unique Local Address*, `fd00::/8`) - privaatvõrgu aadress nagu IPv4 `10.0.0.0/8`, internetti seda ei marsruudita.

</details>

**5.** Mis on SLAAC ja miks antakse serverile pigem staatiline IPv6-aadress?

<details>
<summary>Vastus</summary>

SLAAC: masin moodustab aadressi ise ruuteri teadetes (RA) saadud prefiksist ja oma liidese osast, ilma DHCP-serverita. Serveri aadress peab olema püsiv, et DNS-i `AAAA`-kirje ja tulemüüri reeglid kehtiksid; privaatsuslaienditega SLAAC-aadress muutub.

</details>

**6.** Miks ei tohi IPv6-võrgus tulemüüriga kogu ICMPv6 liiklust blokeerida?

<details>
<summary>Vastus</summary>

IPv6 kasutab ICMPv6-t naabrite leidmiseks (NDP, asendab ARP-i), ruuteri teadeteks (RA) ja MTU tuvastamiseks. Ilma selleta ei leia masinad üksteist ega vaikelüüsi.

</details>

**7.** Mis juhtub füüsilise liidese IP-aadressiga, kui see lisatakse silda? Miks on silda lisamine SSH kaudu ohtlik?

<details>
<summary>Vastus</summary>

Aadress tuleb seadistada sillale; liides ise jääb aadressita ja töötab ainult silla pordina. Kui seadistus on vigane, kaob masinal võrguühendus ja SSH katkeb - seepärast tehakse seda konsoolist või teise liidesega.

</details>

**8.** Mis vahe on access- ja trunk-pordil? Kumba vajab hüperviisor, mille VM-id on eri VLAN-ides?

<details>
<summary>Vastus</summary>

Pääsuport (access-port) edastab ühe VLAN-i kaadreid ilma märgiseta (tavaline arvuti), magistraalport (trunk-port) mitme VLAN-i kaadreid 802.1Q märgisega. Hüperviisor vajab magistraalporti ja jagab VLAN-id VM-idele (nt Proxmoxi VLAN-aware sild ja VM-i *VLAN Tag*).

</details>

**9.** Millise bond'i režiimi valid, kui kommutaator LACP-d ei toeta, ja millise, kui toetab ning tahad ka suuremat koguläbilaskevõimet?

<details>
<summary>Vastus</summary>

LACP-ta: `active-backup` (töökindlus, kommutaatori seadistust pole vaja). LACP-ga: `802.3ad` - liiklus jaotatakse liideste vahel, kuid üks ühendus kasutab ikka ühte liidest.

</details>

**10.** Mis vahe on masquerade'il (SNAT) ja DNAT-il? Too kummagi kohta näide.

<details>
<summary>Vastus</summary>

Masquerade muudab väljuva paketi lähteaadressi ruuteri aadressiks (sisevõrk, konteinerid ja VPN-kliendid internetti). DNAT muudab sissetuleva paketi sihtaadressi (pordi edasisuunamine: ruuteri port 8080 → sisevõrgu veebiserver 10.50.0.2:80).

</details>

**11.** Mida on vaja, et Linux edastaks pakette ühest võrgust teise?

<details>
<summary>Vastus</summary>

Kerneli parameeter `net.ipv4.ip_forward = 1` (IPv6: `net.ipv6.conf.all.forwarding = 1`), tulemüüri luba ahelas `forward` ning kas marsruut tagasiteel või NAT (masquerade).

</details>

**12.** Kuidas töötab konteineri võrguühendus Podmanis või Dockeris (sild, veth, nimeruum, NAT)?

<details>
<summary>Vastus</summary>

Konteiner on oma võrgunimeruumis; veth-paari üks ots on konteineris (`eth0`), teine hosti sillas (`podman0`). Sild on konteinerite lüüs, host edastab paketid ja teeb väljuvale liiklusele masquerade'i; `-p 8080:80` lisab DNAT-reegli.

</details>

**13.** Ühendus serveriga ei tööta. `tcpdump` näitab, et `TCP SYN` paketid jõuavad serveri liidesele, kuid vastust ei tule. Mis on tõenäolised põhjused?

<details>
<summary>Vastus</summary>

Serveri tulemüür viskab paketi ära (`drop`) või vastus läheb teist teed (vale marsruut/asümmeetriline marsruutimine). Kui pordil keegi ei kuulaks, saadaks kernel vastuseks `RST`.

</details>

## Praktilised miniülesanded

**1.** Lisa AlmaLinuxi liidesele `ens18` püsivalt IPv6-aadress `fd83::155/64` ja kontrolli seda.

<details>
<summary>Lahendus</summary>

```bash
sudo nmcli connection modify ens18 ipv6.method manual ipv6.addresses fd83::155/64
sudo nmcli connection up ens18
ip -6 -br address show ens18
```

</details>

**2.** Kirjuta Netplani seadistus, mis loob liidesele `ens19` VLAN-i 30 aadressiga `10.30.0.10/24`.

<details>
<summary>Lahendus</summary>

```yaml
network:
  version: 2
  ethernets:
    ens19: {}
  vlans:
    vlan30:
      id: 30
      link: ens19
      addresses: [10.30.0.10/24]
```

</details>

**3.** Kirjuta nftables'i reeglid, mis lubavad võrgul `10.50.0.0/24` internetti pääseda läbi liidese `ens18` ja suunavad ruuteri pordi 2222 sisevõrgu masina `10.50.0.5` SSH-pordile.

<details>
<summary>Lahendus</summary>

```text
table ip nat {
    chain postrouting {
        type nat hook postrouting priority srcnat;
        ip saddr 10.50.0.0/24 oifname "ens18" masquerade
    }
    chain prerouting {
        type nat hook prerouting priority dstnat;
        iifname "ens18" tcp dport 2222 dnat to 10.50.0.5:22
    }
}
```

Lisaks `net.ipv4.ip_forward = 1` ja tulemüüri `forward` luba.

</details>

**4.** Püüa liidesel `ens18` ainult DNS-päringuid masinast `10.0.83.152` ja salvesta need faili.

<details>
<summary>Lahendus</summary>

```bash
sudo tcpdump -i ens18 -n -w dns.pcap host 10.0.83.152 and port 53
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 13. Võrgu süvendus](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 14. Konteinerid →](../moodul-14-konteinerid/index.md)
<!-- /navigatsioon -->
