<!-- navigatsioon -->
[← Laboritöö 18. OPNsense laborivõrgu tulemüürina](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 19. Võrgu infrastruktuur: DHCP, PXE ja iSCSI →](../moodul-19-dhcp-pxe-iscsi/index.md)
<!-- /navigatsioon -->

# Moodul 18. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Mis on OPNsense ja millisel operatsioonisüsteemil see põhineb? Kuidas on see seotud pfSense'iga?

<details>
<summary>Vastus</summary>

Avatud lähtekoodiga tulemüüri- ja marsruutimistarkvara, mis põhineb FreeBSD-l. OPNsense on 2015. aastal pfSense'ist hargnenud.

</details>

**2.** Mis on WAN ja LAN? Milline liiklus on nende vahel vaikimisi lubatud?

<details>
<summary>Vastus</summary>

WAN on väline võrk (internet, kooli võrk), LAN sisevõrk. Vaikimisi on LAN-ist välja kõik lubatud ja WAN-ist sisse kõik keelatud.

</details>

**3.** Miks vajab OPNsense'i virtuaalmasin Proxmoxis isoleeritud silda või SDN VNet-i?

<details>
<summary>Vastus</summary>

LAN peab olema eraldatud kooli võrgust, et laborivõrgu teenused (nt DHCP) ei segaks teisi ja et kogu laborivõrgu liiklus läbiks tulemüüri.

</details>

**4.** Kuidas on OPNsense'i VirtIO võrguliidesed FreeBSD-s nimetatud?

<details>
<summary>Vastus</summary>

`vtnet0`, `vtnet1` jne.

</details>

**5.** Mida teeb seade „Block private networks from entering via WAN“? Millal võib selle välja lülitada?

<details>
<summary>Vastus</summary>

Keelab WAN-ist sisse tulevad paketid privaatvõrgu aadressidelt (RFC 1918). Välja võib selle lülitada laboris, kus WAN ise on privaatvõrk. Päris interneti ühenduse korral peab see olema sees.

</details>

**6.** Miks tohib võrgus olla ainult üks DHCP-server?

<details>
<summary>Vastus</summary>

Mitu DHCP-serverit jagavad klientidele vastuolulisi aadresse, vaikelüüse ja DNS-servereid - kliendid saavad juhuslikult kas õige või vale seadistuse.

</details>

**7.** Mis järjekorras OPNsense tulemüürireegleid töötleb? Mis juhtub, kui ükski reegel ei sobi?

<details>
<summary>Vastus</summary>

Ülevalt alla, kehtib esimene sobiv reegel. Kui ükski reegel ei sobi, liiklus keelatakse.

</details>

**8.** Mis vahe on reegli tegevustel *Block* ja *Reject*?

<details>
<summary>Vastus</summary>

*Block* viskab paketi vaikselt minema (saatja ootab aegumiseni), *Reject* saadab saatjale keeldumise (ühendus ebaõnnestub kohe).

</details>

**9.** Mis on alias ja miks seda kasutada?

<details>
<summary>Vastus</summary>

Nimega aadresside, võrkude või portide loend. Muudab reeglid loetavaks ja võimaldab muudatusi teha ühes kohas.

</details>

**10.** Mis on väljaminev NAT ja mis on pordisuunamine?

<details>
<summary>Vastus</summary>

Väljaminev NAT asendab sisevõrgu masinate aadressid WAN-aadressiga, et need pääseksid internetti. Pordisuunamine suunab WAN-aadressi kindlale pordile tuleva liikluse sisevõrgu masinale.

</details>

**11.** Kus asub kogu OPNsense'i seadistus ja kuidas seda varundada?

<details>
<summary>Vastus</summary>

Failis `/conf/config.xml`. Varundamine: *System* → *Configuration* → *Backups* → *Download configuration*.

</details>

**12.** Miks ei tohi OPNsense'is süsteemifaile käsitsi muuta?

<details>
<summary>Vastus</summary>

OPNsense genereerib süsteemi seadistusfailid failist `config.xml` - käsitsi tehtud muudatused kirjutatakse järgmisel rakendamisel üle.

</details>

**13.** Millised FreeBSD käsud vastavad Linuxi käskudele `ip a`, `ip r` ja `ss -tulpn`?

<details>
<summary>Vastus</summary>

`ifconfig`, `netstat -rn`, `sockstat -4l`.

</details>

**14.** Mida näitab käsk `pfctl -sr`?

<details>
<summary>Vastus</summary>

Kehtivad pf tulemüürireeglid (genereeritud OPNsense'i seadistusest).

</details>

**15.** Miks ei tohi haldusliidest WAN-i poole avada?

<details>
<summary>Vastus</summary>

Haldusliidese kaudu saab muuta kogu tulemüüri seadistust. Avalik haldusliides on rünnakute (paroolide arvamine, turvaaugud) sihtmärk.

</details>

## Praktilised miniülesanded

**1.** Loo alias `dns-serverid`, kuhu kuuluvad `1.1.1.1` ja `9.9.9.9`.

<details>
<summary>Lahendus</summary>

*Firewall* → *Aliases* → **+**: nimi `dns-serverid`, tüüp *Host(s)*, sisu `1.1.1.1`, `9.9.9.9`.

</details>

**2.** Kirjuta LAN-i reegel, mis lubab laborivõrgust DNS-päringuid (UDP ja TCP 53) ainult aliase `dns-serverid` aadressidele ja OPNsense'ile endale.

<details>
<summary>Lahendus</summary>

*Firewall* → *Rules* → *LAN*, kaks reeglit vaikimisi lubava reegli kohale: *Pass*, TCP/UDP, allikas *LAN net*, sihtkoht `dns-serverid`, port 53; *Pass*, TCP/UDP, allikas *LAN net*, sihtkoht *This Firewall*, port 53; ning nende alla *Block*, TCP/UDP, allikas *LAN net*, sihtkoht *any*, port 53.

</details>

**3.** Tee pordisuunamine, mis teeb Debiani masina SSH (port 22) väljast kättesaadavaks pordil 2222.

<details>
<summary>Lahendus</summary>

*Firewall* → *NAT* → *Port Forward*: liides WAN, TCP, sihtkoht *WAN address*, port 2222, suunamise siht Debiani aadress, port 22.

</details>

**4.** Leia FreeBSD käsurealt, millised pordid OPNsense'is kuulavad.

<details>
<summary>Lahendus</summary>

`sockstat -4l` (või `sockstat -l`).

</details>

**5.** Vaata `tcpdump`-iga WAN-i liidesel DNS-liiklust.

<details>
<summary>Lahendus</summary>

`tcpdump -ni vtnet0 port 53`.

</details>

<!-- navigatsioon -->
---

[← Laboritöö 18. OPNsense laborivõrgu tulemüürina](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 19. Võrgu infrastruktuur: DHCP, PXE ja iSCSI →](../moodul-19-dhcp-pxe-iscsi/index.md)
<!-- /navigatsioon -->
