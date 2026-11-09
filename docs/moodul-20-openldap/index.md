# Moodul 20. Kataloogiteenused: OpenLDAP

**Maht:** 8 tundi · **Laboritöö:** Debian (server), Ubuntu ja AlmaLinux (kliendid) · **Eeldused:** moodulid 1–7, 11–15 · **Valikmoodul**

## Õpiväljundid

Mooduli läbinud õppija:

- selgitab kataloogiteenuste ja tsentraalse autentimise vajadust;
- kirjeldab LDAP-i andmemudelit (DIT, DN, objektiklass, atribuut, skeem);
- paigaldab ja seadistab OpenLDAP-serveri;
- lisab, otsib, muudab ja kustutab kirjeid LDIF-failide ja LDAP-tööriistadega;
- kaitseb LDAP-ühendused TLS-iga;
- haldab kasutajaid veebiliidesega LDAP Account Manager;
- seadistab Linuxi kliendid autentima LDAP-ist SSSD abil;
- varundab ja taastab LDAP-kataloogi.

---

## 20.1 Miks tsentraalne autentimine?

Moodulis 3 lõid kasutajad igasse masinasse eraldi (`/etc/passwd`). Kui sul on 3 serverit ja 5 kasutajat, on see talutav. Kui sul on 50 serverit ja 500 kasutajat (nt kool), tekivad probleemid:

- uus õppija tuleb luua igasse masinasse;
- parooli vahetus tuleb teha igas masinas;
- lahkunud töötaja konto võib mõnes masinas alles jääda;
- UID-d ei klapi masinate vahel (vt NFS, moodul 15).

**Kataloogiteenus** hoiab kasutajad, grupid ja muu info **ühes kohas**. Kõik masinad küsivad kasutaja andmeid ja kontrollivad paroole kataloogist.

| Lahendus | Iseloomustus |
|---|---|
| **OpenLDAP** | Avatud lähtekoodiga LDAP-server, väga paindlik. Kasutatakse Linuxi keskkondades, ka HKHK Proxmoxi autentimises |
| **Active Directory** | Microsofti kataloog (LDAP + Kerberos + DNS + grupipoliitikad). Linuxis rakendab seda **Samba AD** (moodul 21) |
| **389 Directory Server / FreeIPA** | Red Hati lahendused; FreeIPA lisab Kerberose, DNS-i ja sertifikaadid |
| lldap, Authentik, Keycloak | Kergemad või veebirakendustele suunatud lahendused |

## 20.2 LDAP-i põhimõisted

**LDAP** (*Lightweight Directory Access Protocol*) on protokoll kataloogi andmete lugemiseks ja muutmiseks. Kataloog on **puu** (*DIT - Directory Information Tree*):

```text
                    dc=lab,dc=example                 (juur, ehk base DN)
                   /                 \
          ou=People                   ou=Groups
          /       \                   /        \
   uid=mari     uid=jaan        cn=opilased   cn=opetajad
```

| Mõiste | Tähendus | Näide |
|---|---|---|
| **Kirje** (*entry*) | Üks objekt kataloogis (kasutaja, grupp, osakond) | |
| **DN** (*Distinguished Name*) | Kirje täielik unikaalne nimi - tee juureni | `uid=mari,ou=People,dc=lab,dc=example` |
| **RDN** | DN-i esimene osa | `uid=mari` |
| **Base DN** | Kataloogi juur, sageli tuletatud DNS-domeenist | `dc=lab,dc=example` |
| **Atribuut** | Kirje omadus | `cn: Mari Maasikas`, `mail: mari@lab.example` |
| **Objektiklass** (*objectClass*) | Määrab, millised atribuudid on kohustuslikud ja lubatud | `inetOrgPerson`, `posixAccount` |
| **Skeem** (*schema*) | Kõigi objektiklasside ja atribuutide kirjeldus | `core`, `cosine`, `nis`, `inetorgperson` |

Levinud atribuudid:

