<!-- navigatsioon -->
[← Laboritöö 7. Võrk, SSH ja tulemüür](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 8. Kettad, failisüsteemid ja LVM →](../moodul-08-kettad-lvm/index.md)
<!-- /navigatsioon -->

# Moodul 7. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Millise käsuga näed liideste IP-aadresse ja millisega marsruute?

<details>
<summary>Vastus</summary>

Aadressid: `ip address` (või `ip -br a`). Marsruudid: `ip route`.

</details>

**2.** Mis on vaikelüüs?

<details>
<summary>Vastus</summary>

Ruuter, kuhu saadetakse kõik paketid, mille sihtkoht ei ole kohalikus võrgus.

</details>

**3.** Miks kaovad käsuga `ip address add` tehtud muudatused pärast taaskäivitust?

<details>
<summary>Vastus</summary>

`ip` muudab ainult kerneli praegust olekut. Püsiv seadistus loetakse alglaadimisel seadistusfailidest (Netplan, `interfaces`, NetworkManager).

</details>

**4.** Kus seadistatakse püsiv IP-aadress Debianis, Ubuntus ja AlmaLinuxis?

<details>
<summary>Vastus</summary>

Debian: `/etc/network/interfaces`; Ubuntu: Netplan, `/etc/netplan/*.yaml`; AlmaLinux: NetworkManager (`nmcli`, `nmtui`).

</details>

**5.** Mis järjekorras otsitakse nimele IP-aadressi? Millises failis see järjekord on määratud?

<details>
<summary>Vastus</summary>

Tavaliselt kõigepealt fail `/etc/hosts`, seejärel DNS. Järjekord on määratud failis `/etc/nsswitch.conf` (rida `hosts:`).

</details>

**6.** Miks ei tohi Ubuntus faili `/etc/resolv.conf` käsitsi muuta?

<details>
<summary>Vastus</summary>

Ubuntus haldab nimelahendust systemd-resolved ja fail genereeritakse automaatselt - käsitsi tehtud muudatused kirjutatakse üle. DNS-serverid määratakse Netplanis.

</details>

**7.** Mis vahe on teenusel, mis kuulab aadressil `0.0.0.0:3306`, ja teenusel, mis kuulab aadressil `127.0.0.1:3306`?

<details>
<summary>Vastus</summary>

`0.0.0.0` - teenus on kättesaadav kõigist võrkudest. `127.0.0.1` - teenusega saab ühenduda ainult samast masinast.

</details>

**8.** Kirjelda samm-sammult, kuidas diagnoosida olukorda „veebileht ei avane“.

<details>
<summary>Vastus</summary>

Kontrolli järjest: liides ja aadress (`ip -br a`), vaikelüüs (`ip r`), lüüsi ping, interneti ping IP-aadressiga (`ping 1.1.1.1`), nimelahendus (`getent hosts`, `dig`), teenus ja port (`curl -I`, `nc -zv`), serveris teenuse olek (`systemctl status`), kuulav port (`ss -tlpn`) ja tulemüür.

</details>

**9.** Kuidas töötab SSH võtmepõhine autentimine? Kumba võtit tohib jagada?

<details>
<summary>Vastus</summary>

Kasutajal on võtmepaar: privaatvõti jääb tema arvutisse, avalik võti kopeeritakse serveri faili `~/.ssh/authorized_keys`. Ühendumisel tõestab klient krüptograafiliselt, et tal on avalikule võtmele vastav privaatvõti, ilma seda saatmata. Jagada tohib ainult **avalikku** võtit.

</details>

**10.** Millised peavad olema kataloogi `~/.ssh` ja faili `authorized_keys` õigused?

<details>
<summary>Vastus</summary>

`~/.ssh` - `700`, `authorized_keys` - `600` (ka privaatvõti - `600`).

</details>

**11.** Mida tähendab hoiatus `REMOTE HOST IDENTIFICATION HAS CHANGED`? Mida teha?

<details>
<summary>Vastus</summary>

Serveri võti erineb failis `~/.ssh/known_hosts` salvestatust. See võib tähendada vahendajarünnakut või seda, et server paigaldati uuesti. Kui oled kindel, et muudatus on oodatud, eemalda vana kirje käsuga `ssh-keygen -R host`.

</details>

**12.** Mis vahe on käskudel `rsync -av kataloog/ siht/` ja `rsync -av kataloog siht/`?

<details>
<summary>Vastus</summary>

Kaldkriipsuga kopeeritakse kataloogi **sisu** sihtkohta, ilma kaldkriipsuta kopeeritakse kataloog **ise** (tulemuseks `siht/kataloog/`).

</details>

**13.** Milliseid SSH-serveri seadeid soovitatakse karastamiseks muuta?

<details>
<summary>Vastus</summary>

Näiteks `PermitRootLogin no`, `PasswordAuthentication no`, `KbdInteractiveAuthentication no`, `MaxAuthTries`, `AllowUsers` või `AllowGroups`.

</details>

**14.** Miks tuleb enne `ufw enable` käivitamist lubada SSH?

<details>
<summary>Vastus</summary>

Muidu blokeerib tulemüür SSH-ühenduse ja kaotad ligipääsu masinale.

</details>

**15.** Mis vahe on `firewall-cmd` käskudel võtmega `--permanent` ja ilma selleta?

<details>
<summary>Vastus</summary>

Ilma `--permanent`-ita kehtib muudatus kohe, kuid kaob `firewalld` taaskäivitusel. `--permanent` salvestab muudatuse püsivalt, kuid see rakendub alles pärast `firewall-cmd --reload`.

