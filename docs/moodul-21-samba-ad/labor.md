<!-- navigatsioon -->
[← Moodul 21. Active Directory Linuxis: Samba AD DC](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 21. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 21. Samba AD domeen

| | |
|---|---|
| **Distrod** | Debian (`dc1` - Samba AD DC), Ubuntu (`ubuntuklient`) ja AlmaLinux (`alma`) - domeeni liikmed, Windows 10/11 Pro või Education (`winklient`) |
| **Kestus** | 4 × 90 minutit (16A - domeenikontroller ja Windows, 16B - Linuxi kliendid) |
| **Vajalik** | Laboritöö 18 laborivõrk OPNsense'i taga, uus Debiani VM `dc1` (2 vCPU, 2 GiB RAM, 20 GiB ketas), Windowsi kliendi VM |
| **Eesmärk** | Ehitada vaba tarkvaraga Active Directory domeen ja liita sellega Windowsi ning Linuxi masinad |

> **Aruanne:** vasta küsimustele **K1–K18**. Kõik küsimused on koos ka lehe lõpus ([Aruande küsimused](#aruande-küsimused)).

Tähised võrguplaani näite järgi: võrk `10.0.83.0/24`, OPNsense `10.0.83.1`, `dc1` `10.0.83.56`, `alma` `10.0.83.55`, `ubuntuklient` `10.0.83.98`, `winklient` `10.0.83.99`. Domeen `ad.lab.example`, NetBIOS-nimi `AD`. Asenda oma võrguplaani väärtustega.

> [!WARNING]
> **Enne alustamist:** HKHK laboris on `dc1` mallist olemas, iseõppija paigaldab selle (vt [paigalduslisa](../lisad/paigaldus.md)). Anna sellele staatiline aadress ja **tee hetktõmmis** (snapshot). Provisioning'ut on lihtsam korrata puhtalt masinalt kui ebaõnnestunud katset parandada.

---

# Laboritöö 21A. Domeenikontroller ja Windowsi klient (Debian, Windows)

## 1. osa. Ettevalmistus

**1.1** Seadista `dc1` hostinimi ja `/etc/hosts` (teooria punkt 21.3–21.4). Kontrolli:

```bash
hostname
hostname -f
hostname -i
ip -br a
```

> **K1.** Miks peab DC hostinimi lahenduma kohalikuks IP-aadressiks (`10.0.83.56`), mitte `127.0.1.1`-ks?

**1.2** Kontrolli kellaaega:

```bash
timedatectl
```

> **K2.** Miks on kellaaeg AD-s nii oluline? Kui suur võib olla kellade erinevus?

## 2. osa. Domeeni loomine

**2.1** Paigalda paketid, peata `smbd`, `nmbd` ja `winbind`, tõsta vaikimisi `smb.conf` kõrvale.

**2.2** Loo domeen (teooria punkt 21.4) - DNS-i edastajaks OPNsense. Pane administraatori parool kirja turvalisse kohta (mitte aruandesse!).

**2.3** Kopeeri `krb5.conf`, käivita `samba-ad-dc`, seadista DC DNS-iks iseennast ja seadista `chrony` (`ntpsigndsocket`).

```bash
sudo systemctl status samba-ad-dc
sudo ss -tulpn | grep -E ':(53|88|389|445|464|636) '
cat /etc/samba/smb.conf
```

> **K3.** Milliseid porte Samba kuulab? Millist teenust iga port pakub? Mis on `smb.conf` failis jaotises `[global]` peale provisioning'ut?

## 3. osa. DNS ja Kerberos

**3.1** Testi DNS-i:

```bash
host -t SRV _ldap._tcp.ad.lab.example
host -t SRV _kerberos._udp.ad.lab.example
host -t SRV _gc._tcp.ad.lab.example
host -t A dc1.ad.lab.example
host www.debian.org
```

> **K4.** Mida näitavad SRV-kirjed? Miks vajavad kliendid neid? Kust tuli vastus päringule `www.debian.org`?

**3.2** Testi Kerberost:

```bash
kinit administrator
klist
kdestroy
kinit vale-kasutaja
```

> **K5.** Milline pilet tekkis `klist` väljundis ja kui kaua see kehtib? Mis veateate andis vale kasutaja?

**3.3** Testi SMB-d:

```bash
smbclient -L localhost -N
smbclient //localhost/netlogon -U Administrator -c 'ls'
```

**3.4** Seadista OPNsense'is Unbound Query Forwarding domeenile `ad.lab.example` → `10.0.83.56` (teooria punkt 21.3). Testi teisest masinast (nt `debian1`), mille DNS on OPNsense:

```bash
host -t SRV _ldap._tcp.ad.lab.example
```

> **K6.** Miks on parem suunata ainult domeeni `ad.lab.example` päringud DC-le, mitte panna DC kogu laborivõrgu DNS-iks?

## 4. osa. Kasutajad, grupid ja OU-d

**4.1** Loo `samba-tool` abil:

| Objekt | Nimi | Liikmed |
|---|---|---|
| OU | `Opilased`, `Opetajad`, `Linux` | |
| Kasutaja (OU `Opilased`) | `mari`, `jaan` | |
| Kasutaja (OU `Opetajad`) | `kati` | |
| Grupp | `opilased` | `mari`, `jaan` |
| Grupp | `linuxadminid` | `kati` |

```bash
sudo samba-tool ou list
sudo samba-tool user list
sudo samba-tool group listmembers opilased
sudo samba-tool user show mari
```

> **K7.** Kirjuta aruandesse käsud, millega lõid kasutaja `mari` ja paigutasid ta OU-sse `Opilased`. Mis on Mari täielik DN?

**4.2** Vaata ja muuda paroolipoliitikat (min pikkus 10). Proovi seada Jaanile parool `Lyhike1`.

> **K8.** Mis juhtus? Millised on domeeni vaikimisi paroolinõuded?

**4.3** Lisa DNS-kirjed: `www.ad.lab.example → 10.0.83.55` ning pöördtsoon `83.0.10.in-addr.arpa` koos `dc1` PTR-kirjega.

```bash
host www.ad.lab.example
host 10.0.83.56
```

## 5. osa. Windowsi klient

**5.1** Seadista `winklient` DNS-iks `10.0.83.56`. Kontrolli PowerShellis:

```powershell
Resolve-DnsName -Type SRV _ldap._tcp.ad.lab.example
Test-NetConnection dc1.ad.lab.example -Port 389
w32tm /stripchart /computer:dc1.ad.lab.example /samples:3
```

**5.2** Liida `winklient` domeeniga ja taaskäivita. Logi sisse kasutajana `AD\mari`.

```powershell
whoami
whoami /groups
echo $env:LOGONSERVER
klist
```

> **K9.** Mida näitasid `whoami` ja `$env:LOGONSERVER`? Milliseid Kerberose pileteid on Windowsi kliendil?

**5.3** Vaata DC-s, et arvutikonto tekkis:

```bash
sudo samba-tool computer list
host winklient.ad.lab.example
```

> **K10.** Kas Windowsi klient registreeris ennast DNS-is automaatselt?

## 6. osa. RSAT ja rühmapoliitika

**6.1** Logi `winklient`-i sisse kui `AD\Administrator` ja paigalda RSAT-tööriistad (teooria punkt 21.6). Ava `dsa.msc` ja leia 4. osas loodud OU-d ja kasutajad. Loo `dsa.msc`-ga uus kasutaja `ain` OU-sse `Opetajad` ja kontrolli DC-s `samba-tool user list`.

**6.2** Loo `gpmc.msc`-ga GPO, mis keelab OU `Opilased` kasutajatel juhtpaneeli, ja seo see OU-ga. Logi sisse kui `AD\jaan`:

```powershell
gpupdate /force
gpresult /r
```

> **K11.** Kas juhtpaneel oli Jaanile keelatud? Kas see kehtis ka Katile? Miks?

**6.3** Leia GPO failid DC-s:

```bash
sudo ls -R /var/lib/samba/sysvol/ad.lab.example/Policies/ | head -30
```

> **K12.** Kuidas on GPO-d nimetatud? Miks on vaja SYSVOL eraldi varundada, kui DC-sid on mitu?

---

# Laboritöö 21B. Linuxi kliendid (Ubuntu, AlmaLinux)

## 7. osa. Ubuntu liitmine domeeniga

**7.1** Seadista `ubuntuklient` hostinimeks `ubuntuklient.ad.lab.example` ja DNS-iks `10.0.83.56` (Netplan, moodul 7) või OPNsense, kui Query Forwarding on tehtud. Kontrolli kella.

**7.2** Paigalda paketid ja liitu (teooria punkt 21.7):

```bash
realm discover ad.lab.example
sudo realm join -U Administrator ad.lab.example
realm list
sudo klist -k
```

> **K13.** Mida näitas `realm discover`? Millised kirjed on failis `/etc/krb5.keytab` (`klist -k`) ja milleks neid vaja on?

**7.3** Testi:

```bash
id mari@ad.lab.example
getent passwd mari@ad.lab.example
getent group opilased@ad.lab.example
```

**7.4** Muuda `/etc/sssd/sssd.conf`: `use_fully_qualified_names = False`, `fallback_homedir = /home/%u`. Taaskäivita SSSD, tühjenda vahemälu, luba mkhomedir ja logi sisse:

```bash
id mari
ssh mari@ubuntuklient.ad.lab.example
pwd
klist
```

> **K14.** Mis on Mari UID? Kuidas see arvutati (`ldap_id_mapping`)? Kas Maril on pärast sisselogimist Kerberose pilet?

## 8. osa. AlmaLinuxi liitmine domeeniga

**8.1** Tee `alma`-s sama: hostinimi, DNS, paketid, `realm join`. Kontrolli, milline `authselect` profiil valiti:

```bash
authselect current
id mari@ad.lab.example
```

**8.2** Muuda ka siin `use_fully_qualified_names = False` ja `fallback_homedir = /home/%u`.

> **K15.** Kas Mari UID on AlmaLinuxis sama mis Ubuntus? Miks?

## 9. osa. Ligipääsu piiramine ja `sudo`

**9.1** Mõlemas Linuxi kliendis luba sisse logida ainult gruppidel `opilased` ja `linuxadminid`. Proovi sisse logida kasutajana `administrator` ja `ain`.

**9.2** Anna grupile `linuxadminid` `sudo` õigus (fail `/etc/sudoers.d/ad-adminid`). Kontrolli kasutajana `kati`:

```bash
sudo -l
sudo whoami
```

> **K16.** Kirjuta `realm permit` käsud ja sudoers-rida. Mis juhtus `administrator`-i ja `ain`-i sisselogimisel?

**9.3** Keela DC-s Mari konto (`samba-tool user disable mari`), tühjenda kliendis vahemälu ja proovi Marina sisse logida. Seejärel luba konto uuesti.

## 10. osa. Veaotsing

**10.1** Muuda `ubuntuklient`-is kella 10 minutit valeks (peata enne ajasünkroonimine):

```bash
sudo timedatectl set-ntp false
sudo date -s "+10 minutes"
kinit mari
```

Seejärel taasta: `sudo timedatectl set-ntp true`.

> **K17.** Mis veateate said? Miks?

**10.2** Muuda `ubuntuklient`-is ajutiselt DNS-iks `1.1.1.1` ja proovi `realm discover ad.lab.example`. Taasta DNS.

> **K18.** Mis juhtus ja miks? Kirjelda kolme põhjust, miks Linuxi masin ei pruugi domeeniga liituda.

---

## Lisaülesanne (valikuline)

1. **Teine DC:** paigalda `dc2` (`10.0.83.57`) ja liida see domeeniga DC-na. Kontrolli replikatsiooni (`samba-tool drs showrepl`), lülita `dc1` välja ja proovi sisse logida.
2. **Failiserver domeenis:** liida `debian2` domeeniga liikmena (winbind või SSSD), loo jagatud kaust, millele on ligipääs ainult grupil `opilased`, ja haagi see Windowsis automaatselt GPO abil.
3. **Windows Server AD:** kui laboris on Windows Serveri domeen (nt IT25 plaanis `AD1`/`AD2`), liida `alma` sellega ja võrdle samme.
4. **Varundus:** tee `samba-tool domain backup online` ja taasta domeen uude VM-i.

---

<!-- kysimused -->
## Aruande küsimused

Kõik selle laboritöö küsimused ühes kohas. Sulgudes on punkt, mille juures küsimust küsitakse. Kopeeri loend oma aruande alguseks ja kirjuta vastus iga küsimuse alla. Kus küsitakse käsku, kirjuta üles kogu käsk.

- **K1.** *(punkt 1.1)* Miks peab DC hostinimi lahenduma kohalikuks IP-aadressiks (`10.0.83.56`), mitte `127.0.1.1`-ks?
- **K2.** *(punkt 1.2)* Miks on kellaaeg AD-s nii oluline? Kui suur võib olla kellade erinevus?
- **K3.** *(punkt 2.3)* Milliseid porte Samba kuulab? Millist teenust iga port pakub? Mis on `smb.conf` failis jaotises `[global]` peale provisioning'ut?
- **K4.** *(punkt 3.1)* Mida näitavad SRV-kirjed? Miks vajavad kliendid neid? Kust tuli vastus päringule `www.debian.org`?
- **K5.** *(punkt 3.2)* Milline pilet tekkis `klist` väljundis ja kui kaua see kehtib? Mis veateate andis vale kasutaja?
- **K6.** *(punkt 3.4)* Miks on parem suunata ainult domeeni `ad.lab.example` päringud DC-le, mitte panna DC kogu laborivõrgu DNS-iks?
- **K7.** *(punkt 4.1)* Kirjuta aruandesse käsud, millega lõid kasutaja `mari` ja paigutasid ta OU-sse `Opilased`. Mis on Mari täielik DN?
- **K8.** *(punkt 4.2)* Mis juhtus? Millised on domeeni vaikimisi paroolinõuded?
- **K9.** *(punkt 5.2)* Mida näitasid `whoami` ja `$env:LOGONSERVER`? Milliseid Kerberose pileteid on Windowsi kliendil?
- **K10.** *(punkt 5.3)* Kas Windowsi klient registreeris ennast DNS-is automaatselt?
- **K11.** *(punkt 6.2)* Kas juhtpaneel oli Jaanile keelatud? Kas see kehtis ka Katile? Miks?
- **K12.** *(punkt 6.3)* Kuidas on GPO-d nimetatud? Miks on vaja SYSVOL eraldi varundada, kui DC-sid on mitu?
- **K13.** *(punkt 7.2)* Mida näitas `realm discover`? Millised kirjed on failis `/etc/krb5.keytab` (`klist -k`) ja milleks neid vaja on?
- **K14.** *(punkt 7.4)* Mis on Mari UID? Kuidas see arvutati (`ldap_id_mapping`)? Kas Maril on pärast sisselogimist Kerberose pilet?
- **K15.** *(punkt 8.2)* Kas Mari UID on AlmaLinuxis sama mis Ubuntus? Miks?
- **K16.** *(punkt 9.2)* Kirjuta `realm permit` käsud ja sudoers-rida. Mis juhtus `administrator`-i ja `ain`-i sisselogimisel?
- **K17.** *(punkt 10.1)* Mis veateate said? Miks?
- **K18.** *(punkt 10.2)* Mis juhtus ja miks? Kirjelda kolme põhjust, miks Linuxi masin ei pruugi domeeniga liituda.
<!-- /kysimused -->

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 21. Active Directory Linuxis: Samba AD DC](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 21. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
