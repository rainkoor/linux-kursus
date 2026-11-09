<!-- navigatsioon -->
[← Laboritöö 7. Võrk, SSH ja tulemüür](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 8. Kettad, failisüsteemid ja LVM →](../moodul-08-kettad-lvm/index.md)
<!-- /navigatsioon -->

# Moodul 7. Enesekontroll

Vasta küsimustele kõigepealt ise, ilma materjali vaatamata. Seejärel kontrolli vastuseid lehe lõpust.

## Küsimused

1. Millise käsuga näed liideste IP-aadresse ja millisega marsruute?
2. Mis on vaikelüüs?
3. Miks kaovad käsuga `ip address add` tehtud muudatused pärast taaskäivitust?
4. Kus seadistatakse püsiv IP-aadress Debianis, Ubuntus ja AlmaLinuxis?
5. Mis järjekorras otsitakse nimele IP-aadressi? Millises failis see järjekord on määratud?
6. Miks ei tohi Ubuntus faili `/etc/resolv.conf` käsitsi muuta?
7. Mis vahe on teenusel, mis kuulab aadressil `0.0.0.0:3306`, ja teenusel, mis kuulab aadressil `127.0.0.1:3306`?
8. Kirjelda samm-sammult, kuidas diagnoosida olukorda „veebileht ei avane“.
9. Kuidas töötab SSH võtmepõhine autentimine? Kumba võtit tohib jagada?
10. Millised peavad olema kataloogi `~/.ssh` ja faili `authorized_keys` õigused?
11. Mida tähendab hoiatus `REMOTE HOST IDENTIFICATION HAS CHANGED`? Mida teha?
12. Mis vahe on käskudel `rsync -av kataloog/ siht/` ja `rsync -av kataloog siht/`?
13. Milliseid SSH-serveri seadeid soovitatakse karastamiseks muuta?
14. Miks tuleb enne `ufw enable` käivitamist lubada SSH?
15. Mis vahe on `firewall-cmd` käskudel võtmega `--permanent` ja ilma selleta?
16. Too kolm probleemi, mis tekivad, kui serverite kellad on valed. Mis vahe on systemd-timesyncd-l ja chronyl?
17. Mis on lokaat ja milleks kasutatakse skriptides `LC_ALL=C`?
18. Mis on WireGuardis `AllowedIPs` kahekordne roll?
19. Mis on hüppeserver ja kuidas ühenduda sisevõrgu masinaga ühe SSH käsuga?
20. Mis on IPv6 link-local aadress ja miks on IPv6 puhul tulemüür eriti oluline?
21. Mis vahe on sillal, VLAN-il ja bond-liidesel?
22. Miks ei tohi kahel masinal samas alamvõrgus olla sama IP-aadress? Kuidas kontrollid enne staatilise aadressi seadistamist, et aadress on vaba?
23. Kuidas lubad kasutajal ainult SFTP kaudu faile laadida, nii et ta ei näe ülejäänud failisüsteemi? Millised nõuded on chroot-kataloogi omanikule ja õigustele?
24. Mis on TOTP ja miks peab serveri kell selle kasutamisel täpne olema? Mida tähendab `AuthenticationMethods publickey,keyboard-interactive`?

## Praktilised miniülesanded

1. Leia oma masina vaikelüüsi IP-aadress ühe käsuga, mis väljastab ainult aadressi.
2. Leia, millised programmid kuulavad TCP-porte, ja kuva ainult portide numbrid.
3. Leia domeeni `debian.org` nimeserverid (NS-kirjed).
4. Kirjuta `~/.ssh/config` kirje, mis võimaldab käsuga `ssh varu` ühenduda masinaga `10.0.5.20` pordil `2222` kasutajana `backup`.
5. Sünkroniseeri kataloog `/var/www/` masinasse `varu` kataloogi `/srv/www-varu/` nii, et sihtkohas kustutatakse ka allikast kustutatud failid. Kirjuta kõigepealt proovikäsk.
6. AlmaLinuxis: luba püsivalt HTTPS-teenus ja port `8443/tcp` ning kontrolli tulemust.

---

## Vastused