| Atribuut | Tähendus |
|---|---|
| `dc` | *domain component* - domeeni osa |
| `ou` | *organizational unit* - osakond, konteiner |
| `cn` | *common name* - üldnimi |
| `uid` | Kasutajanimi |
| `sn`, `givenName` | Perenimi, eesnimi |
| `uidNumber`, `gidNumber` | Linuxi UID ja GID |
| `homeDirectory`, `loginShell` | Kodukataloog, kest |
| `userPassword` | Parooli räsi |
| `memberUid` | Grupi liige (posixGroup) |

Linuxi kasutaja jaoks vajalikud objektiklassid: **`posixAccount`** (UID, GID, kodukataloog, kest), **`shadowAccount`** (parooli aegumine) ja tavaliselt **`inetOrgPerson`** (nimi, e-post jne). Grupp on **`posixGroup`**.

### Pordid ja turvalisus

| Port | Protokoll |
|---|---|
| 389 | LDAP (krüpteerimata; **StartTLS** muudab ühenduse krüpteerituks) |
| 636 | LDAPS (TLS algusest peale) |
| `ldapi:///` | Unixi pesa kohalikuks halduseks |

**Bind** on LDAP-i sisselogimine: kasutaja tõendab end DN-i ja parooliga. **Anonüümne bind** (ilma kasutajata) võimaldab tavaliselt avalikku infot lugeda - paroolide räsisid mitte.

## 20.3 OpenLDAP-i paigaldus

```bash
sudo apt install slapd ldap-utils
sudo dpkg-reconfigure slapd
```

`dpkg-reconfigure` küsib:

| Küsimus | Vastus |
|---|---|
| Omit OpenLDAP server configuration? | No |
| DNS domain name | `lab.example` → base DN `dc=lab,dc=example` |
| Organization name | Nt `HKHK labor` |
| Administrator password | Tugev parool (admin DN on `cn=admin,dc=lab,dc=example`) |
| Remove the database when slapd is purged? | No |
| Move old database? | Yes |

Kontroll:

```bash
sudo systemctl status slapd
sudo ss -tlpn | grep slapd
ldapsearch -x -H ldap://localhost -b dc=lab,dc=example
ldapwhoami -x -H ldap://localhost -D cn=admin,dc=lab,dc=example -W
sudo slapcat                                   # kogu andmebaas LDIF-ina (otse failidest)
```

### Seadistus: cn=config

Tänapäeva OpenLDAP hoiab oma seadistust **kataloogi sees** - puus `cn=config` (*OLC - On-Line Configuration*). Seda muudetakse LDIF-failidega juurkasutajana üle kohaliku pesa:

```bash
sudo ldapsearch -Y EXTERNAL -H ldapi:/// -b cn=config -LLL dn
sudo ldapmodify -Y EXTERNAL -H ldapi:/// -f muudatus.ldif
```

`-Y EXTERNAL` tähendab, et autentimine toimub operatsioonisüsteemi kasutaja järgi (juurkasutaja = kataloogi seadistuse haldur). Vanemates juhendites kasutatav fail `slapd.conf` on aegunud.

## 20.4 LDIF ja kirjete haldus

**LDIF** (*LDAP Data Interchange Format*) on tekstivorming kirjete kirjeldamiseks. Kirjed eraldatakse tühja reaga.

### Põhistruktuur

```text
# struktuur.ldif
dn: ou=People,dc=lab,dc=example
objectClass: organizationalUnit
ou: People

dn: ou=Groups,dc=lab,dc=example
objectClass: organizationalUnit
ou: Groups
```

```bash
ldapadd -x -H ldap://localhost -D cn=admin,dc=lab,dc=example -W -f struktuur.ldif
```

### Grupp ja kasutaja

Parooli räsi:

```bash
slappasswd
```

```text
{SSHA}y8n3uxbSsl0b7Kg0rQ6s+fqa2pqOe3l5
```

```text
# kasutajad.ldif
dn: cn=opilased,ou=Groups,dc=lab,dc=example
objectClass: posixGroup
cn: opilased
gidNumber: 10000
memberUid: mari

dn: uid=mari,ou=People,dc=lab,dc=example
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: mari
cn: Mari Maasikas
givenName: Mari
sn: Maasikas
mail: mari@lab.example
uidNumber: 10001
gidNumber: 10000
homeDirectory: /home/mari
loginShell: /bin/bash
userPassword: {SSHA}y8n3uxbSsl0b7Kg0rQ6s+fqa2pqOe3l5
```

