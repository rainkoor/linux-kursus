<!-- navigatsioon -->
[← Moodul 24. Kataloogiteenused: OpenLDAP](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 24. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->

# Laboritöö 24. OpenLDAP-kataloog ja Linuxi kliendid

| | |
|---|---|
| **Distrod** | Debian (`debian1` - OpenLDAP server), Ubuntu ja AlmaLinux (kliendid) |
| **Kestus** | 3 × 90 minutit |
| **Vajalik** | Laborivõrk (moodul 21) koos DNS-nimedega (`debian1.lab.example` jt), moodulis 15 loodud oma CA (või loo uus) |
| **Eesmärk** | Ehitada kooli kasutajate kataloog ja panna Linuxi masinad sellest autentima |

> **Aruanne:** vasta küsimustele **K1–K16**. Hoia kõik LDIF-failid kataloogis `~/ldap` ja lisa need oma Giti hoidlasse (moodul 6) - ilma paroolideta! Kõik küsimused on koos ka lehe lõpus ([Aruande küsimused](#aruande-küsimused)).

**Stsenaarium:** kool soovib, et õppijad ja õpetajad saaksid kõigisse laborimasinatesse sisse logida ühe kasutajanime ja parooliga.

---

## 1. osa. Paigaldus

**1.1** Kontrolli, et `debian1` nimi lahendub ja kellaaeg on õige (TLS ja autentimine vajavad õiget aega):

```bash
hostname -f
getent hosts debian1.lab.example
timedatectl
```

**1.2** Paigalda OpenLDAP ja seadista see (teooria punkt 24.3): domeen `lab.example`, organisatsioon `HKHK labor`.

```bash
sudo apt install slapd ldap-utils
sudo dpkg-reconfigure slapd
```

**1.3** Kontrolli:

```bash
sudo systemctl status slapd
sudo ss -tlpn | grep slapd
ldapsearch -x -H ldap://localhost -b dc=lab,dc=example -LLL
ldapwhoami -x -H ldap://localhost -D cn=admin,dc=lab,dc=example -W
sudo ldapsearch -Y EXTERNAL -H ldapi:/// -b cn=config -LLL dn | head -20
```

> **K1.** Millised kirjed on kataloogis kohe pärast paigaldust? Millised skeemid on laaditud (`cn=schema,cn=config` alt)?

## 2. osa. Struktuur, grupid ja kasutajad

**2.1** Loo LDIF-failiga konteinerid `ou=People` ja `ou=Groups` (teooria punkt 24.4) ja lisa need.

**2.2** Loo grupid ja kasutajad:

| Kasutaja | Nimi | UID | Grupp (GID) |
|---|---|---|---|
| `mari` | Mari Maasikas | 10001 | `opilased` (10000) |
| `jaan` | Jaan Tamm | 10002 | `opilased` (10000) |
| `kati` | Kati Kask | 10101 | `opetajad` (10100) |

Genereeri igale parool käsuga `slappasswd`. Lisa gruppidesse liikmed (`memberUid`).

```bash
ldapadd -x -H ldap://localhost -D cn=admin,dc=lab,dc=example -W -f kasutajad.ldif
```

> **K2.** Kirjuta aruandesse ühe kasutaja LDIF (räsi võid lühendada). Miks on igal kasutajal kolm objektiklassi?

**2.3** Proovi lisada kasutaja, kellel puudub kohustuslik atribuut (nt `sn` või `homeDirectory`).

> **K3.** Mis veateate said? Kust tuleb nõue, et atribuut on kohustuslik?

## 3. osa. Otsimine ja muutmine

**3.1** Kirjuta ja käivita otsingud, mis leiavad:

1. kõik kasutajad (`posixAccount`) koos atribuutidega `uid`, `cn`, `uidNumber`;
2. kõik grupi `opilased` liikmed (GID 10000);
3. kasutaja, kelle eesnimi algab tähega „K“;
4. kõik kirjed, mis ei ole kasutajad ega grupid.

> **K4.** Kirjuta kõik neli käsku.

**3.2** Muuda `ldapmodify`-ga: Mari kest `/bin/zsh`-iks, lisa Jaanile e-posti aadress, eemalda Kati telefoninumber (lisa see enne).

**3.3** Proovi anonüümselt (ilma `-D`-ta) lugeda Mari parooli räsi ja seejärel Mari enda nimel:

```bash
ldapsearch -x -H ldap://localhost -b uid=mari,ou=People,dc=lab,dc=example userPassword
ldapsearch -x -H ldap://localhost -D uid=mari,ou=People,dc=lab,dc=example -W -b uid=mari,ou=People,dc=lab,dc=example userPassword
```

> **K5.** Kas anonüümne kasutaja nägi räsi? Kas Mari nägi oma räsi? Milline `olcAccess` reegel seda määrab?

**3.4** Lase Maril oma parool ise muuta ja kontrolli uue parooliga `ldapwhoami`.

```bash
ldappasswd -x -H ldap://localhost -D uid=mari,ou=People,dc=lab,dc=example -W -S
```

## 4. osa. TLS

**4.1** Loo `debian1`-le sertifikaat oma CA-ga (moodul 15, punkt 15.3), SAN = `debian1.lab.example`. Paigalda failid kataloogi `/etc/ldap/tls` õigete õigustega ja rakenda `tls.ldif` (teooria punkt 24.5).

**4.2** Seadista `/etc/ldap/ldap.conf` ja testi:

```bash
ldapwhoami -x -ZZ -H ldap://debian1.lab.example -D cn=admin,dc=lab,dc=example -W
ldapwhoami -x -ZZ -H ldap://localhost -D cn=admin,dc=lab,dc=example -W
```

> **K6.** Miks esimene käsk õnnestus, aga teine ebaõnnestus? (Vihje: sertifikaadi SAN.)

**4.3** Püüa liiklust ja võrdle krüpteerimata ning StartTLS-iga bind'i:

```bash
sudo tcpdump -ni lo -A port 389 | grep -a -i -E "admin|parool" &
ldapwhoami -x -H ldap://localhost -D cn=admin,dc=lab,dc=example -w <parool>
ldapwhoami -x -ZZ -H ldap://debian1.lab.example -D cn=admin,dc=lab,dc=example -w <parool>
sudo kill %1
```

> **K7.** Mida nägid krüpteerimata ühenduse puhul? Miks on TLS LDAP-i puhul kohustuslik?

## 5. osa. LDAP Account Manager

**5.1** Paigalda LAM ja seadista serveri profiil (teooria punkt 24.6). **Muuda LAM-i seadistuse peaparool.**

**5.2** Loo LAM-iga uus kasutaja `ain` (õpetaja) ja lisa ta gruppi `opetajad`. Vaata `ldapsearch`-iga, milline kirje tekkis.

> **K8.** Millise UID-numbri LAM andis? Milliseid atribuute lisas LAM, mida sina käsitsi ei lisanud?

**5.3** (Valikuline) Impordi LAM-iga CSV-failist veel 5 õppijat (*Tools* → *File upload*).

## 6. osa. Linuxi kliendid (SSSD)

**6.1** **Ubuntu** kliendis: paigalda paketid, kopeeri CA sertifikaat kataloogi `/etc/sssd/`, loo `/etc/sssd/sssd.conf` (teooria punkt 24.7) ja käivita SSSD. Luba kodukataloogi loomine.

```bash
getent passwd mari
id mari
getent group opilased
```

> **K9.** Mida näitas `id mari`? Kust see info tuli (vaata `/etc/nsswitch.conf` rida `passwd:`)?

**6.2** Logi Ubuntu kliendisse sisse LDAP-i kasutajana (SSH-ga peab olema parooliga sisselogimine lubatud või kasuta Proxmoxi konsooli või `su - mari`):

```bash
ssh mari@ubuntuklient.lab.example
pwd
id
touch test.txt && ls -ln test.txt
```

> **K10.** Kas kodukataloog loodi automaatselt? Mis on faili `test.txt` numbriline omanik? Miks on see oluline NFS-i puhul (moodul 18)?

**6.3** **AlmaLinuxi** kliendis tee sama (AlmaLinuxi paketid ja `authselect`, teooria punkt 24.7). Logi sisse kasutajana `kati`.

**6.4** Peata `debian1`-s `slapd` ja proovi Ubuntu kliendis uuesti sisse logida kasutajana `mari`. Seejärel käivita `slapd`.

> **K11.** Kas sisselogimine õnnestus, kui server oli maas? Miks? Milline `sssd.conf` valik seda mõjutab?

**6.5** Anna grupile `opetajad` klientides `sudo` õigus. Loo kliendis fail `/etc/sudoers.d/opetajad` (`visudo -f`):

```text
%opetajad ALL=(ALL:ALL) ALL
```

> **K12.** Kas `kati` sai `sudo` kasutada? Kas `mari` sai? Miks on parem anda õigused grupi kaudu?

**6.6** Lukusta LDAP-is Jaani konto: muuda tema `loginShell` väärtuseks `/usr/sbin/nologin`. Tühjenda kliendis vahemälu ja proovi Jaanina sisse logida.

```bash
sudo sss_cache -E
```

> **K13.** Mis juhtus? Mis on teised võimalused konto keelamiseks?

## 7. osa. Varundus ja taastamine

**7.1** Varunda seadistus ja andmed (teooria punkt 24.8). Kontrolli failide sisu.

**7.2** Kustuta kasutaja `kati` ja taasta kogu andmebaas varukoopiast.

> **K14.** Kas `kati` taastus? Miks on vaja eraldi varundada `cn=config` (`-n 0`) ja andmed (`-n 1`)?

## 8. osa. Kokkuvõte

> **K15.** Joonista skeem: kuidas jõuab `ssh mari@ubuntuklient` sisselogimine LDAP-serverini (SSH → PAM → SSSD → TLS → slapd)?

> **K16.** Mis juhtuks koolis, kui ainus LDAP-server rikneks? Kuidas seda riski vähendada?

---

## Lisaülesanne (valikuline)

1. **memberOf:** lülita sisse `memberOf` overlay ja kasuta gruppe objektiklassiga `groupOfNames`, et iga kasutaja juures oleks näha, millistesse gruppidesse ta kuulub.
2. **Replikatsioon:** paigalda teine OpenLDAP-server (`debian2`) ja seadista *syncrepl* replikatsioon. Lisa SSSD-sse mõlemad serverid (`ldap_uri = ldap://debian1…, ldap://debian2…`).
3. **SSH võtmed LDAP-is:** salvesta kasutajate avalikud SSH-võtmed LDAP-i (skeem `openssh-lpk`) ja seadista SSSD (`sss_ssh_authorizedkeys`) neid kasutama.
4. **LAM konteineris:** käivita LAM Podmani konteinerina (pilt `ghcr.io/ldapaccountmanager/lam`) ja pane selle ette nginx koos TLS-iga.

---

<!-- kysimused -->
## Aruande küsimused

Kõik selle laboritöö küsimused ühes kohas. Sulgudes on punkt, mille juures küsimust küsitakse. Kopeeri loend oma aruande alguseks ja kirjuta vastus iga küsimuse alla. Kus küsitakse käsku, kirjuta üles kogu käsk.

- **K1.** *(punkt 1.3)* Millised kirjed on kataloogis kohe pärast paigaldust? Millised skeemid on laaditud (`cn=schema,cn=config` alt)?
- **K2.** *(punkt 2.2)* Kirjuta aruandesse ühe kasutaja LDIF (räsi võid lühendada). Miks on igal kasutajal kolm objektiklassi?
- **K3.** *(punkt 2.3)* Mis veateate said? Kust tuleb nõue, et atribuut on kohustuslik?
- **K4.** *(punkt 3.1)* Kirjuta kõik neli käsku.
- **K5.** *(punkt 3.3)* Kas anonüümne kasutaja nägi räsi? Kas Mari nägi oma räsi? Milline `olcAccess` reegel seda määrab?
- **K6.** *(punkt 4.2)* Miks esimene käsk õnnestus, aga teine ebaõnnestus? (Vihje: sertifikaadi SAN.)
- **K7.** *(punkt 4.3)* Mida nägid krüpteerimata ühenduse puhul? Miks on TLS LDAP-i puhul kohustuslik?
- **K8.** *(punkt 5.2)* Millise UID-numbri LAM andis? Milliseid atribuute lisas LAM, mida sina käsitsi ei lisanud?
- **K9.** *(punkt 6.1)* Mida näitas `id mari`? Kust see info tuli (vaata `/etc/nsswitch.conf` rida `passwd:`)?
- **K10.** *(punkt 6.2)* Kas kodukataloog loodi automaatselt? Mis on faili `test.txt` numbriline omanik? Miks on see oluline NFS-i puhul (moodul 18)?
- **K11.** *(punkt 6.4)* Kas sisselogimine õnnestus, kui server oli maas? Miks? Milline `sssd.conf` valik seda mõjutab?
- **K12.** *(punkt 6.5)* Kas `kati` sai `sudo` kasutada? Kas `mari` sai? Miks on parem anda õigused grupi kaudu?
- **K13.** *(punkt 6.6)* Mis juhtus? Mis on teised võimalused konto keelamiseks?
- **K14.** *(punkt 7.2)* Kas `kati` taastus? Miks on vaja eraldi varundada `cn=config` (`-n 0`) ja andmed (`-n 1`)?
- **K15.** *(8. osa)* Joonista skeem: kuidas jõuab `ssh mari@ubuntuklient` sisselogimine LDAP-serverini (SSH → PAM → SSSD → TLS → slapd)?
- **K16.** *(8. osa)* Mis juhtuks koolis, kui ainus LDAP-server rikneks? Kuidas seda riski vähendada?
<!-- /kysimused -->

---

> [!NOTE]
> **Õpetajale:** kontrollvastused ja märkused on eraldi õpetaja materjalides (privaatne hoidla `linux-kursus-opetajale`).

<!-- navigatsioon -->
---

[← Moodul 24. Kataloogiteenused: OpenLDAP](index.md) · [Sisukord](../../README.md#sisukord) · [Moodul 24. Enesekontroll →](enesekontroll.md)
<!-- /navigatsioon -->