</details>

**16.** Too kolm probleemi, mis tekivad, kui serverite kellad on valed. Mis vahe on systemd-timesyncd-l ja chronyl?

<details>
<summary>Vastus</summary>

Logisid ei saa võrrelda, TLS-sertifikaadid tunduvad kehtetud, Kerberos/AD keeldub autentimast, ajastatud tööd käivituvad valel ajal. systemd-timesyncd on lihtne klient; chrony on täielik NTP-teenus, mis korrigeerib täpsemalt ja võib olla ka sisevõrgu ajaserver.

</details>

**17.** Mis on hüppeserver ja kuidas ühenduda sisevõrgu masinaga ühe SSH käsuga?

<details>
<summary>Vastus</summary>

Server, mille kaudu pääseb sisevõrku (bastion). `ssh -J kasutaja@hupe kasutaja@sisemasin` või `~/.ssh/config`-is `ProxyJump`.

</details>

**18.** Miks ei tohi kahel masinal samas alamvõrgus olla sama IP-aadress? Kuidas kontrollid enne staatilise aadressi seadistamist, et aadress on vaba?

<details>
<summary>Vastus</summary>

Võrk ei tea, kummale masinale pakette saata (ARP-tabelis vahetub MAC-aadress): ühendused katkevad juhuslikult ja SSH võib ühenduda valesse masinasse. Kontrolli aadressiplaani ja teisest masinast `ping`, `ip neigh show <aadress>` või `arping -D`; kooli laboris kasuta ainult õpetaja antud aadressi.

</details>

**19.** Kuidas lubad kasutajal ainult SFTP kaudu faile laadida, nii et ta ei näe ülejäänud failisüsteemi? Millised nõuded on chroot-kataloogi omanikule ja õigustele?

<details>
<summary>Vastus</summary>

`sshd` seadistuses `Match Group …` plokk koos `ChrootDirectory /srv/sftp/%u` ja `ForceCommand internal-sftp`. Chroot-kataloog ja kõik selle ülemkataloogid peavad kuuluma juurkasutajale ega tohi olla teistele kirjutatavad; kasutaja kirjutab alamkataloogi, mis kuulub talle.

</details>

**20.** Mis on TOTP ja miks peab serveri kell selle kasutamisel täpne olema? Mida tähendab `AuthenticationMethods publickey,keyboard-interactive`?

<details>
<summary>Vastus</summary>

Ajapõhine ühekordne kood, mille telefonirakendus ja server arvutavad ühisest saladusest ja kellaajast; kood vahetub iga 30 sekundi järel, seega vale kellaga server ei aktsepteeri õiget koodi. `AuthenticationMethods publickey,keyboard-interactive` nõuab mõlemat: kõigepealt võti, seejärel PAM-i kaudu küsitav kood.

</details>

**21.** Võrk `10.10.0.0/16` on kättesaadav ruuteri `10.0.83.254` kaudu. Kuidas lisad selle marsruudi püsivalt AlmaLinuxis ja kuidas kontrollid, millist marsruuti kasutatakse?

<details>
<summary>Vastus</summary>

`sudo nmcli connection modify ens18 +ipv4.routes "10.10.0.0/16 10.0.83.254"` ja `sudo nmcli connection up ens18`. Kontroll: `ip route` ja `ip route get 10.10.1.5`. Ubuntus lisatakse marsruut Netplani `routes:` alla, Debianis `up ip route add …` rida faili `/etc/network/interfaces`.

</details>

## Praktilised miniülesanded

**1.** Leia oma masina vaikelüüsi IP-aadress ühe käsuga, mis väljastab ainult aadressi.

<details>
<summary>Lahendus</summary>

```bash
ip route | awk '/^default/ {print $3}'
```

</details>

**2.** Leia, millised programmid kuulavad TCP-porte, ja kuva ainult portide numbrid.

<details>
<summary>Lahendus</summary>

```bash
sudo ss -tlpn | awk 'NR>1 {print $4}' | awk -F: '{print $NF}' | sort -nu
```

</details>

**3.** Leia domeeni `debian.org` nimeserverid (NS-kirjed).

<details>
<summary>Lahendus</summary>

```bash
dig NS debian.org +short
```

</details>

**4.** Kirjuta `~/.ssh/config` kirje, mis võimaldab käsuga `ssh varu` ühenduda masinaga `10.0.5.20` pordil `2222` kasutajana `backup`.

<details>
<summary>Lahendus</summary>

`~/.ssh/config`:

```text
Host varu
    HostName 10.0.5.20
    Port 2222
    User backup
```

</details>

**5.** Sünkroniseeri kataloog `/var/www/` masinasse `varu` kataloogi `/srv/www-varu/` nii, et sihtkohas kustutatakse ka allikast kustutatud failid. Kirjuta kõigepealt proovikäsk.

<details>
<summary>Lahendus</summary>

```bash
rsync -avn --delete /var/www/ varu:/srv/www-varu/
rsync -av --delete /var/www/ varu:/srv/www-varu/
```

</details>

**6.** AlmaLinuxis: luba püsivalt HTTPS-teenus ja port `8443/tcp` ning kontrolli tulemust.

<details>
<summary>Lahendus</summary>

```bash
sudo firewall-cmd --add-service=https --permanent
sudo firewall-cmd --add-port=8443/tcp --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --list-all
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 7. Võrk, SSH ja tulemüür](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 8. Kettad, failisüsteemid ja LVM →](../moodul-08-kettad-lvm/index.md)
<!-- /navigatsioon -->