> **UID-d ja GID-d alates 10000** - nii ei satu need konflikti kohalike kasutajatega (1000–9999). Peab kokku leppima, kes ja kuidas uusi numbreid jagab (LAM teeb seda automaatselt).

### Otsimine

```bash
ldapsearch -x -H ldap://localhost -b dc=lab,dc=example "(uid=mari)"
ldapsearch -x -H ldap://localhost -b ou=People,dc=lab,dc=example "(objectClass=posixAccount)" uid cn uidNumber
ldapsearch -x -H ldap://localhost -b dc=lab,dc=example "(&(objectClass=posixAccount)(gidNumber=10000))" uid
ldapsearch -x -H ldap://localhost -b dc=lab,dc=example "(|(uid=mari)(uid=jaan))" mail
ldapsearch -x -H ldap://localhost -b dc=lab,dc=example "(cn=Mari*)" -LLL
```

| Filter | Tähendus |
|---|---|
| `(uid=mari)` | Võrdne |
| `(cn=Mari*)` | Algab |
| `(&(a)(b))` | Ja |
| `(\|(a)(b))` | Või |
| `(!(a))` | Ei |
| `(uidNumber>=10000)` | Suurem või võrdne |

Võti `-LLL` eemaldab väljundist kommentaarid, atribuutide nimed käsu lõpus piiravad väljundit.

### Muutmine, parool ja kustutamine

```text
# muuda.ldif
dn: uid=mari,ou=People,dc=lab,dc=example
changetype: modify
replace: loginShell
loginShell: /bin/zsh
-
add: telephoneNumber
telephoneNumber: +372 5555 5555
```

```bash
ldapmodify -x -H ldap://localhost -D cn=admin,dc=lab,dc=example -W -f muuda.ldif
ldappasswd -x -H ldap://localhost -D cn=admin,dc=lab,dc=example -W -S uid=mari,ou=People,dc=lab,dc=example
ldapdelete -x -H ldap://localhost -D cn=admin,dc=lab,dc=example -W uid=jaan,ou=People,dc=lab,dc=example
```

Kasutaja saab oma parooli ise muuta, kui teeb bind'i enda DN-iga: `ldappasswd -x -D uid=mari,ou=People,dc=lab,dc=example -W -S`.

### Juurdepääsuõigused (ACL)

OpenLDAP-i õigused on `cn=config`-is atribuudis `olcAccess`. Debiani vaikimisi reeglid lubavad:

- kasutajal muuta oma parooli, kuid mitte lugeda teiste paroolide räsisid;
- kõigil lugeda ülejäänud atribuute;
- adminil kõike.

```bash
sudo ldapsearch -Y EXTERNAL -H ldapi:/// -b cn=config "(olcDatabase={1}mdb)" olcAccess -LLL
```

## 20.5 TLS

LDAP-i lihtne bind saadab parooli **avatekstina**. Tootmises peab ühendus olema krüpteeritud.

Sertifikaat luuakse nagu moodulis 13 (oma CA, SAN-iga serveri DNS-nimele, nt `debian1.lab.example`). Failid ja õigused:

```bash
sudo mkdir -p /etc/ldap/tls
sudo cp labori-ca.crt ldap.crt ldap.key /etc/ldap/tls/
sudo chown root:openldap /etc/ldap/tls/ldap.key
sudo chmod 640 /etc/ldap/tls/ldap.key
```

```text
# tls.ldif
dn: cn=config
changetype: modify
replace: olcTLSCACertificateFile
olcTLSCACertificateFile: /etc/ldap/tls/labori-ca.crt
-
replace: olcTLSCertificateFile
olcTLSCertificateFile: /etc/ldap/tls/ldap.crt
-
replace: olcTLSCertificateKeyFile
olcTLSCertificateKeyFile: /etc/ldap/tls/ldap.key
```

```bash
sudo ldapmodify -Y EXTERNAL -H ldapi:/// -f tls.ldif
```

