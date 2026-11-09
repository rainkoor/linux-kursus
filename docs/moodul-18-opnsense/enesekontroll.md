# Moodul 18. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Mis on OPNsense ja millisel operatsioonisüsteemil see põhineb? Kuidas on see seotud pfSense'iga?
2. Mis on WAN ja LAN? Milline liiklus on nende vahel vaikimisi lubatud?
3. Miks vajab OPNsense'i virtuaalmasin Proxmoxis isoleeritud silda või SDN VNet-i?
4. Kuidas on OPNsense'i VirtIO võrguliidesed FreeBSD-s nimetatud?
5. Mida teeb seade „Block private networks from entering via WAN“? Millal võib selle välja lülitada?
6. Miks tohib võrgus olla ainult üks DHCP-server?
7. Mis järjekorras OPNsense tulemüürireegleid töötleb? Mis juhtub, kui ükski reegel ei sobi?
8. Mis vahe on reegli tegevustel *Block* ja *Reject*?
9. Mis on alias ja miks seda kasutada?
10. Mis on väljaminev NAT ja mis on pordisuunamine?
11. Kus asub kogu OPNsense'i seadistus ja kuidas seda varundada?
12. Miks ei tohi OPNsense'is süsteemifaile käsitsi muuta?
13. Millised FreeBSD käsud vastavad Linuxi käskudele `ip a`, `ip r` ja `ss -tulpn`?
14. Mida näitab käsk `pfctl -sr`?
15. Miks ei tohi haldusliidest WAN-i poole avada?

## Praktilised miniülesanded

1. Loo alias `dns-serverid`, kuhu kuuluvad `1.1.1.1` ja `9.9.9.9`.
2. Kirjuta LAN-i reegel, mis lubab laborivõrgust DNS-päringuid (UDP ja TCP 53) ainult aliase `dns-serverid` aadressidele ja OPNsense'ile endale.
3. Tee pordisuunamine, mis teeb Debiani masina SSH (port 22) väljast kättesaadavaks pordil 2222.
4. Leia FreeBSD käsurealt, millised pordid OPNsense'is kuulavad.
5. Vaata `tcpdump`-iga WAN-i liidesel DNS-liiklust.

---

## Vastused

1. Avatud lähtekoodiga tulemüüri- ja marsruutimistarkvara, mis põhineb FreeBSD-l. OPNsense on 2015. aastal pfSense'ist hargnenud.
2. WAN on väline võrk (internet, kooli võrk), LAN sisevõrk. Vaikimisi on LAN-ist välja kõik lubatud ja WAN-ist sisse kõik keelatud.
3. LAN peab olema eraldatud kooli võrgust, et laborivõrgu teenused (nt DHCP) ei segaks teisi ja et kogu laborivõrgu liiklus läbiks tulemüüri.
4. `vtnet0`, `vtnet1` jne.
5. Keelab WAN-ist sisse tulevad paketid privaatvõrgu aadressidelt (RFC 1918). Välja võib selle lülitada laboris, kus WAN ise on privaatvõrk. Päris interneti ühenduse korral peab see olema sees.
6. Mitu DHCP-serverit jagavad klientidele vastuolulisi aadresse, vaikelüüse ja DNS-servereid - kliendid saavad juhuslikult kas õige või vale seadistuse.
7. Ülevalt alla, kehtib esimene sobiv reegel. Kui ükski reegel ei sobi, liiklus keelatakse.
8. *Block* viskab paketi vaikselt minema (saatja ootab aegumiseni), *Reject* saadab saatjale keeldumise (ühendus ebaõnnestub kohe).
9. Nimega aadresside, võrkude või portide loend. Muudab reeglid loetavaks ja võimaldab muudatusi teha ühes kohas.
10. Väljaminev NAT asendab sisevõrgu masinate aadressid WAN-aadressiga, et need pääseksid internetti. Pordisuunamine suunab WAN-aadressi kindlale pordile tuleva liikluse sisevõrgu masinale.
11. Failis `/conf/config.xml`. Varundamine: *System* → *Configuration* → *Backups* → *Download configuration*.
12. OPNsense genereerib süsteemi seadistusfailid failist `config.xml` - käsitsi tehtud muudatused kirjutatakse järgmisel rakendamisel üle.
13. `ifconfig`, `netstat -rn`, `sockstat -4l`.
14. Kehtivad pf tulemüürireeglid (genereeritud OPNsense'i seadistusest).
15. Haldusliidese kaudu saab muuta kogu tulemüüri seadistust. Avalik haldusliides on rünnakute (paroolide arvamine, turvaaugud) sihtmärk.

### Miniülesannete lahendused

1. *Firewall* → *Aliases* → **+**: nimi `dns-serverid`, tüüp *Host(s)*, sisu `1.1.1.1`, `9.9.9.9`.
2. *Firewall* → *Rules* → *LAN*, kaks reeglit vaikimisi lubava reegli kohale: *Pass*, TCP/UDP, allikas *LAN net*, sihtkoht `dns-serverid`, port 53; *Pass*, TCP/UDP, allikas *LAN net*, sihtkoht *This Firewall*, port 53; ning nende alla *Block*, TCP/UDP, allikas *LAN net*, sihtkoht *any*, port 53.
3. *Firewall* → *NAT* → *Port Forward*: liides WAN, TCP, sihtkoht *WAN address*, port 2222, suunamise siht Debiani aadress, port 22.
4. `sockstat -4l` (või `sockstat -l`).
5. `tcpdump -ni vtnet0 port 53`.