1. Aadressid: `ip address` (või `ip -br a`). Marsruudid: `ip route`.
2. Ruuter, kuhu saadetakse kõik paketid, mille sihtkoht ei ole kohalikus võrgus.
3. `ip` muudab ainult kerneli praegust olekut. Püsiv seadistus loetakse alglaadimisel seadistusfailidest (Netplan, `interfaces`, NetworkManager).
4. Debian: `/etc/network/interfaces`; Ubuntu: Netplan, `/etc/netplan/*.yaml`; AlmaLinux: NetworkManager (`nmcli`, `nmtui`).
5. Tavaliselt kõigepealt fail `/etc/hosts`, seejärel DNS. Järjekord on määratud failis `/etc/nsswitch.conf` (rida `hosts:`).
6. Ubuntus haldab nimelahendust systemd-resolved ja fail genereeritakse automaatselt - käsitsi tehtud muudatused kirjutatakse üle. DNS-serverid määratakse Netplanis.
7. `0.0.0.0` - teenus on kättesaadav kõigist võrkudest. `127.0.0.1` - teenusega saab ühenduda ainult samast masinast.
8. Kontrolli järjest: liides ja aadress (`ip -br a`), vaikelüüs (`ip r`), lüüsi ping, interneti ping IP-aadressiga (`ping 1.1.1.1`), nimelahendus (`getent hosts`, `dig`), teenus ja port (`curl -I`, `nc -zv`), serveris teenuse olek (`systemctl status`), kuulav port (`ss -tlpn`) ja tulemüür.
9. Kasutajal on võtmepaar: privaatvõti jääb tema arvutisse, avalik võti kopeeritakse serveri faili `~/.ssh/authorized_keys`. Ühendumisel tõestab klient krüptograafiliselt, et tal on avalikule võtmele vastav privaatvõti, ilma seda saatmata. Jagada tohib ainult **avalikku** võtit.
10. `~/.ssh` - `700`, `authorized_keys` - `600` (ka privaatvõti - `600`).
11. Serveri võti erineb failis `~/.ssh/known_hosts` salvestatust. See võib tähendada vahendajarünnakut või seda, et server paigaldati uuesti. Kui oled kindel, et muudatus on oodatud, eemalda vana kirje käsuga `ssh-keygen -R host`.
12. Kaldkriipsuga kopeeritakse kataloogi **sisu** sihtkohta, ilma kaldkriipsuta kopeeritakse kataloog **ise** (tulemuseks `siht/kataloog/`).
13. Näiteks `PermitRootLogin no`, `PasswordAuthentication no`, `KbdInteractiveAuthentication no`, `MaxAuthTries`, `AllowUsers` või `AllowGroups`.
14. Muidu blokeerib tulemüür SSH-ühenduse ja kaotad ligipääsu masinale.
15. Ilma `--permanent`-ita kehtib muudatus kohe, kuid kaob `firewalld` taaskäivitusel. `--permanent` salvestab muudatuse püsivalt, kuid see rakendub alles pärast `firewall-cmd --reload`.
16. Logisid ei saa võrrelda, TLS-sertifikaadid tunduvad kehtetud, Kerberos/AD keeldub autentimast, ajastatud tööd käivituvad valel ajal. systemd-timesyncd on lihtne klient; chrony on täielik NTP-teenus, mis korrigeerib täpsemalt ja võib olla ka sisevõrgu ajaserver.
17. Lokaat määrab keele, kuupäevade ja arvude vormingu ning järjestuse (nt `et_EE.UTF-8`). `LC_ALL=C` annab ühtse, lokaadist sõltumatu käitumise (järjestus, vead inglise keeles), mistõttu skripti tulemus on igas masinas sama.
18. See on marsruutimistabel (millised aadressid saadetakse sellele partnerile tunnelisse) ja juurdepääsukontroll (millise lähteaadressiga pakette sellelt partnerilt vastu võetakse).
19. Server, mille kaudu pääseb sisevõrku (bastion). `ssh -J kasutaja@hupe kasutaja@sisemasin` või `~/.ssh/config`-is `ProxyJump`.
20. `fe80::`-ga algav aadress, mis on igal liidesel automaatselt ja töötab ainult samas võrgulõigus. IPv6-s NAT-i tavaliselt pole, masinad on otse adresseeritavad - ainult tulemüür kaitseb neid.
21. Sild ühendab mitu liidest/VM-i üheks võrgulõiguks (tarkvaraline kommutaator); VLAN jagab ühe füüsilise võrgu mitmeks loogiliseks (märgistusega); bond koondab mitu füüsilist liidest üheks töökindluse või läbilaskevõime jaoks.
22. Võrk ei tea, kummale masinale pakette saata (ARP-tabelis vahetub MAC-aadress): ühendused katkevad juhuslikult ja SSH võib ühenduda valesse masinasse. Kontrolli aadressiplaani ja teisest masinast `ping`, `ip neigh show <aadress>` või `arping -D`; kooli laboris kasuta ainult õpetaja antud aadressi.
23. `sshd` seadistuses `Match Group …` plokk koos `ChrootDirectory /srv/sftp/%u` ja `ForceCommand internal-sftp`. Chroot-kataloog ja kõik selle ülemkataloogid peavad kuuluma juurkasutajale ega tohi olla teistele kirjutatavad; kasutaja kirjutab alamkataloogi, mis kuulub talle.
24. Ajapõhine ühekordne kood, mille telefonirakendus ja server arvutavad ühisest saladusest ja kellaajast; kood vahetub iga 30 sekundi järel, seega vale kellaga server ei aktsepteeri õiget koodi. `AuthenticationMethods publickey,keyboard-interactive` nõuab mõlemat: kõigepealt võti, seejärel PAM-i kaudu küsitav kood.

### Miniülesannete lahendused

```bash
ip route | awk '/^default/ {print $3}'
sudo ss -tlpn | awk 'NR>1 {print $4}' | awk -F: '{print $NF}' | sort -nu
dig NS debian.org +short
```

`~/.ssh/config`:

```text
Host varu
    HostName 10.0.5.20
    Port 2222
    User backup
```

```bash
rsync -avn --delete /var/www/ varu:/srv/www-varu/
rsync -av --delete /var/www/ varu:/srv/www-varu/
```

```bash
sudo firewall-cmd --add-service=https --permanent
sudo firewall-cmd --add-port=8443/tcp --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --list-all
```

<!-- navigatsioon -->
---

[← Laboritöö 7. Võrk, SSH ja tulemüür](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 8. Kettad, failisüsteemid ja LVM →](../moodul-08-kettad-lvm/index.md)
<!-- /navigatsioon -->