Klientides (ka serveris endas) määrab usaldatava CA fail `/etc/ldap/ldap.conf`:

```text
BASE    dc=lab,dc=example
URI     ldap://debian1.lab.example
TLS_CACERT /etc/ldap/tls/labori-ca.crt
```

StartTLS-i test (`-ZZ` nõuab, et TLS õnnestuks):

```bash
ldapwhoami -x -ZZ -H ldap://debian1.lab.example -D cn=admin,dc=lab,dc=example -W
```

LDAPS-i (port 636) jaoks lisa failis `/etc/default/slapd` reale `SLAPD_SERVICES` `ldaps:///` ja taaskäivita `slapd`.

## 20.6 LDAP Account Manager

**LAM** (*LDAP Account Manager*) on PHP-põhine veebiliides kasutajate, gruppide ja paroolide haldamiseks. See jagab automaatselt UID- ja GID-numbreid, loob parooli räsid ja oskab hulgi importida (CSV).

```bash
sudo apt install ldap-account-manager
```

Veebiliides: `http://<server>/lam`. Esmalt seadista **LAM configuration** → **Edit server profiles** (vaikimisi peaparool on dokumentatsioonis, **muuda see kohe**):

- serveri aadress `ldap://localhost` (või `ldaps://…`);
- tree suffix `dc=lab,dc=example`;
- admin `cn=admin,dc=lab,dc=example`;
- vahekaardil *Account types*: kasutajate konteiner `ou=People,dc=lab,dc=example`, gruppide `ou=Groups,dc=lab,dc=example`;
- *Modules*: kasutajatel `inetOrgPerson`, `posixAccount`, `shadowAccount`; gruppidel `posixGroup`.

LAM-i saab käivitada ka konteinerina (Docker/Podman, moodul 12) ja selle ette panna pöördpuhverserveri koos TLS-iga.

## 20.7 Linuxi kliendid: SSSD

**SSSD** (*System Security Services Daemon*) ühendab Linuxi kataloogiteenusega: kasutajad ja grupid tulevad LDAP-ist (`getent passwd`, `id`), paroolid kontrollitakse LDAP-is ja SSSD hoiab vahemälu, et sisselogimine töötaks ka siis, kui server korraks kättesaamatu on.

```text
login/ssh → PAM → SSSD → LDAP-server
id, ls -l → NSS → SSSD → LDAP-server
```

- **NSS** (*Name Service Switch*) - „kes on kasutaja 10001?“ (`/etc/nsswitch.conf`: `passwd: files sss`);
- **PAM** (*Pluggable Authentication Modules*) - „kas parool on õige?“, „loo kodukataloog“.

### Paigaldus

```bash
sudo apt install sssd-ldap libnss-sss libpam-sss ldap-utils            # Debian, Ubuntu
sudo dnf install sssd sssd-ldap oddjob-mkhomedir openldap-clients     # AlmaLinux
```

### Seadistus

Fail `/etc/sssd/sssd.conf` (õigused **600**, omanik root):

```ini
[sssd]
services = nss, pam
domains = lab

[domain/lab]
id_provider = ldap
auth_provider = ldap
ldap_uri = ldap://debian1.lab.example
ldap_search_base = dc=lab,dc=example
ldap_user_search_base = ou=People,dc=lab,dc=example
ldap_group_search_base = ou=Groups,dc=lab,dc=example
ldap_id_use_start_tls = true
ldap_tls_reqcert = demand
ldap_tls_cacert = /etc/sssd/labori-ca.crt
cache_credentials = true
enumerate = false
```

CA sertifikaat kopeeritakse kõigis distrodes samasse kohta: `sudo cp labori-ca.crt /etc/sssd/`.

```bash
sudo chmod 600 /etc/sssd/sssd.conf
sudo systemctl enable --now sssd
sudo systemctl restart sssd
```

> SSSD keeldub vaikimisi paroole krüpteerimata ühenduse kaudu kontrollimast - TLS (punkt 20.5) on kohustuslik. Ainult kiireks testiks laboris saab seda vältida valikuga `ldap_auth_disable_tls_never_use_in_production = true`, mille nimi ütleb kõik.

