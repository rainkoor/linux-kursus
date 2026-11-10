<!-- navigatsioon -->
[← Laboritöö 24. OpenLDAP-kataloog ja Linuxi kliendid](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 25. Active Directory Linuxis: Samba AD DC →](../moodul-25-samba-ad/index.md)
<!-- /navigatsioon -->

# Moodul 24. Enesekontroll

Vasta igale küsimusele kõigepealt ise, ilma materjali vaatamata. Seejärel ava selle all olev **Vastus** ja võrdle.

## Küsimused

**1.** Milliseid probleeme lahendab tsentraalne kasutajate kataloog võrreldes kohalike kontodega?

<details>
<summary>Vastus</summary>

Üks konto ja parool kõigis masinates, kasutaja loomine ja kustutamine ühes kohas, ühtsed UID/GID-numbrid (NFS), lihtsam paroolipoliitika ja auditeerimine.

</details>

**2.** Mis on DIT, DN ja RDN? Too näide.

<details>
<summary>Vastus</summary>

DIT - kataloogipuu; DN - kirje täisnimi puus (nt `uid=mari,ou=People,dc=lab,dc=example`); RDN - DN-i vasakpoolseim osa (`uid=mari`).

</details>

**3.** Mis on objektiklass? Mis vahe on kohustuslikul ja valikulisel atribuudil?

<details>
<summary>Vastus</summary>

Objektiklass määrab, milliseid atribuute kirje peab (MUST) ja võib (MAY) sisaldada. Kohustuslikuta kirjet ei saa lisada.

</details>

**4.** Milliseid objektiklasse vajab Linuxi kasutaja LDAP-is ja milleks igaüht?

<details>
<summary>Vastus</summary>

`inetOrgPerson` - nimi, e-post jm isikuandmed; `posixAccount` - UID, GID, kodukataloog, kest; `shadowAccount` - parooli aegumise andmed.

</details>

**5.** Millised on LDAP-i pordid ja mis vahe on StartTLS-il ja LDAPS-il?

<details>
<summary>Vastus</summary>

389 - LDAP (StartTLS-iga krüpteeritakse ühendus pärast ühendumist samas pordis); 636 - LDAPS (TLS kohe ühendumisel).

</details>

**6.** Mis on `cn=config` ja miks ei muudeta OpenLDAP-i seadistust tekstifailis?

<details>
<summary>Vastus</summary>

Dünaamiline seadistus, mis on ise LDAP-puu; muudatused jõustuvad kohe, ilma teenust taaskäivitamata.

</details>

**7.** Mida tähendab `ldapmodify -Y EXTERNAL -H ldapi:///`?

<details>
<summary>Vastus</summary>

Ühendus kohaliku Unixi sokli kaudu, autentimine operatsioonisüsteemi kasutaja järgi (root → kataloogi haldaja `cn=config` jaoks).

</details>

**8.** Mida teeb filter `(&(objectClass=posixAccount)(!(loginShell=/usr/sbin/nologin)))`?

<details>
<summary>Vastus</summary>

Leiab kõik kasutajad, kelle kest ei ole `/usr/sbin/nologin`.

</details>

**9.** Miks ei tohi kasutajate parooli räsi olla anonüümselt loetav?

<details>
<summary>Vastus</summary>

Räsi saab võrguühenduseta (offline) murda; nõrgad paroolid leitakse kiiresti.

</details>

**10.** Mis on SSSD roll Linuxi kliendis? Kuidas see seostub NSS-i ja PAM-iga?

<details>
<summary>Vastus</summary>

SSSD on vahelüli: NSS küsib temalt kasutaja ja grupi infot (`getent`, `id`), PAM autentimist; SSSD suhtleb LDAP-iga ja hoiab vahemälu.

</details>

**11.** Mida teeb `cache_credentials = true` ja milline on selle eelis ning risk?

<details>
<summary>Vastus</summary>

Kasutaja saab sisse logida ka siis, kui server pole kättesaadav. Risk: kataloogis keelatud või muudetud parool võib vahemälus veel mõnda aega kehtida.

</details>

**12.** Miks peavad UID- ja GID-numbrid olema kõigis masinates samad?

<details>
<summary>Vastus</summary>

Failide omanik salvestatakse numbrina; erinevad numbrid tähendaksid, et NFS-is või kettal kuuluvad failid valele kasutajale.

</details>

**13.** Kuidas luuakse LDAP-i kasutajale kodukataloog esimesel sisselogimisel (Ubuntu ja AlmaLinux)?

<details>
<summary>Vastus</summary>

Ubuntu: `pam-auth-update --enable mkhomedir`; AlmaLinux: `authselect select sssd with-mkhomedir --force` ja teenus `oddjobd`.

</details>

**14.** Miks pole AlmaLinuxis OpenLDAP-serverit ja mis on selle alternatiivid RHEL-i maailmas?

<details>
<summary>Vastus</summary>

Red Hat lõpetas OpenLDAP-serveri tarnimise; alternatiivid on 389 Directory Server ja FreeIPA / Red Hat IdM. Kliendid ja `openldap-clients` on olemas.

</details>

**15.** Kuidas varundad ja taastad OpenLDAP-i?

<details>
<summary>Vastus</summary>

`slapcat -n 0` (seadistus) ja `slapcat -n 1` (andmed); taastamisel peata `slapd`, tühjenda andmekataloog ja kasuta `slapadd`, siis paranda omanik (`openldap`).

</details>

## Praktilised miniülesanded

**1.** Kirjuta LDIF, mis lisab kasutajale `uid=jaan,ou=People,dc=lab,dc=example` atribuudi `mail` väärtusega `jaan@lab.example`.

<details>
<summary>Lahendus</summary>

```text
dn: uid=jaan,ou=People,dc=lab,dc=example
changetype: modify
add: mail
mail: jaan@lab.example
```

</details>

**2.** Kirjuta `ldapsearch` käsk, mis leiab kõik grupid, mille liige on `mari`, ja kuvab ainult nende nime.

<details>
<summary>Lahendus</summary>

```bash
ldapsearch -x -LLL -b ou=Groups,dc=lab,dc=example "(memberUid=mari)" cn
```

</details>

**3.** Kirjuta LDIF, mis lisab grupi `opetajad` (GID 10100) ilma liikmeteta.

<details>
<summary>Lahendus</summary>

```text
dn: cn=opetajad,ou=Groups,dc=lab,dc=example
objectClass: posixGroup
cn: opetajad
gidNumber: 10100
```

</details>

**4.** Kirjuta käsk, millega kontrollid kliendis, kas SSSD näeb kasutajat `kati` ja tema gruppe.

<details>
<summary>Lahendus</summary>

```bash
id kati
getent passwd kati
```

</details>

**5.** Kirjuta käsk, mis kustutab kasutaja `uid=test,ou=People,dc=lab,dc=example`.

<details>
<summary>Lahendus</summary>

```bash
ldapdelete -x -D cn=admin,dc=lab,dc=example -W "uid=test,ou=People,dc=lab,dc=example"
```

</details>

<!-- navigatsioon -->
---

[← Laboritöö 24. OpenLDAP-kataloog ja Linuxi kliendid](labor.md) · [Sisukord](../../README.md#sisukord) · [Moodul 25. Active Directory Linuxis: Samba AD DC →](../moodul-25-samba-ad/index.md)
<!-- /navigatsioon -->