### Kodukataloogi automaatne loomine

```bash
sudo pam-auth-update --enable mkhomedir                         # Debian, Ubuntu
sudo authselect select sssd with-mkhomedir --force              # AlmaLinux
sudo systemctl enable --now oddjobd                             # AlmaLinux
```

### Kontroll

```bash
getent passwd mari
id mari
getent group opilased
su - mari                       # või ssh mari@klient
sudo sss_cache -E               # tühjenda SSSD vahemälu pärast LDAP-is muutmist
journalctl -u sssd
```

`getent passwd` ilma kasutajanimeta LDAP-i kasutajaid ei näita (`enumerate = false`), kuid nime järgi küsides näitab.

## 20.8 Varundus ja taastamine

```bash
sudo slapcat -n 0 > config.ldif        # seadistus (cn=config)
sudo slapcat -n 1 > andmed.ldif        # andmed
```

Taastamine (andmebaas peab olema tühi):

```bash
sudo systemctl stop slapd
sudo mv /var/lib/ldap /var/lib/ldap.vana && sudo mkdir /var/lib/ldap
sudo slapadd -n 1 -l andmed.ldif
sudo chown -R openldap:openldap /var/lib/ldap
sudo systemctl start slapd
```

Kataloog on kriitiline teenus: kui see ei tööta, ei saa keegi sisse logida. Tootmises kasutatakse vähemalt kahte serverit ja **replikatsiooni** (OpenLDAP-is *syncrepl*).

---

## Distrode erinevused

| | **Debian** | **Ubuntu** | **AlmaLinux** |
|---|---|---|---|
| OpenLDAP server | `slapd` | `slapd` | Puudub ametlikus hoidlas; Red Hat soovitab 389 Directory Serverit/FreeIPA-t (OpenLDAP-i server on saadaval kolmandatest allikatest) |
| LDAP tööriistad | `ldap-utils` | `ldap-utils` | `openldap-clients` |
| Kliendi seadistusfail | `/etc/ldap/ldap.conf` | `/etc/ldap/ldap.conf` | `/etc/openldap/ldap.conf` |
| SSSD | `sssd-ldap` | `sssd-ldap` | `sssd`, `sssd-ldap` |
| Kodukataloogi loomine | `pam-auth-update --enable mkhomedir` | sama | `authselect … with-mkhomedir` + `oddjobd` |
| CA usaldamine | `/usr/local/share/ca-certificates/` + `update-ca-certificates` | sama | `/etc/pki/ca-trust/source/anchors/` + `update-ca-trust` |

Seepärast paigaldatakse selles moodulis OpenLDAP-server Debiani ja AlmaLinux on ainult klient.

---

## Kokkuvõte

| Tegevus | Käsk |
|---|---|
| Paigaldus | `apt install slapd ldap-utils`, `dpkg-reconfigure slapd` |
| Otsing | `ldapsearch -x -H ldap://… -b dc=… "(filter)"` |
| Lisamine | `ldapadd -x -D cn=admin,… -W -f fail.ldif` |
| Muutmine | `ldapmodify … -f fail.ldif` (`changetype: modify`) |
| Parool | `slappasswd`, `ldappasswd … -S <DN>` |
| Kustutamine | `ldapdelete … <DN>` |
| Seadistus | `ldapmodify -Y EXTERNAL -H ldapi:/// -f …` |
| TLS test | `ldapwhoami -x -ZZ …` |
| Klient | `/etc/sssd/sssd.conf`, `getent passwd`, `id` |
| Varundus | `slapcat -n 0`, `slapcat -n 1`, `slapadd` |

**Järgmised sammud:** tee [laboritöö](labor.md) ja kontrolli oma teadmisi [enesekontrolli](enesekontroll.md) abil.

## Lisamaterjal

- OpenLDAP Administrator's Guide (openldap.org/doc/admin)
- Ubuntu Server dokumentatsioon - OpenLDAP (documentation.ubuntu.com)
- LDAP Account Manager dokumentatsioon (ldap-account-manager.org)
- SSSD dokumentatsioon (sssd.io) ja `man sssd-ldap`
